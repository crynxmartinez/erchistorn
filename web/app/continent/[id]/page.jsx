import { notFound } from "next/navigation";
import Link from "next/link";
import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import { CTABand } from "@/components/site/Bits";
import { getWorld } from "@/lib/api";

/**
 * One page per continent — eleven more indexable pages, from data the API already
 * exposes. Each carries its own biomes, towns and creatures as real text, which is
 * what makes them worth having: the tabbed world browser in the game client shows
 * the same data but behind six pieces of client state, invisible to a crawler.
 */

export async function generateStaticParams() {
    const world = await getWorld();
    return (world?.continents || []).map((c) => ({ id: c.id }));
}

async function findContinent(id) {
    const world = await getWorld();
    const list = world?.continents || [];
    return { c: list.find((x) => x.id === id) || null, all: list };
}

export async function generateMetadata({ params }) {
    const { id } = await params;
    const { c } = await findContinent(id);
    if (!c) return { title: "Continent not found", robots: { index: false } };
    return {
        title: c.name,
        description: (c.desc || `${c.name}, one of the eleven continents of Erchis.`).slice(0, 158),
        alternates: { canonical: `/continent/${c.id}` },
        openGraph: { title: c.name, description: c.desc, url: `/continent/${c.id}` },
    };
}

export default async function ContinentPage({ params }) {
    const { id } = await params;
    const { c, all } = await findContinent(id);
    if (!c) notFound();

    const biomes = c.biomes || [];
    const towns = c.towns || [];
    const monsters = c.monsters || [];
    const others = all.filter((x) => x.id !== c.id);

    return (
        <>
            <section className="relative overflow-hidden border-b border-border/60">
                <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0"
                    style={{
                        background:
                            "radial-gradient(ellipse 70% 70% at 25% 30%, rgba(212,175,55,0.09), transparent 65%)",
                    }}
                />
                <div className="relative mx-auto w-full max-w-6xl px-6 py-20 md:py-24">
                    <Link
                        href="/world"
                        className="font-mono text-label uppercase text-muted-foreground hover:text-primary"
                    >
                        ← The whole world
                    </Link>
                    <p className="mt-8 font-mono text-label uppercase text-primary/70">Continent</p>
                    <h1 className="mt-3 font-display text-display uppercase text-foreground">
                        {c.name}
                    </h1>
                    {c.desc && (
                        <p className="mt-7 max-w-prose text-lede text-muted-foreground">{c.desc}</p>
                    )}
                </div>
            </section>

            <Section variant="plain" className="!py-12" label="At a glance">
                <dl className="grid grid-cols-3 gap-y-8 border-y border-border/60 py-8 md:grid-cols-4">
                    {[
                        { label: "Biomes", value: biomes.length || "—" },
                        { label: "Towns", value: towns.length || "—" },
                        { label: "Creatures", value: monsters.length || "—" },
                        { label: "Level", value: c.level_req ? `${c.level_req}+` : "1+" },
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

            {c.specialty && (
                <Section variant="band" label="Specialty">
                    <SectionHeader eyebrow="What it is known for" title="Specialty" />
                    <p className="mt-8 max-w-prose text-body text-foreground/85">{c.specialty}</p>
                    {c.bonus_desc && (
                        <p className="mt-4 max-w-prose border-l-2 border-primary/50 pl-5 text-body-sm text-muted-foreground">
                            {c.bonus_desc}
                        </p>
                    )}
                </Section>
            )}

            {biomes.length > 0 && (
                <Section variant="plain" label="Biomes">
                    <SectionHeader eyebrow={`${biomes.length} regions`} title="Biomes" />
                    <div className="mt-12 grid gap-8 md:grid-cols-2">
                        {biomes.map((b) => (
                            <article key={b.id || b.name} className="border-l-2 border-border/70 pl-6">
                                <h2 className="font-display text-card uppercase text-foreground">
                                    {b.name}
                                </h2>
                                {b.desc && (
                                    <p className="mt-2 text-body-sm text-muted-foreground">{b.desc}</p>
                                )}
                            </article>
                        ))}
                    </div>
                </Section>
            )}

            {towns.length > 0 && (
                <Section variant="band" label="Towns">
                    <SectionHeader eyebrow={`${towns.length} settlements`} title="Towns" />
                    <ul className="mt-10 grid grid-cols-2 gap-x-8 gap-y-3 md:grid-cols-3">
                        {towns.map((t) => (
                            <li key={t.id || t.name} className="font-display text-card uppercase text-foreground">
                                {t.name}
                            </li>
                        ))}
                    </ul>
                </Section>
            )}

            <Section variant="plain" label="Other continents">
                <SectionHeader eyebrow="Eleven in total" title="Elsewhere" />
                <ul className="mt-10 grid grid-cols-2 gap-x-8 gap-y-3 md:grid-cols-4">
                    {others.map((o) => (
                        <li key={o.id}>
                            <Link
                                href={`/continent/${o.id}`}
                                className="font-display text-card uppercase text-foreground hover:text-primary"
                            >
                                {o.name}
                            </Link>
                        </li>
                    ))}
                </ul>
            </Section>

            <CTABand
                title={`Set out for ${c.name}.`}
                primary={{ to: "/races", label: "Pick a bloodline" }}
                secondary={{ to: "/world", label: "See the whole world" }}
            />
        </>
    );
}
