import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import Die from "@/components/site/Die";
import Link from "next/link";
import { PullQuote, CTABand } from "@/components/site/Bits";
import { MASTERIES } from "@/content/masteries";
import { Swords, Hammer, Users, TrendingUp, Zap } from "lucide-react";

/**
 * Mechanics — the differentiator page.
 *
 * Rebuilt from a uniform stack of six identical bordered blocks. The d6 is what
 * makes this game not-like-the-others, so it gets an actual explanation at the top
 * (the outcome table) instead of being one bullet among eighteen.
 *
 * Each system is now a two-column row that alternates side, so the page has a
 * rhythm rather than reading as a spreadsheet.
 */

// The six faces, in the game's own language. This table is the single most useful
// thing the page can show: it makes the core loop legible in one glance.
const OUTCOMES = [
    { face: 1, name: "Catastrophe", note: "The worst reading of events. Materials lost, openings given." },
    { face: 2, name: "Critical failure", note: "You miss, and it costs you something." },
    { face: 3, name: "Failure", note: "Nothing lands. The turn is spent." },
    { face: 4, name: "Partial success", note: "It works, but not cleanly." },
    { face: 5, name: "Success", note: "What you intended, at full effect." },
    { face: 6, name: "Critical success", note: "Better than intended. Bonus effects fire." },
];

const SYSTEMS = [
    {
        icon: Swords,
        title: "Turn-based combat",
        body: "Combat is automatic but tactical. Your character picks skills by situation, and you override when the stakes are high. Eleven masteries each carry their own resource system — Oath stacks, a Faith bar that grows as your HP falls, elemental imbues, Combo Flow, a shadow pool. Enemies use the same rules you do.",
        points: [
            "Auto-skill selection with manual override",
            "11 masteries, 11 different resources",
            "Items and statuses trigger on their own",
        ],
    },
    {
        icon: Hammer,
        title: "Crafting & rarity",
        body: "Gather materials from biomes across eleven continents. Six rarity tiers from Common to Mythic. Recipes are gated by profession, rank and location — you learn a trade from a town's trade master, and some are taught in exactly one place on the map.",
        points: ["Six tiers: Common → Mythic", "Profession and location gated", "Queued crafts with real timers"],
    },
    {
        icon: TrendingUp,
        title: "Progression",
        body: "Levels come from combat, crafting and exploration, and each one raises your mastery's signature stats on a fixed curve — no random allocation. Skills come from wandering teachers and rare skillbook drops.",
        points: ["Deterministic stat growth per mastery", "Skillbooks drop from monsters", "Teachers gate the rarest skills"],
    },
    {
        icon: Users,
        title: "Guilds & hall buffs",
        body: "Found a guild or join one. At three members the Guild Hall unlocks, and the Grandmaster spends treasury gold on buffs that apply to every member: combat XP, crafting success, gather yield, trade profit, expedition speed.",
        points: ["Up to 30 members", "Hall unlocks at 3", "Five buffs, 24h, treasury-funded"],
    },
    {
        icon: Zap,
        title: "Status effects",
        body: "More than fifteen statuses, split between the dark and the light. Bleeding, poisoned, burning, stunned, ensnared against blessed, focused, warded, hidden, evasive. Durations tick per action, not per turn, so a long fight is not a free ride.",
        points: ["10+ debuffs", "5+ buffs", "Durations tick per action"],
    },
];

export const metadata = {
    title: "Mechanics",
    description:
        "Every action in Erchis resolves on one weighted d6 across six outcomes. Turn-based combat, eleven masteries with their own resources, crafting, guilds and status effects.",
    alternates: { canonical: "/mechanics" },
};

export default function MechanicsPage() {
    return (
        <>
            {/* Hero: the die does the explaining. */}
            <section className="relative overflow-hidden border-b border-border/60">
                <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0"
                    style={{
                        background:
                            "radial-gradient(ellipse 60% 60% at 78% 40%, rgba(212,175,55,0.09), transparent 65%)",
                    }}
                />
                <div className="relative mx-auto grid w-full max-w-6xl items-center gap-12 px-6 py-20 md:grid-cols-[1fr_minmax(0,280px)] md:py-28">
                    <div>
                        <p className="mb-5 font-mono text-label uppercase text-primary/70">
                            Mechanics
                        </p>
                        <h1 className="font-display text-display uppercase text-foreground">
                            One die
                            <br />
                            decides
                            <br />
                            <span className="text-primary">everything</span>
                        </h1>
                        <p className="mt-7 max-w-prose text-lede text-muted-foreground">
                            Attacking, crafting, gathering, exploring — every action in Erchis
                            resolves on a single weighted six-sided die. Your stats shift the odds.
                            They never remove them.
                        </p>
                    </div>
                    <div className="flex justify-center md:justify-end">
                        <Die size={230} face={6} />
                    </div>
                </div>
            </section>

            {/* The outcome table: the most informative thing on the page. */}
            <Section variant="plain" label="The six outcomes">
                <SectionHeader
                    eyebrow="The d6"
                    title="Six faces, six readings"
                    lede="Every roll lands on one of these. Each has more than twenty narrative variants, so the same outcome rarely reads the same way twice."
                />
                <ol className="mt-14 divide-y divide-border/50">
                    {OUTCOMES.map((o) => (
                        <li
                            key={o.face}
                            className="grid grid-cols-[auto_1fr] items-baseline gap-x-6 gap-y-1 py-5 md:grid-cols-[auto_minmax(0,14rem)_1fr]"
                        >
                            <span
                                className={`font-display text-subtitle ${
                                    o.face === 6
                                        ? "text-primary"
                                        : o.face === 1
                                        ? "text-destructive/80"
                                        : "text-muted-foreground/60"
                                }`}
                                aria-hidden="true"
                            >
                                {o.face}
                            </span>
                            <span className="font-display text-card uppercase text-foreground">
                                {o.name}
                            </span>
                            <span className="col-span-2 text-body-sm text-muted-foreground md:col-span-1">
                                {o.note}
                            </span>
                        </li>
                    ))}
                </ol>
                <p className="mt-10 max-w-prose font-mono text-caption uppercase leading-relaxed text-muted-foreground/70">
                    Stats move the weighting toward the top of this table. Nothing removes the
                    bottom of it.
                </p>
            </Section>

            <Section variant="band" label="On failure">
                <PullQuote cite="Outcome 3 of 6 — a plain failure">
                    “Your blade whistles past the Highway Bandit, harmless. He does not even
                    bother to step aside.”
                </PullQuote>
            </Section>

            {/* Systems: alternating two-column rows rather than a uniform grid. */}
            <Section variant="plain" label="Systems">
                <SectionHeader eyebrow="Everything else" title="The systems around the die" />
                <div className="mt-14">
                    {SYSTEMS.map((s, i) => {
                        const Icon = s.icon;
                        const flip = i % 2 === 1;
                        return (
                            <article
                                key={s.title}
                                className={`grid gap-6 border-b border-border/50 py-10 md:grid-cols-2 md:gap-16 ${
                                    flip ? "md:[&>*:first-child]:order-2" : ""
                                }`}
                            >
                                <div>
                                    <Icon className="mb-4 h-7 w-7 text-primary/80" aria-hidden="true" />
                                    <h3 className="font-display text-subtitle uppercase text-foreground">
                                        {s.title}
                                    </h3>
                                    <p className="mt-4 max-w-prose text-body-sm text-muted-foreground">
                                        {s.body}
                                    </p>
                                </div>
                                <ul className="space-y-3 md:pt-16">
                                    {s.points.map((p) => (
                                        <li
                                            key={p}
                                            className="flex gap-3 font-mono text-caption uppercase text-muted-foreground"
                                        >
                                            <span aria-hidden="true" className="text-primary/60">
                                                ·
                                            </span>
                                            {p}
                                        </li>
                                    ))}
                                </ul>
                            </article>
                        );
                    })}
                </div>
            </Section>

            <Section variant="band" label="Masteries">
                <SectionHeader
                    eyebrow="Eleven masteries"
                    title="Pick how you fight"
                    lede="Each mastery has its own resource system. They do not play alike."
                />
                <ul className="mt-12 grid grid-cols-2 gap-x-8 gap-y-5 md:grid-cols-3">
                    {MASTERIES.map((m) => (
                        <li key={m.id}>
                            <Link
                                href={`/mastery/${m.id}`}
                                className="group block border-l-2 border-border/70 pl-5 py-1 transition-colors hover:border-primary"
                            >
                                <span className="block font-display text-card uppercase text-foreground group-hover:text-primary">
                                    {m.name}
                                </span>
                                <span className="font-mono text-label uppercase text-primary/60">
                                    {m.resource}
                                </span>
                                <span className="mt-1 block text-body-sm text-muted-foreground">
                                    {m.tagline}
                                </span>
                            </Link>
                        </li>
                    ))}
                </ul>
            </Section>

            <CTABand
                title="Roll and find out."
                lede="The systems only matter once the die is in your hand."
                primary={{ to: "/register", label: "Create a character" }}
                secondary={{ to: "/races", label: "Pick a bloodline" }}
            />
        </>
    );
}
