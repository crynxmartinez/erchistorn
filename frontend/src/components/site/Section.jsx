/**
 * Section wrapper with a variant per rhythm.
 *
 * The old site had six sections of identical shape — centred heading, then a grid
 * of bordered boxes — so scrolling felt like no progress was being made. Variants
 * exist so consecutive sections can differ structurally rather than only in copy.
 *
 *   plain  — contained, transparent (the default)
 *   band   — full-bleed slightly lighter panel, for breaking up a run of plain
 *   inset  — narrower measure, for reading-heavy stretches
 *   flush  — full-bleed with no horizontal padding, for edge-to-edge grids
 */
export default function Section({
    variant = "plain",
    id,
    className = "",
    children,
    label,
}) {
    const pad = "py-section-sm md:py-section";
    const shell = {
        plain: "",
        band: "bg-card/40 border-y border-border/60",
        inset: "",
        flush: "",
    }[variant];

    const inner = {
        plain: "mx-auto w-full max-w-6xl px-6",
        band: "mx-auto w-full max-w-6xl px-6",
        inset: "mx-auto w-full max-w-3xl px-6",
        flush: "w-full",
    }[variant];

    return (
        <section id={id} aria-label={label} className={`${pad} ${shell} ${className}`}>
            <div className={inner}>{children}</div>
        </section>
    );
}
