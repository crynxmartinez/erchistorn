import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { toast } from "sonner";

const POLL_MS = 6000;

/**
 * Generic multi-channel chat hook. Each channel instance polls independently
 * and tracks its own unread count.
 *
 * @param {object}   opts
 * @param {boolean}  opts.enabled   - whether to poll at all
 * @param {boolean}  opts.active    - whether this channel is currently visible (clears unread)
 * @param {string}   opts.channel   - "world" | "country" | "guild"
 * @param {string|null} opts.myId   - character id
 * @param {string}   opts.myName    - character name
 */
export function useChatChannel({ enabled = true, active = false, channel = "country", myId = null, myName = "" } = {}) {
    const [label, setLabel] = useState("");
    const [messages, setMessages] = useState([]);
    const [online, setOnline] = useState([]);
    const [onlineCount, setOnlineCount] = useState(0);
    const [me, setMe] = useState(myId);
    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);
    const [unread, setUnread] = useState(0);
    const [error, setError] = useState(null);

    const seenSystemRef = useRef(new Set());
    const seenUserRef = useRef(new Set());
    const initializedRef = useRef(false);
    const inFlightRef = useRef(false);
    const activeRef = useRef(active);
    const myNameRef = useRef(myName);

    useEffect(() => { activeRef.current = active; }, [active]);
    useEffect(() => { myNameRef.current = myName; }, [myName]);
    useEffect(() => { if (active) setUnread(0); }, [active]);

    const pollUrl = channel === "world" ? "/chat/world/poll" : channel === "guild" ? "/chat/guild/poll" : "/chat/poll";
    const sendUrl = channel === "world" ? "/chat/world/send" : channel === "guild" ? "/chat/guild/send" : "/chat/send";

    const processPoll = useCallback((data) => {
        if (data.error) {
            setError(data.error);
            setMessages([]);
            setOnline([]);
            setOnlineCount(0);
            setLoading(false);
            return;
        }
        setError(null);
        setLabel(data.label || "");
        setMe(data.me);
        setOnline(data.online || []);
        setOnlineCount(data.online_count ?? (data.online || []).length);
        setMessages(data.messages || []);

        const msgs = data.messages || [];
        if (!initializedRef.current) {
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
            const { data } = await api.get(pollUrl);
            processPoll(data);
        } catch {
            // Chat is non-critical; stay silent on transient poll failures.
        } finally {
            inFlightRef.current = false;
            setLoading(false);
        }
    }, [pollUrl, processPoll]);

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
            const { data } = await api.post(sendUrl, { text: t });
            if (data?.message) {
                seenUserRef.current.add(data.message.id);
                setMessages((prev) => (prev.some((m) => m.id === data.message.id) ? prev : [...prev, data.message]));
            }
            return true;
        } catch {
            toast.error("Message failed to send.");
            return false;
        } finally {
            setSending(false);
        }
    }, [sendUrl]);

    return { label, messages, online, onlineCount, me, loading, sending, unread, error, send };
}
