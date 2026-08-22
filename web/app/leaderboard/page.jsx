import Section from "@/components/site/Section";
import { CTABand } from "@/components/site/Bits";
import { getLeaderboard } from "@/lib/api";

/**
 * The ladder.
 *
 * The table is always here — columns, ranks and all — because the ladder is a real
 * feature and a visitor should be able to see exactly what gets tracked. Only the
 * *rows* wait on a real player database.
 *
 * `SHOW_ROWS` is the switch. It is off because the only characters in the database
 * are development ones, and publishing a top ten of "Cv99999614" is worse than an
 * empty table. Flip it to true once real players exist; the rendering path below is
 * live and already handles rows.
 */
const SHOW_ROWS = false;

export const metadata = {
    title: "Leaderboard",
    description:
        "The Erchis ladder — every hero ranked by level, race and mastery in one shared world. Opening with the first real players.",
    alternates: { canonical: "/leaderboard" },
};

const COLUMNS = ["Rank", "Hero", "Race", "Mastery", "Level", "Gold"];

export default async function LeaderboardPage() {
    const rows = SHOW_ROWS ? await getLeaderboard() : [];

    return (
        <>
            <section className="border-b border-border/60">
                <div className="mx-auto w-full max-w-6xl px-6 py-16 md:py-20">
                    <p className="mb-5 font-mono text-label uppercase text-primary/70">The ladder</p>
                    <h1 className="font-display text-display uppercase text-foreground">
                        Leader<span className="text-primary">board</span>
                    </h1>
                    <p className="mt-6 max-w-prose text-lede text-muted-foreground">
                        One shared world. One ranking. Every hero on the same table — no seasons,
                        no brackets, no resets.
                    </p>
                </div>
            </section>

            <Section variant="plain" label="Ranking">
                <div className="overflow-x-auto">
                    <table className="w-full min-w-[40rem] border-collapse text-left">
                        <caption className="sr-only">
                            Erchis player rankings by level
                        </caption>
                        <thead>
                            <tr className="border-b border-border">
                                {COLUMNS.map((c) => (
                                    <th
                                        key={c}
                                        scope="col"
                                        className="pb-3 font-mono text-label uppercase text-primary/70"
                                    >
                                        {c}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {rows.length > 0 ? (
                                rows.map((p, i) => (
                                    <tr key={p.name || i} className="border-b border-border/40">
                                        <td className="py-4 font-display text-card text-primary/70">
                                            {String(i + 1).padStart(2, "0")}
                                        </td>
                                        <td className="py-4 font-display text-card uppercase text-foreground">
                                            {p.name}
                                        </td>
                                        <td className="py-4 font-mono text-caption uppercase text-muted-foreground">
                                            {p.race}
                                        </td>
                                        <td className="py-4 font-mono text-caption uppercase text-muted-foreground">
                                            {p.mastery}
                                        </td>
                                        <td className="py-4 font-mono text-caption uppercase text-primary">
                                            {p.level}
                                        </td>
                                        <td className="py-4 font-mono text-caption uppercase text-muted-foreground">
                                            {p.gold}
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <>
                                    {/* Three placeholder ranks: the table reads as a ladder
                                        waiting for players rather than a broken page. */}
                                    {[1, 2, 3].map((n) => (
                                        <tr key={n} className="border-b border-border/40">
                                            <td className="py-4 font-display text-card text-primary/30">
                                                {String(n).padStart(2, "0")}
                                            </td>
                                            <td
                                                colSpan={5}
                                                className="py-4 font-mono text-caption uppercase text-muted-foreground/40"
                                            >
                                                Unclaimed
                                            </td>
                                        </tr>
                                    ))}
                                </>
                            )}
                        </tbody>
                    </table>
                </div>

                {rows.length === 0 && (
                    <div className="mt-12 max-w-prose border-l-2 border-primary/50 pl-6">
                        <p className="font-display text-card uppercase text-foreground">
                            The ladder opens with the first real heroes
                        </p>
                        <p className="mt-3 text-body text-muted-foreground">
                            Rankings go live once players start claiming places. Level, race,
                            mastery and gold are all tracked from your first roll — so the first
                            entry is there for the taking.
                        </p>
                    </div>
                )}
            </Section>

            <CTABand
                title="Be the first name on it."
                lede="Pick a bloodline, swear an oath, and start climbing."
                primary={{ to: "/races", label: "Pick a bloodline" }}
                secondary={{ to: "/mechanics", label: "How the die works" }}
            />
        </>
    );
}
