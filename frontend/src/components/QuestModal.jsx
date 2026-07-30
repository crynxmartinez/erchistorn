import { useEffect, useState } from "react";
import { ScrollText, X } from "lucide-react";

const TYPE_LABEL = {
    accept: { label: "QUEST ACCEPTED", color: "text-primary border-primary" },
    abandon: { label: "QUEST ABANDONED", color: "text-destructive border-destructive" },
    complete: { label: "QUEST COMPLETE", color: "text-rarity-legendary border-rarity-legendary" },
};

export default function QuestModal({ result, onClose }) {
    const [revealed, setRevealed] = useState(false);

    useEffect(() => {
        if (!result) return;
        setRevealed(false);
        const t = setTimeout(() => setRevealed(true), 400);
        return () => clearTimeout(t);
    }, [result]);

    if (!result) return null;

    const typeInfo = TYPE_LABEL[result.type] || TYPE_LABEL.accept;
    const quest = result.quest || {};
    const questName = quest.name || quest.title || "Unknown Quest";
    const questBrief = quest.brief || "";

    return (
        <div
            className="fixed inset-0 z-40 bg-black/85 flex items-center justify-center p-4 animate-fade-in"
            data-testid="quest-modal"
            onClick={onClose}
        >
            <div
                className="panel max-w-2xl w-full p-8 relative"
                onClick={(e) => e.stopPropagation()}
                style={{ boxShadow: "0 0 40px rgba(0,0,0,0.9)" }}
            >
                <button
                    onClick={onClose}
                    className="absolute top-3 right-3 text-muted-foreground hover:text-foreground"
                >
                    <X size={20} />
                </button>

                <div className="flex items-center gap-3 mb-6">
                    <ScrollText size={28} className="text-primary" />
                    <div className={`stat-label px-3 py-1 border-2 ${typeInfo.color} font-pixel text-lg tracking-widest`}>
                        {typeInfo.label}
                    </div>
                </div>

                <div className="font-pixel text-2xl uppercase text-primary mb-2">
                    {questName}
                </div>

                {revealed && (
                    <>
                        <div className="narr text-lg md:text-xl text-foreground/90 leading-relaxed mb-4" data-testid="quest-modal-narrative">
                            {result.narrative}
                        </div>

                        {questBrief && (
                            <div className="border-t border-border pt-4 mt-4">
                                <div className="stat-label text-primary/70 mb-1">BRIEF</div>
                                <div className="text-sm text-foreground/80">{questBrief}</div>
                            </div>
                        )}

                        {quest.requirements && (
                            <div className="border-t border-border pt-4 mt-4">
                                <div className="stat-label text-primary/70 mb-1">OBJECTIVES</div>
                                <div className="text-sm text-foreground/80">
                                    {(quest.requirements.kills || []).map(([t, n]) => (
                                        <span key={"k" + t} className="mr-3">Slay {n} × {t.replace(/_/g, " ")}</span>
                                    ))}
                                    {(quest.requirements.gathers || []).map(([t, n]) => (
                                        <span key={"g" + t} className="mr-3">Gather {n} × {t.replace(/_/g, " ")}</span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {quest.objectives && (
                            <div className="border-t border-border pt-4 mt-4">
                                <div className="stat-label text-primary/70 mb-1">OBJECTIVES</div>
                                <div className="text-sm text-foreground/80">
                                    {quest.objectives.map((o, i) => (
                                        <span key={i} className="mr-3">
                                            {o.kind === "kill" ? `Slay ${o.count} × ${o.id.replace(/_/g, " ")}` :
                                             o.kind === "gather" ? `Gather ${o.count} × ${o.id.replace(/_/g, " ")}` :
                                             `${o.kind}: ${o.id.replace(/_/g, " ")} × ${o.count}`}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {(quest.rewards || quest.reward) && (
                            <div className="border-t border-border pt-4 mt-4">
                                <div className="stat-label text-primary/70 mb-1">REWARDS</div>
                                <div className="text-sm text-primary">
                                    {(() => {
                                        const r = quest.rewards || quest.reward || {};
                                        const parts = [];
                                        if (r.gold) parts.push(`${r.gold}g`);
                                        if (r.xp) parts.push(`${r.xp}xp`);
                                        if (r.relationship) parts.push(`+${r.relationship} rel`);
                                        return parts.join(" · ");
                                    })()}
                                </div>
                            </div>
                        )}

                        <button
                            data-testid="quest-modal-close"
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
