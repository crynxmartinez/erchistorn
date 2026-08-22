import { useEffect, useState } from "react";
import { api } from "@/lib/api";

/**
 * Live numbers, straight from the API.
 *
 * The strongest proof a small game is real and running is a number that moves.
 * The old home page asserted scale in prose ("Eleven Continents") but showed
 * nothing measured, which reads as marketing copy rather than evidence.
 *
 * Fails quietly: if the request errors the strip renders the static facts only,
 * rather than showing zeroes or an error to a first-time visitor.
 */
const STATIC = [
    { label: "Continents", value: "11" },
    { label: "Masteries", value: "11" },
    { label: "Races", value: "8" },
];

export default function StatStrip() {
    const [live, setLive] = useState(null);

    useEffect(() => {
        let cancelled = false;
        api.get("/public/leaderboard")
            .then(({ data }) => {
                if (cancelled) return;
                const rows = data?.leaderboard || data?.players || [];
                if (!Array.isArray(rows) || rows.length === 0) return;
                const top = rows[0] || {};
                setLive([
                    { label: "Heroes", value: String(rows.length) },
                    {
                        label: "Highest level",
                        value: String(top.level ?? top.lvl ?? "—"),
                    },
                ]);
            })
            .catch(() => {});
        return () => {
            cancelled = true;
        };
    }, []);

    const items = [...STATIC, ...(live || [])];

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
