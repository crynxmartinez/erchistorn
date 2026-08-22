import { useEffect, useState } from "react";
import { api } from "@/lib/api";

/**
 * "N players online", beside the primary CTA.
 *
 * Reads `/api/public/online`, which counts non-stale chat-presence heartbeats — the
 * game's own existing definition of a player being here, not a second invented one.
 *
 * **Renders nothing when the count is zero or unavailable.** A marketing page saying
 * "0 players online" is worse than one that stays quiet, and inventing a number would
 * be worse still. So this is an absent claim rather than a false one, and it appears
 * on its own the moment somebody is actually playing.
 */
export default function OnlineCount({ className = "" }) {
    const [online, setOnline] = useState(null);

    useEffect(() => {
        let cancelled = false;

        const read = async () => {
            try {
                const { data } = await api.get("/public/online");
                if (!cancelled) setOnline(Number(data?.online) || 0);
            } catch {
                // Offline or backend down: leave it hidden rather than showing a zero.
            }
        };

        read();
        // A minute is plenty for a header badge, and keeps this off the hot path.
        const id = setInterval(read, 60_000);
        return () => {
            cancelled = true;
            clearInterval(id);
        };
    }, []);

    if (!online) return null;

    return (
        <span
            className={`flex items-center gap-2 font-mono text-label uppercase text-muted-foreground ${className}`}
            title="Players currently in the world"
        >
            <span
                aria-hidden="true"
                className="inline-block h-2 w-2 shrink-0 bg-primary"
                style={{ boxShadow: "0 0 8px hsl(var(--primary))" }}
            />
            {online} {online === 1 ? "player" : "players"} online
        </span>
    );
}
