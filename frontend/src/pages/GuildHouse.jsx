import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { ArrowLeft, Coins, Shield, Users, Crown, Search, Zap, Swords, Hammer, Sprout, TrendingUp, Tent, LogOut } from "lucide-react";

const EMBLEMS = ["⚜","⚔","🗡","🛡","♛","🏰","🐺","🦅","🌙","☀","🐉","💎"];

const BUFF_META = {
    combat_xp:   { icon: Swords,        label: "Combat XP +5%",        cost: 500, desc: "+5% XP from all combat encounters" },
    craft_succ:  { icon: Hammer,        label: "Crafting Success +10%",cost: 800, desc: "+10% chance to succeed on crafting rolls" },
    gather_yield:{ icon: Sprout,        label: "Gather Yield +10%",    cost: 600, desc: "+10% materials from gathering actions" },
    trade_cut:   { icon: TrendingUp,    label: "Trade Profit +8%",     cost: 400, desc: "+8% gold when selling to NPC shops" },
    expedition:  { icon: Tent,          label: "Expedition Speed +15%",cost: 700, desc: "Expeditions complete 15% faster" },
};

function fmtTime(s) {
    if (s <= 0) return "Expired";
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m`;
}

export default function GuildHouse({ character: characterProp, onCharacterUpdate, embedded }) {
    const navigate = useNavigate();
    const [localCharacter, setLocalCharacter] = useState(characterProp || null);
    const character = characterProp || localCharacter;
    const [guilds, setGuilds] = useState([]);
    const [guild, setGuild] = useState(null);
    const [buffs, setBuffs] = useState([]);
    const [hallUnlocked, setHallUnlocked] = useState(false);
    const [treasury, setTreasury] = useState(0);
    const [view, setView] = useState("entrance");
    const [subTab, setSubTab] = useState("overview");
    const [search, setSearch] = useState("");
    const [sortBy, setSortBy] = useState("members");
    const [newGuildName, setNewGuildName] = useState("");
    const [newGuildTagline, setNewGuildTagline] = useState("");
    const [newGuildEmblem, setNewGuildEmblem] = useState("⚜");
    const [donateAmt, setDonateAmt] = useState(100);
    const [confirmLeave, setConfirmLeave] = useState(false);

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
    }, [onCharacterUpdate]);

    const loadGuild = useCallback(async () => {
        if (!character?.guild_id) return;
        try {
            const [g, b] = await Promise.all([
                api.get(`/game/guilds/${character.guild_id}`),
                api.get(`/game/guilds/${character.guild_id}/buffs`),
            ]);
            setGuild(g.data.guild);
            setBuffs(b.data.buffs);
            setHallUnlocked(b.data.hall_unlocked);
            setTreasury(b.data.treasury);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, [character?.guild_id]);

    useEffect(() => { loadAll(); }, [loadAll]);
    useEffect(() => {
        if (character?.guild_id) {
            setView("dashboard");
            loadGuild();
        } else {
            setView("entrance");
        }
    }, [character?.guild_id, loadGuild]);

    if (!character) return <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-2xl">ENTERING THE GUILD HOUSE…</div>;

    const createGuild = async () => {
        try {
            await api.post("/game/guilds", { name: newGuildName, tagline: newGuildTagline, emblem: newGuildEmblem });
            toast.success(`Guild "${newGuildName}" founded!`);
            setNewGuildName(""); setNewGuildTagline("");
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
            setConfirmLeave(false);
            setGuild(null);
            loadAll();
        } catch (e) { toast.error(extractError(e)); }
    };

    const donate = async () => {
        try {
            const { data } = await api.post(`/game/guilds/${character.guild_id}/donate`, { amount: donateAmt });
            toast.success(`Donated ${data.donated}g`);
            if (onCharacterUpdate) onCharacterUpdate(data.character);
            else setLocalCharacter(data.character);
            loadGuild();
        } catch (e) { toast.error(extractError(e)); }
    };

    const purchaseBuff = async (buffId) => {
        try {
            const { data } = await api.post(`/game/guilds/${character.guild_id}/buffs/purchase`, { buff_id: buffId });
            toast.success("Buff activated!");
            setTreasury(data.treasury);
            loadGuild();
        } catch (e) { toast.error(extractError(e)); }
    };

    const isGrandmaster = character.guild_rank === "grandmaster";

    const filteredGuilds = guilds
        .filter(g => g.name.toLowerCase().includes(search.toLowerCase()))
        .sort((a, b) => {
            if (sortBy === "members") return b.member_count - a.member_count;
            if (sortBy === "treasury") return (b.treasury || 0) - (a.treasury || 0);
            if (sortBy === "name") return a.name.localeCompare(b.name);
            return 0;
        });

    // ---------- ENTRANCE (no guild) ----------
    if (view === "entrance" && !character.guild_id) {
        return (
            <div className={embedded ? "" : "min-h-screen p-4 md:p-6"} data-testid="guild-house-page">
                <div className={embedded ? "" : "max-w-4xl mx-auto"}>
                    {!embedded && (
                        <button onClick={() => navigate(-1)} className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-4">
                            <ArrowLeft size={12} /> BACK
                        </button>
                    )}
                    <div className="panel p-8 mb-4 text-center">
                        <div className="text-6xl mb-3">🏰</div>
                        <h1 className="font-pixel text-4xl uppercase text-primary tracking-wider">The Guild House</h1>
                        <p className="narr text-muted-foreground mt-2 max-w-lg mx-auto">
                            Where guilds are forged and heroes gather. Will you found your own, or join an existing order?
                        </p>
                        <div className="stat-label mt-3 flex items-center justify-center gap-2">
                            <Coins size={12} className="text-primary" /> <span className="text-primary">{character.gold}g</span>
                        </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <button
                            data-testid="btn-found-guild"
                            onClick={() => setView("create")}
                            className="panel p-8 border-2 border-primary/40 hover:border-primary transition-all text-left group"
                        >
                            <Shield size={40} className="text-primary mb-3 group-hover:scale-110 transition-transform" />
                            <h2 className="font-pixel text-2xl uppercase text-primary">Found a Guild</h2>
                            <div className="stat-label mt-1">Cost: 5,000g</div>
                            <p className="narr text-sm text-muted-foreground mt-2">Create your own guild, choose an emblem, and recruit members to unlock hall buffs.</p>
                        </button>
                        <button
                            data-testid="btn-join-guild"
                            onClick={() => setView("join")}
                            className="panel p-8 border-2 border-border hover:border-primary transition-all text-left group"
                        >
                            <Users size={40} className="text-primary mb-3 group-hover:scale-110 transition-transform" />
                            <h2 className="font-pixel text-2xl uppercase text-primary">Join a Guild</h2>
                            <div className="stat-label mt-1">{guilds.length} guilds recruiting</div>
                            <p className="narr text-sm text-muted-foreground mt-2">Browse existing guilds and join one to fight alongside your guildmates.</p>
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // ---------- CREATE GUILD ----------
    if (view === "create" && !character.guild_id) {
        return (
            <div className={embedded ? "" : "min-h-screen p-4 md:p-6"} data-testid="guild-house-page">
                <div className={embedded ? "" : "max-w-2xl mx-auto"}>
                    <button onClick={() => setView("entrance")} className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-4">
                        <ArrowLeft size={12} /> BACK
                    </button>
                    <div className="panel p-6">
                        <h1 className="font-pixel text-3xl uppercase text-primary mb-1">Found a Guild</h1>
                        <div className="stat-label text-muted-foreground mb-6">5,000g required · You will become Grandmaster</div>
                        <div className="space-y-4">
                            <div>
                                <label className="stat-label block mb-1">Guild Name</label>
                                <input
                                    data-testid="new-guild-name"
                                    value={newGuildName}
                                    onChange={(e) => setNewGuildName(e.target.value)}
                                    maxLength={30}
                                    className="w-full bg-background border border-border px-3 py-2 font-mono"
                                    placeholder="Bearers of the Dawn"
                                />
                                <div className="stat-label text-muted-foreground mt-1">{newGuildName.length}/30</div>
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
                                <div className="flex gap-2 flex-wrap">
                                    {EMBLEMS.map((e) => (
                                        <button
                                            key={e}
                                            data-testid={`emblem-${e}`}
                                            onClick={() => setNewGuildEmblem(e)}
                                            className={`w-11 h-11 border-2 text-xl flex items-center justify-center transition-all ${newGuildEmblem === e ? "border-primary bg-primary/15 scale-110" : "border-border hover:border-primary/50"}`}
                                        >
                                            {e}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="flex items-center justify-between border-t border-border pt-4">
                                <div className="stat-label">
                                    Your gold: <span className="text-primary">{character.gold}g</span>
                                    <span className="ml-2 text-muted-foreground">→ After: <span className={character.gold - 5000 < 0 ? "text-destructive" : "text-primary"}>{character.gold - 5000}g</span></span>
                                </div>
                                <button
                                    data-testid="submit-create-guild"
                                    onClick={createGuild}
                                    disabled={!newGuildName.trim() || newGuildName.length < 3 || character.gold < 5000}
                                    className="press-btn font-pixel text-lg uppercase px-5 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary disabled:opacity-40"
                                >
                                    FOUND FOR 5,000g
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // ---------- JOIN GUILD ----------
    if (view === "join" && !character.guild_id) {
        return (
            <div className={embedded ? "" : "min-h-screen p-4 md:p-6"} data-testid="guild-house-page">
                <div className={embedded ? "" : "max-w-4xl mx-auto"}>
                    <button onClick={() => setView("entrance")} className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-4">
                        <ArrowLeft size={12} /> BACK
                    </button>
                    <div className="panel p-6 mb-4">
                        <h1 className="font-pixel text-3xl uppercase text-primary mb-4">Join a Guild</h1>
                        <div className="flex gap-3 items-center mb-2">
                            <div className="relative flex-1">
                                <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                                <input
                                    data-testid="guild-search"
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                    className="w-full bg-background border border-border pl-9 pr-3 py-2 font-mono text-sm"
                                    placeholder="Search by name…"
                                />
                            </div>
                            <select
                                data-testid="guild-sort"
                                value={sortBy}
                                onChange={(e) => setSortBy(e.target.value)}
                                className="bg-background border border-border px-3 py-2 font-mono text-sm"
                            >
                                <option value="members">Most Members</option>
                                <option value="treasury">Most Treasury</option>
                                <option value="name">Name (A-Z)</option>
                            </select>
                        </div>
                    </div>
                    {filteredGuilds.length === 0 ? (
                        <div className="panel p-6 text-center">
                            <div className="stat-label text-muted-foreground">{guilds.length === 0 ? "No guilds founded yet. Be the first." : "No guilds match your search."}</div>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {filteredGuilds.map((g) => (
                                <div key={g.id} data-testid={`guild-card-${g.id}`} className="panel p-4">
                                    <div className="flex items-start justify-between">
                                        <div className="flex items-center gap-3">
                                            <div className="text-3xl">{g.emblem}</div>
                                            <div>
                                                <div className="font-pixel text-xl uppercase text-primary">{g.name}</div>
                                                <div className="stat-label">{g.member_count}/30 members{g.hall_unlocked ? " · Hall ✓" : ""}</div>
                                            </div>
                                        </div>
                                        <button
                                            data-testid={`join-guild-${g.id}`}
                                            onClick={() => joinGuild(g.id)}
                                            disabled={g.member_count >= 30}
                                            className="press-btn stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                        >
                                            {g.member_count >= 30 ? "FULL" : "JOIN"}
                                        </button>
                                    </div>
                                    {g.tagline && <div className="narr text-xs text-muted-foreground mt-2">&ldquo;{g.tagline}&rdquo;</div>}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        );
    }

    // ---------- DASHBOARD (in a guild) ----------
    if (view === "dashboard" && character.guild_id) {
        if (!guild) return <div className="min-h-[400px] flex items-center justify-center text-primary font-pixel text-2xl">LOADING GUILD…</div>;
        return (
            <div className={embedded ? "" : "min-h-screen p-4 md:p-6"} data-testid="guild-house-page">
                <div className={embedded ? "" : "max-w-5xl mx-auto"}>
                    {!embedded && (
                        <button onClick={() => navigate(-1)} className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-4">
                            <ArrowLeft size={12} /> BACK
                        </button>
                    )}

                    {/* Guild Banner */}
                    <div className="panel p-6 mb-4">
                        <div className="flex items-center gap-4">
                            <div className="text-6xl">{guild.emblem}</div>
                            <div className="flex-1">
                                <div className="stat-label text-primary/70">{guild.member_count} MEMBERS{guild.hall_unlocked ? " · HALL UNLOCKED" : " · HALL LOCKED"}</div>
                                <h1 className="font-pixel text-3xl uppercase text-primary tracking-wider">{guild.name}</h1>
                                {guild.tagline && <div className="narr text-sm text-muted-foreground mt-1">&ldquo;{guild.tagline}&rdquo;</div>}
                            </div>
                            <div className="text-right">
                                <div className="stat-label">YOUR RANK</div>
                                <div className="font-pixel text-lg uppercase text-primary flex items-center gap-1 justify-end">
                                    {isGrandmaster && <Crown size={16} className="text-primary" />}{character.guild_rank}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Sub-tabs */}
                    <div className="flex gap-2 mb-4">
                        {[
                            { id: "overview", label: "Overview", icon: Shield },
                            { id: "members", label: "Members", icon: Users },
                            { id: "hall", label: "Hall", icon: Zap },
                        ].map(t => (
                            <button
                                key={t.id}
                                data-testid={`guild-subtab-${t.id}`}
                                onClick={() => setSubTab(t.id)}
                                className={`press-btn font-pixel text-sm uppercase px-4 py-2 border-2 flex items-center gap-1.5 transition-all ${
                                    subTab === t.id
                                        ? "border-primary bg-primary text-primary-foreground"
                                        : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                                }`}
                            >
                                <t.icon size={14} /> {t.label}
                            </button>
                        ))}
                    </div>

                    {/* Overview Tab */}
                    {subTab === "overview" && (
                        <div className="space-y-4">
                            <div className="grid grid-cols-3 gap-3">
                                <div className="panel p-4 text-center">
                                    <div className="stat-label">TREASURY</div>
                                    <div className="text-primary font-mono text-2xl" data-testid="guild-treasury">{treasury}g</div>
                                </div>
                                <div className="panel p-4 text-center">
                                    <div className="stat-label">MEMBERS</div>
                                    <div className="text-primary font-mono text-2xl">{guild.member_count}/30</div>
                                </div>
                                <div className="panel p-4 text-center">
                                    <div className="stat-label">HALL</div>
                                    <div className={`font-mono text-2xl ${hallUnlocked ? "text-primary" : "text-muted-foreground"}`}>{hallUnlocked ? "ACTIVE" : "LOCKED"}</div>
                                </div>
                            </div>

                            {/* Donate Panel */}
                            <div className="panel p-6" data-testid="donate-panel">
                                <h2 className="font-pixel text-xl uppercase text-primary mb-3 flex items-center gap-2">
                                    <Coins size={18} /> Donate to Treasury
                                </h2>
                                <div className="flex gap-2 items-center flex-wrap">
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
                                    <div className="stat-label text-muted-foreground ml-2">Your gold: <span className="text-primary">{character.gold}g</span></div>
                                </div>
                            </div>

                            {/* Leave Guild */}
                            <div className="panel p-6 border-destructive/30">
                                {!confirmLeave ? (
                                    <button
                                        data-testid="leave-guild-btn"
                                        onClick={() => setConfirmLeave(true)}
                                        className="press-btn stat-label px-4 py-2 border border-destructive text-destructive hover:bg-destructive hover:text-destructive-foreground flex items-center gap-2"
                                    >
                                        <LogOut size={14} /> LEAVE GUILD
                                    </button>
                                ) : (
                                    <div className="flex items-center gap-3">
                                        <span className="narr text-sm">Are you sure? {isGrandmaster && "You are the Grandmaster — leadership will pass to the next member."}</span>
                                        <button
                                            data-testid="confirm-leave"
                                            onClick={leaveGuild}
                                            className="press-btn stat-label px-4 py-2 border border-destructive bg-destructive text-destructive-foreground"
                                        >
                                            YES, LEAVE
                                        </button>
                                        <button onClick={() => setConfirmLeave(false)} className="press-btn stat-label px-4 py-2 border border-border text-muted-foreground hover:text-primary">
                                            CANCEL
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Members Tab */}
                    {subTab === "members" && (
                        <div className="panel p-6" data-testid="member-list">
                            <h2 className="font-pixel text-xl uppercase text-primary mb-3 flex items-center gap-2">
                                <Users size={18} /> Members ({guild.member_count})
                            </h2>
                            <div className="space-y-2">
                                {(guild.members_populated || []).map((m) => (
                                    <div key={m.id} data-testid={`member-${m.id}`} className="flex items-center justify-between border-b border-border/40 pb-2">
                                        <div className="flex items-center gap-2">
                                            {m.rank === "grandmaster" && <Crown size={14} className="text-primary" />}
                                            <div>
                                                <div className="font-mono text-sm text-foreground">{m.name}</div>
                                                <div className="stat-label">{m.race} · {m.mastery} · Lv {m.level}</div>
                                            </div>
                                        </div>
                                        <div className="stat-label uppercase text-primary/80">{m.rank}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Hall Tab */}
                    {subTab === "hall" && (
                        <div className="panel p-6" data-testid="hall-panel">
                            <h2 className="font-pixel text-xl uppercase text-primary mb-3 flex items-center gap-2">
                                <Zap size={18} /> Guild Hall
                            </h2>
                            {!hallUnlocked ? (
                                <div className="text-center py-8">
                                    <div className="text-4xl mb-3">🔒</div>
                                    <div className="narr text-muted-foreground">Recruit 3+ members to unlock the Guild Hall.</div>
                                    <div className="stat-label mt-2">Current: {guild.member_count}/3</div>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {/* Active Buffs */}
                                    <div>
                                        <div className="stat-label mb-2">ACTIVE BUFFS</div>
                                        {buffs.length === 0 ? (
                                            <div className="stat-label text-muted-foreground">No active buffs. Purchase one below.</div>
                                        ) : (
                                            <div className="space-y-2">
                                                {buffs.map(b => {
                                                    const meta = BUFF_META[b.buff_id];
                                                    const Icon = meta?.icon || Zap;
                                                    return (
                                                        <div key={b.buff_id} className="flex items-center gap-3 border border-primary/30 bg-primary/5 p-3">
                                                            <Icon size={18} className="text-primary" />
                                                            <div className="flex-1">
                                                                <div className="font-pixel text-sm uppercase text-primary">{b.label}</div>
                                                                <div className="stat-label text-muted-foreground">{b.desc}</div>
                                                            </div>
                                                            <div className="stat-label text-primary" data-testid={`buff-timer-${b.buff_id}`}>{fmtTime(b.remaining_seconds)}</div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        )}
                                    </div>

                                    {/* Buff Shop */}
                                    <div>
                                        <div className="stat-label mb-2">PURCHASE BUFFS (FROM TREASURY)</div>
                                        {!isGrandmaster ? (
                                            <div className="stat-label text-muted-foreground">Only the Grandmaster can purchase hall buffs.</div>
                                        ) : (
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                                {Object.entries(BUFF_META).map(([id, meta]) => {
                                                    const Icon = meta.icon;
                                                    const isActive = buffs.some(b => b.buff_id === id);
                                                    const canAfford = treasury >= meta.cost;
                                                    return (
                                                        <div key={id} className={`panel p-4 border-2 ${isActive ? "border-primary/50" : "border-border"}`}>
                                                            <div className="flex items-start justify-between">
                                                                <div className="flex items-center gap-2">
                                                                    <Icon size={20} className="text-primary" />
                                                                    <div>
                                                                        <div className="font-pixel text-sm uppercase text-primary">{meta.label}</div>
                                                                        <div className="stat-label text-muted-foreground">{meta.desc}</div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div className="flex items-center justify-between mt-3">
                                                                <div className="stat-label flex items-center gap-1">
                                                                    <Coins size={12} className="text-primary" /> {meta.cost}g
                                                                </div>
                                                                <button
                                                                    data-testid={`buy-buff-${id}`}
                                                                    onClick={() => purchaseBuff(id)}
                                                                    disabled={!canAfford}
                                                                    className="press-btn stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                                                >
                                                                    {isActive ? "RENEW" : "ACTIVATE"}
                                                                </button>
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        );
    }

    // Fallback
    return <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-2xl">LOADING…</div>;
}
