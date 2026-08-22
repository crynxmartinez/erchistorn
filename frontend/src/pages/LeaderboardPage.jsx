import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import Seo from "@/components/site/Seo";
import { Trophy, Crown } from "lucide-react";

export default function LeaderboardPage({ embedded }) {
    const [rows, setRows] = useState([]);

    useEffect(() => {
        (async () => {
            try {
                const endpoint = embedded ? "/game/leaderboard" : "/public/leaderboard";
                const { data } = await api.get(endpoint);
                setRows(data.rows || data.leaderboard || []);
            } catch {
                setRows([]);
            }
        })();
    }, [embedded]);

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
