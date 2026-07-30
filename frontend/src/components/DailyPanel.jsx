import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { CheckCircle2, Circle } from "lucide-react";

export default function DailyPanel({ character, onCharacterUpdate }) {
    const missions = character.daily_missions || [];
    const streak = character.login_streak || 0;

    const claim = async (mission_id) => {
        try {
            const { data } = await api.post("/game/daily/claim", { mission_id });
            onCharacterUpdate?.(data.character);
            toast.success(`Claimed ${data.reward?.gold ?? 0}g + ${data.reward?.xp ?? 0}xp!`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    return (
        <div className="panel p-4 space-y-3" data-testid="daily-panel">
            <div className="flex justify-between items-baseline">
                <h3 className="font-pixel text-xl uppercase text-primary">Daily Missions</h3>
                <div className="stat-label text-primary/80" data-testid="login-streak">
                    STREAK: {streak}/7
                </div>
            </div>

            {missions.length === 0 && (
                <div className="stat-label text-muted-foreground">Refreshing at midnight…</div>
            )}

            {missions.map((m) => {
                const pct = Math.min(100, Math.round((m.progress / (m.target?.count || 1)) * 100));
                return (
                    <div key={m.id} data-testid={`mission-${m.id}`} className="border border-border p-2">
                        <div className="flex items-start gap-2">
                            {m.complete ? (
                                <CheckCircle2 size={14} className="text-primary flex-shrink-0 mt-0.5" />
                            ) : (
                                <Circle size={14} className="text-muted-foreground flex-shrink-0 mt-0.5" />
                            )}
                            <div className="flex-1 min-w-0">
                                <div className="text-xs font-mono text-foreground leading-snug">{m.desc}</div>
                                <div className="mt-1 h-1.5 bg-background border border-border">
                                    <div className="h-full bg-primary" style={{ width: `${pct}%` }} />
                                </div>
                                <div className="flex justify-between stat-label mt-1">
                                    <span>{m.progress}/{m.target?.count}</span>
                                    <span className="text-primary">+{m.reward?.gold}g · +{m.reward?.xp}xp</span>
                                </div>
                            </div>
                        </div>
                        {m.complete && !m.claimed && (
                            <button
                                data-testid={`claim-${m.id}`}
                                onClick={() => claim(m.id)}
                                className="press-btn w-full mt-2 stat-label py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                            >
                                CLAIM
                            </button>
                        )}
                        {m.claimed && (
                            <div className="stat-label text-center mt-1 text-muted-foreground">✓ CLAIMED</div>
                        )}
                    </div>
                );
            })}
        </div>
    );
}
