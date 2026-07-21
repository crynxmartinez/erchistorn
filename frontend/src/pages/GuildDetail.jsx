import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { ArrowLeft, Users, Coins, Crown } from "lucide-react";

export default function GuildDetail() {
    const { guildId } = useParams();
    const navigate = useNavigate();
    const [guild, setGuild] = useState(null);
    const [character, setCharacter] = useState(null);
    const [donateAmt, setDonateAmt] = useState(100);

    const load = async () => {
        try {
            const [g, ch] = await Promise.all([
                api.get(`/game/guilds/${guildId}`),
                api.get("/game/character"),
            ]);
            setGuild(g.data.guild);
            setCharacter(ch.data.character);
        } catch (e) {
            toast.error(extractError(e));
            navigate("/guild-house");
        }
    };

    useEffect(() => { load(); }, [guildId]);

    if (!guild || !character) return <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-2xl">LOADING…</div>;

    const isMember = character.guild_id === guild.id;

    const donate = async () => {
        try {
            const { data } = await api.post(`/game/guilds/${guild.id}/donate`, { amount: donateAmt });
            toast.success(`Donated ${data.donated}g`);
            setCharacter(data.character);
            load();
        } catch (e) { toast.error(extractError(e)); }
    };

    return (
        <div className="min-h-screen p-4 md:p-6" data-testid="guild-detail-page">
            <div className="max-w-5xl mx-auto">
                <Link to="/guild-house" data-testid="guild-detail-back" className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-4">
                    <ArrowLeft size={12} /> GUILD HOUSE
                </Link>

                <div className="panel p-6 mb-4">
                    <div className="flex items-center gap-4">
                        <div className="text-6xl">{guild.emblem}</div>
                        <div className="flex-1">
                            <div className="stat-label text-primary/70">GUILD · {guild.member_count} MEMBERS{guild.hall_unlocked ? " · HALL UNLOCKED" : " · HALL LOCKED"}</div>
                            <h1 className="font-pixel text-4xl uppercase text-primary tracking-wider">{guild.name}</h1>
                            {guild.tagline && <div className="narr text-lg text-muted-foreground mt-1">&ldquo;{guild.tagline}&rdquo;</div>}
                        </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 mt-6 border-t border-border pt-4">
                        <div><div className="stat-label">TREASURY</div><div className="text-primary font-mono text-xl" data-testid="guild-treasury">{guild.treasury}g</div></div>
                        <div><div className="stat-label">MEMBERS</div><div className="text-primary font-mono text-xl">{guild.member_count}/30</div></div>
                        <div><div className="stat-label">HALL</div><div className={`font-mono text-xl ${guild.hall_unlocked ? "text-primary" : "text-muted-foreground"}`}>{guild.hall_unlocked ? "ACTIVE" : "LOCKED"}</div></div>
                    </div>
                </div>

                {isMember && (
                    <div className="panel p-6 mb-4" data-testid="donate-panel">
                        <h2 className="font-pixel text-xl uppercase text-primary mb-2 flex items-center gap-2">
                            <Coins size={18} /> Donate to Treasury
                        </h2>
                        <div className="flex gap-2 items-center">
                            <input
                                data-testid="donate-amount"
                                type="number"
                                min={1}
                                value={donateAmt}
                                onChange={(e) => setDonateAmt(parseInt(e.target.value) || 0)}
                                className="w-32 bg-background border border-border px-3 py-2 font-mono"
                            />
                            <button
                                data-testid="donate-btn"
                                onClick={donate}
                                disabled={donateAmt <= 0 || character.gold < donateAmt}
                                className="press-btn stat-label px-4 py-2 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                            >
                                DONATE
                            </button>
                            <div className="stat-label text-muted-foreground ml-3">Your gold: <span className="text-primary">{character.gold}g</span></div>
                        </div>
                    </div>
                )}

                <div className="panel p-6" data-testid="member-list">
                    <h2 className="font-pixel text-xl uppercase text-primary mb-3 flex items-center gap-2">
                        <Users size={18} /> Members
                    </h2>
                    <div className="space-y-2">
                        {(guild.members_populated || []).map((m) => (
                            <div key={m.id} data-testid={`member-${m.id}`} className="flex items-center justify-between border-b border-border/40 pb-2">
                                <div className="flex items-center gap-2">
                                    {m.rank === "grandmaster" && <Crown size={14} className="text-primary" />}
                                    <div>
                                        <div className="font-mono text-sm text-foreground">{m.name}</div>
                                        <div className="stat-label">
                                            {m.race} · {m.mastery} · Lv {m.level}
                                        </div>
                                    </div>
                                </div>
                                <div className="stat-label uppercase text-primary/80">{m.rank}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
