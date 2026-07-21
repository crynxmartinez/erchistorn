import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function WorldEvents() {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const load = async () => {
            try {
                const { data } = await api.get("/game/events");
                setEvents(data.events);
            } catch {
                /* ignore */
            }
        };
        load();
        const t = setInterval(load, 20000);
        return () => clearInterval(t);
    }, []);

    return (
        <div className="panel p-4" data-testid="world-events">
            <h3 className="font-pixel text-xl uppercase text-primary mb-3">World Feed</h3>
            <div className="space-y-2 max-h-80 overflow-y-auto no-scrollbar">
                {events.length === 0 && (
                    <div className="stat-label text-muted-foreground">The world is quiet.</div>
                )}
                {events.map((e) => (
                    <div key={e.id} className="stat-label border-b border-border/40 pb-1.5">
                        <span className="text-primary/80">{e.character_name}</span>
                        <div className="text-muted-foreground normal-case tracking-normal font-mono text-xs mt-0.5">
                            {e.text}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
