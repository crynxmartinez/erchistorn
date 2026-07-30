import { useEffect, useState } from "react";
import Dice from "@/components/Dice";
import PixelSprite from "@/components/PixelSprite";
import ItemTooltip from "@/components/ItemTooltip";
import { TooltipProvider } from "@/components/ui/tooltip";

const RARITY_STYLE = {
    common: "text-muted-foreground border-border",
    uncommon: "text-primary border-primary/40",
    rare: "text-amber-400 border-amber-400/50",
    epic: "text-orange-400 border-orange-400/50",
    legendary: "text-purple-400 border-purple-400/50",
    exotic: "text-pink-400 border-pink-400/50",
};

/**
 * NarrativeReveal: shows the dice + typewriter narrative for a resolved action.
 * `result` shape: { outcome, narrative, rewards, hp_delta, status_applied, target_name, discoveries }
 */
export default function NarrativeReveal({ result, onClose, itemsById }) {
    const [rolling, setRolling] = useState(true);
    const [revealed, setRevealed] = useState(false);

    useEffect(() => {
        if (!result) return;
        setRolling(true);
        setRevealed(false);
        const t1 = setTimeout(() => setRolling(false), 850);
        const t2 = setTimeout(() => setRevealed(true), 950);
        return () => {
            clearTimeout(t1);
            clearTimeout(t2);
        };
    }, [result]);

    if (!result) return null;

    const outcomeLabel = {
        1: "CRITICAL FAIL",
        2: "FAIL · CONSEQUENCE",
        3: "FAIL",
        4: "SUCCESS · WITH COST",
        5: "SUCCESS",
        6: "CRITICAL SUCCESS",
    }[result.outcome];

    const outcomeColor = {
        1: "text-rarity-mythic border-rarity-mythic",
        2: "text-rarity-legendary border-rarity-legendary",
        3: "text-muted-foreground border-border",
        4: "text-rarity-uncommon border-rarity-uncommon",
        5: "text-primary border-primary",
        6: "text-rarity-legendary border-rarity-legendary",
    }[result.outcome];

    return (
        <TooltipProvider delayDuration={120}>
        <div
            className="fixed inset-0 z-40 bg-black/85 flex items-center justify-center p-4 animate-fade-in"
            data-testid="narrative-reveal"
            onClick={onClose}
        >
            <div
                className="panel max-w-2xl w-full p-8 relative"
                onClick={(e) => e.stopPropagation()}
                style={{ boxShadow: "0 0 40px rgba(0,0,0,0.9)" }}
            >
                <div className="flex justify-between items-start mb-6">
                    <Dice result={result.outcome} rolling={rolling} size={110} />
                    <div className={`stat-label px-3 py-1 border-2 ${outcomeColor} font-pixel text-lg tracking-widest`}>
                        {outcomeLabel}
                    </div>
                </div>

                {revealed && (
                    <>
                        <div className="narr text-xl md:text-2xl text-foreground/95 leading-relaxed mb-6" data-testid="narrative-text">
                            {result.narrative}
                        </div>

                        <div className="grid grid-cols-2 gap-4 text-sm font-mono border-t border-border pt-4">
                            {result.hp_delta !== 0 && (
                                <div>
                                    <div className="stat-label">HP</div>
                                    <div className={result.hp_delta > 0 ? "text-primary" : "text-destructive"}>
                                        {result.hp_delta > 0 ? "+" : ""}{result.hp_delta}
                                    </div>
                                </div>
                            )}
                            {result.rewards?.gold ? (
                                <div>
                                    <div className="stat-label">GOLD</div>
                                    <div className="text-primary">+{result.rewards.gold}</div>
                                </div>
                            ) : null}
                            {result.rewards?.xp ? (
                                <div>
                                    <div className="stat-label">XP</div>
                                    <div className="text-primary">+{result.rewards.xp}</div>
                                </div>
                            ) : null}
                            {result.status_applied && (
                                <div>
                                    <div className="stat-label">STATUS</div>
                                    <div className="text-destructive uppercase">{result.status_applied}</div>
                                </div>
                            )}
                        </div>

                        {result.rewards?.items?.length > 0 && (
                            <div className="border-t border-border pt-4 mt-4">
                                <div className="stat-label mb-2">ITEMS FOUND</div>
                                <div className="flex flex-wrap gap-2">
                                    {result.rewards.items.map((it, i) => {
                                        const [iid, q] = Array.isArray(it) ? it : [it, 1];
                                        // Handle procedural item instances (dicts with instance_id)
                                        const def = (typeof iid === "object" && iid !== null) ? iid : (itemsById?.[iid] || null);
                                        const displayName = def?.name || (typeof iid === "string" ? iid.replace(/_/g, " ") : "Unknown");
                                        const displayId = def?.instance_id || (typeof iid === "string" ? iid : `item-${i}`);
                                        return (
                                            <ItemTooltip key={i} item={def}>
                                            <span
                                                className="stat-label px-2 py-1 border border-primary text-primary flex items-center gap-1.5"
                                                data-testid={`reward-item-${displayId}`}
                                            >
                                                {def && <PixelSprite item={def} size={20} />}
                                                {displayName} × {q}
                                            </span>
                                            </ItemTooltip>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                        {result.discoveries !== undefined && (
                            <div className="border-t border-border pt-4 mt-4">
                                <div className="stat-label mb-2">DISCOVERY</div>
                                {result.discoveries.length === 0 ? (
                                    <div className="text-sm text-muted-foreground">Nothing new discovered this time.</div>
                                ) : (
                                    <div className="flex flex-wrap gap-2">
                                        {result.discoveries.map((d) => (
                                            <span
                                                key={`${d.kind}-${d.id}`}
                                                className={`stat-label px-2 py-1 border ${RARITY_STYLE[d.rarity] || "text-primary border-primary"}`}
                                                data-testid={`discovery-${d.kind}-${d.id}`}
                                            >
                                                {d.kind === "waystone" ? "WAYSTONE: " : d.kind === "monster" ? "MONSTER: " : d.kind === "node" ? "NODE: " : ""}
                                                {d.name}
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        <button
                            data-testid="narrative-close"
                            onClick={onClose}
                            className="press-btn mt-8 font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                        >
                            Continue →
                        </button>
                    </>
                )}
            </div>
        </div>
        </TooltipProvider>
    );
}
