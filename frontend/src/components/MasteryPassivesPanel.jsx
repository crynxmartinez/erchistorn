import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";

function PassiveTooltip({ passive, children }) {
    return (
        <Tooltip>
            <TooltipTrigger asChild>
                {children}
            </TooltipTrigger>
            <TooltipContent
                side="bottom"
                sideOffset={4}
                className="max-w-[260px] bg-popover border border-border text-popover-foreground"
            >
                <div className="font-pixel text-xs uppercase text-primary mb-1">
                    {passive.name}
                </div>
                {passive.level != null && (
                    <div className="text-[10px] text-muted-foreground mb-1">
                        Level {passive.level}
                    </div>
                )}
                {passive.school && (
                    <div className="text-[10px] text-muted-foreground mb-1">
                        School: {passive.school}
                    </div>
                )}
                {passive.research_req && (
                    <div className="text-[10px] text-amber-400 mb-1">
                        Research: {passive.research_req}
                    </div>
                )}
                <div className="text-[10px] text-popover-foreground/80 italic">
                    {passive.desc}
                </div>
            </TooltipContent>
        </Tooltip>
    );
}

export default function MasteryPassivesPanel({ character, masteryPassives }) {
    const mastery = character?.mastery;
    if (!mastery || !masteryPassives) return null;

    const passives = masteryPassives[mastery];
    if (!passives || passives.length === 0) return null;

    const level = character?.level || 1;

    return (
        <TooltipProvider delayDuration={120}>
            <div className="space-y-2" data-testid="mastery-passives-panel">
                <h4 className="font-pixel text-sm uppercase text-primary mb-2">
                    {mastery.charAt(0).toUpperCase() + mastery.slice(1)} Passives
                </h4>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    {passives.map((p) => {
                        const unlocked = p.level == null || level >= p.level;
                        return (
                            <PassiveTooltip key={p.id} passive={p}>
                                <div
                                    className={`px-2 py-1.5 border text-[10px] font-pixel uppercase cursor-help transition-colors ${
                                        unlocked
                                            ? "border-primary/40 text-primary bg-primary/5"
                                            : "border-border text-muted-foreground/40"
                                    }`}
                                    data-testid={`mastery-passive-${p.id}`}
                                >
                                    <div className="flex items-center justify-between">
                                        <span>{p.name}</span>
                                        {p.level != null && (
                                            <span className="text-[8px] opacity-70">L{p.level}</span>
                                        )}
                                    </div>
                                    {!unlocked && (
                                        <div className="text-[8px] opacity-50 mt-0.5">LOCKED</div>
                                    )}
                                    {p.school && unlocked && (
                                        <div className="text-[8px] opacity-50 mt-0.5">{p.school}</div>
                                    )}
                                </div>
                            </PassiveTooltip>
                        );
                    })}
                </div>
            </div>
        </TooltipProvider>
    );
}
