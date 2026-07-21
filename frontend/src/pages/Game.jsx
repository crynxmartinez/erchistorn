import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import { useGameData } from "@/data/gameData";
import { toast } from "sonner";
import { LogOut, Trophy, Map, Package, Hammer, BookOpen, Home as HomeIcon } from "lucide-react";

import CharacterSheet from "@/components/CharacterSheet";
import BiomeView from "@/components/BiomeView";
import WorldMap from "@/components/WorldMap";
import CombatScreen from "@/components/CombatScreen";
import NarrativeReveal from "@/components/NarrativeReveal";
import Inventory from "@/components/Inventory";
import CraftingPanel from "@/components/CraftingPanel";
import SkillsPanel from "@/components/SkillsPanel";
import DailyPanel from "@/components/DailyPanel";
import WorldEvents from "@/components/WorldEvents";
import TutorialOverlay from "@/components/TutorialOverlay";
import LoginRewardModal from "@/components/LoginRewardModal";

const TABS = [
    { id: "biome",   label: "Biome",    icon: HomeIcon },
    { id: "map",     label: "World",    icon: Map },
    { id: "inv",     label: "Inventory",icon: Package },
    { id: "craft",   label: "Forge",    icon: Hammer },
    { id: "skills",  label: "Skills",   icon: BookOpen },
];

export default function Game() {
    const { logout } = useAuth();
    const gd = useGameData();
    const [character, setCharacter] = useState(null);
    const [loginReward, setLoginReward] = useState(null);
    const [tab, setTab] = useState("biome");
    const [narrativeResult, setNarrativeResult] = useState(null);
    const [combat, setCombat] = useState(null);
    const [showTutorial, setShowTutorial] = useState(false);

    const loadCharacter = useCallback(async () => {
        try {
            const { data } = await api.get("/game/character");
            setCharacter(data.character);
            if (data.login_reward) setLoginReward(data.login_reward);
            if (!data.character.tutorial_complete) setShowTutorial(true);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, []);

    useEffect(() => {
        loadCharacter();
    }, [loadCharacter]);

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

    const handleActionResult = (data) => {
        setNarrativeResult(data.result);
        setCharacter(data.character);
    };

    const handleCombatStart = (data) => {
        setCombat(data);
    };

    const handleCombatEnd = (updatedChar) => {
        setCharacter(updatedChar);
        setCombat(null);
    };

    const handleBiomeChange = async (biome) => {
        try {
            const { data } = await api.post("/game/character/travel", {
                continent: character.current_continent,
                biome,
            });
            setCharacter(data.character);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const handleTravel = async (continentId, biomeId) => {
        try {
            const { data } = await api.post("/game/character/travel", {
                continent: continentId,
                biome: biomeId,
            });
            setCharacter(data.character);
            setTab("biome");
            toast.success("You travel to a new land");
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    return (
        <div className="min-h-screen p-3 md:p-4" data-testid="game-root">
            {/* Top bar */}
            <div className="max-w-7xl mx-auto mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-border pb-3">
                <div className="flex items-center gap-3">
                    <div className="font-pixel text-2xl uppercase text-primary tracking-wider">ERCHIS</div>
                    <div className="stat-label text-muted-foreground hidden md:block">
                        {activeContinent?.name} · {character.current_biome.replace(/_/g, " ").toUpperCase()}
                    </div>
                </div>
                <div className="flex items-center gap-2 flex-wrap">
                    {TABS.map((t) => {
                        const Ic = t.icon;
                        return (
                            <button
                                key={t.id}
                                data-testid={`tab-${t.id}`}
                                onClick={() => setTab(t.id)}
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
                    <Link
                        to="/leaderboard"
                        data-testid="tab-leaderboard"
                        className="press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 border-border text-muted-foreground hover:border-primary hover:text-primary flex items-center gap-1.5"
                    >
                        <Trophy size={14} strokeWidth={1.5} /> Ladder
                    </Link>
                    <button
                        data-testid="btn-logout"
                        onClick={logout}
                        className="press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 border-border text-muted-foreground hover:border-destructive hover:text-destructive flex items-center gap-1.5"
                    >
                        <LogOut size={14} strokeWidth={1.5} /> Exit
                    </button>
                </div>
            </div>

            {/* Main 3-column grid */}
            <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-4">
                <aside className="lg:col-span-3">
                    <CharacterSheet
                        character={character}
                        portraits={gd.portraits}
                        race={race}
                        role={role}
                        mastery={mastery}
                        itemsById={gd.itemsById}
                    />
                </aside>

                <main className="lg:col-span-6">
                    {combat ? (
                        <CombatScreen
                            combatStart={combat}
                            character={character}
                            itemsById={gd.itemsById}
                            skillsById={gd.skillsById}
                            onEnd={handleCombatEnd}
                        />
                    ) : (
                        <>
                            {tab === "biome" && (
                                <BiomeView
                                    character={character}
                                    continent={activeContinent}
                                    onBiomeChange={handleBiomeChange}
                                    onActionResult={handleActionResult}
                                    onCombatStart={handleCombatStart}
                                />
                            )}
                            {tab === "map" && (
                                <WorldMap
                                    continents={gd.continents}
                                    character={character}
                                    onTravel={handleTravel}
                                />
                            )}
                            {tab === "inv" && (
                                <Inventory
                                    character={character}
                                    itemsById={gd.itemsById}
                                    onCharacterUpdate={setCharacter}
                                />
                            )}
                            {tab === "craft" && (
                                <CraftingPanel
                                    character={character}
                                    recipes={gd.recipes}
                                    itemsById={gd.itemsById}
                                    onCharacterUpdate={setCharacter}
                                />
                            )}
                            {tab === "skills" && (
                                <SkillsPanel
                                    character={character}
                                    skillsById={gd.skillsById}
                                    teachers={gd.teachers}
                                    onCharacterUpdate={setCharacter}
                                />
                            )}
                        </>
                    )}
                </main>

                <aside className="lg:col-span-3 space-y-4">
                    <DailyPanel character={character} onCharacterUpdate={setCharacter} />
                    <WorldEvents />
                </aside>
            </div>

            {narrativeResult && !combat && (
                <NarrativeReveal
                    result={narrativeResult}
                    onClose={() => setNarrativeResult(null)}
                />
            )}
            {loginReward && (
                <LoginRewardModal reward={loginReward} onClose={() => setLoginReward(null)} />
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
