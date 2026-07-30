import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { ArrowLeft, Coins, Plus } from "lucide-react";

export default function GuildHouse({ character: characterProp, onCharacterUpdate, embedded }) {
    const navigate = useNavigate();
    const [localCharacter, setLocalCharacter] = useState(characterProp || null);
    const character = characterProp || localCharacter;
    const [guilds, setGuilds] = useState([]);
    const [createOpen, setCreateOpen] = useState(false);
    const [newGuildName, setNewGuildName] = useState("");
    const [newGuildTagline, setNewGuildTagline] = useState("");
    const [newGuildEmblem, setNewGuildEmblem] = useState("⚜");

    const loadAll = useCallback(async () => {
        try {
            const [ch, gs] = await Promise.all([
                api.get("/game/character"),
                api.get("/game/guilds"),
            ]);
            if (onCharacterUpdate) onCharacterUpdate(ch.data.character);
            else setLocalCharacter(ch.data.character);
            setGuilds(gs.data.guilds);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, []);

    useEffect(() => { loadAll(); }, [loadAll]);

    if (!character) return <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-2xl">ENTERING THE GUILD HOUSE…</div>;

    const createGuild = async () => {
        try {
            await api.post("/game/guilds", { name: newGuildName, tagline: newGuildTagline, emblem: newGuildEmblem });
            toast.success(`Guild "${newGuildName}" founded!`);
            setCreateOpen(false);
            setNewGuildName("");
            setNewGuildTagline("");
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

    const joinGuild = async (gid) => {
        try {
            await api.post(`/game/guilds/${gid}/join`);
            toast.success("Joined guild");
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

    const leaveGuild = async () => {
        try {
            await api.post("/game/guilds/leave");
            toast.success("Left guild");
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

    return (
        <div className={embedded ? "" : "min-h-screen p-4 md:p-6"} data-testid="guild-house-page">
            <div className={embedded ? "" : "max-w-6xl mx-auto"}>
                {!embedded && (
                    <button onClick={() => navigate(-1)} data-testid="guild-back" className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-4">
                        <ArrowLeft size={12} /> BACK
                    </button>
                )}

                <div className="panel p-6 mb-4">
                    <div className="stat-label text-primary/70">CENTRAL HALL · GRAND GUILD HOUSE</div>
                    <h1 className="font-pixel text-5xl uppercase text-primary tracking-wider">The Guild House</h1>
                    <p className="narr text-muted-foreground mt-2 max-w-2xl">
                        Where guilds are forged and heroes gather to answer the world&apos;s call.
                    </p>
                    <div className="stat-label mt-3 flex items-center gap-2">
                        <Coins size={12} className="text-primary" /> <span className="text-primary">{character.gold}g</span>
                        <span className="ml-4">GUILD: <span className="text-primary">{character.guild_id ? "MEMBER" : "NONE"}</span></span>
                    </div>
                </div>

                <div className="space-y-4" data-testid="guilds-panel">
                        {!character.guild_id && (
                            <div className="panel p-6 border-primary/60">
                                <div className="flex justify-between items-center">
                                    <div>
                                        <h2 className="font-pixel text-2xl uppercase text-primary">Found a Guild</h2>
                                        <div className="stat-label mt-1">5,000g · Recruit 3+ members to unlock hall buffs</div>
                                    </div>
                                    <button
                                        data-testid="open-create-guild"
                                        onClick={() => setCreateOpen(!createOpen)}
                                        className="press-btn font-pixel text-sm uppercase px-3 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary flex items-center gap-1"
                                    >
                                        <Plus size={14} /> Create
                                    </button>
                                </div>
                                {createOpen && (
                                    <div className="mt-4 space-y-3 border-t border-border pt-4">
                                        <div>
                                            <label className="stat-label block mb-1">Guild Name</label>
                                            <input
                                                data-testid="new-guild-name"
                                                value={newGuildName}
                                                onChange={(e) => setNewGuildName(e.target.value)}
                                                className="w-full bg-background border border-border px-3 py-2 font-mono"
                                                placeholder="Bearers of the Dawn"
                                            />
                                        </div>
                                        <div>
                                            <label className="stat-label block mb-1">Tagline (optional)</label>
                                            <input
                                                data-testid="new-guild-tagline"
                                                value={newGuildTagline}
                                                onChange={(e) => setNewGuildTagline(e.target.value)}
                                                className="w-full bg-background border border-border px-3 py-2 font-mono"
                                                placeholder="First to the fight."
                                            />
                                        </div>
                                        <div>
                                            <label className="stat-label block mb-1">Emblem</label>
                                            <div className="flex gap-1 flex-wrap">
                                                {["⚜","⚔","🗡","🛡","♛","🏰","🐺","🦅","🌙","☀"].map((e) => (
                                                    <button
                                                        key={e}
                                                        data-testid={`emblem-${e}`}
                                                        onClick={() => setNewGuildEmblem(e)}
                                                        className={`w-9 h-9 border-2 text-xl ${newGuildEmblem === e ? "border-primary bg-primary/10" : "border-border"}`}
                                                    >
                                                        {e}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                        <button
                                            data-testid="submit-create-guild"
                                            onClick={createGuild}
                                            disabled={!newGuildName.trim() || character.gold < 5000}
                                            className="press-btn font-pixel text-lg uppercase px-4 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary disabled:opacity-40"
                                        >
                                            FOUND FOR 5,000g
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}

                        {character.guild_id && (
                            <div className="panel p-6 border-primary">
                                <div className="stat-label text-primary/70">CURRENTLY IN A GUILD</div>
                                <div className="flex justify-between items-center mt-2">
                                    <Link to={`/guild/${character.guild_id}`} className="font-pixel text-2xl uppercase text-primary hover:underline" data-testid="my-guild-link">
                                        View My Guild →
                                    </Link>
                                    <button
                                        data-testid="leave-guild-btn"
                                        onClick={leaveGuild}
                                        className="press-btn stat-label px-3 py-1 border border-destructive text-destructive hover:bg-destructive hover:text-destructive-foreground"
                                    >
                                        LEAVE GUILD
                                    </button>
                                </div>
                            </div>
                        )}

                        <div className="panel p-6">
                            <h2 className="font-pixel text-2xl uppercase text-primary mb-4">All Guilds ({guilds.length})</h2>
                            {guilds.length === 0 && (
                                <div className="stat-label text-muted-foreground">No guilds founded yet. Be the first.</div>
                            )}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {guilds.map((g) => (
                                    <div key={g.id} data-testid={`guild-card-${g.id}`} className="panel p-4">
                                        <div className="flex items-start justify-between">
                                            <div className="flex items-center gap-3">
                                                <div className="text-3xl">{g.emblem}</div>
                                                <div>
                                                    <div className="font-pixel text-xl uppercase text-primary">{g.name}</div>
                                                    <div className="stat-label">{g.member_count} members{g.hall_unlocked ? " · Hall ✓" : ""}</div>
                                                </div>
                                            </div>
                                            {!character.guild_id && (
                                                <button
                                                    data-testid={`join-guild-${g.id}`}
                                                    onClick={() => joinGuild(g.id)}
                                                    className="press-btn stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                                                >
                                                    JOIN
                                                </button>
                                            )}
                                        </div>
                                        {g.tagline && <div className="narr text-xs text-muted-foreground mt-2">&ldquo;{g.tagline}&rdquo;</div>}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
            </div>
        </div>
    );
}
