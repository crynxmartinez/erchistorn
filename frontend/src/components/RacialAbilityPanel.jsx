import { useEffect, useState, useRef } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Zap, ChevronUp, Flame } from "lucide-react";
import { HERITAGE_LABEL, HERITAGE_SURGES, HERITAGE_RANK_LEVEL_REQS, HERITAGE_RANK_MULT, MAX_HERITAGE_RANK } from "@/data/racialConstants";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import { RESOURCE_META as SHARED_RESOURCE_META, RACE_TO_RESOURCE } from "@/data/hints";

const RESOURCE_COLORS = {
    oath_progress:    "hsl(46 65% 52%)",
    celestial_charge: "hsl(207 90% 54%)",
    stoneguard:       "hsl(35 5% 62%)",
    harmony:          "hsl(291 64% 52%)",
    defiance:         "hsl(0 60% 45%)",
    inner_blood:      "hsl(4 90% 58%)",
    tide:             "hsl(196 70% 50%)",
    verdant_essence:  "hsl(122 39% 49%)",
};
const RESOURCE_META = Object.fromEntries(
    Object.entries(SHARED_RESOURCE_META).map(([k, v]) => [k, { ...v, color: RESOURCE_COLORS[k] }])
);

/**
 * RacialAbilityPanel — shows racial rank, resource meter, and active racial abilities.
 */
export default function RacialAbilityPanel({ character, onCharacterUpdate, timeOfDay }) {
    const [state, setState] = useState({ race: null, abilities: [] });
    const [busy, setBusy] = useState(false);
    const [heritageInfo, setHeritageInfo] = useState(null);
    const [now, setNow] = useState(Date.now());
    const fetchedAt = useRef(0);

    // Tick every second for cooldown countdowns
    useEffect(() => {
        const timer = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(timer);
    }, []);

    const reload = async () => {
        try {
            const r = await api.get("/game/racial/status");
            setState(r.data);
            fetchedAt.current = Date.now();
        } catch (e) { toast.error(extractError(e)); }
    };
    useEffect(() => { reload(); }, [
        character?.race,
        character?.heritage_rank,
        character?.heritage_surge_active,
        character?.statuses?.length,
    ]);

    const reloadHeritage = async () => {
        try {
            const r = await api.get("/game/heritage/info");
            setHeritageInfo(r.data);
        } catch (e) { /* silent */ }
    };
    useEffect(() => { reloadHeritage(); }, [
        character?.heritage_rank,
        character?.level,
        character?.oath_progress, character?.celestial_charge, character?.stoneguard,
        character?.harmony, character?.defiance, character?.inner_blood,
        character?.tide, character?.verdant_essence,
    ]);

    const rankUp = async () => {
        setBusy(true);
        try {
            const r = await api.post("/game/heritage/rankup");
            toast.success(r.data.message);
            onCharacterUpdate?.(r.data.character);
            await reloadHeritage();
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };

    const [surgeNarrative, setSurgeNarrative] = useState("");

    const use = async (ability_id, extra = {}) => {
        setBusy(true);
        try {
            const r = await api.post("/game/racial/ability", { ability_id, ...extra });
            toast.success(r.data.message);
            if (r.data.narrative) {
                setSurgeNarrative(r.data.narrative);
            }
            onCharacterUpdate?.(r.data.character);
            await reload();
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };

    const race = character.race;
    const resourceKey = RACE_TO_RESOURCE[race];
    const meta = RESOURCE_META[resourceKey] || {};
    const value = character[resourceKey] || 0;
    const pct = Math.round((value / (meta.max || 1)) * 100);
    const heritageLabel = HERITAGE_LABEL[race] || "Racial";
    const isResourceFull = value >= (meta.max || 1);
    const heritageRank = character.heritage_rank || 1;
    const charLevel = character.level || 1;
    const isMaxRank = heritageRank >= MAX_HERITAGE_RANK;
    const nextRankIdx = heritageRank - 1;
    const nextLevelReq = isMaxRank ? null : HERITAGE_RANK_LEVEL_REQS[nextRankIdx];
    const surge = HERITAGE_SURGES[race] || {};
    const canRankUp = !isMaxRank && isResourceFull && charLevel >= (nextLevelReq || 0);
    const levelLocked = !isMaxRank && charLevel < (nextLevelReq || 0);
    const passiveMult = HERITAGE_RANK_MULT[heritageRank - 1] || 1.0;

    const rankHeader = (
        <div className="border-t border-border pt-3 mb-3" data-testid="racial-panel">
            <div className="stat-label mb-2 flex items-center justify-between">
                <span>RACIAL — RANK {heritageRank}{isMaxRank ? " (MAX)" : ""}</span>
                {race === "elf" || race === "sylvan" ? (
                    <span className={`stat-label ${timeOfDay === "lunar" ? "text-rarity-rare" : "text-primary"}`} data-testid="celestial-state">
                        {timeOfDay === "lunar" ? "☾ LUNAR" : "☀ SOLAR"}
                    </span>
                ) : null}
            </div>

            {/* Passive multiplier indicator */}
            {passiveMult > 1.0 && (
                <div className="stat-label text-primary/60 mb-1 text-[10px]">
                    Passive Power: <span className="text-primary">{Math.round(passiveMult * 100)}%</span>
                </div>
            )}

            <Tooltip>
                <TooltipTrigger asChild>
                    <div className="text-xs font-mono mb-1 flex justify-between cursor-help">
                        <span className="text-muted-foreground">{meta.label || heritageLabel}</span>
                        <span className="text-primary" data-testid="racial-resource-value">{value}/{meta.max}</span>
                    </div>
                </TooltipTrigger>
                <TooltipContent side="bottom"><div className="font-pixel text-xs leading-snug max-w-[240px]">{meta.hint || "Racial resource — grows through your bloodline's ways. Fill to rank up."}</div></TooltipContent>
            </Tooltip>
            <div className="h-2 bg-background border border-border relative">
                <div
                    className={`h-full transition-all ${isResourceFull ? "animate-pulse" : ""}`}
                    style={{ width: `${pct}%`, backgroundColor: meta.color || "hsl(var(--primary))" }}
                />
            </div>

            {/* Rank Up section — one bar, one button */}
            <div className="mt-2">
                {isMaxRank ? (
                    <div className="stat-label text-center text-amber-500 text-[10px] py-1">MAX RANK ACHIEVED</div>
                ) : canRankUp ? (
                    <button
                        onClick={rankUp}
                        disabled={busy}
                        data-testid="btn-heritage-rankup"
                        className="press-btn font-pixel text-xs uppercase w-full px-3 py-1.5 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground flex items-center justify-center gap-1.5 disabled:opacity-40"
                    >
                        <ChevronUp size={14} /> RANK UP TO {heritageRank + 1}
                    </button>
                ) : levelLocked ? (
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <div className="stat-label text-center text-muted-foreground/50 text-[10px] py-1 cursor-help" data-testid="rankup-locked-level">
                                LOCKED — Requires Lv {nextLevelReq} (you are {charLevel})
                            </div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom">
                            <div className="font-pixel text-xs leading-snug max-w-[220px]">
                                Rank up every 10 character levels. Keep leveling!
                            </div>
                        </TooltipContent>
                    </Tooltip>
                ) : !isResourceFull ? (
                    <div className="stat-label text-center text-muted-foreground/50 text-[10px] py-1" data-testid="rankup-need-resource">
                        FILL RESOURCE BAR TO RANK UP
                    </div>
                ) : null}

                {/* Next rank surge preview */}
                {!isMaxRank && surge && (
                    <div className="stat-label text-[10px] text-muted-foreground mt-1 text-center">
                        Next Rank unlocks: <span className="text-amber-500">{surge.name}</span>
                    </div>
                )}
            </div>

            {race === "wildblood" && character.beast_aspect && (
                <div className="stat-label mt-2 text-muted-foreground">
                    ASPECT: <span className="text-primary uppercase">{character.beast_aspect.replace(/_/g, " ")}</span>
                </div>
            )}
            {race === "hyliondrian" && character.marine_adaptation && (
                <div className="stat-label mt-2 text-muted-foreground">
                    ADAPTATION: <span className="text-primary uppercase">{character.marine_adaptation.replace(/_/g, " ")}</span>
                </div>
            )}
        </div>
    );

    if (!state.abilities || state.abilities.length === 0) {
        return (
            <TooltipProvider delayDuration={120}>
            <div data-testid="racial-ability-panel">
                {rankHeader}
                <div className="stat-label text-muted-foreground italic" data-testid="racial-ability-panel-empty">
                    No active racial abilities for your bloodline yet. More coming in a future season.
                </div>
            </div>
            </TooltipProvider>
        );
    }

    return (
        <TooltipProvider delayDuration={120}>
        <div data-testid="racial-ability-panel">
            {rankHeader}
            <div className="mb-3">
                <div className="stat-label text-primary/70">BLOODLINE ART</div>
                <div className="font-pixel text-2xl uppercase text-primary flex items-center gap-2">
                    <Zap size={16} strokeWidth={1.5} /> Racial Abilities
                </div>
            </div>
            <div className="space-y-3">
                {state.abilities.map((a) => {
                    const elapsed = fetchedAt.current ? Math.floor((now - fetchedAt.current) / 1000) : 0;
                    const remaining = Math.max(0, (a.seconds_remaining || 0) - elapsed);
                    const mins = Math.floor(remaining / 60);
                    const secs = remaining % 60;
                    return (
                        <div key={a.id} className="border border-border p-3 overflow-hidden" data-testid={`racial-ability-${a.id}`}>
                            <div className="flex justify-between items-baseline gap-2">
                                <div className="font-pixel text-lg uppercase text-primary break-words">{a.name}</div>
                                <div className="stat-label text-primary/70 whitespace-nowrap flex-shrink-0">CD: {a.cooldown_hours}h</div>
                            </div>
                            {a.cost ? (
                                <div className="stat-label text-primary/50 text-[10px] mt-0.5 break-words">
                                    Costs {a.cost} {a.cost_resource?.replace(/_/g, " ")}
                                </div>
                            ) : null}
                            {!a.available && a.reason && (
                                <div className="stat-label text-destructive mt-1 break-words">
                                    {a.reason}{remaining > 0 ? ` · ${mins}m ${secs}s` : ""}
                                </div>
                            )}

                            {/* Heritage Surge — the one and only racial active ability */}
                            {a.id === "heritage_surge" && (
                                <>
                                    {a.description && (
                                        <div className="text-xs text-amber-500/80 mt-2 italic leading-relaxed break-words">
                                            {a.description}
                                        </div>
                                    )}
                                    {a.duration && (
                                        <div className="stat-label text-amber-500/50 mt-1 text-[10px] break-words leading-relaxed">
                                            Duration: {a.duration} actions · Cooldown: {a.cooldown_hours}h · Cost: Full {a.cost_resource?.replace(/_/g, " ")}
                                        </div>
                                    )}
                                    {surgeNarrative && a.active_surge && (
                                        <div className="text-xs text-amber-500/60 mt-2 italic border-l-2 border-amber-500/30 pl-2" data-testid="surge-narrative">
                                            {surgeNarrative}
                                        </div>
                                    )}
                                    {a.active_surge ? (
                                        <div className="mt-2">
                                            <div className="stat-label text-amber-500 text-[10px] mb-1" data-testid="surge-active">
                                                ACTIVE — {a.active_surge.actions_remaining} action{a.active_surge.actions_remaining !== 1 ? "s" : ""} remaining
                                            </div>
                                            <div className="h-1.5 bg-background border border-amber-500/30">
                                                <div
                                                    className="h-full bg-amber-500 transition-all animate-pulse"
                                                    style={{ width: `${(a.active_surge.actions_remaining / a.duration) * 100}%` }}
                                                />
                                            </div>
                                        </div>
                                    ) : (
                                        <button
                                            onClick={() => use("heritage_surge")}
                                            disabled={busy || !a.available}
                                            data-testid="btn-heritage-surge"
                                            className="press-btn font-pixel text-sm uppercase mt-2 px-3 py-1 border-2 border-amber-500 text-amber-500 hover:bg-amber-500 hover:text-amber-950 flex items-center justify-center gap-1.5 disabled:opacity-40"
                                        >
                                            <Flame size={12} /> {a.name}
                                        </button>
                                    )}
                                </>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
        </TooltipProvider>
    );
}
