import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import Dice from "@/components/Dice";

export default function CombatScreen({ combatStart, character, itemsById, skillsById, onEnd }) {
    const [state, setState] = useState(combatStart.state);
    const [ch, setCh] = useState(character);
    const [rolling, setRolling] = useState(false);
    const [lastOutcome, setLastOutcome] = useState(null);
    const [pendingSkillId, setPendingSkillId] = useState(null);
    const [pendingItemId, setPendingItemId] = useState(null);
    const [victory, setVictory] = useState(null);
    const [rewards, setRewards] = useState(null);

    useEffect(() => {
        setState(combatStart.state);
        setCh(character);
    }, [combatStart, character]);

    const takeTurn = async () => {
        setRolling(true);
        setLastOutcome(null);
        try {
            const { data } = await api.post("/game/combat/turn", {
                combat_id: state.combat_id,
                manual_skill_id: pendingSkillId,
                manual_item_id: pendingItemId,
            });
            setState({ ...data.result.state, combat_id: state.combat_id });
            setCh(data.character);
            const strike = data.result.log?.find((l) => l.kind === "player_strike");
            if (strike) setLastOutcome(strike.outcome);
            if (data.result.victory === true) {
                setVictory(true);
                setRewards(data.result.rewards);
            } else if (data.result.victory === false) {
                setVictory(false);
            }
            setPendingSkillId(null);
            setPendingItemId(null);
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    const monsterHpPct = Math.round((state.monster_hp / Math.max(1, state.monster_max_hp)) * 100);
    const playerHpPct = Math.round((ch.hp / Math.max(1, ch.max_hp)) * 100);

    // learned skills (with cooldown info)
    const learnedSkills = (ch.skills || []).map((s) => {
        const sid = s.skill_id || s;
        return {
            id: sid,
            def: skillsById?.[sid],
            cooldown: state.skill_cooldowns?.[sid] || 0,
        };
    });

    // consumable items
    const consumables = (ch.inventory || [])
        .filter((i) => itemsById?.[i.item_id]?.kind === "consumable" && i.quantity > 0)
        .map((i) => ({ id: i.item_id, qty: i.quantity, def: itemsById[i.item_id] }));

    if (victory !== null) {
        return (
            <div className="panel p-6" data-testid="combat-result">
                <h3 className="font-pixel text-4xl uppercase mb-4"
                    style={{ color: victory ? "hsl(var(--primary))" : "hsl(var(--destructive))" }}>
                    {victory ? "VICTORY" : "DEFEAT"}
                </h3>
                <div className="narr text-lg text-foreground/90 mb-4">
                    {victory
                        ? `The ${state.monster_id.replace(/_/g, " ")} lies still. Erchis notices.`
                        : `${ch.name} collapses in the dust. The world does not weep.`}
                </div>
                {victory && rewards && (
                    <div className="grid grid-cols-3 gap-4 font-mono text-sm mb-4">
                        <div>
                            <div className="stat-label">GOLD</div>
                            <div className="text-primary text-xl">+{rewards.gold}</div>
                        </div>
                        <div>
                            <div className="stat-label">XP</div>
                            <div className="text-primary text-xl">+{rewards.xp}</div>
                        </div>
                        <div>
                            <div className="stat-label">DROPS</div>
                            <div className="text-primary text-xl">{rewards.items?.length || 0}</div>
                        </div>
                    </div>
                )}
                {victory && rewards?.items?.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                        {rewards.items.map((it, i) => {
                            const [iid, q] = it;
                            return (
                                <span key={i} data-testid={`combat-drop-${iid}`}
                                      className="stat-label px-2 py-1 border border-primary text-primary">
                                    {itemsById?.[iid]?.name || iid} × {q}
                                </span>
                            );
                        })}
                    </div>
                )}
                <button
                    data-testid="combat-end-continue"
                    onClick={() => onEnd?.(ch)}
                    className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                >
                    Continue →
                </button>
            </div>
        );
    }

    return (
        <div className="panel p-6 space-y-4" data-testid="combat-screen">
            {/* Combatants */}
            <div className="grid grid-cols-2 gap-4">
                <div className="p-3 border border-border">
                    <div className="stat-label mb-1">{ch.name}</div>
                    <div className="h-3 bg-background border border-border relative">
                        <div className="h-full bg-primary transition-all" style={{ width: `${playerHpPct}%` }} />
                    </div>
                    <div className="font-mono text-xs text-muted-foreground mt-1">
                        HP {ch.hp}/{ch.max_hp}
                    </div>
                </div>
                <div className="p-3 border border-destructive">
                    <div className="stat-label mb-1 text-destructive uppercase">{state.monster_id.replace(/_/g, " ")}</div>
                    <div className="h-3 bg-background border border-border relative">
                        <div className="h-full bg-destructive transition-all" style={{ width: `${monsterHpPct}%` }} />
                    </div>
                    <div className="font-mono text-xs text-muted-foreground mt-1">
                        HP {state.monster_hp}/{state.monster_max_hp}
                    </div>
                </div>
            </div>

            {/* Dice + last log */}
            <div className="flex items-center gap-6 border-t border-border pt-4">
                <Dice result={lastOutcome || "?"} rolling={rolling} size={90} testId="combat-dice" />
                <div className="flex-1 max-h-40 overflow-y-auto space-y-2" data-testid="combat-log">
                    {state.log?.slice(-6).map((entry, i) => (
                        <div key={i} className="narr text-sm text-foreground/85 leading-snug">
                            {entry.skill_text && <div className="stat-label text-primary/70 mb-0.5">{entry.skill_text}</div>}
                            {entry.text}
                            {entry.damage !== undefined && (
                                <span className="ml-2 font-mono text-xs text-destructive">[{entry.damage} dmg]</span>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Skill / item override */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 border-t border-border pt-4">
                <div>
                    <div className="stat-label mb-2">SKILL (auto-select if none)</div>
                    <div className="flex flex-wrap gap-1">
                        <button
                            data-testid="skill-manual-none"
                            onClick={() => setPendingSkillId(null)}
                            className={`stat-label px-2 py-1 border ${!pendingSkillId ? "border-primary text-primary" : "border-border text-muted-foreground"}`}
                        >
                            AUTO
                        </button>
                        {learnedSkills.map((s) => (
                            <button
                                key={s.id}
                                data-testid={`skill-manual-${s.id}`}
                                disabled={s.cooldown > 0 || !s.def}
                                onClick={() => setPendingSkillId(s.id)}
                                className={`stat-label px-2 py-1 border ${
                                    pendingSkillId === s.id
                                        ? "border-primary text-primary"
                                        : "border-border text-muted-foreground hover:border-primary"
                                } disabled:opacity-40`}
                            >
                                {s.def?.name || s.id}
                                {s.cooldown > 0 && <span className="ml-1 text-destructive">({s.cooldown})</span>}
                            </button>
                        ))}
                    </div>
                </div>
                <div>
                    <div className="stat-label mb-2">ITEM (auto-use if none)</div>
                    <div className="flex flex-wrap gap-1">
                        <button
                            data-testid="item-manual-none"
                            onClick={() => setPendingItemId(null)}
                            className={`stat-label px-2 py-1 border ${!pendingItemId ? "border-primary text-primary" : "border-border text-muted-foreground"}`}
                        >
                            AUTO
                        </button>
                        {consumables.map((c) => (
                            <button
                                key={c.id}
                                data-testid={`item-manual-${c.id}`}
                                onClick={() => setPendingItemId(c.id)}
                                className={`stat-label px-2 py-1 border ${
                                    pendingItemId === c.id
                                        ? "border-primary text-primary"
                                        : "border-border text-muted-foreground hover:border-primary"
                                }`}
                            >
                                {c.def?.name || c.id} × {c.qty}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            <div className="border-t border-border pt-4">
                <button
                    data-testid="combat-attack-btn"
                    onClick={takeTurn}
                    disabled={rolling}
                    className="press-btn w-full font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40"
                    style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                >
                    {rolling ? "ROLLING…" : "STRIKE"}
                </button>
            </div>
        </div>
    );
}
