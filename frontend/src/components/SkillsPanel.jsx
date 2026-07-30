import { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import RogueInnatePanel from "@/components/RogueInnatePanel";
import MasteryPassivesPanel from "@/components/MasteryPassivesPanel";

export default function SkillsPanel({ character, skillsById, rogueInnateSkills, roguePassives, masteryPassives, onCharacterUpdate }) {
    const [pickingSlot, setPickingSlot] = useState(null);
    const [dropPos, setDropPos] = useState(null);
    const btnRefs = useRef([]);

    const learnedSkills = (character.skills || []).map((s) => s.skill_id || s);
    const learnedSet = new Set(learnedSkills);
    const bar = character.skill_bar || Array(10).fill(null);

    const assign = async (slot, skill_id) => {
        try {
            const { data } = await api.post("/game/skill/assign", { slot, skill_id });
            onCharacterUpdate?.(data.character);
            setPickingSlot(null);
            setDropPos(null);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const unassign = async (slot) => {
        try {
            const { data } = await api.post("/game/skill/unassign", { slot });
            onCharacterUpdate?.(data.character);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const SkillDetail = ({ s }) => {
        if (!s) return null;
        const reqs = [];
        if (s.level_req) reqs.push(`Lv ${s.level_req}`);
        if (s.mastery_req?.length) reqs.push(s.mastery_req.join(" / "));
        if (s.weapon_req && s.weapon_req !== "none") reqs.push(s.weapon_req);
        return (
            <div className="text-xs space-y-1">
                <div className="font-pixel text-sm uppercase text-primary">{s.name}</div>
                <div className="stat-label text-primary/70">
                    {s.power_type}{s.damage_type ? ` · ${s.damage_type.toUpperCase()}` : ""} · CD {s.cooldown} · PWR {s.power} · CAP {s.skill_capacity_cost ?? 1}
                </div>
                {s.trigger && (
                    <div className="stat-label text-muted-foreground">Trigger: {s.trigger}</div>
                )}
                {s.desc && <div className="narr text-muted-foreground">{s.desc}</div>}
                {reqs.length > 0 && (
                    <div className="stat-label text-primary/60">Requires: {reqs.join(" · ")}</div>
                )}
                {(s.status_apply || s.self_status) && (
                    <div className="stat-label text-primary/60">
                        Effect: {s.status_apply || s.self_status}
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="panel p-6 space-y-6" data-testid="skills-panel">
            {character.mastery === "rogue" && (
                <RogueInnatePanel
                    character={character}
                    innateSkills={rogueInnateSkills || []}
                    passives={roguePassives || []}
                    onCharacterUpdate={onCharacterUpdate}
                />
            )}
            <MasteryPassivesPanel
                character={character}
                masteryPassives={masteryPassives}
            />
            <div className="border-t border-border pt-4">
                <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Skill Library</h3>
                {learnedSet.size === 0 && (
                    <div className="stat-label text-muted-foreground">No skills learned yet. Visit a town trainer to learn skills.</div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {[...learnedSet].map((sid) => {
                        const s = skillsById?.[sid];
                        if (!s) return null;
                        return (
                            <div key={sid} className="panel p-3" data-testid={`skill-known-${sid}`}>
                                <SkillDetail s={s} />
                            </div>
                        );
                    })}
                </div>
            </div>

            <div className="border-t border-border pt-4">
                <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Skill Bar</h3>
                <div className="stat-label text-muted-foreground mb-4">
                    Equip up to 10 skills. Click a slot to choose.
                </div>
                <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
                    {bar.map((sid, idx) => {
                        const s = sid ? skillsById?.[sid] : null;
                        const isPicking = pickingSlot === idx;
                        const options = learnedSkills;
                        const openDrop = () => {
                            const btn = btnRefs.current[idx];
                            if (btn) {
                                const rect = btn.getBoundingClientRect();
                                setDropPos({ top: rect.bottom + 4, left: rect.left, width: 192 });
                            }
                            setPickingSlot(isPicking ? null : idx);
                        };
                        return (
                            <div key={idx} className="relative">
                                <button
                                    ref={(el) => { btnRefs.current[idx] = el; }}
                                    data-testid={`skill-slot-${idx}`}
                                    onClick={openDrop}
                                    className={`relative w-full h-12 border flex items-center justify-center text-xs font-pixel uppercase ${sid ? "border-primary text-primary" : "border-border text-muted-foreground hover:border-primary/50"}`}
                                >
                                    <span className="absolute top-0.5 left-1 text-[9px] leading-none opacity-70">{idx + 1}</span>
                                    <span className="mt-1">{s ? s.name.slice(0, 3) : ""}</span>
                                </button>
                            </div>
                        );
                    })}
                </div>
            </div>

            {pickingSlot !== null && dropPos && createPortal(
                <>
                    <div className="fixed inset-0 z-40" onClick={() => { setPickingSlot(null); setDropPos(null); }} />
                    <div
                        className="fixed z-50 bg-background border border-primary p-2 max-h-60 overflow-y-auto"
                        style={{ top: dropPos.top, left: dropPos.left, width: dropPos.width }}
                    >
                        {(() => {
                            const idx = pickingSlot;
                            const sid = bar[idx];
                            return (
                                <>
                                    {sid && (
                                        <button
                                            onClick={() => { unassign(idx); setPickingSlot(null); setDropPos(null); }}
                                            className="block w-full text-left text-xs text-destructive py-1 mb-1 border-b border-border hover:underline"
                                        >
                                            ✕ Clear slot
                                        </button>
                                    )}
                                    {learnedSkills.length === 0 && (
                                        <div className="stat-label text-muted-foreground">No skills learned</div>
                                    )}
                                    {learnedSkills.map((id) => {
                                        const opt = skillsById?.[id];
                                        const inSlot = bar.indexOf(id);
                                        const equippedElsewhere = inSlot >= 0 && inSlot !== idx;
                                        return (
                                            <button
                                                key={id}
                                                onClick={() => assign(idx, id)}
                                                className={`block w-full text-left text-xs font-mono py-1 hover:text-primary ${equippedElsewhere ? "opacity-50" : ""}`}
                                            >
                                                {opt?.name || id}
                                                {equippedElsewhere && <span className="text-muted-foreground text-[10px]"> (slot {inSlot + 1})</span>}
                                            </button>
                                        );
                                    })}
                                </>
                            );
                        })()}
                    </div>
                </>,
                document.body
            )}
        </div>
    );
}
