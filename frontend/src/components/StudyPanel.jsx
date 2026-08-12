import { useState, useEffect, useCallback } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import {
    GraduationCap, Coins, Clock, Flame, CheckCircle2, Circle,
    Zap, AlertTriangle, X, TrendingUp, Calendar,
} from "lucide-react";

const ACADEMY = {
    name: "Atlantyrion Academy",
    title: "Tide Court — Atlantyrion, Hylion",
    desc: "The pearl-white halls of the undersea capital. Tide Mothers teach the old arts — body, mind, and current.",
    greeting: "Knowledge is a tide. It comes to those who wait, and it leaves those who do not. Enroll, and return each day.",
};

const STAT_LABELS = {
    might: "Might", grace: "Grace", cognition: "Cognition", insight: "Insight",
    essence: "Essence", durability: "Durability",
    vitality: "Vitality", max_hp: "Max HP", max_mp: "Max MP", max_stamina: "Max Stamina",
};

function fmtCountdown(seconds) {
    if (seconds <= 0) return "Expired";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}h ${m}m ${s}s`;
    if (m > 0) return `${m}m ${s}s`;
    return `${s}s`;
}

function tierDots(completed) {
    return Array.from({ length: 5 }, (_, i) => i < completed);
}

export default function StudyPanel({ character, onCharacterUpdate }) {
    const [status, setStatus] = useState(null);
    const [busy, setBusy] = useState(false);
    const [now, setNow] = useState(Date.now());

    const fetchStatus = useCallback(async () => {
        try {
            const { data } = await api.get("/game/study/status");
            setStatus(data);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, []);

    useEffect(() => {
        fetchStatus();
    }, [fetchStatus]);

    useEffect(() => {
        const interval = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(interval);
    }, []);

    const handleEnroll = async (courseId) => {
        setBusy(true);
        try {
            const { data } = await api.post("/game/study/enroll", { course_id: courseId });
            onCharacterUpdate?.(data.character);
            setStatus((prev) => ({ ...prev, ...data.enroll_result }));
            await fetchStatus();
            toast.success(
                `Enrolled in ${data.enroll_result.course_name} — Tier ${data.enroll_result.tier}! ` +
                `Check in daily for ${data.enroll_result.required_days} days.`
            );
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const handleCheckin = async () => {
        setBusy(true);
        try {
            const { data } = await api.post("/game/study/checkin");
            onCharacterUpdate?.(data.character);
            const r = data.checkin_result;
            if (r.tier_completed) {
                toast.success(
                    `Tier ${r.tier} complete! +${r.permanent_bonus_pct}% ${STAT_LABELS[r.stat]} permanently!`
                );
            } else if (r.is_exam_day) {
                toast.success(
                    `Exam Day! +${r.bonus_pct}% ${STAT_LABELS[r.stat]} for ${r.buff_hours}h — one more day to go!`
                );
            } else {
                toast.success(
                    `Checked in! +${r.bonus_pct}% ${STAT_LABELS[r.stat]} for ${r.buff_hours}h ` +
                    `(+${r.xp_bonus_pct}% ${r.xp_bonus_type} XP). Day ${r.login_days_completed}/${r.required_days}.`
                );
            }
            await fetchStatus();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const handleAbandon = async () => {
        setBusy(true);
        try {
            const { data } = await api.post("/game/study/abandon");
            onCharacterUpdate?.(data.character);
            await fetchStatus();
            toast.success("Course abandoned. Progress lost, no refund.");
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const enrollment = status?.enrollment;
    const buff = status?.buff;
    const courses = status?.courses || [];
    const gold = status?.gold ?? character?.gold ?? 0;

    const buffRemaining = buff
        ? Math.max(0, Math.floor((new Date(buff.expires_at) - now) / 1000))
        : 0;

    const mainCourses = courses.filter((c) => c.category === "main");
    const lifeCourses = courses.filter((c) => c.category === "life");

    const renderCourseCard = (course) => {
        const dots = tierDots(course.completed_tiers);
        const canEnroll = course.next_tier !== null && !enrollment;
        const canAfford = gold >= (course.next_tier_cost || 0);
        const isEnrolled = course.is_enrolled;

        return (
            <div
                key={course.id}
                className={`border-2 p-3 transition-all ${
                    isEnrolled
                        ? "border-primary bg-primary/10"
                        : course.completed_tiers >= 5
                        ? "border-amber-500/40 bg-amber-500/5"
                        : "border-border bg-card/50"
                }`}
            >
                <div className="flex items-start justify-between mb-1">
                    <div>
                        <div className="font-pixel text-xs uppercase">
                            {course.name}
                        </div>
                        <div className="stat-label text-muted-foreground">
                            {STAT_LABELS[course.stat]}
                            {course.completed_tiers > 0 && (
                                <span className="text-amber-500 ml-1">
                                    +{course.permanent_bonus_pct}% permanent
                                </span>
                            )}
                        </div>
                    </div>
                    <div className="flex gap-1">
                        {dots.map((filled, i) => (
                            <span key={i}>
                                {filled ? (
                                    <CheckCircle2 size={14} className="text-amber-500" />
                                ) : (
                                    <Circle size={14} className="text-muted-foreground/40" />
                                )}
                            </span>
                        ))}
                    </div>
                </div>

                <p className="text-xs text-muted-foreground italic mb-2">
                    {course.desc}
                </p>

                {isEnrolled ? (
                    <div className="text-xs text-primary font-bold">
                        Currently enrolled — Tier {enrollment?.current_tier}
                    </div>
                ) : course.next_tier ? (
                    <button
                        disabled={busy || !canAfford}
                        onClick={() => handleEnroll(course.id)}
                        className="press-btn font-pixel text-[10px] uppercase px-3 py-1.5 border-2 border-primary text-primary hover:bg-primary hover:text-white disabled:opacity-40 flex items-center gap-1"
                    >
                        <Coins size={12} />
                        Enroll T{course.next_tier} — {course.next_tier_cost.toLocaleString()}g
                    </button>
                ) : (
                    <div className="text-xs text-amber-500 font-bold flex items-center gap-1">
                        <CheckCircle2 size={12} /> Mastered
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="space-y-4">
            {/* Academy header */}
            <div className="border-2 border-border bg-card/50 p-4">
                <div className="flex items-start gap-3">
                    <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                        <GraduationCap className="text-primary" size={24} />
                    </div>
                    <div>
                        <div className="font-pixel text-sm uppercase text-primary">
                            {ACADEMY.name}
                        </div>
                        <div className="stat-label text-muted-foreground">{ACADEMY.title}</div>
                        <div className="text-xs text-muted-foreground italic mt-1">
                            "{ACADEMY.greeting}"
                        </div>
                    </div>
                </div>
            </div>

            {/* Active buff */}
            {buff && (
                <div className={`border-2 p-4 ${buff.is_exam_day ? "border-amber-500 bg-amber-500/10" : "border-green-500/40 bg-green-500/5"}`}>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Zap size={20} className={buff.is_exam_day ? "text-amber-500" : "text-green-500"} />
                            <div>
                                <div className="font-pixel text-xs uppercase">
                                    Study Buff: +{buff.bonus_pct}% {STAT_LABELS[buff.stat]}
                                    {buff.is_exam_day && (
                                        <span className="text-amber-500 ml-2">EXAM DAY!</span>
                                    )}
                                </div>
                                <div className="stat-label text-muted-foreground">
                                    {fmtCountdown(buffRemaining)} remaining
                                </div>
                            </div>
                        </div>
                        <div className="text-right">
                            <div className="text-xs text-green-500 flex items-center gap-1 justify-end">
                                <TrendingUp size={12} />
                                +{buff.xp_bonus_pct}% {buff.xp_bonus_type} XP
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Active enrollment */}
            {enrollment && (
                <div className="border-2 border-primary/40 bg-primary/5 p-4 space-y-3">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Calendar size={20} className="text-primary" />
                            <div>
                                <div className="font-pixel text-xs uppercase">
                                    Enrolled: {courses.find((c) => c.id === enrollment.course_id)?.name || enrollment.course_id}
                                </div>
                                <div className="stat-label text-muted-foreground">
                                    Tier {enrollment.current_tier} — {enrollment.login_days_completed}/{enrollment.required_days} login days
                                </div>
                            </div>
                        </div>
                        <button
                            disabled={busy}
                            onClick={handleAbandon}
                            className="press-btn font-pixel text-[10px] uppercase px-3 py-1.5 border-2 border-red-500/60 text-red-500 hover:bg-red-500 hover:text-white disabled:opacity-40 flex items-center gap-1"
                        >
                            <X size={12} /> Abandon
                        </button>
                    </div>

                    {/* Progress bar */}
                    <div>
                        <div className="h-3 bg-muted rounded-full overflow-hidden">
                            <div
                                className="h-full bg-primary transition-all"
                                style={{
                                    width: `${Math.min(100, (enrollment.login_days_completed / enrollment.required_days) * 100)}%`,
                                }}
                            />
                        </div>
                    </div>

                    {/* Streak + exam day info */}
                    <div className="flex items-center gap-4 flex-wrap">
                        <div className="flex items-center gap-1 text-xs">
                            <Flame size={14} className={enrollment.streak >= 7 ? "text-orange-500" : "text-muted-foreground"} />
                            <span className="text-muted-foreground">Streak: {enrollment.streak} days</span>
                            {enrollment.streak >= 7 && (
                                <span className="text-orange-500 ml-1">
                                    (+{enrollment.buff_hours - 3}h bonus!)
                                </span>
                            )}
                        </div>
                        {enrollment.is_exam_day && (
                            <div className="flex items-center gap-1 text-xs text-amber-500 font-bold">
                                <AlertTriangle size={14} />
                                Exam Day next check-in — double buff!
                            </div>
                        )}
                    </div>

                    {/* Check-in button */}
                    <button
                        disabled={busy || enrollment.today_checked_in}
                        onClick={handleCheckin}
                        className="press-btn font-pixel text-xs uppercase px-6 py-2.5 border-2 border-primary text-primary hover:bg-primary hover:text-white disabled:opacity-40 flex items-center gap-2 w-full justify-center"
                    >
                        {enrollment.today_checked_in ? (
                            <><CheckCircle2 size={16} /> Checked in today — come back tomorrow</>
                        ) : enrollment.is_exam_day ? (
                            <><Flame size={16} /> Check In — Exam Day!</>
                        ) : (
                            <><Calendar size={16} /> Daily Check-In</>
                        )}
                    </button>
                </div>
            )}

            {/* Gold display */}
            <div className="flex items-center gap-2 text-sm">
                <Coins size={16} className="text-amber-500" />
                <span className="font-pixel text-xs uppercase">{gold.toLocaleString()} gold</span>
            </div>

            {/* Main stat courses */}
            <div>
                <div className="font-pixel text-xs uppercase text-primary mb-2 flex items-center gap-2">
                    <GraduationCap size={14} /> Main Stat Courses
                    <span className="text-muted-foreground text-[10px] normal-case">
                        (+10% hunting XP during buff)
                    </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {mainCourses.map(renderCourseCard)}
                </div>
            </div>

            {/* Life stat courses */}
            <div>
                <div className="font-pixel text-xs uppercase text-primary mb-2 flex items-center gap-2">
                    <GraduationCap size={14} /> Life Stat Courses
                    <span className="text-muted-foreground text-[10px] normal-case">
                        (+10% gathering XP during buff)
                    </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {lifeCourses.map(renderCourseCard)}
                </div>
            </div>

            {/* How it works */}
            <div className="border-2 border-border bg-card/30 p-3 text-xs text-muted-foreground space-y-1">
                <div className="font-pixel text-[10px] uppercase text-primary mb-1">How It Works</div>
                <div>• Enroll in one course at a time. Each tier requires daily check-ins (7 days for tier 1, 14 for tier 2, etc.)</div>
                <div>• Each check-in grants a temporary buff to the studied stat for 3+ hours.</div>
                <div>• Complete a tier to make the bonus permanent (+2% per tier, up to +10% at tier 5).</div>
                <div>• 7-day streak: +1h buff. 14-day streak: +2h. 21-day streak: +3h (cap).</div>
                <div>• Exam Day (final day of a tier): buff is doubled!</div>
                <div>• Missing a day just pauses progress — no penalty, but streak resets.</div>
            </div>
        </div>
    );
}
