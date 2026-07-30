import { useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Sword, MessageSquare, AlertTriangle, Sparkles, ShoppingBag, Leaf, HelpCircle } from "lucide-react";

const TYPE_META = {
    combat: { icon: Sword, color: "text-destructive", border: "border-destructive/50", label: "COMBAT" },
    npc: { icon: MessageSquare, color: "text-primary", border: "border-primary/50", label: "ENCOUNTER" },
    hazard: { icon: AlertTriangle, color: "text-amber-400", border: "border-amber-400/50", label: "HAZARD" },
    shrine: { icon: Sparkles, color: "text-purple-400", border: "border-purple-400/50", label: "SHRINE" },
    merchant: { icon: ShoppingBag, color: "text-primary", border: "border-primary/50", label: "MERCHANT" },
    resource: { icon: Leaf, color: "text-primary", border: "border-primary/50", label: "RESOURCE" },
    mystery: { icon: HelpCircle, color: "text-cyan-400", border: "border-cyan-400/50", label: "MYSTERY" },
};

export default function EncounterModal({ encounter, character, onClose, onCharacterUpdate, onCombatStart }) {
    const [resolving, setResolving] = useState(false);
    const [resolution, setResolution] = useState(null);

    if (!encounter) return null;

    const typeMeta = TYPE_META[encounter.type] || TYPE_META.npc;
    const TypeIcon = typeMeta.icon;

    const handleChoose = async (actionId) => {
        if (resolving) return;
        setResolving(true);
        try {
            const { data } = await api.post("/game/encounter/resolve", {
                action_id: actionId,
            });
            setResolution(data.resolution);
            onCharacterUpdate?.(data.character);

            if (data.combat_monster_id) {
                const biome = character.current_biome;
                const combatRes = await api.post("/game/combat/start", {
                    biome_id: biome,
                    monster_id: data.combat_monster_id,
                });
                onCombatStart?.(combatRes.data);
                onClose?.();
                return;
            }
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setResolving(false);
        }
    };

    return (
        <div
            className="fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4 animate-fade-in"
            data-testid="encounter-modal"
        >
            <div
                className="panel max-w-2xl w-full p-8 relative"
                onClick={(e) => e.stopPropagation()}
                style={{ boxShadow: "0 0 40px rgba(0,0,0,0.9)" }}
            >
                {/* Header */}
                <div className="flex items-center gap-3 mb-4">
                    <div className={`p-2 border-2 ${typeMeta.border} ${typeMeta.color}`}>
                        <TypeIcon size={28} />
                    </div>
                    <div>
                        <div className={`stat-label ${typeMeta.color} text-xs`}>{typeMeta.label}</div>
                        <h2 className="font-pixel text-2xl uppercase text-foreground">{encounter.name}</h2>
                    </div>
                </div>

                {/* Description */}
                {!resolution && (
                    <>
                        <div className="narr text-lg text-foreground/90 leading-relaxed mb-6 border-l-2 border-border pl-4">
                            {encounter.desc}
                        </div>

                        {/* Action choices */}
                        <div className="space-y-3">
                            <div className="stat-label text-muted-foreground text-xs mb-2">WHAT DO YOU DO?</div>
                            {encounter.actions.map((action) => (
                                <button
                                    key={action.id}
                                    data-testid={`encounter-action-${action.id}`}
                                    disabled={resolving}
                                    onClick={() => handleChoose(action.id)}
                                    className="press-btn w-full text-left p-4 panel hover:border-primary border-2 border-border transition-colors disabled:opacity-50"
                                >
                                    <span className="font-pixel text-sm uppercase text-primary">{action.label}</span>
                                </button>
                            ))}
                        </div>
                    </>
                )}

                {/* Resolution */}
                {resolution && (
                    <>
                        <div className="narr text-xl text-foreground/95 leading-relaxed mb-6 border-l-2 border-primary pl-4">
                            {resolution.narrative}
                        </div>

                        {/* Effects summary */}
                        {resolution.effects && Object.keys(resolution.effects).length > 0 && (
                            <div className="grid grid-cols-3 gap-3 text-sm font-mono border-t border-border pt-4 mb-6">
                                {resolution.effects.gold ? (
                                    <div>
                                        <div className="stat-label">GOLD</div>
                                        <div className={resolution.effects.gold > 0 ? "text-primary" : "text-destructive"}>
                                            {resolution.effects.gold > 0 ? "+" : ""}{resolution.effects.gold}
                                        </div>
                                    </div>
                                ) : null}
                                {resolution.effects.hp ? (
                                    <div>
                                        <div className="stat-label">HP</div>
                                        <div className={resolution.effects.hp > 0 ? "text-primary" : "text-destructive"}>
                                            {resolution.effects.hp > 0 ? "+" : ""}{resolution.effects.hp}
                                        </div>
                                    </div>
                                ) : null}
                                {resolution.effects.xp ? (
                                    <div>
                                        <div className="stat-label">XP</div>
                                        <div className="text-primary">+{resolution.effects.xp}</div>
                                    </div>
                                ) : null}
                                {resolution.effects.items?.length > 0 && (
                                    <div className="col-span-3">
                                        <div className="stat-label mb-1">ITEMS</div>
                                        <div className="flex flex-wrap gap-2">
                                            {resolution.effects.items.map((it, i) => {
                                                const [iid, q] = Array.isArray(it) ? it : [it, 1];
                                                return (
                                                    <span
                                                        key={i}
                                                        className="stat-label px-2 py-1 border border-primary text-primary"
                                                    >
                                                        {iid.replace(/_/g, " ")} {q > 0 ? `× ${q}` : q}
                                                    </span>
                                                );
                                            })}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        <button
                            data-testid="encounter-close"
                            onClick={onClose}
                            className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                        >
                            Continue →
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}
