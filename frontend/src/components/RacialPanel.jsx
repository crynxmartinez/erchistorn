import { HERITAGE_LABEL } from "@/data/racialConstants";
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { RESOURCE_META as SHARED_RESOURCE_META, RACE_TO_RESOURCE, EXHAUSTION_HINT, RESOLVE_HINT } from "@/data/hints";

// Colors are UI-only, so we merge with the shared hint metadata.
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

/** Compact racial panel — shows resource meter, heritage rank, celestial state */
export default function RacialPanel({ character, timeOfDay }) {
    const race = character.race;
    const resourceKey = RACE_TO_RESOURCE[race];
    const meta = RESOURCE_META[resourceKey] || {};
    const value = character[resourceKey] || 0;
    const pct = Math.round((value / (meta.max || 1)) * 100);
    const heritageLabel = HERITAGE_LABEL[race] || "Racial";

    return (
        <div className="border-t border-border pt-3" data-testid="racial-panel">
            <div className="stat-label mb-2 flex items-center justify-between">
                <span>RACIAL — RANK {character.heritage_rank || 1}</span>
                {race === "elf" || race === "sylvan" ? (
                    <span className={`stat-label ${timeOfDay === "lunar" ? "text-rarity-rare" : "text-primary"}`} data-testid="celestial-state">
                        {timeOfDay === "lunar" ? "☾ LUNAR" : "☀ SOLAR"}
                    </span>
                ) : null}
            </div>

            <Tooltip>
                <TooltipTrigger asChild>
                    <div className="text-xs font-mono mb-1 flex justify-between cursor-help">
                        <span className="text-muted-foreground">{meta.label || heritageLabel}</span>
                        <span className="text-primary" data-testid="racial-resource-value">{value}/{meta.max}</span>
                    </div>
                </TooltipTrigger>
                <TooltipContent side="right"><div className="font-pixel text-xs leading-snug max-w-[240px]">{meta.hint || "Racial resource — grows through your bloodline's ways."}</div></TooltipContent>
            </Tooltip>
            <div className="h-2 bg-background border border-border relative">
                <div
                    className="h-full transition-all"
                    style={{ width: `${pct}%`, backgroundColor: meta.color || "hsl(var(--primary))" }}
                />
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

            {/* Exhaustion + Resolve — secondary bars */}
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs font-mono">
                <Tooltip>
                    <TooltipTrigger asChild>
                        <div className="cursor-help" data-testid="exhaust-tip">
                            <div className="stat-label">EXHAUST</div>
                            <div className="h-1.5 bg-background border border-border">
                                <div className="h-full bg-destructive/70" style={{ width: `${Math.min(100, character.exhaustion || 0)}%` }} />
                            </div>
                            <div className="text-right text-muted-foreground" data-testid="exhaust-value">{character.exhaustion || 0}</div>
                        </div>
                    </TooltipTrigger>
                    <TooltipContent side="top"><div className="font-pixel text-xs leading-snug max-w-[260px]">{EXHAUSTION_HINT}</div></TooltipContent>
                </Tooltip>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <div className="cursor-help" data-testid="resolve-tip">
                            <div className="stat-label">RESOLVE</div>
                            <div className="h-1.5 bg-background border border-border">
                                <div className="h-full bg-primary" style={{ width: `${character.resolve || 0}%` }} />
                            </div>
                            <div className="text-right text-muted-foreground" data-testid="resolve-value">{character.resolve || 0}</div>
                        </div>
                    </TooltipTrigger>
                    <TooltipContent side="top"><div className="font-pixel text-xs leading-snug max-w-[260px]">{RESOLVE_HINT}</div></TooltipContent>
                </Tooltip>
            </div>
        </div>
    );
}
