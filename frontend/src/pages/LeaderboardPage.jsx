import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import Seo from "@/components/site/Seo";
import { Trophy, Crown } from "lucide-react";

/**
 * Two audiences, one component.
 *
 * `embedded` is the in-game ladder (rendered from Game.jsx) and keeps showing real
 * rows — a logged-in player should see where they stand.
 *
 * The **public** view shows a placeholder instead. The only characters in the
 * database are development ones, so it was publishing a ranking full of names like
 * "Cv99999614". To turn it back on, delete the `if (!embedded)` block below; the
 * fetch and the table it feeds are untouched.
 */
export default function LeaderboardPage({ embedded }) {
    const [rows, setRows] = useState([]);

    useEffect(() => {
        if (!embedded) return; // public view does not fetch; see the note above
        (async () => {
            try {
                const { data } = await api.get("/game/leaderboard");
                setRows(data.rows || data.leaderboard || []);
            } catch {
                setRows([]);
            }
        })();
    }, [embedded]);

    if (!embedded) {
        return (
            <SiteLayout>
                <Seo
                    title="Leaderboard"
                    description="The Erchis ladder. One shared world, one ranking — opening when the first heroes take the field."
                    path="/leaderboard"
                />
                <section className="border-b border-border/60">
                    <div className="mx-auto w-full max-w-6xl px-6 py-16 md:py-20">
                        <p className="mb-5 font-mono text-label uppercase text-primary/70">
                            The ladder
                        </p>
                        <h1 className="font-display text-display uppercase text-foreground">
                            Leader<span className="text-primary">board</span>
                        </h1>
                        <p className="mt-6 max-w-prose text-lede text-muted-foreground">
                            One shared world. One ranking. Every hero on the same table.
                        </p>
                    </div>
                </section>
                <div className="mx-auto w-full max-w-6xl px-6 py-section-sm md:py-section">
                    <div className="max-w-prose">
                        <h2 className="font-display text-subtitle uppercase text-foreground">
                            No one has been ranked yet
                        </h2>
                        <p className="mt-5 text-body text-muted-foreground">
                            The ladder opens when the first heroes take the field. Levels, races and
                            masteries will all be listed here — one table for the whole world.
                        </p>
                        <p className="mt-4 text-body text-muted-foreground">
                            Create a character now and the first entry is yours.
                        </p>
                        <div className="mt-8">
                            <Link
                                to="/register"
                                className="inline-flex items-center justify-center gap-2 border-2 border-primary bg-primary px-6 py-2.5 font-display uppercase tracking-wide text-primary-foreground transition-colors hover:bg-transparent hover:text-primary"
                            >
                                Create a character
                            </Link>
                        </div>
                    </div>
                </div>
            </SiteLayout>
        );
    }

    const content = (
        <>
            <div className="flex items-center gap-3 mb-10">
                <Trophy className="text-primary" size={40} />
                <h1 className="font-display text-display uppercase text-foreground">Leader<span className="text-primary">board</span></h1>
            </div>

            <div className="panel p-6 md:p-8">
                <div className="grid grid-cols-12 gap-2 stat-label text-primary/60 border-b border-border pb-2 mb-2">
                    <div className="col-span-1">#</div>
                    <div className="col-span-3">NAME</div>
                    <div className="col-span-2">RACE</div>
                    <div className="col-span-2">MASTERY</div>
                    <div className="col-span-1">LV</div>
                    <div className="col-span-1">KILLS</div>
                    <div className="col-span-1">CRAFTS</div>
                    <div className="col-span-1">GOLD</div>
                </div>
                {rows.map((r, i) => (
                    <div
                        key={r.id || i}
                        data-testid={`leaderboard-row-${i}`}
                        className="grid grid-cols-12 gap-2 font-mono text-base py-3 border-b border-border/40 hover:bg-primary/5"
                    >
                        <div className="col-span-1 text-primary flex items-center gap-1">
                            {i === 0 && <Crown size={12} />}
                            {i + 1}
                        </div>
                        <div className="col-span-3 truncate text-foreground">{r.name}</div>
                        <div className="col-span-2 text-muted-foreground capitalize">{r.race}</div>
                        <div className="col-span-2 text-muted-foreground capitalize">{r.mastery}</div>
                        <div className="col-span-1 text-primary">{r.level}</div>
                        <div className="col-span-1 text-foreground">{r.kills || "—"}</div>
                        <div className="col-span-1 text-foreground">{r.crafts || "—"}</div>
                        <div className="col-span-1 text-primary">{r.gold}</div>
                    </div>
                ))}
                {rows.length === 0 && (
                    <div className="stat-label text-muted-foreground text-center py-12">No heroes yet.</div>
                )}
            </div>
        </>
    );

    if (embedded) return content;
    return (
        <SiteLayout>
            <Seo
                title="Leaderboard"
                description="The live Erchis ladder. One shared world, one ranking — see who is ahead right now."
                path="/leaderboard"
            />
            <div className="max-w-5xl mx-auto px-4 md:px-8 py-16" data-testid="leaderboard-page">
                {content}
            </div>
        </SiteLayout>
    );
}
