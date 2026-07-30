import { useEffect, useState, useRef } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Globe, Crown, Clock } from "lucide-react";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";

export default function WaypointPanel({ character, onCharacterUpdate, onTravel }) {
    const [destinations, setDestinations] = useState({
        list: [],
        fee: 0,
        cooldown_secs: 0,
        block_reason: null,
    });
    const [busy, setBusy] = useState(false);
    const [activeHeritage, setActiveHeritage] = useState(null);
    const [now, setNow] = useState(Date.now());
    const fetchedAt = useRef(0);

    // Tick every second for cooldown countdown
    useEffect(() => {
        const timer = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(timer);
    }, []);

    const loadDestinations = async () => {
        try {
            const r = await api.get("/game/teleporter/destinations");
            setDestinations({
                list: r.data.destinations || [],
                fee: r.data.fee_base || 0,
                cooldown_secs: r.data.cooldown_secs || 0,
                block_reason: r.data.block_reason || null,
            });
            fetchedAt.current = Date.now();
            setActiveHeritage({
                continent: r.data.active_heritage_continent,
                name: r.data.active_heritage_name,
            });
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    useEffect(() => {
        loadDestinations();
    }, [character?.current_town]);

    const travel = async (continent_id, fee, is_available) => {
        if (!is_available) return;
        if (character.gold < fee) {
            toast.error("Not enough gold for the fare.");
            return;
        }
        setBusy(true);
        try {
            const r = await api.post("/game/teleporter/travel", { continent_id });
            toast.success(r.data.narrative || "You travel to a new land.");
            onCharacterUpdate?.(r.data.character);
            if (onTravel) onTravel(r.data.hometown);
            else toast.info("Travelled to " + (r.data.hometown || "new town") + ". Return to game to continue.");
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    if (!character?.current_town) {
        return (
            <div className="stat-label text-muted-foreground italic">
                No town waypoint available.
            </div>
        );
    }

    return (
        <TooltipProvider delayDuration={120}>
        <div data-testid="waypoint-panel">
            <div className="stat-label text-primary/70">FOLDED SPACE TRAVEL</div>
            <h2 className="font-pixel text-3xl uppercase text-primary mb-1">Grand Waypoint</h2>
            <p className="narr text-sm text-muted-foreground mb-4">
                A weathered stone humming with folded-space resonance. Step through to another continent.
            </p>

            {destinations.block_reason && !destinations.block_reason.includes("recharging") && (
                <div className="text-xs text-destructive mb-4">{destinations.block_reason}</div>
            )}

            {(() => {
                const elapsed = fetchedAt.current ? Math.floor((now - fetchedAt.current) / 1000) : 0;
                const cd = Math.max(0, destinations.cooldown_secs - elapsed);
                if (cd <= 0) return null;
                const mins = Math.floor(cd / 60);
                const secs = cd % 60;
                return (
                    <div className="flex items-center gap-1 text-xs text-amber-400 mb-4">
                        <Clock size={12} /> Waypoint cooldown: {mins > 0 ? `${mins}m ` : ""}{secs}s
                    </div>
                );
            })()}

            <div className="space-y-2">
                {destinations.list.map((d) => (
                    <Tooltip key={d.continent_id}>
                        <TooltipTrigger asChild>
                            <div className={`border p-3 flex justify-between items-center cursor-help relative ${
                                d.is_heritage ? "border-primary/60 bg-primary/5" : "border-border/70"
                            }`}>
                                {d.is_heritage && (
                                    <div className="absolute -top-2 -right-2 flex items-center gap-0.5 bg-primary text-primary-foreground px-1.5 py-0.5 border border-primary shadow-sm">
                                        <Crown size={10} />
                                        <span className="font-pixel text-[8px] uppercase">Festival</span>
                                    </div>
                                )}
                                <div>
                                    <div className="font-pixel text-sm uppercase text-primary flex items-center gap-1">
                                        {d.continent_name}
                                        {d.is_heritage && <Crown size={12} className="text-primary" />}
                                    </div>
                                    <div className="stat-label text-muted-foreground">{d.hometown_name}</div>
                                </div>
                                <button
                                    onClick={() => travel(d.continent_id, d.fee, d.is_available)}
                                    disabled={busy || !d.is_available || character.gold < d.fee}
                                    className="press-btn font-pixel text-xs uppercase px-3 py-1 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                >
                                    {d.is_current ? "HERE" : d.fee === 0 ? "FREE" : `${d.fee}g TRAVEL`}
                                </button>
                            </div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom" align="start" className="max-w-[300px] bg-popover border border-border text-popover-foreground z-[60]" >
                            <div className="font-pixel text-xs uppercase text-primary mb-1">{d.continent_name}</div>
                            <div className="text-[10px] space-y-1.5">
                                {d.is_heritage && (
                                    <div className="text-primary font-pixel text-[10px] uppercase border-b border-primary/30 pb-1 mb-1">
                                        <Crown size={10} className="inline mr-1" />{d.heritage_name}
                                    </div>
                                )}
                                {d.home_race && (
                                    <div className="text-muted-foreground">Home: {d.home_race.replace(/_/g, " ")}</div>
                                )}
                                {d.specialty && (
                                    <div className="text-muted-foreground">Specialty: {d.specialty}</div>
                                )}
                                {d.desc && (
                                    <div className="text-popover-foreground/80 italic pt-1 border-t border-border/50">
                                        {d.desc}
                                    </div>
                                )}
                                {d.bonus_desc && (
                                    <div className="text-primary/80 pt-1">✦ {d.bonus_desc}</div>
                                )}
                                {d.is_heritage && d.heritage_bonuses && (
                                    <div className="text-primary/80 pt-1 border-t border-border/50">
                                        ✦ {d.heritage_bonuses.desc}
                                    </div>
                                )}
                            </div>
                        </TooltipContent>
                    </Tooltip>
                ))}
            </div>
        </div>
        </TooltipProvider>
    );
}
