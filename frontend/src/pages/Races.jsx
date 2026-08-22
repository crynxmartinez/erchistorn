import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import Seo from "@/components/site/Seo";
import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import { CTABand } from "@/components/site/Bits";

/**
 * Races.
 *
 * Rebuilt from a stack of eight identical `.panel` blocks with a 6xl emoji each.
 * Now: a numbered index of the bloodlines, then alternating detail rows that use
 * the pixel sprite slot the game UI already ships.
 *
 * The old hero hotlinked a 2000px Unsplash photo at 15% opacity — full download
 * cost on every visit, an external dependency with no license record, and a
 * photograph in a pixel-art dark-fantasy site. Replaced with the vignette
 * treatment used across the rest of the redo: no asset, on-brand, free.
 */
export default function Races() {
    const [races, setRaces] = useState([]);
    const [beastAspects, setBeastAspects] = useState([]);
    const [marineAdaptations, setMarineAdaptations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let cancelled = false;
        Promise.all([
            api.get("/public/races"),
            api.get("/public/beast_aspects"),
            api.get("/public/marine_adaptations"),
        ])
            .then(([r, ba, ma]) => {
                if (cancelled) return;
                setRaces(r.data?.races || []);
                setBeastAspects(ba.data?.beast_aspects || []);
                setMarineAdaptations(ma.data?.marine_adaptations || []);
            })
            .catch(() => {})
            .finally(() => !cancelled && setLoading(false));
        return () => {
            cancelled = true;
        };
    }, []);

    return (
        <SiteLayout>
            <Seo
                title="The eight races"
                description="Eight playable bloodlines, each with a racial gift that changes how you play: Sacred Oaths, Sun-and-Moon magic, beast aspects and aquatic adaptations."
                path="/races"
            />
            <section className="relative overflow-hidden border-b border-border/60">
                <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0"
                    style={{
                        background:
                            "radial-gradient(ellipse 70% 70% at 20% 30%, rgba(212,175,55,0.09), transparent 65%)," +
                            "radial-gradient(ellipse 100% 100% at 50% 50%, transparent 45%, rgba(0,0,0,0.5) 100%)",
                    }}
                />
                <div className="relative mx-auto w-full max-w-6xl px-6 py-20 md:py-28">
                    <p className="mb-5 font-mono text-label uppercase text-primary/70">
                        Bloodlines
                    </p>
                    <h1 className="max-w-3xl font-display text-display uppercase text-foreground">
                        Eight playable <span className="text-primary">races</span>
                    </h1>
                    <p className="mt-7 max-w-prose text-lede text-muted-foreground">
                        Each bloodline carries its own gift and its own price. From the sworn
                        Humans to the shrinking Sylvans, your race shapes every roll you make.
                    </p>
                </div>
            </section>

            {loading && (
                <Section variant="plain">
                    <p className="font-mono text-label uppercase text-muted-foreground">
                        Reading the bloodlines…
                    </p>
                </Section>
            )}

            {/* A quick index first: eight names in one glance, before the detail. */}
            {!loading && races.length > 0 && (
                <Section variant="band" label="Index">
                    <ol className="grid grid-cols-2 gap-x-8 gap-y-4 md:grid-cols-4">
                        {races.map((r, i) => (
                            <li key={r.id} className="flex items-baseline gap-3">
                                <span
                                    aria-hidden="true"
                                    className="font-mono text-label text-primary/50"
                                >
                                    {String(i + 1).padStart(2, "0")}
                                </span>
                                <a
                                    href={`#race-${r.id}`}
                                    className="font-display text-card uppercase text-foreground hover:text-primary"
                                >
                                    {r.name}
                                </a>
                            </li>
                        ))}
                    </ol>
                </Section>
            )}

            {!loading && races.length > 0 && (
                <Section variant="plain" label="The bloodlines">
                    <div>
                        {races.map((r, i) => (
                            <article
                                key={r.id}
                                id={`race-${r.id}`}
                                data-testid={`race-detail-${r.id}`}
                                className={`flex scroll-mt-24 flex-col gap-8 border-b border-border/50 py-12 md:flex-row md:gap-12 ${
                                    i % 2 === 1 ? "md:flex-row-reverse" : ""
                                }`}
                            >
                                <div
                                    className="sprite-slot w-full shrink-0 !aspect-square md:w-56"
                                    aria-hidden="true"
                                >
                                    {r.name.slice(0, 2).toUpperCase()}
                                </div>

                                <div className="min-w-0">
                                    <p className="font-mono text-label uppercase text-primary/60">
                                        Race {String(i + 1).padStart(2, "0")}
                                    </p>
                                    <h2 className="mt-2 font-display text-subtitle uppercase text-foreground">
                                        {r.name}
                                    </h2>
                                    {r.title && (
                                        <p className="mt-1 font-mono text-caption uppercase text-muted-foreground/80">
                                            {r.title}
                                        </p>
                                    )}
                                    {r.story && (
                                        <p className="mt-5 max-w-prose text-body text-foreground/85">
                                            {r.story}
                                        </p>
                                    )}
                                    {r.perk && (
                                        <div className="mt-6 border-l-2 border-primary/50 pl-5">
                                            <p className="font-mono text-label uppercase text-primary/80">
                                                Racial gift — {r.perk.name}
                                            </p>
                                            <p className="mt-1 max-w-prose text-body-sm text-muted-foreground">
                                                {r.perk.desc}
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </article>
                        ))}
                    </div>
                </Section>
            )}

            {!loading && beastAspects.length > 0 && (
                <Section variant="band" label="Beast aspects">
                    <SectionHeader
                        eyebrow="Wildblood only"
                        title="Beast aspects"
                        lede="Choose your inner animal at creation. It shapes your instincts and your gifts."
                    />
                    <div className="mt-12 grid gap-8 md:grid-cols-2">
                        {beastAspects.map((a) => (
                            <article key={a.id} className="border-l-2 border-border/70 pl-6">
                                <h3 className="font-display text-card uppercase text-foreground">
                                    {a.name}
                                </h3>
                                {a.desc && (
                                    <p className="mt-2 text-body-sm text-muted-foreground">
                                        {a.desc}
                                    </p>
                                )}
                            </article>
                        ))}
                    </div>
                </Section>
            )}

            {!loading && marineAdaptations.length > 0 && (
                <Section variant="plain" label="Marine adaptations">
                    <SectionHeader
                        eyebrow="Hyliondrian only"
                        title="Marine adaptations"
                        lede="The sea leaves its mark. Pick which one."
                    />
                    <div className="mt-12 grid gap-8 md:grid-cols-2">
                        {marineAdaptations.map((a) => (
                            <article key={a.id} className="border-l-2 border-border/70 pl-6">
                                <h3 className="font-display text-card uppercase text-foreground">
                                    {a.name}
                                </h3>
                                {a.desc && (
                                    <p className="mt-2 text-body-sm text-muted-foreground">
                                        {a.desc}
                                    </p>
                                )}
                            </article>
                        ))}
                    </div>
                </Section>
            )}

            <CTABand
                title="Choose your blood."
                lede="Eight bloodlines, eleven masteries. The combination is yours."
                primary={{ to: "/register", label: "Create a character" }}
                secondary={{ to: "/mechanics", label: "How the die works" }}
            />
        </SiteLayout>
    );
}
