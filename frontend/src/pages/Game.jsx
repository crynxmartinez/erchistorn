import { useCallback, useEffect, useState, useRef } from "react";
import { Link } from "react-router-dom";
import { api, extractError, API_BASE } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import { useGameData } from "@/data/gameData";
import { getThemeVars } from "@/data/themes";
import { toast } from "sonner";
import { LogOut, Trophy, ScrollText, Home as HomeIcon, Building2, Shield, Sun, Globe, User, Package, BookOpen } from "lucide-react";

import CharacterPanel from "@/components/CharacterPanel";
import CharacterSheet from "@/components/CharacterSheet";
import BiomeView from "@/components/BiomeView";
import CombatScreen from "@/components/CombatScreen";
import NarrativeReveal from "@/components/NarrativeReveal";
import EncounterModal from "@/components/EncounterModal";
import Inventory from "@/components/Inventory";
import SkillsPanel from "@/components/SkillsPanel";
import DailyPanel from "@/components/DailyPanel";
import WorldEvents from "@/components/WorldEvents";
import TutorialOverlay from "@/components/TutorialOverlay";
import LoginRewardModal from "@/components/LoginRewardModal";
import JournalDrawer from "@/components/JournalDrawer";
import RacialAbilityPanel from "@/components/RacialAbilityPanel";
import SlidePanel from "@/components/SlidePanel";
import HeritageArrivalModal from "@/components/HeritageArrivalModal";
import TownView from "@/components/TownView";
import GuildHouse from "@/pages/GuildHouse";
import LeaderboardPage from "@/pages/LeaderboardPage";

const TABS = [
    { id: "character", label: "Character", icon: User },
    { id: "biome",   label: "Biome",    icon: HomeIcon },
];

export default function Game() {
    const { logout } = useAuth();
    const gd = useGameData();
    const [character, setCharacter] = useState(null);
    const [loginReward, setLoginReward] = useState(null);
    const [tab, setTab] = useState("biome");
    const [townId, setTownId] = useState(null);
    const [narrativeResult, setNarrativeResult] = useState(null);
    const [encounter, setEncounter] = useState(null);
    const [combat, setCombat] = useState(null);
    const [pendingSkillId, setPendingSkillId] = useState(null);
    const [pendingItemId, setPendingItemId] = useState(null);
    const [showTutorial, setShowTutorial] = useState(false);
    const [timeOfDay, setTimeOfDay] = useState("solar");
    const [towns, setTowns] = useState([]);
    const [townMenuOpen, setTownMenuOpen] = useState(false);
    const [townInitialTab, setTownInitialTab] = useState(null);
    const [heritageArrival, setHeritageArrival] = useState(null);
    const [leftPanelOpen, setLeftPanelOpen] = useState(false);
    const [rightPanelOpen, setRightPanelOpen] = useState(false);
    const prevContinentRef = useRef(null);

    const closePanels = () => {
        setLeftPanelOpen(false);
        setRightPanelOpen(false);
    };

    const ensureBiome = (next) => {
        if (!next?.current_biome) {
            const cont = gd.continents.find((c) => c.id === next.current_continent);
            const fallback = cont?.biomes?.[0]?.id;
            if (fallback) return { ...next, current_biome: fallback };
        }
        return next;
    };

    const loadCharacter = useCallback(async () => {
        try {
            const [ch, wt, tw] = await Promise.all([
                api.get("/game/character"),
                api.get("/game/world/time"),
                api.get("/game/data/towns"),
            ]);
            setCharacter(ch.data.character);
            setTimeOfDay(wt.data.time_of_day);
            setTowns(tw.data.towns);
            if (ch.data.login_reward) setLoginReward(ch.data.login_reward);
            if (!ch.data.character.tutorial_complete) setShowTutorial(true);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, []);

    useEffect(() => {
        loadCharacter();
    }, [loadCharacter]);

    // Track logout screen for PvP safety
    useEffect(() => {
        const handler = () => {
            const screen = combat ? "combat" : townId ? "town" : tab;
            const blob = new Blob([JSON.stringify({ screen })], { type: "application/json" });
            navigator.sendBeacon(`${API_BASE}/game/character/logout-screen`, blob);
        };
        window.addEventListener("beforeunload", handler);
        return () => window.removeEventListener("beforeunload", handler);
    }, [tab, townId, combat]);

    useEffect(() => {
        if (gd.ready && character && !character.current_biome) {
            setCharacter((prev) => ensureBiome(prev));
        }
    }, [character, gd.ready]);

    // Heritage arrival detection — when character's continent changes to a heritage month continent
    useEffect(() => {
        if (!character) return;
        const currCont = character.current_continent;
        const prevCont = prevContinentRef.current;
        if (prevCont !== undefined && prevCont !== currCont) {
            api.get("/game/heritage/current").then(({ data }) => {
                if (data.active && data.continent === currCont) {
                    const year = new Date().getFullYear();
                    const dismissKey = `${currCont}_${year}`;
                    const dismissed = character.heritage_dismissed || [];
                    if (!dismissed.includes(dismissKey)) {
                        setHeritageArrival({
                            continent: currCont,
                            name: data.name,
                            desc: data.desc,
                            bonuses: data.bonuses,
                        });
                    }
                }
            }).catch(() => {});
        }
        prevContinentRef.current = currCont;
    }, [character?.current_continent]);

    if (!character || !gd.ready) {
        return (
            <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-3xl">
                LOADING ERCHIS…
            </div>
        );
    }

    const race = gd.races.find((r) => r.id === character.race);
    const role = gd.roles.find((r) => r.id === character.role);
    const mastery = gd.masteries.find((m) => m.id === character.mastery);
    const continent = gd.continents.find((c) => c.id === character.current_continent);
    const activeContinent = continent || gd.continents[0];
    const themeVars = getThemeVars(character.current_continent, character.current_biome);

    const handleActionResult = (data) => {
        setNarrativeResult(data.result);
        setCharacter(data.character);
        if (data.encounter) {
            setEncounter(data.encounter);
        }
        if (data.waystone_discovered) {
            toast.success(`A waystone hums to life: ${data.waystone_discovered.name}`);
        }
        if (data.rep_change) {
            const [newLevel, contId, oldLevel] = data.rep_change;
            if (newLevel !== oldLevel) {
                const contName = gd.continents.find((c) => c.id === contId)?.name || contId;
                toast.info(`Reputation with ${contName} is now ${newLevel}.`);
            }
        }
        if (data.profession_ranks && data.profession_ranks.length > 0) {
            for (const [newRank, oldRank] of data.profession_ranks) {
                toast.success(`Profession rank up: ${oldRank} → ${newRank}!`);
            }
        }
    };

    const handleCombatStart = (data) => {
        setCombat(data);
    };

    const handleCombatEnd = (updatedChar, opts = {}) => {
        applyCharacterUpdate(updatedChar);
        setCombat(null);
        // On defeat with sanctuary teleport, go to the sanctuary town's sanctuary tab
        if (opts.sanctuaryTeleport?.town) {
            setTownId(opts.sanctuaryTeleport.town);
            setTownInitialTab("sanctuary");
            setTab("town");
        } else {
            setTownInitialTab(null);
        }
    };

    const applyCharacterUpdate = (next) => setCharacter(ensureBiome(next));

    const handleBiomeChange = async (biome) => {
        try {
            const { data } = await api.post("/game/character/travel", {
                continent: character.current_continent,
                biome,
            });
            applyCharacterUpdate(data.character);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    return (
        <div style={themeVars} className="min-h-screen p-3 md:p-4 bg-background text-foreground" data-testid="game-root">
            {/* Top bar */}
            <div className="max-w-7xl mx-auto mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-border pb-3">
                <div className="flex items-center gap-3">
                    <div className="font-pixel text-2xl uppercase text-primary tracking-wider">ERCHIS</div>
                    <div className="stat-label text-muted-foreground hidden md:block">
                        {activeContinent?.name} · {(character.current_biome?.replace(/_/g, " ") || "").toUpperCase()}
                    </div>
                </div>
                <div className="flex items-center gap-2 flex-wrap">
                    {TABS.map((t) => {
                        const Ic = t.icon;
                        return (
                            <button
                                key={t.id}
                                data-testid={`tab-${t.id}`}
                                onClick={() => { setTab(t.id); setTownId(null); setTownMenuOpen(false); closePanels(); }}
                                className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 flex items-center gap-1.5 ${
                                    tab === t.id
                                        ? "border-primary bg-primary text-primary-foreground"
                                        : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                                }`}
                            >
                                <Ic size={14} strokeWidth={1.5} /> {t.label}
                            </button>
                        );
                    })}
                    <div className="relative">
                        <button
                            data-testid="tab-town"
                            onClick={() => setTownMenuOpen((v) => !v)}
                            className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 flex items-center gap-1.5 ${
                                townId
                                    ? "border-primary bg-primary text-primary-foreground"
                                    : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                            }`}
                        >
                            <Building2 size={14} strokeWidth={1.5} /> Town
                        </button>
                        {townMenuOpen && (
                            <div className="absolute z-20 mt-2 min-w-[200px] bg-background border border-primary p-2 shadow-lg">
                                {(() => {
                                    const nearby = towns.filter((t) => t.continent === character.current_continent);
                                    if (nearby.length === 0) return <div className="stat-label text-muted-foreground px-2 py-1">No towns nearby</div>;
                                    return nearby.map((t) => (
                                        <button
                                            key={t.id}
                                            onClick={() => { setTownId(t.id); setTab("town"); setTownMenuOpen(false); closePanels(); }}
                                            data-testid={`goto-town-${t.id}`}
                                            className="block w-full text-left text-xs font-mono py-1 px-2 hover:text-primary"
                                        >
                                            {t.name}{(character.visited_towns || []).includes(t.id) ? "" : "?"}
                                        </button>
                                    ));
                                })()}
                            </div>
                        )}
                    </div>
                    <button
                        data-testid="tab-guild"
                        onClick={() => { setTab("guild"); setTownId(null); setTownMenuOpen(false); closePanels(); }}
                        className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 flex items-center gap-1.5 ${
                            tab === "guild"
                                ? "border-primary bg-primary text-primary-foreground"
                                : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                        }`}
                    >
                        <Shield size={14} strokeWidth={1.5} /> Guild
                    </button>
                    <button
                        data-testid="tab-journal"
                        onClick={() => { setTab("journal"); setTownId(null); setTownMenuOpen(false); closePanels(); }}
                        className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 flex items-center gap-1.5 ${
                            tab === "journal"
                                ? "border-primary bg-primary text-primary-foreground"
                                : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                        }`}
                    >
                        <ScrollText size={14} strokeWidth={1.5} /> Journal
                    </button>
                    <button
                        data-testid="tab-ladder"
                        onClick={() => { setTab("ladder"); setTownId(null); setTownMenuOpen(false); closePanels(); }}
                        className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 flex items-center gap-1.5 ${
                            tab === "ladder"
                                ? "border-primary bg-primary text-primary-foreground"
                                : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                        }`}
                    >
                        <Trophy size={14} strokeWidth={1.5} /> Ladder
                    </button>
                    <button
                        data-testid="btn-logout"
                        onClick={logout}
                        className="press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 border-border text-muted-foreground hover:border-destructive hover:text-destructive flex items-center gap-1.5"
                    >
                        <LogOut size={14} strokeWidth={1.5} /> Exit
                    </button>
                </div>
            </div>

            {/* Main full-width content + slide panels */}
            <div className="max-w-7xl mx-auto">
                <main className="w-full">
                    {combat ? (
                        <CombatScreen
                            combatStart={combat}
                            character={character}
                            itemsById={gd.itemsById}
                            skillsById={gd.skillsById}
                            onEnd={handleCombatEnd}
                            onCharacterUpdate={applyCharacterUpdate}
                            pendingSkillId={pendingSkillId}
                            setPendingSkillId={setPendingSkillId}
                            pendingItemId={pendingItemId}
                            setPendingItemId={setPendingItemId}
                        />
                    ) : townId ? (
                        <TownView
                            townId={townId}
                            character={character}
                            onCharacterUpdate={applyCharacterUpdate}
                            onLeave={() => { setTownId(null); setTownInitialTab(null); setTab("biome"); }}
                            onTravel={setTownId}
                            onCombatStart={handleCombatStart}
                            initialTab={townInitialTab}
                            onTabChange={closePanels}
                        />
                    ) : (
                        <>
                            {tab === "character" && (
                                <CharacterPanel
                                    character={character}
                                    portraits={gd.portraits}
                                    race={race}
                                    role={role}
                                    mastery={mastery}
                                    itemsById={gd.itemsById}
                                    skillsById={gd.skillsById}
                                    rogueInnateSkills={gd.rogueInnateSkills}
                                    roguePassives={gd.roguePassives}
                                    masteryPassives={gd.masteryPassives}
                                    timeOfDay={timeOfDay}
                                    onCharacterUpdate={applyCharacterUpdate}
                                    onDeleteCharacter={async () => {
                                        try {
                                            await api.delete("/game/character");
                                            toast.success("Character deleted.");
                                        } catch (e) {
                                            toast.error(extractError(e));
                                        }
                                        logout();
                                    }}
                                />
                            )}
                            {tab === "biome" && (
                                <BiomeView
                                    character={character}
                                    continent={activeContinent}
                                    onBiomeChange={handleBiomeChange}
                                    onActionResult={handleActionResult}
                                    onCombatStart={handleCombatStart}
                                />
                            )}
                            {tab === "guild" && (
                                <GuildHouse
                                    character={character}
                                    embedded
                                    onCharacterUpdate={applyCharacterUpdate}
                                />
                            )}
                            {tab === "ladder" && (
                                <LeaderboardPage embedded />
                            )}
                            {tab === "journal" && (
                                <JournalDrawer embedded />
                            )}
                        </>
                    )}
                </main>
            </div>

            {/* Left slide panel — character sheet + racial abilities */}
            <SlidePanel
                side="left"
                defaultOpen={true}
                open={leftPanelOpen}
                onOpenChange={setLeftPanelOpen}
                tabs={[
                    {
                        id: "char",
                        label: "Hero",
                        icon: User,
                        content: (
                            <div className="space-y-4">
                                <CharacterSheet
                                    character={character}
                                    portraits={gd.portraits}
                                    race={race}
                                    role={role}
                                    mastery={mastery}
                                    itemsById={gd.itemsById}
                                    timeOfDay={timeOfDay}
                                />
                                <div className="panel p-4">
                                    <RacialAbilityPanel character={character} onCharacterUpdate={setCharacter} timeOfDay={timeOfDay} />
                                </div>
                            </div>
                        ),
                    },
                ]}
            />

            {/* Right slide panel — dailies + world events */}
            <SlidePanel
                side="right"
                defaultOpen={false}
                open={rightPanelOpen}
                onOpenChange={setRightPanelOpen}
                tabs={[
                    {
                        id: "daily",
                        label: "Dailies",
                        icon: Sun,
                        content: <DailyPanel character={character} onCharacterUpdate={setCharacter} />,
                    },
                    {
                        id: "world",
                        label: "World",
                        icon: Globe,
                        content: <WorldEvents />,
                    },
                ]}
            />

            {narrativeResult && !combat && !encounter && (
                <NarrativeReveal
                    result={narrativeResult}
                    itemsById={gd.itemsById}
                    onClose={() => setNarrativeResult(null)}
                />
            )}
            {encounter && !combat && (
                <EncounterModal
                    encounter={encounter}
                    character={character}
                    onCharacterUpdate={applyCharacterUpdate}
                    onCombatStart={handleCombatStart}
                    onClose={() => setEncounter(null)}
                />
            )}
            {loginReward && (
                <LoginRewardModal reward={loginReward} onClose={() => setLoginReward(null)} />
            )}
            {heritageArrival && (
                <HeritageArrivalModal
                    character={character}
                    continent={heritageArrival.continent}
                    heritageData={heritageArrival}
                    onClose={() => setHeritageArrival(null)}
                    onCharacterUpdate={setCharacter}
                />
            )}
            {showTutorial && (
                <TutorialOverlay
                    character={character}
                    onComplete={() => {
                        setShowTutorial(false);
                        setCharacter((prev) => (prev ? { ...prev, tutorial_complete: true } : prev));
                    }}
                />
            )}
        </div>
    );
}
