import { notFound } from "next/navigation";
import Link from "next/link";
import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import Die from "@/components/site/Die";
import { CTABand } from "@/components/site/Bits";
import { MASTERIES, MASTERIES_BY_ID } from "@/content/masteries";

/**
 * One page per mastery — eleven real landing pages.
 *
 * The highest-leverage SEO item in the plan: each is a genuine long-tail target
 * ("knight build", "how does the alchemist work") built from copy that mostly
 * existed already. All eleven are prerendered at build time.
 */

export async function generateStaticParams() {
    return MASTERIES.map((m) => ({ id: m.id }));
}

export async function generateMetadata({ params }) {
    const { id } = await params;
    const m = MASTERIES_BY_ID[id];
    if (!m) return { title: "Mastery not found", robots: { index: false } };
    return {
        title: `${m.name}: ${m.tagline}`,
        description: `${m.desc} ${m.plays}`.slice(0, 158),
        alternates: { canonical: `/mastery/${m.id}` },
        openGraph: {
            title: `${m.name}: ${m.tagline}`,
            description: m.desc,
            url: `/mastery/${m.id}`,
        },
    };
}

export default async function MasteryPage({ params }) {
    const { id } = await params;
    const m = MASTERIES_BY_ID[id];
    if (!m) notFound();

    const others = MASTERIES.filter((x) => x.id !== m.id);

    return (
        <>
            <section className="relative overflow-hidden border-b border-border/60">
                <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0"
                    style={{
                        background:
                            "radial-gradient(ellipse 60% 60% at 80% 35%, rgba(212,175,55,0.09), transparent 65%)",
                    }}
                />
                <div className="relative mx-auto grid w-full max-w-6xl items-center gap-12 px-6 py-20 md:grid-cols-[1fr_minmax(0,240px)] md:py-24">
                    <div>
                        <Link
                            href="/mechanics"
                            className="font-mono text-label uppercase text-muted-foreground hover:text-primary"
                        >
                            ← All masteries
                        </Link>
                        <p className="mt-8 font-mono text-label uppercase text-primary/70">
                            {m.tagline}
                        </p>
                        <h1 className="mt-3 font-display text-display uppercase text-foreground">
                            {m.name}
                        </h1>
                        <p className="mt-7 max-w-prose text-lede text-muted-foreground">{m.hook}</p>
                    </div>
                    <div className="hidden justify-end md:flex">
                        <Die size={190} face={6} />
                    </div>
                </div>
            </section>

            <Section variant="plain" className="!py-12" label="At a glance">
                <dl className="grid grid-cols-2 gap-y-8 border-y border-border/60 py-8 md:grid-cols-3">
                    {[
                        { label: "Resource", value: m.resource },
                        { label: "Role", value: m.role },
                        { label: "Starting skills", value: m.skills.join(", ") },
                    ].map((s) => (
                        <div key={s.label}>
                            <dt className="font-mono text-label uppercase text-muted-foreground">
                                {s.label}
                            </dt>
                            <dd className="mt-2 font-display text-card uppercase text-primary">
                                {s.value}
                            </dd>
                        </div>
                    ))}
                </dl>
            </Section>

            <Section variant="inset" label="How it plays">
                <SectionHeader eyebrow="How it works" title={`Playing the ${m.name}`} />
                <div className="mt-10 max-w-prose space-y-5 text-body text-foreground/85">
                    <p>{m.desc}</p>
                    <p className="border-l-2 border-primary/50 pl-5 italic text-muted-foreground">
                        {m.plays}
                    </p>
                </div>
            </Section>

            <Section variant="band" label="Other masteries">
                <SectionHeader eyebrow="Eleven in total" title="Or play something else" />
                <ul className="mt-10 grid grid-cols-2 gap-x-8 gap-y-4 md:grid-cols-4">
                    {others.map((o) => (
                        <li key={o.id}>
                            <Link
                                href={`/mastery/${o.id}`}
                                className="group block border-l-2 border-border/70 pl-4 py-1 transition-colors hover:border-primary"
                            >
                                <span className="block font-display text-card uppercase text-foreground group-hover:text-primary">
                                    {o.name}
                                </span>
                                <span className="font-mono text-label uppercase text-primary/60">
                                    {o.resource}
                                </span>
                            </Link>
                        </li>
                    ))}
                </ul>
            </Section>

            <CTABand
                title={`Roll a ${m.name}.`}
                lede={m.hook}
                primary={{ to: "/races", label: "Pick a bloodline" }}
                secondary={{ to: "/mechanics", label: "How the die works" }}
            />
        </>
    );
}
