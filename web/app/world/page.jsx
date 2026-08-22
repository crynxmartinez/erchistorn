import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import { ContinentRow } from "@/components/site/Cards";
import { CTABand } from "@/components/site/Bits";
import { getWorld } from "@/lib/api";

/**
 * World — server-rendered continent overview.
 *
 * Deliberately not a port of the CRA page's tabbed browser (continents / biomes /
 * towns / bestiary / materials). That is an *app* feature: six interacting pieces of
 * client state, useful once you are playing, and not what should rank. What belongs
 * on the marketing site is the world itself, in HTML a crawler can read — eleven
 * continents with their specialties and biome counts, each a real block of indexable
 * text. The deep browser stays in the game client.
 *
 * This is also the first use of the ContinentRow component, which was built during
 * the redo and had nowhere to live: the CRA page rendered continents inside its tab
 * state instead.
 */

export const metadata = {
    title: "The world",
    description:
        "Eleven continents, thirty biomes, sixteen towns, and hundreds of creatures and materials — from the imperial halls of Valeria to the sunken depths of Hylion.",
    alternates: { canonical: "/world" },
};

export default async function WorldPage() {
    const world = await getWorld();
    const continents = world?.continents || [];
    const biomeCount = (world?.all_biomes || []).length;
    const townCount = (world?.all_towns || []).length;
    const monsterCount = (world?.all_monsters || []).length;

    return (
        <>
            <section className="relative overflow-hidden border-b border-border/60">
                <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0"
                    style={{
                        background:
                            "radial-gradient(ellipse 70% 70% at 78% 25%, rgba(212,175,55,0.09), transparent 65%)," +
                            "radial-gradient(ellipse 100% 100% at 50% 50%, transparent 45%, rgba(0,0,0,0.5) 100%)",
                    }}
                />
                <div className="relative mx-auto w-full max-w-6xl px-6 py-20 md:py-28">
                    <p className="mb-5 font-mono text-label uppercase text-primary/70">The world</p>
                    <h1 className="max-w-3xl font-display text-display uppercase text-foreground">
                        The world of <span className="text-primary">Erchis</span>
                    </h1>
                    <p className="mt-7 max-w-prose text-lede text-muted-foreground">
                        From the imperial halls of Valeria to the sunken depths of Hylion. Explore a
                        region to unlock the next one — nothing is handed to you.
                    </p>
                </div>
            </section>

            {/* Counts come from the payload rather than being asserted in prose, so
                they cannot drift out of date the way "Thirty biomes" would. */}
            <Section variant="plain" className="!py-12" label="At a glance">
                <dl className="grid grid-cols-2 gap-y-8 border-y border-border/60 py-10 md:grid-cols-4">
                    {[
                        { label: "Continents", value: continents.length || "11" },
                        { label: "Biomes", value: biomeCount || "—" },
                        { label: "Towns", value: townCount || "—" },
                        { label: "Creatures", value: monsterCount || "—" },
                    ].map((s) => (
                        <div key={s.label} className="text-center">
                            <dd className="font-display text-stat text-primary">{s.value}</dd>
                            <dt className="mt-1 font-mono text-label uppercase text-muted-foreground">
                                {s.label}
                            </dt>
                        </div>
                    ))}
                </dl>
            </Section>

            {continents.length > 0 ? (
                <Section variant="plain" label="Continents">
                    <SectionHeader
                        eyebrow="Eleven continents"
                        title="Where you will end up"
                        lede="Each continent has its own biomes, monsters, materials and a specialty that changes what is worth doing there."
                    />
                    <div className="mt-14">
                        {continents.map((c, i) => (
                            <ContinentRow
                                key={c.id}
                                index={i}
                                name={c.name}
                                blurb={c.desc}
                                biomes={(c.biomes || []).length || null}
                            />
                        ))}
                    </div>
                </Section>
            ) : (
                <Section variant="plain">
                    <p className="font-mono text-label uppercase text-muted-foreground">
                        The map is being redrawn. Check back shortly.
                    </p>
                </Section>
            )}

            <CTABand
                title="Go and look."
                lede="Eleven continents, and you start on one of them."
                primary={{ to: "/races", label: "Pick a bloodline" }}
                secondary={{ to: "/mechanics", label: "How the die works" }}
            />
        </>
    );
}
