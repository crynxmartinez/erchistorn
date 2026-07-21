import { api, extractError } from "@/lib/api";
import { toast } from "sonner";

export default function SkillsPanel({ character, skillsById, teachers, onCharacterUpdate }) {
    const learned = new Set((character.skills || []).map((s) => s.skill_id || s));

    const learn = async (skill_id, teacher_id) => {
        try {
            const { data } = await api.post("/game/skill/learn", { skill_id, teacher_id });
            onCharacterUpdate?.(data.character);
            toast.success(`Learned ${skillsById?.[skill_id]?.name || skill_id}!`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    return (
        <div className="panel p-6 space-y-6" data-testid="skills-panel">
            <div>
                <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Your Skills</h3>
                {learned.size === 0 && (
                    <div className="stat-label text-muted-foreground">No skills learned yet.</div>
                )}
                <div className="flex flex-wrap gap-2">
                    {[...learned].map((sid) => {
                        const s = skillsById?.[sid];
                        if (!s) return null;
                        return (
                            <div
                                key={sid}
                                data-testid={`skill-known-${sid}`}
                                className="panel p-3 min-w-[160px]"
                            >
                                <div className="font-pixel text-lg uppercase text-primary">{s.name}</div>
                                <div className="stat-label mt-1">
                                    {s.power_type} · CD {s.cooldown} · PWR {s.power}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            <div className="border-t border-border pt-4">
                <h3 className="font-pixel text-2xl uppercase text-primary mb-2">NPC Teachers</h3>
                <div className="stat-label text-muted-foreground mb-4">
                    Find these masters across Aetheria. Coin and level required.
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {teachers.map((t) => (
                        <div
                            key={t.id}
                            data-testid={`teacher-${t.id}`}
                            className="panel p-4"
                        >
                            <div className="font-pixel text-xl uppercase text-primary">{t.name}</div>
                            <div className="stat-label mb-2">{t.biome.replace(/_/g, " ").toUpperCase()}</div>
                            <div className="narr text-sm text-muted-foreground mb-3">{t.desc}</div>
                            <div className="space-y-2">
                                {t.teaches.map((offer) => {
                                    const s = skillsById?.[offer.skill_id];
                                    const already = learned.has(offer.skill_id);
                                    const canAfford = character.gold >= offer.cost_gold;
                                    const canLevel = character.level >= offer.level_req;
                                    return (
                                        <div key={offer.skill_id} className="flex justify-between items-center border-t border-border pt-2">
                                            <div>
                                                <div className="font-mono text-sm text-foreground">{s?.name || offer.skill_id}</div>
                                                <div className="stat-label">
                                                    {offer.cost_gold}g · Lv {offer.level_req}+
                                                </div>
                                            </div>
                                            <button
                                                data-testid={`teach-${t.id}-${offer.skill_id}`}
                                                disabled={already || !canAfford || !canLevel}
                                                onClick={() => learn(offer.skill_id, t.id)}
                                                className="press-btn stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                            >
                                                {already ? "KNOWN" : "LEARN"}
                                            </button>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
