import Button from "./Button";

/**
 * Small shared pieces: pull-quote, closing CTA band, and the blog prose wrapper.
 */

/**
 * A narrative line given room to breathe.
 *
 * The italic serif was already the best-looking thing on the site and was buried
 * in small text. At quote size against a hairline rule it does the job the missing
 * artwork would otherwise do.
 */
export function PullQuote({ children, cite }) {
    return (
        <figure className="border-l-2 border-primary/60 pl-8">
            <blockquote className="font-body text-quote italic text-foreground/90">
                {children}
            </blockquote>
            {cite && (
                <figcaption className="mt-4 font-mono text-label uppercase text-muted-foreground">
                    {cite}
                </figcaption>
            )}
        </figure>
    );
}

/** Closing call to action. One per page, always last. */
export function CTABand({
    title = "The die is cast.",
    lede = "Create a character, swear an oath, and find out what the dice think of you.",
    primary = { to: "/register", label: "Begin your saga" },
    secondary = null,
}) {
    return (
        <section
            className="relative border-y border-border/60 bg-card/40 py-section-sm md:py-section"
            aria-label="Get started"
        >
            <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0"
                style={{
                    background:
                        "radial-gradient(ellipse 60% 100% at 50% 100%, rgba(212,175,55,0.08), transparent 70%)",
                }}
            />
            <div className="relative mx-auto max-w-3xl px-6 text-center">
                <h2 className="font-display text-title uppercase text-foreground">{title}</h2>
                <p className="mx-auto mt-5 max-w-prose text-lede text-muted-foreground">{lede}</p>
                <div className="mt-9 flex flex-wrap justify-center gap-4">
                    <Button to={primary.to}>{primary.label}</Button>
                    {secondary && (
                        <Button to={secondary.to} variant="ghost">
                            {secondary.label}
                        </Button>
                    )}
                </div>
            </div>
        </section>
    );
}

/**
 * Long-form body copy (blog posts, about).
 *
 * Caps the measure at 68ch and sets the serif at reading size. Headings inside
 * still pick up VT323 from the base layer.
 */
export function Prose({ children, className = "" }) {
    return (
        <div
            className={`max-w-prose text-body text-foreground/90 [&_p]:mb-5 [&_h2]:mt-12 [&_h2]:mb-4 [&_h2]:font-display [&_h2]:text-subtitle [&_h2]:uppercase [&_h3]:mt-8 [&_h3]:mb-3 [&_h3]:font-display [&_h3]:text-card [&_h3]:uppercase [&_ul]:mb-5 [&_ul]:list-disc [&_ul]:pl-6 [&_li]:mb-2 [&_a]:text-primary [&_a]:underline [&_a]:decoration-primary/40 hover:[&_a]:decoration-primary [&_strong]:text-foreground [&_em]:italic ${className}`}
        >
            {children}
        </div>
    );
}
