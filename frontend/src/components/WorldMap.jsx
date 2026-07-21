import { Lock, Compass } from "lucide-react";

export default function WorldMap({ continents, character, onTravel }) {
    const currentCont = character?.current_continent;
    return (
        <div className="panel p-6" data-testid="world-map">
            <h3 className="font-pixel text-2xl uppercase text-primary mb-1">The World of Erchis</h3>
            <div className="stat-label text-muted-foreground mb-6">
                Seven continents. Travel gated by level. Danger scales with distance.
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {continents.map((c) => {
                    const locked = character.level < (c.level_req || 1);
                    const active = c.id === currentCont;
                    return (
                        <button
                            key={c.id}
                            data-testid={`continent-${c.id}`}
                            disabled={locked}
                            onClick={() =>
                                onTravel?.(c.id, c.biomes?.[0]?.id || character.current_biome)
                            }
                            className={`press-btn text-left p-4 border-2 transition-colors relative ${
                                locked
                                    ? "border-border/50 text-muted-foreground/50 cursor-not-allowed"
                                    : active
                                      ? "border-primary bg-primary/10 text-foreground"
                                      : "border-border hover:border-primary/60 text-foreground"
                            }`}
                        >
                            <div className="flex items-start justify-between">
                                <div className="font-pixel text-xl uppercase text-primary">{c.name}</div>
                                {locked ? <Lock size={16} className="text-muted-foreground/50" /> :
                                    active ? <Compass size={16} className="text-primary" /> : null}
                            </div>
                            <div className="stat-label mt-1">
                                {locked ? `Requires Lv ${c.level_req}` : c.biomes?.length ? `${c.biomes.length} biomes` : "Locked in this era"}
                            </div>
                            <div className="text-xs text-muted-foreground mt-2 leading-relaxed">{c.desc}</div>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
