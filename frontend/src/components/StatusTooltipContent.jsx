import { STATUS_HINTS } from "@/data/hints";

/**
 * Rich tooltip content for a status effect.
 * Shows: name, type badge, description, mechanical effect (with magnitude/duration substituted),
 * duration remaining, and DoT type if applicable.
 *
 * `status` shape: { id, name, kind, duration, magnitude, dot_type }
 */
export default function StatusTooltipContent({ status }) {
    const hint = STATUS_HINTS[status.id];
    const isBuff = status.kind === "buff";
    const effectColor = isBuff ? "text-primary" : "text-destructive";

    // Substitute {mag} and {dur} placeholders in effect text
    const effectText = hint
        ? hint.effect
              .replace("{mag}", status.magnitude ?? "?")
              .replace("{dur}", status.duration ?? "?")
        : "Active status effect";

    const desc = hint?.desc || `${status.name} — active status effect.`;
    const typeLabel = hint?.type || (isBuff ? "Buff" : "Debuff");

    return (
        <div className="font-pixel text-xs leading-snug max-w-[260px] space-y-1.5">
            <div className="flex items-center justify-between gap-2">
                <span className="text-sm text-foreground">{status.name}</span>
                <span className={`stat-label px-1 py-0.5 border ${isBuff ? "border-primary/50 text-primary" : "border-destructive/50 text-destructive"} text-[9px] uppercase tracking-wider`}>
                    {typeLabel}
                </span>
            </div>
            <div className="text-muted-foreground italic">{desc}</div>
            <div className="border-t border-border/40 pt-1">
                <span className="stat-label text-[9px] uppercase text-muted-foreground">Effect: </span>
                <span className={effectColor}>{effectText}</span>
            </div>
            {status.duration != null && status.duration > 0 && (
                <div>
                    <span className="stat-label text-[9px] uppercase text-muted-foreground">Duration: </span>
                    <span className="text-foreground">{status.duration} action{status.duration !== 1 ? "s" : ""}</span>
                </div>
            )}
            {status.dot_type && (
                <div>
                    <span className="stat-label text-[9px] uppercase text-muted-foreground">Damage Type: </span>
                    <span className="text-foreground capitalize">{status.dot_type}</span>
                </div>
            )}
            {status.magnitude != null && status.magnitude > 0 && (
                <div>
                    <span className="stat-label text-[9px] uppercase text-muted-foreground">Magnitude: </span>
                    <span className={effectColor}>{status.magnitude}</span>
                </div>
            )}
        </div>
    );
}
