import Section from "@/components/site/Section";
import Die from "@/components/site/Die";
import { CTABand } from "@/components/site/Bits";

/**
 * Leaderboard — deliberately empty for now.
 *
 * The ladder is live in the game, but the only characters in the database are
 * development ones, so publishing it would put names like "Cv99999614" on a public
 * page. A page that honestly says "no one has been ranked yet" reads better than a
 * top ten of test accounts.
 *
 * To turn it back on: import `getLeaderboard` from lib/api, await it, and render the
 * rows. The ordered-list markup that did this is in git history at 4415ee3. Keep the
 * five-minute `revalidate` on `REVALIDATE.live` when you do — a ladder that hits the
 * database once per view is a ladder that falls over the first time it gets traffic.
 */

export const metadata = {
    title: "Leaderboard",
    description:
        "The Erchis ladder. One shared world, one ranking — opening when the first heroes take the field.",
    alternates: { canonical: "/leaderboard" },
};

export default function LeaderboardPage() {
    return (
        <>
            <section className="border-b border-border/60">
                <div className="mx-auto w-full max-w-6xl px-6 py-16 md:py-20">
                    <p className="mb-5 font-mono text-label uppercase text-primary/70">The ladder</p>
                    <h1 className="font-display text-display uppercase text-foreground">
                        Leader<span className="text-primary">board</span>
                    </h1>
                    <p className="mt-6 max-w-prose text-lede text-muted-foreground">
                        One shared world. One ranking. Every hero on the same table.
                    </p>
                </div>
            </section>

            <Section variant="plain" label="Ranking">
                <div className="flex flex-col items-center gap-10 py-8 text-center md:flex-row md:justify-center md:gap-16 md:text-left">
                    <Die size={200} face={1} />
                    <div className="max-w-prose">
                        <h2 className="font-display text-subtitle uppercase text-foreground">
                            No one has been ranked yet
                        </h2>
                        <p className="mt-5 text-body text-muted-foreground">
                            The ladder opens when the first heroes take the field. Levels, races and
                            masteries will all be listed here — one table for the whole world, so
                            there is exactly one answer to who is ahead.
                        </p>
                        <p className="mt-4 text-body text-muted-foreground">
                            Create a character now and the first entry is yours.
                        </p>
                    </div>
                </div>
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
