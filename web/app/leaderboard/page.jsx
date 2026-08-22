import Section from "@/components/site/Section";
import { CTABand } from "@/components/site/Bits";
import { getLeaderboard } from "@/lib/api";

/**
 * Leaderboard — server-rendered, revalidated every five minutes.
 *
 * The strongest proof a small game is alive is a ranking that changes, so it is
 * worth having in the HTML rather than behind a fetch. Five minutes is a deliberate
 * compromise: fresh enough to be true, cached enough that a crawler or a traffic
 * spike does not hammer the database once per view.
 */

export const metadata = {
    title: "Leaderboard",
    description:
        "The live Erchis ladder. One shared world, one ranking — see who is ahead right now.",
    alternates: { canonical: "/leaderboard" },
};

export default async function LeaderboardPage() {
    const rows = await getLeaderboard();

    return (
        <>
            <section className="border-b border-border/60">
                <div className="mx-auto w-full max-w-6xl px-6 py-16 md:py-20">
                    <p className="mb-5 font-mono text-label uppercase text-primary/70">Live</p>
                    <h1 className="font-display text-display uppercase text-foreground">
                        Leader<span className="text-primary">board</span>
                    </h1>
                    <p className="mt-6 max-w-prose text-lede text-muted-foreground">
                        One shared world. One ranking. Updated continuously.
                    </p>
                </div>
            </section>

            <Section variant="plain" label="Ranking">
                {rows.length === 0 ? (
                    <p className="font-mono text-label uppercase text-muted-foreground">
                        No heroes ranked yet. Be the first.
                    </p>
                ) : (
                    <ol className="divide-y divide-border/50">
                        {rows.map((p, i) => (
                            <li key={p.name || i} className="flex items-center gap-5 py-4">
                                <span className="w-12 font-display text-card text-primary/70">
                                    {String(i + 1).padStart(2, "0")}
                                </span>
                                <span className="min-w-0 flex-1 truncate font-display text-card uppercase text-foreground">
                                    {p.name}
                                </span>
                                <span className="hidden font-mono text-label uppercase text-muted-foreground sm:inline">
                                    {p.race} · {p.mastery}
                                </span>
                                <span className="w-20 text-right font-mono text-label uppercase text-primary">
                                    Lv {p.level}
                                </span>
                            </li>
                        ))}
                    </ol>
                )}
            </Section>

            <CTABand
                title="Put your name on it."
                primary={{ to: "/races", label: "Pick a bloodline" }}
            />
        </>
    );
}
