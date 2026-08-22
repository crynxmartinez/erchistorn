/**
 * Eyebrow + title + optional lede.
 *
 * Every section title on the site went through its own hand-rolled markup, which
 * is how they drifted apart and how 149 of them ended up relying on a stray
 * font-size override. One component, one scale token.
 *
 * `align="left"` is the default on purpose: the old site centred every heading,
 * which is part of why each section looked like the last one.
 */
export default function SectionHeader({
    eyebrow,
    title,
    lede,
    align = "left",
    className = "",
}) {
    const center = align === "center";
    return (
        <header className={`${center ? "text-center mx-auto" : ""} ${className}`}>
            {eyebrow && (
                <p
                    className={`font-mono text-label uppercase text-primary/70 mb-4 flex items-center gap-3 ${
                        center ? "justify-center" : ""
                    }`}
                >
                    <span aria-hidden="true" className="inline-block h-px w-8 bg-primary/50" />
                    {eyebrow}
                </p>
            )}
            {/* whitespace-pre-line so a caller can place a deliberate line break with a
                newline in the title string, instead of every title being one ragged run. */}
            <h2 className="whitespace-pre-line font-display text-title uppercase text-foreground">
                {title}
            </h2>
            {lede && (
                <p
                    className={`text-lede text-muted-foreground mt-5 max-w-prose ${
                        center ? "mx-auto" : ""
                    }`}
                >
                    {lede}
                </p>
            )}
        </header>
    );
}
