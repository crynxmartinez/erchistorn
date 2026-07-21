import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Compass, Swords, Sprout, Fish, Skull } from "lucide-react";

const ACTION_META = {
    hunt: { icon: Swords, label: "Hunt", flavor: "Pursue and slay." },
    gather: { icon: Sprout, label: "Gather", flavor: "Take what the land offers." },
    explore: { icon: Compass, label: "Explore", flavor: "Wander and see." },
    fish: { icon: Fish, label: "Fish", flavor: "Cast the line." },
    loot_ruins: { icon: Skull, label: "Loot Ruins", flavor: "Steal from the dead." },
};

export default function BiomeView({ character, continent, onBiomeChange, onActionResult, onCombatStart }) {
    const [actions, setActions] = useState([]);
    const [rolling, setRolling] = useState(false);
    const biome = character.current_biome;
    const biomeMeta = continent?.biomes?.find((b) => b.id === biome);

    useEffect(() => {
        (async () => {
            try {
                const { data } = await api.get(`/game/data/biome/${biome}/actions`);
                setActions(data.actions);
            } catch (e) {
                toast.error(extractError(e));
            }
        })();
    }, [biome]);

    const doAction = async (action, targetId = null) => {
        if (rolling) return;
        setRolling(true);
        try {
            if (action === "hunt" && targetId) {
                // Trigger combat for hunt
                const { data } = await api.post("/game/combat/start", {
                    biome_id: biome,
                    monster_id: targetId,
                });
                onCombatStart?.(data);
                return;
            }
            const { data } = await api.post("/game/action", {
                action_id: action,
                biome_id: biome,
                target_id: targetId,
            });
            onActionResult?.(data);
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    return (
        <div className="panel p-6" data-testid="biome-view">
            <div className="flex items-start justify-between mb-4">
                <div>
                    <div className="stat-label text-primary/80">{continent?.name}</div>
                    <h3 className="font-pixel text-3xl uppercase text-primary">{biomeMeta?.name || biome}</h3>
                    <div className="narr text-sm text-muted-foreground mt-2 max-w-2xl">
                        {biomeMeta?.desc}
                    </div>
                </div>
            </div>

            {continent?.biomes?.length > 1 && (
                <div className="mb-6 flex flex-wrap gap-2">
                    {continent.biomes.map((b) => (
                        <button
                            key={b.id}
                            data-testid={`biome-tab-${b.id}`}
                            onClick={() => onBiomeChange?.(b.id)}
                            className={`press-btn font-pixel text-sm uppercase px-3 py-1 border-2 ${
                                b.id === biome
                                    ? "border-primary bg-primary text-primary-foreground"
                                    : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                            }`}
                        >
                            {b.name}
                        </button>
                    ))}
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {actions.map((a) => {
                    const meta = ACTION_META[a.id] || { icon: Compass, label: a.name, flavor: "" };
                    const Ic = meta.icon;
                    return (
                        <div key={a.id} className="panel p-4 hover:border-primary transition-colors">
                            <div className="flex items-center gap-2 mb-2">
                                <Ic className="text-primary" size={20} strokeWidth={1.5} />
                                <div className="font-pixel text-xl uppercase text-primary">{meta.label}</div>
                            </div>
                            <div className="text-xs text-muted-foreground mb-3 narr">{meta.flavor}</div>
                            {a.targets && a.targets.length > 0 ? (
                                <div className="space-y-1">
                                    {a.targets.map((t) => (
                                        <button
                                            key={t}
                                            data-testid={`action-${a.id}-${t}`}
                                            disabled={rolling}
                                            onClick={() => doAction(a.id, t)}
                                            className="press-btn w-full font-mono text-xs uppercase px-2 py-1.5 border border-border hover:border-primary hover:text-primary text-left disabled:opacity-40"
                                        >
                                            › {t.replace(/_/g, " ")}
                                        </button>
                                    ))}
                                </div>
                            ) : (
                                <button
                                    data-testid={`action-${a.id}`}
                                    disabled={rolling}
                                    onClick={() => doAction(a.id, null)}
                                    className="press-btn w-full font-pixel text-lg uppercase py-2 bg-primary/10 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                >
                                    Roll →
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
