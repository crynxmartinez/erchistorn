import { useEffect, useState } from "react";
import Dice from "@/components/Dice";

/**
 * NarrativeReveal: shows the dice + typewriter narrative for a resolved action.
 * `result` shape: { outcome, narrative, rewards, hp_delta, status_applied, target_name }
 */
export default function NarrativeReveal({ result, onClose }) {
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
                                        return (
                                            <span
                                                key={i}
                                                className="stat-label px-2 py-1 border border-primary text-primary"
                                                data-testid={`reward-item-${iid}`}
                                            >
                                                {iid.replace(/_/g, " ")} × {q}
                                            </span>
                                        );
                                    })}
                                </div>
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
    );
}
