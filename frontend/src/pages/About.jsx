import { Link } from "react-router-dom";
import SiteLayout from "@/components/SiteLayout";
import Seo from "@/components/site/Seo";
import Section from "@/components/site/Section";
import SectionHeader from "@/components/site/SectionHeader";
import Die from "@/components/site/Die";
import { PullQuote, CTABand } from "@/components/site/Bits";

/**
 * About.
 *
 * The previous version led with a "Tech Stack" list — FastAPI, MongoDB Atlas, React +
 * CRACO, Tailwind, shadcn/ui, Render + Vercel. That is a CV, not a reason to play.
 * Nobody deciding whether to try a game cares which framework renders it, and putting
 * it above the fold on the page meant to persuade them was the wrong audience
 * entirely.
 *
 * What replaces it: what the game actually is, what makes it different from the
 * genre, who builds it, and where the community lives. The solo-dev angle stays —
 * that is genuinely interesting to the indie-RPG audience — but as a story rather
 * than a dependency list.
 */

const DISCORD = "https://discord.gg/eWRnDWWMt";
const GITHUB = "https://github.com/crynxmartinez/erchistorn";

const DIFFERENT = [
    {
        title: "One die, not a damage formula",
        body: "Most RPGs hide their maths. Erchis shows you the throw: six outcomes, each with more than twenty different narratives, and your stats move the weighting rather than removing the risk. A critical failure is always on the table.",
    },
    {
        title: "No energy, no timers on fun",
        body: "There is no stamina bar gating how much you can play, and nothing asks you to come back in four hours to keep progressing. Crafting has real timers because forging takes time; your attention does not have a meter.",
    },
    {
        title: "Eleven masteries that genuinely differ",
        body: "Not eleven damage numbers with different names. Each has its own resource: Oath stacks, a Faith bar that fills as your HP drops, elemental imbues, Combo Flow, a shadow pool. Two characters at the same level can play nothing alike.",
    },
    {
        title: "One world, one ladder",
        body: "No seasons, no brackets, no resets. Everybody is on the same table and the same map, and the leaderboard means what it says.",
    },
];

const ROADMAP = [
    { title: "PvP arena", body: "Ranked dice combat against other players." },
    { title: "Expeditions", body: "Send mercenary parties on timed missions for rare materials." },
    { title: "Guild hall buffs", body: "Treasury-funded, server-wide buffs for every member." },
    { title: "Elixirs and Resolve", body: "A readiness system that makes when you play a real decision." },
];

export default function AboutPage() {
    return (
        <SiteLayout>
            <Seo
                title="About"
                description="Erchis is a free browser fantasy RPG where one weighted six-sided die decides everything. Built by a solo developer — what it is, how it plays, and where it is going."
                path="/about"
            />
            <section className="relative overflow-hidden border-b border-border/60">
                <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0"
                    style={{
                        background:
                            "radial-gradient(ellipse 60% 60% at 80% 40%, rgba(212,175,55,0.09), transparent 65%)",
                    }}
                />
                <div className="relative mx-auto grid w-full max-w-6xl items-center gap-12 px-6 py-20 md:grid-cols-[1fr_minmax(0,240px)] md:py-28">
                    <div>
                        <p className="mb-5 font-mono text-label uppercase text-primary/70">About</p>
                        <h1 className="font-display text-display uppercase text-foreground">
                            One die.
                            <br />
                            <span className="text-primary">No mercy.</span>
                        </h1>
                        <p className="mt-7 max-w-prose text-lede text-muted-foreground">
                            Erchis is a free browser fantasy RPG where every action — every swing,
                            every craft, every step into a new biome — is decided by a single
                            weighted six-sided die.
                        </p>
                    </div>
                    <div className="hidden justify-end md:flex">
                        <Die size={200} loop />
                    </div>
                </div>
            </section>

            <Section variant="inset" label="What it is">
                <SectionHeader eyebrow="The short version" title="What is Erchis?" />
                <div className="mt-10 max-w-prose space-y-5 text-body text-foreground/85">
                    <p>
                        You pick one of eight races, one of eleven masteries, and a constellation you
                        were born under. Then you go out into eleven continents and find out what
                        the dice think of you.
                    </p>
                    <p>
                        Combat is turn-based and mostly automatic — your character chooses sensible
                        skills on their own — but you can override any turn when the stakes are
                        high. Everything else is the loop around it: explore a biome to unlock the
                        next one, hunt for materials, learn a trade from a town&apos;s trade master,
                        craft what you cannot find, and climb one shared ladder.
                    </p>
                    <p>
                        No downloads, no launcher, no energy caps. It runs in a browser tab.
                    </p>
                </div>
            </Section>

            <Section variant="band" label="What makes it different">
                <SectionHeader
                    eyebrow="Why this one"
                    title="Four things it does differently"
                />
                <div className="mt-14 grid gap-10 md:grid-cols-2">
                    {DIFFERENT.map((d) => (
                        <article key={d.title} className="border-l-2 border-border/70 pl-6">
                            <h2 className="font-display text-card uppercase text-foreground">
                                {d.title}
                            </h2>
                            <p className="mt-3 text-body-sm text-muted-foreground">{d.body}</p>
                        </article>
                    ))}
                </div>
            </Section>

            <Section variant="inset" label="Who builds it">
                <SectionHeader eyebrow="The maker" title="Built by one person" />
                <div className="mt-10 max-w-prose space-y-5 text-body text-foreground/85">
                    <p>
                        Erchis is made by a solo developer. Every race, every one of the eleven
                        mastery systems, three hundred and fifty skills and the narrative lines
                        behind each of the six dice outcomes — all of it written by hand, in the
                        open, at whatever pace real life allows.
                    </p>
                    <p>
                        That has consequences worth being honest about. Updates land in bursts.
                        Balance is a work in progress. Bugs happen and get fixed in public — the{" "}
                        <Link to="/changelog">changelog</Link> is the whole history, including the
                        embarrassing parts.
                    </p>
                    <p>
                        The upside is that there is nobody to ask for permission. If a system is
                        not fun, it changes.
                    </p>
                </div>
                <div className="mt-10">
                    <PullQuote>
                        The dice are loaded, the world is vast, and the saga continues.
                    </PullQuote>
                </div>
            </Section>

            <Section variant="band" label="Roadmap">
                <SectionHeader
                    eyebrow="What is next"
                    title="Roadmap"
                    lede="Planned, in rough order. No dates, because a solo developer promising dates is how you get lied to."
                />
                <div className="mt-14 grid gap-10 md:grid-cols-2">
                    {ROADMAP.map((r, i) => (
                        <article key={r.title} className="flex gap-5">
                            <span
                                aria-hidden="true"
                                className="font-display text-subtitle text-primary/40"
                            >
                                {String(i + 1).padStart(2, "0")}
                            </span>
                            <div>
                                <h2 className="font-display text-card uppercase text-foreground">
                                    {r.title}
                                </h2>
                                <p className="mt-2 text-body-sm text-muted-foreground">{r.body}</p>
                            </div>
                        </article>
                    ))}
                </div>
            </Section>

            <Section variant="inset" label="Community">
                <SectionHeader
                    eyebrow="Come and talk"
                    title="Community"
                    lede="Bug reports, build arguments and screenshots of improbable dice all welcome."
                />
                <ul className="mt-10 space-y-4">
                    <li>
                        <a
                            href={DISCORD}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group flex items-baseline gap-4 border-l-2 border-border/70 pl-5 py-1 transition-colors hover:border-primary"
                        >
                            <span className="font-display text-card uppercase text-foreground group-hover:text-primary">
                                Discord
                            </span>
                            <span className="text-body-sm text-muted-foreground">
                                The fastest way to reach the developer, and where patches get
                                argued about first.
                            </span>
                        </a>
                    </li>
                    <li>
                        <Link
                            href="/blog"
                            className="group flex items-baseline gap-4 border-l-2 border-border/70 pl-5 py-1 transition-colors hover:border-primary"
                        >
                            <span className="font-display text-card uppercase text-foreground group-hover:text-primary">
                                Dev log
                            </span>
                            <span className="text-body-sm text-muted-foreground">
                                Longer writing about what is being built and why.
                            </span>
                        </Link>
                    </li>
                    <li>
                        <a
                            href={GITHUB}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group flex items-baseline gap-4 border-l-2 border-border/70 pl-5 py-1 transition-colors hover:border-primary"
                        >
                            <span className="font-display text-card uppercase text-foreground group-hover:text-primary">
                                GitHub
                            </span>
                            <span className="text-body-sm text-muted-foreground">
                                The source, if you are the sort of person who wants to look.
                            </span>
                        </a>
                    </li>
                </ul>
            </Section>

            <CTABand
                title="Enough reading."
                lede="Roll a character and see what the dice make of you."
                primary={{ to: "/races", label: "Pick a bloodline" }}
                secondary={{ to: "/mechanics", label: "How the die works" }}
            />
        </SiteLayout>
    );
}
