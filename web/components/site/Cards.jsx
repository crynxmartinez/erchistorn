import Link from "next/link";

/**
 * The card family, in one module because they share a shell.
 *
 * Deliberately fewer borders than the old site, where every card had a 1px outline
 * and the page read as a wireframe. These lean on a left accent rule and hover
 * state instead, so grouping comes from whitespace.
 */

const shell =
    "group relative border-l-2 border-border/70 pl-6 py-1 " +
    "transition-colors duration-150 hover:border-primary";

export function FeatureCard({ icon: Icon, title, children }) {
    return (
        <article className={shell}>
            {Icon && (
                <Icon
                    className="mb-4 h-7 w-7 text-primary/80 transition-colors group-hover:text-primary"
                    aria-hidden="true"
                />
            )}
            <h3 className="font-display text-card uppercase text-foreground">{title}</h3>
            <p className="mt-3 text-body-sm text-muted-foreground">{children}</p>
        </article>
    );
}

/**
 * Race card. Uses the pixel checkerboard sprite slot that already exists for the
 * game UI and appeared on zero public pages, so the eight race cards stop being
 * empty text boxes.
 */
export function RaceCard({ name, tag, blurb, to, compact = false }) {
    const Wrapper = to ? Link : "div";

    // The home page shows all eight as a dense strip; the sprite art belongs on
    // /races where someone is actually comparing bloodlines. Without this the
    // strip alone ran to 1,006px, which is most of a viewport spent on a list of
    // eight names.
    if (compact) {
        return (
            <Wrapper
                {...(to ? { href: to } : {})}
                className="group block border-l-2 border-border/70 pl-4 py-2 transition-colors hover:border-primary"
            >
                <h3 className="font-display text-card uppercase text-foreground group-hover:text-primary">
                    {name}
                </h3>
                <p className="mt-0.5 font-mono text-label uppercase text-primary/60">{tag}</p>
            </Wrapper>
        );
    }

    return (
        <Wrapper
            {...(to ? { href: to } : {})}
            className="group block border border-border/60 bg-card/30 p-5 transition-colors hover:border-primary/70 hover:bg-card/60"
        >
            <div className="sprite-slot mb-4 !aspect-[4/3]" aria-hidden="true">
                {name.slice(0, 2).toUpperCase()}
            </div>
            <h3 className="font-display text-card uppercase text-foreground group-hover:text-primary">
                {name}
            </h3>
            <p className="mt-1 font-mono text-label uppercase text-primary/70">{tag}</p>
            {blurb && <p className="mt-3 text-body-sm text-muted-foreground">{blurb}</p>}
        </Wrapper>
    );
}

/** Continent row — full-bleed alternating layout rather than a uniform grid. */
export function ContinentRow({ name, blurb, biomes, index = 0 }) {
    const flip = index % 2 === 1;
    return (
        <article
            className={`flex flex-col gap-6 border-b border-border/50 py-10 md:flex-row md:items-center md:gap-12 ${
                flip ? "md:flex-row-reverse" : ""
            }`}
        >
            <div className="sprite-slot w-full shrink-0 !aspect-[16/9] md:w-72" aria-hidden="true">
                {name.slice(0, 3).toUpperCase()}
            </div>
            <div className="min-w-0">
                <p className="font-mono text-label uppercase text-primary/70">
                    Continent {String(index + 1).padStart(2, "0")}
                </p>
                <h3 className="mt-2 font-display text-subtitle uppercase text-foreground">
                    {name}
                </h3>
                {blurb && (
                    <p className="mt-3 max-w-prose text-body-sm text-muted-foreground">{blurb}</p>
                )}
                {biomes != null && (
                    <p className="mt-3 font-mono text-caption uppercase text-muted-foreground/70">
                        {biomes} biomes
                    </p>
                )}
            </div>
        </article>
    );
}

/** Blog post card. */
export function PostCard({ slug, title, excerpt, date, tag }) {
    return (
        <article className="border-l-2 border-border/70 pl-6 transition-colors hover:border-primary">
            <p className="font-mono text-label uppercase text-muted-foreground/70">
                {date}
                {tag ? ` · ${tag}` : ""}
            </p>
            <h3 className="mt-2 font-display text-card uppercase">
                <Link href={`/blog/${slug}`} className="text-foreground hover:text-primary">
                    {title}
                </Link>
            </h3>
            {excerpt && <p className="mt-3 text-body-sm text-muted-foreground">{excerpt}</p>}
        </article>
    );
}
