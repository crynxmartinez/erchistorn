import { useState, useEffect, useCallback } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import {
    Dumbbell, Heart, Clock, Coins, Zap, ShoppingCart,
    CheckCircle2, Timer, TrendingUp, Gift,
} from "lucide-react";

const MAIN_TRAINER = {
    name: "Master Ardent",
    title: "Main Stat Trainer — Oathspire",
    desc: "A scarred veteran whose gym echoes with the ring of steel. He forges bodies the way smiths forge blades.",
    greeting: "Strength, speed, wit — pick your poison. I'll make you better. But I don't work cheap, and I don't work forever.",
};

const LIFE_TRAINER = {
    name: "Elder Cho",
    title: "Life Stat Trainer — Solunara",
    desc: "An ageless elf who tends the Sun-Moon gardens. Her trainees leave with deeper breaths and steadier hearts.",
    greeting: "The body is a garden. Tend it daily, and it will sustain you through any storm.",
};

function fmtTime(min) {
    if (min < 60) return `${min}m`;
    const h = Math.floor(min / 60);
    const m = min % 60;
    return m ? `${h}h ${m}m` : `${h}h`;
}

function fmtCountdown(seconds) {
    if (seconds <= 0) return "Ready!";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}h ${m}m ${s}s`;
    if (m > 0) return `${m}m ${s}s`;
    return `${s}s`;
}

export default function TrainingPanel({ character, onCharacterUpdate, trainerType = "main" }) {
    const [status, setStatus] = useState(null);
    const [shop, setShop] = useState(null);
    const [selectedStat, setSelectedStat] = useState(null);
    const [amount, setAmount] = useState(1);
    const [busy, setBusy] = useState(false);
    const [now, setNow] = useState(Date.now());

    const trainer = trainerType === "main" ? MAIN_TRAINER : LIFE_TRAINER;
    const statsList = trainerType === "main" ? status?.main_stats : status?.life_stats;

    const fetchStatus = useCallback(async () => {
        try {
            const { data } = await api.get("/game/training/status");
            setStatus(data);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, []);

    const fetchShop = useCallback(async () => {
        try {
            const { data } = await api.get("/game/training/shop");
            setShop(data);
        } catch (e) {
            toast.error(extractError(e));
        }
    }, []);

    useEffect(() => {
        fetchStatus();
        fetchShop();
    }, [fetchStatus, fetchShop]);

    // Real-time countdown
    useEffect(() => {
        const interval = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(interval);
    }, []);

    const queue = trainerType === "main" ? status?.queue_main : status?.queue_life;
    const timeUsed = trainerType === "main" ? status?.time_used_main : status?.time_used_life;
    const carryOver = trainerType === "main" ? status?.carry_over_main : status?.carry_over_life;
    const budget = status?.daily_budget_min ?? 180;
    const available = budget + (carryOver ?? 0) - (timeUsed ?? 0);

    const queueRemaining = queue
        ? Math.max(0, Math.floor((new Date(queue.finishes_at) - now) / 1000))
        : 0;
    const queueReady = queue && queueRemaining <= 0;

    const selectedStatInfo = statsList?.find((s) => s.stat === selectedStat);

    // Compute preview cost
    const previewCost = (() => {
        if (!selectedStatInfo) return null;
        let totalTime = 0;
        let totalGold = 0;
        for (let i = 0; i < amount; i++) {
            const statAt = selectedStatInfo.total + i;
            const t = 30 + Math.max(0, statAt - 10) * 5;
            totalTime += t;
            totalGold += 500;
        }
        return { time: totalTime, gold: totalGold };
    })();

    const handleStart = async () => {
        if (!selectedStat) return;
        setBusy(true);
        try {
            const { data } = await api.post("/game/training/start", {
                trainer_type: trainerType,
                stat: selectedStat,
                amount,
            });
            onCharacterUpdate?.(data.character);
            setStatus((prev) => ({
                ...prev,
                [`queue_${trainerType}`]: data.training_result.queue,
                [`time_used_${trainerType}`]:
                    (prev?.[`time_used_${trainerType}`] ?? 0) + data.training_result.time_spent,
            }));
            toast.success(
                `Training ${amount} ${selectedStat} — finishes in ${fmtTime(previewCost.time)}`
            );
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const handleCollect = async () => {
        setBusy(true);
        try {
            const { data } = await api.post("/game/training/collect", {
                trainer_type: trainerType,
            });
            onCharacterUpdate?.(data.character);
            setStatus((prev) => ({ ...prev, [`queue_${trainerType}`]: null }));
            toast.success(
                `+${data.training_result.amount} ${data.training_result.stat} collected!`
            );
            fetchStatus();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const handleBuy = async (itemId) => {
        setBusy(true);
        try {
            const { data } = await api.post("/game/training/shop/buy", { item_id: itemId });
            onCharacterUpdate?.(data.character);
            toast.success(`Purchased ${data.purchase_result.item}!`);
            fetchStatus();
            fetchShop();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const budgetPct = budget > 0 ? Math.min(100, (timeUsed / budget) * 100) : 0;

    return (
        <div className="space-y-4">
            {/* Trainer header */}
            <div className="border-2 border-border bg-card/50 p-4">
                <div className="flex items-start gap-3">
                    <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                        {trainerType === "main" ? (
                            <Dumbbell className="text-primary" size={24} />
                        ) : (
                            <Heart className="text-primary" size={24} />
                        )}
                    </div>
                    <div>
                        <div className="font-pixel text-sm uppercase text-primary">
                            {trainer.name}
                        </div>
                        <div className="stat-label text-muted-foreground">{trainer.title}</div>
                        <div className="text-xs text-muted-foreground italic mt-1">
                            "{trainer.greeting}"
                        </div>
                    </div>
                </div>
            </div>

            {/* Daily budget bar */}
            <div className="border-2 border-border bg-card/50 p-4">
                <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                        <Clock size={16} className="text-primary" />
                        <span className="font-pixel text-xs uppercase">Daily Training Time</span>
                    </div>
                    <span className="stat-label text-muted-foreground">
                        {fmtTime(timeUsed ?? 0)} / {fmtTime(budget)} used
                        {carryOver > 0 && ` (+${fmtTime(carryOver)} carried)`}
                    </span>
                </div>
                <div className="h-3 bg-muted rounded-full overflow-hidden">
                    <div
                        className="h-full bg-primary transition-all"
                        style={{ width: `${budgetPct}%` }}
                    />
                </div>
                <div className="stat-label text-muted-foreground mt-1">
                    {fmtTime(available)} remaining today
                </div>
                {status?.login_streak >= 7 && (
                    <div className="flex items-center gap-1 mt-1 text-xs text-green-500">
                        <Gift size={12} /> 7-day streak bonus active (+1hr)
                    </div>
                )}
                {status?.bonus_purchased > 0 && (
                    <div className="flex items-center gap-1 mt-1 text-xs text-amber-500">
                        <TrendingUp size={12} /> Mentor's Blessing: +{status.bonus_purchased * 30}m permanent
                    </div>
                )}
            </div>

            {/* Active queue */}
            {queue && (
                <div className="border-2 border-primary/40 bg-primary/5 p-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Timer size={20} className={queueReady ? "text-green-500" : "text-primary"} />
                            <div>
                                <div className="font-pixel text-xs uppercase">
                                    Training: {queue.amount}x {queue.stat}
                                </div>
                                <div className="stat-label text-muted-foreground">
                                    {queueReady ? (
                                        <span className="text-green-500 font-bold">Complete! Collect now.</span>
                                    ) : (
                                        <>Finishes in {fmtCountdown(queueRemaining)}</>
                                    )}
                                </div>
                            </div>
                        </div>
                        {queueReady && (
                            <button
                                data-testid="training-collect"
                                disabled={busy}
                                onClick={handleCollect}
                                className="press-btn font-pixel text-xs uppercase px-4 py-2 border-2 border-green-500 text-green-500 hover:bg-green-500 hover:text-white disabled:opacity-40 flex items-center gap-2"
                            >
                                <CheckCircle2 size={14} /> Collect
                            </button>
                        )}
                    </div>
                </div>
            )}

            {/* Stat picker */}
            <div className="border-2 border-border bg-card/50 p-4">
                <div className="font-pixel text-xs uppercase mb-3">Train a Stat</div>
                <div className="grid grid-cols-2 gap-2">
                    {statsList?.map((s) => {
                        const isMaxed = s.cap !== null && s.trained >= s.cap;
                        const isSelected = selectedStat === s.stat;
                        return (
                            <button
                                key={s.stat}
                                data-testid={`training-stat-${s.stat}`}
                                disabled={isMaxed || (queue && !queueReady)}
                                onClick={() => {
                                    setSelectedStat(s.stat);
                                    setAmount(1);
                                }}
                                className={`p-3 border-2 text-left transition-all disabled:opacity-30 disabled:cursor-not-allowed ${
                                    isSelected
                                        ? "border-primary bg-primary/10"
                                        : "border-border hover:border-primary/50"
                                }`}
                            >
                                <div className="font-pixel text-xs uppercase">{s.stat.replace(/_/g, " ")}</div>
                                <div className="stat-label text-muted-foreground">
                                    Base: {s.base} · Trained: +{s.trained} · Total: {s.total}
                                </div>
                                <div className="text-xs text-muted-foreground mt-1">
                                    {fmtTime(s.time_per_point)} / +1 · {s.gold_per_point}g / +1
                                </div>
                                {s.cap !== null && (
                                    <div className="text-xs mt-1">
                                        {isMaxed ? (
                                            <span className="text-red-500">CAP REACHED (+{s.cap})</span>
                                        ) : (
                                            <span className="text-muted-foreground">
                                                Cap: +{s.cap} ({s.cap - s.trained} left)
                                            </span>
                                        )}
                                    </div>
                                )}
                                {s.cap === null && (
                                    <div className="text-xs text-green-500 mt-1">No cap</div>
                                )}
                            </button>
                        );
                    })}
                </div>

                {/* Amount selector + cost preview */}
                {selectedStatInfo && !(queue && !queueReady) && (
                    <div className="mt-4 space-y-3">
                        <div className="flex items-center gap-3">
                            <label className="stat-label text-muted-foreground">Amount:</label>
                            <input
                                type="number"
                                min={1}
                                max={20}
                                value={amount}
                                onChange={(e) => setAmount(Math.max(1, Math.min(20, parseInt(e.target.value) || 1)))}
                                className="w-20 px-2 py-1 bg-muted border border-border text-sm"
                            />
                            <span className="text-xs text-muted-foreground">max 20 at once</span>
                        </div>

                        {previewCost && (
                            <div className="flex gap-4 text-sm">
                                <span className="flex items-center gap-1">
                                    <Clock size={14} className="text-primary" />
                                    {fmtTime(previewCost.time)}
                                </span>
                                <span className="flex items-center gap-1">
                                    <Coins size={14} className="text-amber-500" />
                                    {previewCost.gold.toLocaleString()}g
                                </span>
                                {previewCost.time > available && (
                                    <span className="text-red-500 text-xs">
                                        ⚠ Not enough time today
                                    </span>
                                )}
                                {previewCost.gold > (character?.gold ?? 0) && (
                                    <span className="text-red-500 text-xs">
                                        ⚠ Not enough gold
                                    </span>
                                )}
                            </div>
                        )}

                        <button
                            data-testid="training-start"
                            disabled={
                                busy ||
                                !selectedStat ||
                                (queue && !queueReady) ||
                                (previewCost?.time > available) ||
                                (previewCost?.gold > (character?.gold ?? 0))
                            }
                            onClick={handleStart}
                            className="press-btn font-pixel text-xs uppercase w-full px-4 py-2 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            <Dumbbell size={14} /> {busy ? "Starting..." : "Start Training"}
                        </button>
                    </div>
                )}
            </div>

            {/* Trainer Shop */}
            <div className="border-2 border-border bg-card/50 p-4">
                <div className="flex items-center gap-2 mb-3">
                    <ShoppingCart size={16} className="text-primary" />
                    <span className="font-pixel text-xs uppercase">Trainer Shop</span>
                    <span className="stat-label text-muted-foreground ml-auto">
                        {character?.gold?.toLocaleString() ?? 0}g
                    </span>
                </div>
                <div className="text-xs text-muted-foreground italic mb-3">
                    Exclusive items — not available on the market, not tradeable.
                </div>
                <div className="space-y-2">
                    {shop?.items?.map((item) => {
                        const maxed = item.max_purchases && item.purchased >= item.max_purchases;
                        const usedToday = item.uses_today ?? 0;
                        const dailyMaxed = item.max_uses_per_day && usedToday >= item.max_uses_per_day;
                        const canAfford = (character?.gold ?? 0) >= item.price;
                        return (
                            <div
                                key={item.id}
                                className="flex items-center justify-between p-2 border border-border/50"
                            >
                                <div className="flex-1">
                                    <div className="font-pixel text-xs uppercase">{item.name}</div>
                                    <div className="stat-label text-muted-foreground text-xs">
                                        {item.desc}
                                    </div>
                                    {item.max_uses_per_day && (
                                        <div className="text-xs text-muted-foreground">
                                            Uses today: {usedToday}/{item.max_uses_per_day}
                                        </div>
                                    )}
                                    {item.max_purchases && (
                                        <div className="text-xs text-muted-foreground">
                                            Purchased: {item.purchased}/{item.max_purchases}
                                        </div>
                                    )}
                                </div>
                                <button
                                    data-testid={`training-buy-${item.id}`}
                                    disabled={busy || maxed || dailyMaxed || !canAfford}
                                    onClick={() => handleBuy(item.id)}
                                    className="press-btn font-pixel text-xs uppercase px-3 py-1 border border-amber-500 text-amber-500 hover:bg-amber-500 hover:text-black disabled:opacity-30 disabled:cursor-not-allowed flex items-center gap-1 shrink-0"
                                >
                                    <Coins size={12} /> {item.price.toLocaleString()}g
                                </button>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
