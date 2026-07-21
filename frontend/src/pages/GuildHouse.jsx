import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { ArrowLeft, ScrollText, Shield, Megaphone, Sparkles, Coins, Plus, Users, CheckCircle2 } from "lucide-react";

const TABS = [
    { id: "quests",     label: "Quest Board",  icon: ScrollText },
    { id: "guilds",     label: "Guilds",       icon: Shield },
    { id: "events",     label: "Events",       icon: Sparkles },
    { id: "bulletin",   label: "Bulletin",     icon: Megaphone },
];

export default function GuildHouse() {
    const navigate = useNavigate();
    const [tab, setTab] = useState("quests");
    const [character, setCharacter] = useState(null);
    const [availableQuests, setAvailableQuests] = useState([]);
    const [activeQuests, setActiveQuests] = useState([]);
    const [completedQuests, setCompletedQuests] = useState([]);
    const [guilds, setGuilds] = useState([]);
    const [events, setEvents] = useState([]);
    const [announcements, setAnnouncements] = useState([]);
    const [createOpen, setCreateOpen] = useState(false);
    const [newGuildName, setNewGuildName] = useState("");
    const [newGuildTagline, setNewGuildTagline] = useState("");
    const [newGuildEmblem, setNewGuildEmblem] = useState("⚜");

    const loadAll = useCallback(async () => {
        try {
            const [ch, qs, gs, ev, an] = await Promise.all([
                api.get("/game/character"),
                api.get("/game/quests/available"),
                api.get("/game/guilds"),
                api.get("/game/events/active"),
                api.get("/game/announcements"),
            ]);
            setCharacter(ch.data.character);
            setAvailableQuests(qs.data.available);
            setActiveQuests(qs.data.active);
            setCompletedQuests(qs.data.completed);
            setGuilds(gs.data.guilds);
            setEvents(ev.data.events);
            setAnnouncements(an.data.announcements);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, []);

    useEffect(() => { loadAll(); }, [loadAll]);

    if (!character) return <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-2xl">ENTERING THE GUILD HOUSE…</div>;

    const acceptQuest = async (qid) => {
        try {
            await api.post(`/game/quests/${qid}/accept`);
            toast.success("Quest accepted");
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

    const abandonQuest = async (qid) => {
        try {
            await api.post(`/game/quests/${qid}/abandon`);
            toast.success("Quest abandoned");
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

    const claimQuest = async (qid) => {
        try {
            const { data } = await api.post(`/game/quests/${qid}/claim`);
            toast.success(`Claimed +${data.claimed.gold}g +${data.claimed.xp}xp`);
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

    const joinEvent = async (eid) => {
        try {
            await api.post(`/game/events/${eid}/join`);
            toast.success("Joined event — quest added");
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

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
        <div className="min-h-screen p-4 md:p-6" data-testid="guild-house-page">
            <div className="max-w-6xl mx-auto">
                <button onClick={() => navigate(-1)} data-testid="guild-back" className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-4">
                    <ArrowLeft size={12} /> BACK
                </button>

                <div className="panel p-6 mb-4">
                    <div className="stat-label text-primary/70">CENTRAL HALL · GRAND GUILD HOUSE</div>
                    <h1 className="font-pixel text-5xl uppercase text-primary tracking-wider">The Guild House</h1>
                    <p className="narr text-muted-foreground mt-2 max-w-2xl">
                        Where quests are given, guilds are forged, and heroes gather to answer the world&apos;s call.
                    </p>
                    <div className="stat-label mt-3 flex items-center gap-2">
                        <Coins size={12} className="text-primary" /> <span className="text-primary">{character.gold}g</span>
                        <span className="ml-4">GUILD: <span className="text-primary">{character.guild_id ? "MEMBER" : "NONE"}</span></span>
                    </div>
                </div>

                <div className="flex flex-wrap gap-2 mb-4">
                    {TABS.map((t) => {
                        const Ic = t.icon;
                        return (
                            <button
                                key={t.id}
                                data-testid={`guild-tab-${t.id}`}
                                onClick={() => setTab(t.id)}
                                className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 flex items-center gap-1.5 ${
                                    tab === t.id
                                        ? "border-primary bg-primary text-primary-foreground"
                                        : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                                }`}
                            >
                                <Ic size={14} strokeWidth={1.5} /> {t.label}
                            </button>
                        );
                    })}
                </div>

                {/* QUEST BOARD */}
                {tab === "quests" && (
                    <div className="space-y-6" data-testid="quest-board">
                        {activeQuests.length > 0 && (
                            <div className="panel p-6">
                                <h2 className="font-pixel text-2xl uppercase text-primary mb-3">Active Quests</h2>
                                <div className="space-y-3">
                                    {activeQuests.map((aq) => {
                                        const q = availableQuests.find((x) => x.id === aq.quest_id) ||
                                                  events.find((x) => x.id === aq.quest_id) ||
                                                  { title: aq.quest_id, brief: "", objectives: [], reward: {} };
                                        return (
                                            <div key={aq.quest_id} data-testid={`active-quest-${aq.quest_id}`} className="panel p-4">
                                                <div className="flex justify-between items-start">
                                                    <div className="font-pixel text-lg uppercase text-primary">{q.title || q.name}</div>
                                                    {aq.complete && <CheckCircle2 size={18} className="text-primary" />}
                                                </div>
                                                <div className="mt-2 space-y-1">
                                                    {(q.objectives || []).map((obj, i) => {
                                                        const p = (aq.progress || [])[i] || 0;
                                                        return (
                                                            <div key={i} className="stat-label flex justify-between">
                                                                <span>{obj.kind} {obj.id || ""}</span>
                                                                <span className={p >= obj.count ? "text-primary" : "text-muted-foreground"}>
                                                                    {p}/{obj.count}
                                                                </span>
                                                            </div>
                                                        );
                                                    })}
                                                </div>
                                                <div className="flex gap-2 mt-3">
                                                    {aq.complete ? (
                                                        <button
                                                            data-testid={`claim-quest-${aq.quest_id}`}
                                                            onClick={() => claimQuest(aq.quest_id)}
                                                            className="press-btn stat-label px-4 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                                                        >
                                                            CLAIM REWARDS
                                                        </button>
                                                    ) : (
                                                        <button
                                                            data-testid={`abandon-quest-${aq.quest_id}`}
                                                            onClick={() => abandonQuest(aq.quest_id)}
                                                            className="press-btn stat-label px-3 py-1 border border-destructive/50 text-destructive/80 hover:bg-destructive hover:text-destructive-foreground"
                                                        >
                                                            ABANDON
                                                        </button>
                                                    )}
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )}
                        <div className="panel p-6">
                            <h2 className="font-pixel text-2xl uppercase text-primary mb-3">Available Quests</h2>
                            {availableQuests.length === 0 && (
                                <div className="stat-label text-muted-foreground">No new quests available. Level up to unlock more.</div>
                            )}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {availableQuests.map((q) => (
                                    <div key={q.id} data-testid={`avail-quest-${q.id}`} className="panel p-4">
                                        <div className="stat-label text-primary/70">{q.category?.toUpperCase()} · LV {q.level_req}+</div>
                                        <div className="font-pixel text-lg uppercase text-primary mt-1">{q.title}</div>
                                        <p className="narr text-xs text-foreground/85 mt-2">{q.brief}</p>
                                        <div className="stat-label mt-2 text-primary">+{q.reward.gold}g · +{q.reward.xp}xp</div>
                                        <button
                                            data-testid={`accept-avail-${q.id}`}
                                            onClick={() => acceptQuest(q.id)}
                                            className="press-btn mt-2 stat-label w-full py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                                        >
                                            ACCEPT
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {completedQuests.length > 0 && (
                            <div className="panel p-6">
                                <h3 className="font-pixel text-xl uppercase text-primary/70 mb-2">Completed ({completedQuests.length})</h3>
                                <div className="stat-label text-muted-foreground">{completedQuests.join(", ")}</div>
                            </div>
                        )}
                    </div>
                )}

                {/* GUILDS */}
                {tab === "guilds" && (
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
                )}

                {/* EVENTS */}
                {tab === "events" && (
                    <div className="panel p-6" data-testid="events-panel">
                        <h2 className="font-pixel text-2xl uppercase text-primary mb-2">Active Events</h2>
                        <p className="narr text-muted-foreground mb-4">Weekly cycle: Mon boss · Wed tournament · Sat-Sun festival. Standing bounties are always open.</p>
                        {events.length === 0 && (
                            <div className="stat-label text-muted-foreground">No active events today.</div>
                        )}
                        <div className="space-y-3">
                            {events.map((e) => {
                                const isJoined = activeQuests.some((aq) => aq.quest_id === e.id);
                                return (
                                    <div key={e.id} data-testid={`event-${e.id}`} className="panel p-4">
                                        <div className="stat-label text-primary/70">{e.kind?.toUpperCase()} · LV {e.level_req}+</div>
                                        <div className="font-pixel text-xl uppercase text-primary mt-1">{e.name}</div>
                                        <p className="narr text-sm text-foreground/85 mt-2">{e.brief}</p>
                                        <div className="stat-label mt-2 text-primary">+{e.reward.gold}g · +{e.reward.xp}xp</div>
                                        <button
                                            data-testid={`join-event-${e.id}`}
                                            onClick={() => joinEvent(e.id)}
                                            disabled={isJoined}
                                            className="press-btn mt-3 stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                        >
                                            {isJoined ? "JOINED" : "JOIN EVENT"}
                                        </button>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}

                {/* BULLETIN */}
                {tab === "bulletin" && (
                    <div className="panel p-6" data-testid="bulletin-panel">
                        <h2 className="font-pixel text-2xl uppercase text-primary mb-4">Bulletin Board</h2>
                        <div className="space-y-3">
                            {announcements.map((a) => (
                                <div key={a.id} data-testid={`bulletin-${a.id}`} className="panel p-4">
                                    <div className="stat-label text-primary/70">{a.kind?.toUpperCase() || "NOTICE"}</div>
                                    <div className="font-pixel text-lg uppercase text-primary mt-1">{a.title}</div>
                                    <div className="narr text-sm text-foreground/85 mt-2">{a.body}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
