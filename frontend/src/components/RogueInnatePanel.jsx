import { useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";

const TYPE_COLOR = {
    action: "text-blue-400 border-blue-400/40",
    reaction: "text-amber-400 border-amber-400/40",
    passive: "text-green-400 border-green-400/40",
};

const TYPE_LABEL = {
    action: "Action",
    reaction: "Reaction",
    passive: "Passive",
};

function InnateTooltip({ skill, children }) {
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
                    {skill.name}
                </div>
                <div className="text-[10px] text-muted-foreground mb-1">
                    {TYPE_LABEL[skill.type] || skill.type}
                </div>
                <div className="text-[10px] text-popover-foreground/80 italic">
                    {skill.desc}
                </div>
            </TooltipContent>
        </Tooltip>
    );
}

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
                <div className="text-[10px] text-muted-foreground mb-1">
                    Level {passive.level}
                </div>
                <div className="text-[10px] text-popover-foreground/80 italic">
                    {passive.desc}
                </div>
            </TooltipContent>
        </Tooltip>
    );
}

export default function RogueInnatePanel({ character, innateSkills = [], passives = [], onCharacterUpdate }) {
    const [pickingSlot, setPickingSlot] = useState(null);

    const equipped = character?.rogue_innate_equipped || [];
    const level = character?.level || 1;
    const maxSlots = level >= 100 ? 7 : level >= 10 ? 6 : 5;
    const equippedSet = new Set(equipped.filter(Boolean));
    const available = innateSkills.filter((s) => !equippedSet.has(s.id));

    const equip = async (slot, innateId) => {
        try {
            const { data } = await api.post("/game/rogue/innate/equip", { slot, innate_id: innateId });
            onCharacterUpdate?.(data.character);
            setPickingSlot(null);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const unequip = async (slot) => {
        try {
            const { data } = await api.post("/game/rogue/innate/unequip", { slot });
            onCharacterUpdate?.(data.character);
            setPickingSlot(null);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    return (
        <TooltipProvider delayDuration={120}>
            <div className="space-y-4" data-testid="rogue-innate-panel">
                {/* Equip slots */}
                <div>
                    <h4 className="font-pixel text-sm uppercase text-primary mb-2">
                        Innate Slots ({equipped.filter(Boolean).length}/{maxSlots})
                    </h4>
                    <div className="grid grid-cols-5 sm:grid-cols-7 gap-2">
                        {Array.from({ length: maxSlots }).map((_, idx) => {
                            const id = equipped[idx];
                            const skill = innateSkills.find((s) => s.id === id);
                            const isPicking = pickingSlot === idx;
                            return (
                                <div key={idx} className="relative">
                                    <InnateTooltip skill={skill || { name: "Empty", type: "passive", desc: "Click to equip an innate skill." }}>
                                        <button
                                            data-testid={`innate-slot-${idx}`}
                                            onClick={() => setPickingSlot(isPicking ? null : idx)}
                                            className={`relative w-full h-12 border flex items-center justify-center text-[10px] font-pixel uppercase transition-colors ${
                                                skill
                                                    ? `${TYPE_COLOR[skill.type] || "border-primary text-primary"} bg-primary/5`
                                                    : "border-border text-muted-foreground hover:border-primary/50"
                                            }`}
                                        >
                                            <span className="absolute top-0.5 left-1 text-[8px] leading-none opacity-70">{idx + 1}</span>
                                            <span className="mt-1">{skill ? skill.name.slice(0, 6) : ""}</span>
                                        </button>
                                    </InnateTooltip>
                                    {isPicking && (
                                        <div className="absolute z-20 mt-1 bg-background border border-primary p-2 w-48 max-h-60 overflow-y-auto shadow-lg">
                                            {available.length === 0 && (
                                                <div className="stat-label text-muted-foreground">No available innates</div>
                                            )}
                                            {available.map((s) => (
                                                <InnateTooltip key={s.id} skill={s}>
                                                    <button
                                                        onClick={() => equip(idx, s.id)}
                                                        className="block w-full text-left text-xs font-mono py-1 hover:text-primary"
                                                    >
                                                        {s.name}
                                                    </button>
                                                </InnateTooltip>
                                            ))}
                                            {skill && (
                                                <button
                                                    onClick={() => unequip(idx)}
                                                    className="block w-full text-left text-xs text-destructive py-1 hover:underline"
                                                >
                                                    Clear slot
                                                </button>
                                            )}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* All 10 innate skills with hover descriptions */}
                <div>
                    <h4 className="font-pixel text-sm uppercase text-primary mb-2">All Innate Skills</h4>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                        {innateSkills.map((s) => {
                            const isEquipped = equippedSet.has(s.id);
                            return (
                                <InnateTooltip key={s.id} skill={s}>
                                    <div
                                        className={`px-2 py-1.5 border text-[10px] font-pixel uppercase cursor-help transition-colors ${
                                            isEquipped
                                                ? `${TYPE_COLOR[s.type] || "border-primary text-primary"} bg-primary/5`
                                                : "border-border text-muted-foreground hover:border-primary/30"
                                        }`}
                                        data-testid={`innate-skill-${s.id}`}
                                    >
                                        <div className="flex items-center justify-between">
                                            <span>{s.name}</span>
                                            {isEquipped && <span className="text-[8px] opacity-70">EQUIPPED</span>}
                                        </div>
                                        <div className="text-[8px] opacity-50 mt-0.5">{TYPE_LABEL[s.type] || s.type}</div>
                                    </div>
                                </InnateTooltip>
                            );
                        })}
                    </div>
                </div>

                {/* Passives with hover descriptions */}
                <div>
                    <h4 className="font-pixel text-sm uppercase text-primary mb-2">Rogue Passives</h4>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                        {passives.map((p) => {
                            const unlocked = level >= p.level;
                            return (
                                <PassiveTooltip key={p.id} passive={p}>
                                    <div
                                        className={`px-2 py-1.5 border text-[10px] font-pixel uppercase cursor-help transition-colors ${
                                            unlocked
                                                ? "border-primary/40 text-primary bg-primary/5"
                                                : "border-border text-muted-foreground/40"
                                        }`}
                                        data-testid={`rogue-passive-${p.id}`}
                                    >
                                        <div className="flex items-center justify-between">
                                            <span>{p.name}</span>
                                            <span className="text-[8px] opacity-70">L{p.level}</span>
                                        </div>
                                        {!unlocked && (
                                            <div className="text-[8px] opacity-50 mt-0.5">LOCKED</div>
                                        )}
                                    </div>
                                </PassiveTooltip>
                            );
                        })}
                    </div>
                </div>
            </div>
        </TooltipProvider>
    );
}
