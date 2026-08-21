import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { toast } from "sonner";

// Live country (continent) chat. Polls the backend on a short interval so the feed
// feels real-time and, just as importantly, so the caller's presence heartbeat keeps
// refreshing while they are in-game. Enter/leave of OTHER players surface as toasts.
const POLL_MS = 6000;

export function useCountryChat({ enabled = true, active = false, myId = null, myName = "" } = {}) {
    const [continent, setContinent] = useState(null);
    const [continentName, setContinentName] = useState("");
    const [messages, setMessages] = useState([]);
    const [online, setOnline] = useState([]);
    const [onlineCount, setOnlineCount] = useState(0);
    const [me, setMe] = useState(myId);
    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);
    const [unread, setUnread] = useState(0);

    const seenSystemRef = useRef(new Set());
    const seenUserRef = useRef(new Set());
    const initializedRef = useRef(false);
    const inFlightRef = useRef(false);
    const activeRef = useRef(active);
    const continentRef = useRef(null);
    const myNameRef = useRef(myName);

    useEffect(() => { activeRef.current = active; }, [active]);
    useEffect(() => { myNameRef.current = myName; }, [myName]);
    // Opening the chat clears the unread badge immediately.
    useEffect(() => { if (active) setUnread(0); }, [active]);

    const processPoll = useCallback((data) => {
        const newContinent = data.continent;
        // Travelled to a new country -> start its feed fresh (no stale toasts).
        if (continentRef.current !== null && continentRef.current !== newContinent) {
            seenSystemRef.current = new Set();
            seenUserRef.current = new Set();
            initializedRef.current = false;
        }
        continentRef.current = newContinent;
        setContinent(newContinent);
        setContinentName(data.continent_name || "");
        setMe(data.me);
        setOnline(data.online || []);
        setOnlineCount(data.online_count ?? (data.online || []).length);
        setMessages(data.messages || []);

        const msgs = data.messages || [];
        if (!initializedRef.current) {
            // First poll for this country: seed dedupe sets so we don't toast history.
            for (const m of msgs) {
                if (m.kind === "system") seenSystemRef.current.add(m.id);
                else seenUserRef.current.add(m.id);
            }
            initializedRef.current = true;
            return;
        }
        for (const m of msgs) {
            if (m.kind === "system") {
                if (!seenSystemRef.current.has(m.id)) {
                    seenSystemRef.current.add(m.id);
                    const mine = myNameRef.current && m.text && m.text.startsWith(myNameRef.current);
                    if (!mine) toast.info(m.text);
                }
            } else if (!seenUserRef.current.has(m.id)) {
                seenUserRef.current.add(m.id);
                const mine = m.character_id && data.me && m.character_id === data.me;
                if (!mine && !activeRef.current) setUnread((u) => u + 1);
            }
        }
    }, []);

    const poll = useCallback(async () => {
        if (inFlightRef.current) return;
        inFlightRef.current = true;
        try {
            const { data } = await api.get("/chat/poll");
            processPoll(data);
        } catch (e) {
            // Chat is non-critical; stay silent on transient poll failures.
        } finally {
            inFlightRef.current = false;
            setLoading(false);
        }
    }, [processPoll]);

    useEffect(() => {
        if (!enabled) return undefined;
        poll();
        const id = setInterval(poll, POLL_MS);
        return () => clearInterval(id);
    }, [enabled, poll]);

    const send = useCallback(async (text) => {
        const t = (text || "").trim();
        if (!t) return false;
        setSending(true);
        try {
            const { data } = await api.post("/chat/send", { text: t });
            if (data?.message) {
                seenUserRef.current.add(data.message.id);
                setMessages((prev) => (prev.some((m) => m.id === data.message.id) ? prev : [...prev, data.message]));
            }
            return true;
        } catch (e) {
            toast.error("Message failed to send.");
            return false;
        } finally {
            setSending(false);
        }
    }, []);

    return { continent, continentName, messages, online, onlineCount, me, loading, sending, unread, send };
}
