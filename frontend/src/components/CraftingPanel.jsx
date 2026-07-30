import { useEffect, useState, useMemo, useRef } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import Dice from "@/components/Dice";
import PixelSprite from "@/components/PixelSprite";
import ItemTooltip from "@/components/ItemTooltip";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Clock, X, Package, Search, ChevronDown } from "lucide-react";
import { RARITY_TEXT } from "@/data/gameData";

const TIER_LABELS = ["T1", "T2", "T3", "T4", "T5", "T6"];
const RANK_LABELS = ["Novice", "Apprentice", "Journeyman", "Expert", "Master", "Grandmaster"];

export default function CraftingPanel({ character, itemsById, onCharacterUpdate, professions: propProfessions, professionsLoading: propProfessionsLoading }) {
    const [rolling, setRolling] = useState(false);
    const [lastCraft, setLastCraft] = useState(null);
    const [queue, setQueue] = useState(character?.crafting_queue || []);
    const [recipes, setRecipes] = useState([]);
    const [recipesLoading, setRecipesLoading] = useState(true);
    const [localProfessions, setLocalProfessions] = useState([]);
    const [localProfessionsLoading, setLocalProfessionsLoading] = useState(true);
    const professions = propProfessions !== undefined ? propProfessions : localProfessions;
    const professionsLoading = propProfessionsLoading !== undefined ? propProfessionsLoading : localProfessionsLoading;
    const [currentTown, setCurrentTown] = useState(character?.current_town);
    const [activeProf, setActiveProf] = useState(null);
    const [activeSubTab, setActiveSubTab] = useState("refine");
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        setQueue(character?.crafting_queue || []);
        setCurrentTown(character?.current_town);
    }, [character?.crafting_queue, character?.current_town]);

    useEffect(() => {
        const handler = (e) => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener("mousedown", handler);
        return () => document.removeEventListener("mousedown", handler);
    }, []);

    useEffect(() => {
        setSelectedRecipe(null);
        setSearchQuery("");
    }, [activeProf, activeSubTab]);

    // Fetch recipes available at the current town/continent
    useEffect(() => {
        let mounted = true;
        const load = async () => {
            try {
                setRecipesLoading(true);
                const { data } = await api.get("/game/data/recipes");
                if (mounted) setRecipes(data.recipes || []);
            } catch (e) { toast.error(extractError(e)); }
            finally { if (mounted) setRecipesLoading(false); }
        };
        load();
        return () => { mounted = false; };
    }, [character?.current_continent, character?.current_town, professions]);

    // Fetch character's learned professions
    useEffect(() => {
        if (propProfessions !== undefined) return;
        let mounted = true;
        const load = async () => {
            try {
                const { data } = await api.get("/game/professions/mine");
                if (mounted) {
                    setLocalProfessions(data.professions || []);
                    const craftProfs = (data.professions || []).filter(p => p.kind === "crafting");
                    if (craftProfs.length > 0 && !activeProf) {
                        setActiveProf(craftProfs[0].id);
                    }
                }
            } catch (e) { /* ignore */ }
            finally { if (mounted) setLocalProfessionsLoading(false); }
        };
        load();
        return () => { mounted = false; };
    }, [character?.professions, propProfessions]);

    // Set active profession when data arrives (from props or local fetch)
    useEffect(() => {
        if (!activeProf && professions.length > 0) {
            const craftProfs = professions.filter(p => p.kind === "crafting");
            if (craftProfs.length > 0) setActiveProf(craftProfs[0].id);
        }
    }, [professions, activeProf]);

    // Poll crafting queue for timer updates (only when a craft is in progress)
    const [queueActive, setQueueActive] = useState((character?.crafting_queue || []).some(q => !q.claimed));
    useEffect(() => {
        // Check if there's an active (unclaimed) craft in the queue
        const hasActive = (queue || []).some(q => !q.claimed);
        setQueueActive(hasActive);
    }, [queue]);

    useEffect(() => {
        if (!queueActive) return;
        let mounted = true;
        const tick = async () => {
            try {
                const { data } = await api.get("/game/craft/queue");
                if (mounted) {
                    setQueue(data.queue || []);
                    onCharacterUpdate?.(data.character);
                }
            } catch { /* ignore */ }
        };
        tick();
        const id = setInterval(tick, 1000);
        return () => { mounted = false; clearInterval(id); };
    }, [queueActive, onCharacterUpdate]);

    const invMap = Object.fromEntries((character.inventory || []).map(i => [i.item_id, i.quantity]));
    const busy = queue.length > 0 && !queue[0].claimed;

    const canCraft = (recipe) => {
        if (busy) return false;
        if (!currentTown) return false;
        if (!recipe.available_here) return false;
        if (character.level < (recipe.min_level || 1)) return false;
        if (recipe.profession_id && !recipe.rank_ok) return false;
        for (const [mat, q] of recipe.materials) {
            if ((invMap[mat] || 0) < q) return false;
        }
        return true;
    };

    const craft = async (recipe_id) => {
        setRolling(true);
        setLastCraft(null);
        try {
            const { data } = await api.post("/game/craft", { recipe_id });
            onCharacterUpdate?.(data.character);
            if (data.queued) {
                setQueue(data.character?.crafting_queue || []);
                toast.info(`${data.result.recipe_name} is being crafted.`);
            } else {
                setLastCraft(data.result);
                try {
                    const { data: profData } = await api.get("/game/professions/mine");
                    setLocalProfessions(profData.professions || []);
                } catch { /* ignore */ }
            }
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    const claim = async () => {
        setRolling(true);
        try {
            const { data } = await api.post("/game/craft/claim");
            onCharacterUpdate?.(data.character);
            setLastCraft(data.result);
            setQueue(data.character?.crafting_queue || []);
            try {
                const { data: profData } = await api.get("/game/professions/mine");
                setLocalProfessions(profData.professions || []);
            } catch { /* ignore */ }
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    const cancel = async () => {
        setRolling(true);
        try {
            const { data } = await api.post("/game/craft/cancel");
            onCharacterUpdate?.(data.character);
            setQueue(data.character?.crafting_queue || []);
            toast(data.message);
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    const fmtDuration = (secs) => secs <= 0 ? "instant" : secs < 60 ? `${secs}s` : `${Math.ceil(secs / 60)}m`;
    const nowMs = Date.now();
    const active = busy ? queue[0] : null;
    const finishesAt = active ? new Date(active.finishes_at).getTime() : 0;
    const remainingMs = Math.max(0, finishesAt - nowMs);
    const isReady = active && remainingMs <= 0;

    // Group recipes by profession and tier
    const craftingProfessions = professions.filter(p => p.kind === "crafting");
    const activeProfData = craftingProfessions.find(p => p.id === activeProf);

    const profRecipes = useMemo(() => {
        if (!activeProf) return [];
        return recipes.filter(r => r.profession_id === activeProf);
    }, [recipes, activeProf]);

    const refineRecipes = useMemo(() => profRecipes.filter(r => r.is_refinement), [profRecipes]);
    const tierRecipes = useMemo(() => {
        const byTier = {};
        for (let t = 1; t <= 6; t++) {
            byTier[t] = profRecipes.filter(r => !r.is_refinement && r.gear_tier === t);
        }
        return byTier;
    }, [profRecipes]);

    const introRecipes = useMemo(() => recipes.filter(r => !r.profession_id), [recipes]);
    const profTier = activeProfData?.tier ?? 0;

    const activeRecipes = !activeProf
        ? introRecipes
        : activeSubTab === "refine" ? refineRecipes : (tierRecipes[parseInt(activeSubTab.slice(1))] || []);

    const filteredRecipes = useMemo(() => {
        if (!searchQuery.trim()) return activeRecipes;
        const q = searchQuery.toLowerCase();
        return activeRecipes.filter(r => {
            const output = itemsById?.[r.output_by_tier?.fine || r.output_by_tier?.crude];
            return (r.name || "").toLowerCase().includes(q) ||
                   (output?.name || "").toLowerCase().includes(q);
        });
    }, [activeRecipes, searchQuery, itemsById]);

    const renderRecipeDetail = (r) => {
        if (!r) return null;
        const output = itemsById?.[r.output_by_tier?.fine || r.output_by_tier?.crude];
        const okay = canCraft(r);
        return (
            <div className="panel p-4" data-testid={`recipe-detail-${r.id}`}>
                <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center gap-3">
                        {output && <ItemTooltip item={output}><span><PixelSprite item={output} size={40} /></span></ItemTooltip>}
                        <div>
                            <div className={`font-pixel text-lg uppercase ${RARITY_TEXT[output?.rarity || "common"]}`}>
                                {r.name}
                            </div>
                            {output?.name && output?.name !== r.name && (
                                <div className="stat-label text-muted-foreground mt-0.5">{output.name}</div>
                            )}
                        </div>
                    </div>
                    <div className="stat-label">Lv {r.min_level}+</div>
                </div>
                {output?.stats && Object.keys(output.stats).length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3 text-xs font-mono">
                        {Object.entries(output.stats).map(([stat, val]) => (
                            <span key={stat} className={`px-2 py-0.5 border ${val > 0 ? "border-primary/40 text-primary" : "border-destructive/40 text-destructive"}`}>
                                {val > 0 ? "+" : ""}{val} {stat.slice(0, 3).toUpperCase()}
                            </span>
                        ))}
                    </div>
                )}
                {output?.power > 0 && (
                    <div className="stat-label text-xs text-muted-foreground mb-3">
                        Power {output.power}
                    </div>
                )}
                <div className="flex justify-between items-center text-xs text-muted-foreground mb-3">
                    <span className="flex items-center gap-1"><Clock size={12} /> {fmtDuration(r.duration_seconds)}</span>
                    <span className="flex items-center gap-1"><Package size={12} /> {r.rarity}</span>
                </div>
                <div className="border-t border-border pt-3 mb-3">
                    <div className="stat-label text-primary/70 mb-2">MATERIALS</div>
                    <div className="text-xs font-mono space-y-1">
                        {r.materials.map(([mat, q]) => {
                            const have = invMap[mat] || 0;
                            return (
                                <div key={mat} className="flex justify-between">
                                    <span className="text-muted-foreground">
                                        {itemsById?.[mat]?.name || mat}
                                    </span>
                                    <span className={have >= q ? "text-primary" : "text-destructive"}>
                                        {have}/{q}
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                </div>
                <button
                    data-testid={`craft-btn-${r.id}`}
                    disabled={!okay || rolling}
                    onClick={() => craft(r.id)}
                    className="press-btn w-full font-pixel text-sm uppercase py-2 bg-primary/10 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                >
                    {r.duration_seconds > 0 ? "Begin Craft" : "Craft"}
                </button>
            </div>
        );
    };

    if (recipesLoading || professionsLoading) {
        return (
            <div className="panel p-6" data-testid="crafting-panel">
                <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Forge & Workshop</h3>
                <div className="text-center text-muted-foreground stat-label py-8">
                    Loading workshop...
                </div>
            </div>
        );
    }

    return (
        <TooltipProvider delayDuration={120}>
        <div className="panel p-6" data-testid="crafting-panel">
            <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Forge & Workshop</h3>
            <div className="stat-label text-muted-foreground mb-4">
                Every craft is a dice roll. Quality tiers: Crude · Fine · Masterwork.
            </div>

            {!currentTown && (
                <div className="mb-4 p-3 border border-destructive/50 bg-destructive/5 text-destructive stat-label">
                    You must be in a town with a trade NPC to craft here.
                </div>
            )}
            {active && (
                <div className="mb-4 p-3 border border-amber-400/50 bg-amber-400/5">
                    <div className="flex items-center justify-between mb-2">
                        <div className="font-pixel text-lg uppercase text-amber-400 flex items-center gap-2">
                            <Clock size={16} /> {active.recipe_name}
                        </div>
                        <div className="stat-label text-muted-foreground">
                            {isReady ? "READY" : `${Math.ceil(remainingMs / 1000)}s`}
                        </div>
                    </div>
                    <div className="h-1.5 bg-background border border-border mb-3">
                        <div
                            className="h-full bg-amber-400 transition-all"
                            style={{ width: active.duration_seconds > 0 ? `${Math.min(100, Math.max(0, ((active.duration_seconds * 1000 - remainingMs) / (active.duration_seconds * 1000)) * 100))}%` : "100%" }}
                        />
                    </div>
                    <div className="flex gap-2">
                        <button
                            onClick={claim}
                            disabled={!isReady || rolling}
                            className="press-btn flex-1 font-pixel text-sm uppercase py-1.5 bg-primary/10 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                        >
                            Claim
                        </button>
                        <button
                            onClick={cancel}
                            disabled={rolling}
                            className="press-btn font-pixel text-sm uppercase px-3 py-1.5 border border-destructive text-destructive hover:bg-destructive hover:text-destructive-foreground disabled:opacity-40"
                            title="Cancel (half materials refunded)"
                        >
                            <X size={14} />
                        </button>
                    </div>
                </div>
            )}

            {lastCraft && (
                <div className="mb-4 p-3 border border-primary bg-primary/5 flex items-center gap-4">
                    <Dice result={lastCraft.outcome} rolling={false} size={64} />
                    <div>
                        <div className="stat-label uppercase text-primary">
                            {lastCraft.tier.toUpperCase()}
                        </div>
                        <div className="narr text-sm text-foreground/85">{lastCraft.narrative}</div>
                        {lastCraft.output_item && (
                            <div className="stat-label mt-1 flex items-center gap-1.5">
                                {itemsById?.[lastCraft.output_item] && <PixelSprite item={itemsById[lastCraft.output_item]} size={20} />}
                                Produced: {itemsById?.[lastCraft.output_item]?.name || lastCraft.output_item}
                            </div>
                        )}
                        {(lastCraft.profession_points_gain || lastCraft.profession_xp_gain) && (
                            <div className="stat-label text-primary/70 mt-1">
                                +{lastCraft.profession_points_gain || lastCraft.profession_xp_gain} profession points
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Profession tabs */}
            {craftingProfessions.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                    {craftingProfessions.map(p => (
                        <button
                            key={p.id}
                            onClick={() => { setActiveProf(p.id); setActiveSubTab("refine"); }}
                            className={`press-btn px-3 py-1.5 font-pixel text-sm uppercase border transition-colors ${
                                activeProf === p.id
                                    ? "bg-primary text-primary-foreground border-primary"
                                    : "bg-primary/10 text-primary border-primary/30 hover:bg-primary/20"
                            }`}
                        >
                            {p.name}
                        </button>
                    ))}
                </div>
            )}

            {/* Profession progress bar */}
            {activeProfData && (
                <div className="mb-4 p-3 border border-border bg-background/50">
                    <div className="flex items-center justify-between mb-1">
                        <div className="font-pixel text-sm uppercase text-primary">
                            {activeProfData.name} — {RANK_LABELS[activeProfData.tier] || activeProfData.rank}
                        </div>
                        <div className="stat-label text-muted-foreground">
                            {activeProfData.points_in_tier}/{activeProfData.points_per_tier} pts
                        </div>
                    </div>
                    <div className="h-2 bg-background border border-border relative">
                        <div
                            className="h-full bg-primary transition-all"
                            style={{ width: `${Math.min(100, (activeProfData.points_in_tier / activeProfData.points_per_tier) * 100)}%` }}
                        />
                    </div>
                    {activeProfData.points_to_next > 0 && (
                        <div className="stat-label text-[10px] text-muted-foreground mt-1">
                            {activeProfData.points_to_next} points to {RANK_LABELS[activeProfData.tier + 1] || "next rank"}
                        </div>
                    )}
                </div>
            )}

            {/* Sub-tabs: Refine | T1 | T2 | T3 | T4 | T5 | T6 */}
            {activeProf && (
                <div className="flex flex-wrap gap-1 mb-4">
                    <button
                        onClick={() => setActiveSubTab("refine")}
                        className={`press-btn px-2 py-1 text-xs uppercase border ${activeSubTab === "refine" ? "bg-primary text-primary-foreground border-primary" : "border-border text-muted-foreground hover:bg-primary/10"}`}
                    >
                        Refine
                    </button>
                    {TIER_LABELS.map((label, idx) => {
                        const tier = idx + 1;
                        const unlocked = profTier >= tier - 1;
                        const hasRecipes = (tierRecipes[tier] || []).length > 0;
                        if (!hasRecipes) return null;
                        return (
                            <button
                                key={tier}
                                onClick={() => unlocked && setActiveSubTab(`t${tier}`)}
                                disabled={!unlocked}
                                className={`press-btn px-2 py-1 text-xs uppercase border ${
                                    activeSubTab === `t${tier}`
                                        ? "bg-primary text-primary-foreground border-primary"
                                        : unlocked
                                            ? "border-border text-muted-foreground hover:bg-primary/10"
                                            : "border-border/30 text-muted-foreground/30 cursor-not-allowed"
                                }`}
                            >
                                {label}{!unlocked && " \u{1F512}"}
                            </button>
                        );
                    })}
                </div>
            )}

            {/* Searchable dropdown + recipe detail */}
            {(activeProf || introRecipes.length > 0) && (
                <div className="space-y-4">
                    {/* Searchable dropdown */}
                    <div className="relative" ref={dropdownRef}>
                        <div
                            onClick={() => setDropdownOpen(v => !v)}
                            className="flex items-center gap-2 p-3 border border-border bg-background cursor-pointer hover:border-primary/50"
                        >
                            <Search size={16} className="text-muted-foreground" />
                            <span className="text-sm text-muted-foreground flex-1">
                                {selectedRecipe ? selectedRecipe.name : !activeProf ? "Search basic recipes..." : `Search ${activeSubTab === "refine" ? "refinement" : activeSubTab.toUpperCase()} recipes...`}
                            </span>
                            <ChevronDown size={16} className={`text-muted-foreground transition-transform ${dropdownOpen ? "rotate-180" : ""}`} />
                        </div>
                        {dropdownOpen && (
                            <div className="absolute z-30 left-0 right-0 mt-1 border border-border bg-background max-h-72 overflow-y-auto shadow-lg">
                                <div className="sticky top-0 bg-background border-b border-border p-2">
                                    <input
                                        type="text"
                                        autoFocus
                                        value={searchQuery}
                                        onChange={e => setSearchQuery(e.target.value)}
                                        placeholder="Type to search..."
                                        className="w-full text-sm bg-transparent border border-border px-2 py-1.5 focus:outline-none focus:border-primary"
                                    />
                                </div>
                                {filteredRecipes.length === 0 ? (
                                    <div className="p-3 text-center text-muted-foreground stat-label">No recipes found.</div>
                                ) : filteredRecipes.map(r => {
                                    const output = itemsById?.[r.output_by_tier?.fine || r.output_by_tier?.crude];
                                    const okay = canCraft(r);
                                    return (
                                        <div
                                            key={r.id}
                                            data-testid={`recipe-option-${r.id}`}
                                            onClick={() => { setSelectedRecipe(r); setDropdownOpen(false); }}
                                            className={`flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-primary/10 border-b border-border/30 ${!okay ? "opacity-50" : ""} ${selectedRecipe?.id === r.id ? "bg-primary/10" : ""}`}
                                        >
                                            {output && <ItemTooltip item={output}><span className="flex-shrink-0"><PixelSprite item={output} size={24} /></span></ItemTooltip>}
                                            <div className="flex-1 min-w-0">
                                                <div className={`text-sm truncate ${RARITY_TEXT[output?.rarity || "common"]}`}>{r.name}</div>
                                                <div className="text-[10px] text-muted-foreground">
                                                    {r.materials.map(([m, q]) => `${q}× ${itemsById?.[m]?.name || m}`).join(", ")}
                                                </div>
                                            </div>
                                            <div className="stat-label text-[10px] ml-2 shrink-0">Lv {r.min_level}+</div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>

                    {/* Selected recipe detail */}
                    {selectedRecipe ? (
                        renderRecipeDetail(selectedRecipe)
                    ) : (
                        <div className="text-center text-muted-foreground stat-label py-8 border border-border border-dashed">
                            {activeRecipes.length === 0
                                ? (!activeProf ? "No basic recipes available." : activeSubTab === "refine" ? "No refinement recipes available." : "No recipes at this tier.")
                                : `Select a recipe from the dropdown above to craft.`}
                        </div>
                    )}
                </div>
            )}

            {/* No professions learned and no intro recipes */}
            {craftingProfessions.length === 0 && introRecipes.length === 0 && (
                <div className="p-4 border border-border text-center text-muted-foreground stat-label">
                    You haven't learned any crafting professions yet. Visit a town and speak to the trade NPC to learn one.
                </div>
            )}
        </div>
        </TooltipProvider>
    );
}
