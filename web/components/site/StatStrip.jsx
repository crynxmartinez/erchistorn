/**
 * The facts about the game, on the server.
 *
 * The "Heroes" and "Highest level" figures were derived from the leaderboard and are
 * gone with it: the ladder currently holds only development characters, and a public
 * page asserting a player count it cannot back is worse than one that says nothing.
 * Restore them here once there is a real player database — the shape is unchanged,
 * just pass the rows back in.
 */
const STATS = [
    { label: "Continents", value: "11" },
    { label: "Masteries", value: "11" },
    { label: "Races", value: "8" },
    { label: "Outcomes per roll", value: "6" },
];

export default function StatStrip() {
    return (
        <dl className="grid grid-cols-2 gap-y-8 border-y border-border/60 py-10 md:grid-cols-4">
            {STATS.map((s) => (
                <div key={s.label} className="text-center">
                    <dd className="font-display text-stat text-primary">{s.value}</dd>
                    <dt className="mt-1 font-mono text-label uppercase text-muted-foreground">
                        {s.label}
                    </dt>
                </div>
            ))}
        </dl>
    );
}
