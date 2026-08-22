/**
 * Live numbers, rendered on the server.
 *
 * The CRA version fetched the ladder in a `useEffect`, so the one piece of evidence
 * that this is a real running game was invisible to crawlers and appeared only after
 * a round trip. Here the parent page fetches it server-side and passes it in, so the
 * numbers are in the HTML — and this stops needing to be a client component at all.
 *
 * Fails soft: with no data the strip still renders the static facts rather than
 * showing zeroes or an error to a first-time visitor.
 */
const STATIC = [
    { label: "Continents", value: "11" },
    { label: "Masteries", value: "11" },
    { label: "Races", value: "8" },
];

export default function StatStrip({ initialLeaders = [] }) {
    const live = [];
    if (Array.isArray(initialLeaders) && initialLeaders.length > 0) {
        const top = initialLeaders[0] || {};
        live.push({ label: "Heroes", value: String(initialLeaders.length) });
        live.push({
            label: "Highest level",
            value: String(top.level ?? top.lvl ?? "—"),
        });
    }

    const items = [...STATIC, ...live];

    return (
        <dl className="grid grid-cols-3 gap-y-8 border-y border-border/60 py-10 md:grid-cols-5">
            {items.map((s) => (
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
