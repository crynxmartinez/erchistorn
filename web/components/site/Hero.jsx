import Die from "./Die";
import Button from "./Button";

/**
 * The hero.
 *
 * Asymmetric two-column on desktop rather than the old centred stack: the die
 * anchors one side and the headline reads across the other, which gives the page
 * a focal point instead of a column of centred text.
 *
 * The headline is a single `text-display` token (clamp 48->96px). It previously
 * carried `text-5xl md:text-7xl lg:text-8xl` and rendered at 20.7px because a
 * stray override beat all three.
 */
export default function Hero() {
    return (
        <section
            className="relative overflow-hidden border-b border-border/60"
            aria-label="Erchis"
        >
            {/* Vignette: darkens the edges so the die's bloom reads as the light
                source. Cheap art direction with no asset. */}
            <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0"
                style={{
                    background:
                        "radial-gradient(ellipse 70% 60% at 32% 45%, rgba(212,175,55,0.10), transparent 65%)," +
                        "radial-gradient(ellipse 100% 100% at 50% 50%, transparent 40%, rgba(0,0,0,0.55) 100%)",
                }}
            />

            <div className="relative mx-auto grid w-full max-w-6xl items-center gap-12 px-6 py-24 md:grid-cols-[minmax(0,340px)_1fr] md:gap-16 md:py-36">
                <div className="order-2 flex justify-center md:order-1 md:justify-start">
                    <Die size={300} face={6} />
                </div>

                <div className="order-1 md:order-2">
                    <p className="font-mono text-label uppercase text-primary/70 mb-6">
                        A fantasy dice RPG · multiplayer · free to play
                    </p>

                    <h1 className="font-display text-display uppercase text-foreground">
                        Roll the
                        <br />
                        bones of
                        <br />
                        <span className="text-primary">Erchis</span>
                    </h1>

                    <p className="mt-8 max-w-prose text-lede text-muted-foreground">
                        Eight races. Eleven continents. One six-sided die that will decide
                        whether you become legend — or footnote.
                    </p>

                    <div className="mt-10 flex flex-wrap gap-4">
                        <Button to="/register">Begin your saga</Button>
                        <Button to="/login" variant="ghost">
                            Sign in
                        </Button>
                    </div>

                    <ul className="mt-10 flex flex-wrap gap-x-8 gap-y-2 font-mono text-caption uppercase tracking-wider text-muted-foreground/80">
                        <li>D6 · 20+ narratives</li>
                        <li>Shared world · global ladder</li>
                        <li>No energy caps</li>
                    </ul>
                </div>
            </div>
        </section>
    );
}
