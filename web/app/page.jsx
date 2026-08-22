import { Dices, Swords, Map } from "lucide-react";
import Hero from "@/components/site/Hero";
import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import StatStrip from "@/components/site/StatStrip";
import Button from "@/components/site/Button";
import { FeatureCard, RaceCard, PostCard } from "@/components/site/Cards";
import { PullQuote, CTABand } from "@/components/site/Bits";
import { getPosts, fmtDate } from "@/lib/api";

/**
 * Home — a server component.
 *
 * The dev-log posts are fetched on the server, so they are present in the HTML a
 * crawler receives. On the CRA version they arrived via `useEffect` and were
 * invisible to anything that does not execute JavaScript.
 *
 * The live ladder section was removed: the only characters in the database are
 * development ones, and a public page is better saying nothing than showing a top
 * five called "Cv99999614". Bring it back when there are real players — the
 * `getLeaderboard` helper in lib/api.js is still there.
 */

export const metadata = {
    // The default title is the un-templated one; only home wants that.
    title: { absolute: "Erchis — A Fantasy Dice RPG" },
    description:
        "A free browser fantasy RPG decided by one weighted six-sided die. Eight races, eleven continents, eleven masteries. No energy caps.",
    alternates: { canonical: "/" },
};

const FEATURES = [
    {
        icon: Dices,
        title: "Weighted d6 fate",
        desc: "Every action is a dice throw. Six outcomes, each with more than twenty narratives. Your stats shift the odds — they never guarantee them.",
    },
    {
        icon: Swords,
        title: "Turn-based combat",
        desc: "Eleven masteries, each with its own resource system: Oath stacks, a Faith bar, elemental imbues, Combo Flow. Skills fire automatically, or you override when it matters.",
    },
    {
        icon: Map,
        title: "A world with corners",
        desc: "Eleven continents, each with its own biomes, monsters and materials. Explore to unlock the next region; nothing is handed to you.",
    },
];

const RACE_CARDS = [
    { name: "Human", tag: "Sacred Oath" },
    { name: "Elf", tag: "Sun & Moon" },
    { name: "Dwarf", tag: "Mountain Resilience" },
    { name: "Half-Elf", tag: "Dual Heritage" },
    { name: "Orc", tag: "Blood of the Liberated" },
    { name: "Wildblood", tag: "The Zone" },
    { name: "Hyliondrian", tag: "Children of the Sea" },
    { name: "Sylvan", tag: "Shrink" },
];

/** Schema.org VideoGame — server-rendered, so it is actually parseable. */
const JSON_LD = {
    "@context": "https://schema.org",
    "@type": "VideoGame",
    name: "Erchis",
    url: "https://erchis.online",
    description:
        "A free browser-based fantasy RPG decided by a single weighted six-sided die. Eight races, eleven continents, eleven masteries.",
    image: "https://erchis.online/og-image.png",
    genre: ["Role-playing game", "Text-based game", "MMORPG"],
    gamePlatform: "Web browser",
    applicationCategory: "Game",
    playMode: "MultiPlayer",
    operatingSystem: "Any",
    offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
};

export default async function HomePage() {
    const posts = await getPosts(3);

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(JSON_LD) }}
            />

            <Hero />

            <Section variant="plain" className="!py-12" label="At a glance">
                <StatStrip />
            </Section>

            <Section variant="plain" label="How it plays">
                <SectionHeader
                    eyebrow="Section 01 — Mechanics"
                    title={"The dice do not care\nwho you are"}
                    lede="But your gear, race and cunning tilt the throw."
                />
                <div className="mt-14 grid gap-10 md:grid-cols-3">
                    {FEATURES.map((f) => (
                        <FeatureCard key={f.title} icon={f.icon} title={f.title}>
                            {f.desc}
                        </FeatureCard>
                    ))}
                </div>
                <div className="mt-12">
                    <Button to="/mechanics" variant="ghost" size="md">
                        See every system
                    </Button>
                </div>
            </Section>

            <Section variant="band" label="Fate">
                <div className="grid gap-12 md:grid-cols-[1fr_auto] md:items-center">
                    <PullQuote cite="Outcome 1 of 6 — a critical failure">
                        “Your blade finds only air. The Highway Bandit grins, and for one long
                        moment you understand exactly how this ends.”
                    </PullQuote>
                    <p className="font-mono text-label uppercase leading-relaxed text-muted-foreground md:text-right">
                        6 outcomes
                        <br />
                        20+ narratives each
                        <br />
                        350 skills
                    </p>
                </div>
            </Section>

            <Section variant="plain" label="Races">
                <SectionHeader
                    eyebrow="Section 02 — Bloodlines"
                    title="Eight playable races"
                    lede="Each with a racial gift that changes how you play, not just what you look like."
                />
                <div className="mt-14 grid grid-cols-2 gap-5 md:grid-cols-4">
                    {RACE_CARDS.map((r) => (
                        <RaceCard key={r.name} name={r.name} tag={r.tag} to="/races" compact />
                    ))}
                </div>
            </Section>

            {posts.length > 0 && (
                <Section variant="plain" label="Latest posts">
                    <div className="flex flex-wrap items-end justify-between gap-6">
                        <SectionHeader eyebrow="Section 03 — Dispatches" title="From the dev log" />
                        <Button to="/blog" variant="ghost" size="md">
                            All posts
                        </Button>
                    </div>
                    <div className="mt-12 grid gap-10 md:grid-cols-3">
                        {posts.map((p) => (
                            <PostCard
                                key={p.slug}
                                slug={p.slug}
                                title={p.title}
                                excerpt={p.excerpt}
                                date={fmtDate(p.published_at || p.created_at)}
                                tag={p.tag}
                            />
                        ))}
                    </div>
                </Section>
            )}

            <CTABand
                title="The die is cast."
                lede="Create a character, swear an oath, and find out what the dice think of you."
                primary={{ to: "/register", label: "Begin your saga" }}
                secondary={{ to: "/world", label: "See the world first" }}
            />
        </>
    );
}
