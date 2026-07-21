import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { ScrollText, Heart, Lock, Check, Sword } from "lucide-react";

const TIER_LABEL = {
    stranger: "Stranger", acquainted: "Acquainted", friend: "Friend",
    trusted: "Trusted", bonded: "Bonded",
};
const TIER_COLOR = {
    stranger: "text-muted-foreground",
    acquainted: "text-foreground",
    friend: "text-primary",
    trusted: "text-primary",
    bonded: "text-rarity-legendary",
};
const STATE_LABEL = {
    available: "AVAILABLE",
    active: "IN PROGRESS",
    completed: "COMPLETE",
    locked: "LOCKED",
};

/**
 * NpcPanel — shows all NPCs local to the character's current town, plus their
 * story-quest chain gated by relationship tier. Only the NPCs that live in the
 * current town are shown; travelling to a new hometown will surface new ones.
 */
export default function NpcPanel({ character, onCharacterUpdate }) {
    const [npcs, setNpcs] = useState([]);
    const [thresholds, setThresholds] = useState({});
    const [selectedNpc, setSelectedNpc] = useState(null);
    const [busy, setBusy] = useState(false);

    const reload = async () => {
        try {
            const r = await api.get("/game/npcs");
            const localOnly = (r.data.npcs || []).filter((n) => n.town === character?.current_town);
            setNpcs(localOnly);
            setThresholds(r.data.relationship_thresholds || {});
            if (localOnly.length > 0 && !selectedNpc) setSelectedNpc(localOnly[0].id);
        } catch (e) { toast.error(extractError(e)); }
    };
    useEffect(() => { reload(); }, [character?.current_town, character?.completed_npc_quests, character?.active_npc_quests]);

    if (!character?.current_town) {
        return (
            <div className="stat-label text-muted-foreground italic">
                No NPCs in the wilderness. Enter a hometown to meet its keepers of stories.
            </div>
        );
    }
    if (npcs.length === 0) {
        return (
            <div className="stat-label text-muted-foreground italic">
                No one here has a story to tell you yet. Come back with more travel behind you.
            </div>
        );
    }

    const active = npcs.find((n) => n.id === selectedNpc) || npcs[0];

    const acceptQuest = async (qid) => {
        setBusy(true);
        try {
            const r = await api.post("/game/npc/quest/accept", { quest_id: qid });
            toast.success(r.data.narrative || "Quest accepted.");
            onCharacterUpdate?.(r.data.character);
            await reload();
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };
    const completeQuest = async (qid) => {
        setBusy(true);
        try {
            const r = await api.post("/game/npc/quest/complete", { quest_id: qid });
            toast.success(r.data.narrative || "Quest complete.");
            if (r.data.relationship_rank_change) {
                toast.success(`Relationship: ${r.data.relationship_rank_change[1]} → ${r.data.relationship_rank_change[0]}!`);
            }
            onCharacterUpdate?.(r.data.character);
            await reload();
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };

    const rel = active.relationship || { points: 0, level: "stranger" };
    const nextTierPts = ["acquainted", "friend", "trusted", "bonded"]
        .map((t) => thresholds[t]).find((th) => rel.points < th);

    return (
        <div data-testid="npc-panel">
            <div className="mb-4">
                <div className="stat-label text-primary/70">STORIES & DEEDS</div>
                <h2 className="font-pixel text-3xl uppercase text-primary">The Voices of {character.current_town.replace(/_/g, " ")}</h2>
                <div className="narr text-sm text-muted-foreground mt-1">
                    Speak, and be spoken to. Every deed you do for them writes another line in their book about you.
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Left rail: NPC list */}
                <div className="md:col-span-1 space-y-1">
                    {npcs.map((n) => (
                        <button
                            key={n.id}
                            data-testid={`npc-select-${n.id}`}
                            onClick={() => setSelectedNpc(n.id)}
                            className={`press-btn text-left w-full p-2 border-2 ${
                                selectedNpc === n.id ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"
                            }`}
                        >
                            <div className="font-pixel text-sm uppercase text-primary">{n.name.split(" of ")[0]}</div>
                            <div className={`stat-label ${TIER_COLOR[n.relationship.level] || "text-muted-foreground"}`}>
                                {TIER_LABEL[n.relationship.level]}
                            </div>
                        </button>
                    ))}
                </div>

                {/* Right: NPC detail */}
                <div className="md:col-span-3 border border-border p-4">
                    <div className="font-pixel text-2xl uppercase text-primary">{active.name}</div>
                    <div className="stat-label text-muted-foreground italic">{active.title}</div>
                    <div className="narr text-sm text-foreground/85 mt-2">{active.description}</div>
                    <div className="stat-label text-primary/70 mt-2 italic">&ldquo;{active.personality}&rdquo;</div>

                    {/* Relationship bar */}
                    <div className="border-t border-border mt-4 pt-3">
                        <div className="stat-label flex justify-between mb-1">
                            <span className="text-primary/70">RELATIONSHIP</span>
                            <span className={TIER_COLOR[rel.level]}>{TIER_LABEL[rel.level]} · {rel.points} pts</span>
                        </div>
                        <div className="h-2 bg-background border border-border">
                            <div className="h-full bg-primary" style={{ width: `${Math.min(100, (rel.points / (nextTierPts || 2000)) * 100)}%` }} />
                        </div>
                    </div>

                    {/* Quests */}
                    <div className="border-t border-border mt-4 pt-3">
                        <div className="stat-label text-primary/70 mb-2 flex items-center gap-1"><ScrollText size={12} /> STORY QUESTS</div>
                        <div className="space-y-2">
                            {active.quests.map((q) => (
                                <div key={q.id} className="border border-border/70 p-3" data-testid={`npc-quest-${q.id}`}>
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <div className="font-pixel text-lg uppercase text-primary">{q.name}</div>
                                            <div className="stat-label text-muted-foreground">Chain {q.order} · requires {TIER_LABEL[q.tier]}</div>
                                        </div>
                                        <div className={`stat-label ${
                                            q.state === "completed" ? "text-primary/70" :
                                            q.state === "active" ? "text-rarity-legendary" :
                                            q.state === "locked" ? "text-muted-foreground/50" :
                                            "text-primary"
                                        }`}>
                                            {q.state === "completed" ? <Check size={14} className="inline" /> :
                                             q.state === "locked" ? <Lock size={12} className="inline" /> :
                                             q.state === "active" ? <Sword size={12} className="inline" /> :
                                             <Heart size={12} className="inline" />
                                            } {STATE_LABEL[q.state]}
                                        </div>
                                    </div>
                                    <div className="text-sm text-foreground/85 mt-1">{q.brief}</div>

                                    {/* Requirements */}
                                    {(q.requirements?.kills?.length > 0 || q.requirements?.gathers?.length > 0) && q.state === "active" && (
                                        <div className="stat-label text-primary/70 mt-2">
                                            OBJECTIVES:
                                            {(q.requirements.kills || []).map(([t, n]) => (
                                                <span key={"k" + t} className="ml-2">
                                                    Kill {n} × {t.replace(/_/g, " ")}
                                                    {" ("}{character?.npc_quest_progress?.[q.id]?.kills?.[t] || 0}/{n}{")"}
                                                </span>
                                            ))}
                                            {(q.requirements.gathers || []).map(([t, n]) => (
                                                <span key={"g" + t} className="ml-2">
                                                    Gather {n} × {t.replace(/_/g, " ")}
                                                    {" ("}{character?.npc_quest_progress?.[q.id]?.gathers?.[t] || 0}/{n}{")"}
                                                </span>
                                            ))}
                                        </div>
                                    )}

                                    {/* Rewards */}
                                    <div className="stat-label text-primary/70 mt-2">
                                        REWARD: {q.rewards.gold}g · {q.rewards.xp}xp · +{q.rewards.relationship} rel
                                        {q.rewards.unique_item && (
                                            <span className="ml-2 text-rarity-epic">
                                                · UNIQUE: {q.rewards.unique_item.name}
                                            </span>
                                        )}
                                    </div>

                                    {/* Action button */}
                                    {q.state === "available" && (
                                        <button
                                            onClick={() => acceptQuest(q.id)}
                                            disabled={busy}
                                            data-testid={`npc-quest-accept-${q.id}`}
                                            className="press-btn font-pixel text-sm uppercase mt-2 px-3 py-1 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-50"
                                        >
                                            Accept
                                        </button>
                                    )}
                                    {q.state === "active" && (
                                        <button
                                            onClick={() => completeQuest(q.id)}
                                            disabled={busy}
                                            data-testid={`npc-quest-complete-${q.id}`}
                                            className="press-btn font-pixel text-sm uppercase mt-2 px-3 py-1 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-50"
                                        >
                                            Hand In
                                        </button>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
