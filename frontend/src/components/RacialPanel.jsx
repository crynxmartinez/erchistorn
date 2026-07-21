import { HERITAGE_LABEL } from "@/data/racialConstants";
import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";

const RESOURCE_META = {
    oath_progress:    { label: "Oath Progress",    max: 100, color: "hsl(46 65% 52%)",  hint: "Fulfilling your Sacred Oath fills this meter. At 100 you awaken a Human ability."},
    celestial_charge: { label: "Celestial Charge", max: 5,   color: "hsl(207 90% 54%)", hint: "Charges gained by acting under the right sky (☀ Solar / ☾ Lunar). Spend on Elven arts."},
    stoneguard:       { label: "Stoneguard",       max: 5,   color: "hsl(35 5% 62%)",   hint: "Dwarven grit — earned in successful stands, spent to shrug off a hit."},
    harmony:          { label: "Harmony",          max: 5,   color: "hsl(291 64% 52%)", hint: "Half-Elf's balance between two heritages. Peak Harmony unlocks the awakened hybrid gift."},
    defiance:         { label: "Defiance",         max: 100, color: "hsl(0 60% 45%)",   hint: "Orc rage from broken chains. Grows on hardship, spent on furious counter-strikes."},
    inner_blood:      { label: "Inner Blood",      max: 100, color: "hsl(4 90% 58%)",   hint: "Wildblood beast-fury. Rises with Exhaustion, unleashed in a single savage turn."},
    tide:             { label: "Tide",             max: 5,   color: "hsl(196 70% 50%)", hint: "Hyliondrian sea-charge. Full pool = your Marine Adaptation triggers next action."},
    verdant_essence:  { label: "Verdant Essence",  max: 5,   color: "hsl(122 39% 49%)", hint: "Sylvan grove-bond. Roots you to a biome and heals over time when full."},
};

const RACE_TO_RESOURCE = {
    human: "oath_progress",
    elf: "celestial_charge",
    dwarf: "stoneguard",
    half_elf: "harmony",
    orc: "defiance",
    wildblood: "inner_blood",
    hyliondrian: "tide",
    sylvan: "verdant_essence",
};

const EXHAUSTION_HINT = "Exhaustion (numeric resource, 0–100). Rises as you push through actions; NOT the 'Weary' status. Wildbloods weaponise it via Inner Blood; Orcs at high exhaust see Defiance spike.";
const RESOLVE_HINT    = "Resolve (0–100). Mental steel — buffers against fear and rout effects. Drops on grim outcomes, recovers slowly with rest.";

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
