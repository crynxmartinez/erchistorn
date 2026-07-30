import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { EXHAUSTION_HINT, RESOLVE_HINT } from "@/data/hints";

/** Compact panel — exhaustion & resolve bars (secondary stamina/morale meters) */
export default function RacialPanel({ character }) {
    return (
        <div className="border-t border-border pt-3" data-testid="racial-panel">
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
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
