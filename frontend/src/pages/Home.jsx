import { useEffect, useState } from "react";
import { Dices, Swords, Map } from "lucide-react";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import Seo, { GAME_JSON_LD } from "@/components/site/Seo";
import Hero from "@/components/site/Hero";
import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import StatStrip from "@/components/site/StatStrip";
import Button from "@/components/site/Button";
import { FeatureCard, RaceCard, PostCard } from "@/components/site/Cards";
import { PullQuote, CTABand } from "@/components/site/Bits";

/**
 * Home.
 *
 * Rebuilt on the site component set. The previous version was 4,428px of six
 * structurally identical sections — centred heading, then a grid of bordered
 * boxes — which is why scrolling felt like standing still. This one alternates
 * contained / band / flush and leads with a two-column hero, so each section
 * looks different from the one above it.
 *
 * Six feature cards became three. The other three claims (lore, crafting,
 * skillbooks) live on /mechanics, where someone who wants that detail is already
 * heading.
 *
 * The live ladder section was removed: the only characters in the database are
 * development ones, so it showed a top five called "Cv99999614". Restore it when
 * there are real players.
 */

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

function fmtDate(s) {
    if (!s) return "";
    return new Date(s).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    });
}

export default function Home() {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        let cancelled = false;
        api.get("/blog?limit=3")
            .then((r) => !cancelled && setPosts(r.data?.posts || []))
            .catch(() => {});
        return () => {
            cancelled = true;
        };
    }, []);

    return (
        <SiteLayout>
            <Seo
                description="A free browser fantasy RPG decided by one weighted six-sided die. Eight races, eleven continents, eleven masteries. No energy caps."
                path="/"
                jsonLd={GAME_JSON_LD}
            />
            <Hero />

            {/* Measured facts immediately under the hero: a number that moves is
                better evidence than a paragraph claiming scale. */}
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

            {/* Band: breaks the run of contained sections, and gives the quote
                the room that makes the serif do the work of missing artwork. */}
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
                        <SectionHeader
                            eyebrow="Section 03 — Dispatches"
                            title="From the dev log"
                        />
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
        </SiteLayout>
    );
}
