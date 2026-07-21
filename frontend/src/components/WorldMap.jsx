import { useEffect, useState } from "react";
import { Lock, Compass, Sparkles } from "lucide-react";
import { api } from "@/lib/api";

const RACE_LABEL = {
    human: "Human", elf: "Elf", dwarf: "Dwarf", half_elf: "Half-Elf",
    orc: "Orc", wildblood: "Wildblood", hyliondrian: "Hyliondrian", sylvan: "Sylvan",
};
const CONTINENT_LABEL = {
    valeria: "Valeria", mushkara: "Mushkara", concordia: "Concordia", khardrum: "Khardrum",
    haya: "Haya", gennel: "Gennel", hylion: "Hylion", daw_ul_talalu: "Daw'ul Talalu",
    azurea: "Azurea", vael_turog: "Vael'Turog", orinth: "Orinth",
};
const prettifyContinents = (arr) => (arr || []).map((c) => CONTINENT_LABEL[c] || c).join(", ");

/**
 * World Map — the 11 continents of Erchis (8 accessible + 3 locked) plus a
 * per-biome Exploration Progress readout for whichever continent you're on.
 */
export default function WorldMap({ continents, character, onTravel }) {
    const currentCont = character?.current_continent;
    const [exploration, setExploration] = useState({ biomes: [], continent_id: null });

    useEffect(() => {
        (async () => {
            try {
                const r = await api.get("/game/exploration");
                setExploration(r.data);
            } catch { /* ignore */ }
        })();
    }, [currentCont, character?.current_biome]);

    return (
        <div className="panel p-6" data-testid="world-map">
            <h3 className="font-pixel text-2xl uppercase text-primary mb-1">The World of Erchis</h3>
            <div className="stat-label text-muted-foreground mb-6">
                Eight peopled continents. Three sealed behind the storm. Fold the world with the Grand Teleporter or walk the roads.
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {continents.map((c) => {
                    const isLocked = !!c.locked;
                    const active = c.id === currentCont;
                    return (
                        <button
                            key={c.id}
                            data-testid={`continent-${c.id}`}
                            disabled={isLocked || active}
                            onClick={() => onTravel?.(c.id, c.biomes?.[0]?.id || character.current_biome)}
                            className={`press-btn text-left p-4 border-2 transition-colors relative ${
                                isLocked
                                    ? "border-border/50 text-muted-foreground/50 cursor-not-allowed"
                                    : active
                                      ? "border-primary bg-primary/10 text-foreground cursor-default"
                                      : "border-border hover:border-primary/60 text-foreground"
                            }`}
                        >
                            <div className="flex items-start justify-between">
                                <div className="font-pixel text-xl uppercase text-primary">{c.name}</div>
                                {isLocked ? <Lock size={16} className="text-muted-foreground/50" /> :
                                    active ? <Compass size={16} className="text-primary" /> : null}
                            </div>
                            <div className="stat-label mt-1">
                                {isLocked ? "Sealed" : `${c.biomes?.length || 0} biomes${c.home_race ? ` · Home of the ${RACE_LABEL[c.home_race] || c.home_race}` : ""}`}
                            </div>
                            <div className="text-xs text-muted-foreground mt-2 leading-relaxed">{c.desc}</div>
                            {c.specialty && !isLocked && (
                                <div className="stat-label text-primary/60 mt-2 italic">
                                    <Sparkles size={9} className="inline text-primary" /> {c.specialty}
                                </div>
                            )}
                        </button>
                    );
                })}
            </div>

            {/* Exploration Progress for current continent */}
            {exploration.biomes.length > 0 && (
                <div className="border-t border-border mt-6 pt-4">
                    <div className="stat-label text-primary/70 mb-3">EXPLORATION · {continents.find(c => c.id === exploration.continent_id)?.name}</div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {exploration.biomes.map((b) => (
                            <div key={b.biome_id} className="border border-border/60 px-3 py-2" data-testid={`explore-bar-${b.biome_id}`}>
                                <div className="flex justify-between items-baseline stat-label">
                                    <span className="text-primary">{b.biome_name}</span>
                                    <span className="text-muted-foreground">{b.progress_pct}%</span>
                                </div>
                                <div className="h-1.5 bg-background border border-border mt-1">
                                    <div className="h-full bg-primary transition-all"
                                         style={{ width: `${b.progress_pct}%` }} />
                                </div>
                                <div className="text-[10px] text-muted-foreground mt-1">
                                    Lv {b.level_req}+ · {b.thresholds_met.filter(Boolean).length}/5 milestones
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
