import { useEffect, useRef, useState } from "react";
import { Send, Users } from "lucide-react";

/**
 * Reusable chat channel view — used inside the ChatWidget for world/country/guild.
 * All live state comes from the useChatChannel hook (held at the widget level).
 */
export default function ChatChannel({
    label = "",
    messages = [],
    online = [],
    onlineCount = 0,
    me,
    loading = false,
    sending = false,
    error = null,
    onSend,
    accentColor = "text-primary",
    borderColor = "border-primary/30",
    bgColor = "bg-primary/5",
}) {
    const [draft, setDraft] = useState("");
    const [showOnline, setShowOnline] = useState(false);
    const scrollRef = useRef(null);

    useEffect(() => {
        const el = scrollRef.current;
        if (el) el.scrollTop = el.scrollHeight;
    }, [messages]);

    const submit = async (e) => {
        if (e && e.preventDefault) e.preventDefault();
        const text = draft.trim();
        if (!text || sending) return;
        const ok = await onSend(text);
        if (ok) setDraft("");
    };

    if (error) {
        return (
            <div className="flex items-center justify-center h-full text-xs font-mono text-muted-foreground p-4 text-center">
                {error}
            </div>
        );
    }

    return (
        <div className="flex flex-col h-full" data-testid={`chat-channel`}>
            {/* header */}
            <div className="flex items-center justify-between border-b border-border px-3 py-2 shrink-0">
                <div className="min-w-0">
                    <div className="stat-label text-muted-foreground text-[10px]">Channel</div>
                    <div className={`font-pixel text-sm uppercase tracking-wider truncate ${accentColor}`} data-testid="chat-channel-label">
                        {label || "—"}
                    </div>
                </div>
                <button
                    onClick={() => setShowOnline((v) => !v)}
                    data-testid="chat-online-toggle"
                    className="flex items-center gap-1 border border-border px-1.5 py-0.5 text-[10px] font-mono hover:border-primary shrink-0"
                >
                    <span className="inline-block w-1.5 h-1.5 rounded-full bg-green-500" />
                    <Users size={11} /> {onlineCount}
                </button>
            </div>

            {showOnline && (
                <div className="border-b border-border px-2 py-1 max-h-24 overflow-y-auto bg-muted/20 shrink-0" data-testid="chat-online-list">
                    {online.length === 0 ? (
                        <div className="stat-label text-muted-foreground px-1 text-[10px]">Nobody here yet.</div>
                    ) : (
                        online.map((o) => (
                            <div key={o.character_id} className="text-[10px] font-mono py-0.5 px-1 flex items-center gap-1.5">
                                <span className="inline-block w-1 h-1 rounded-full bg-green-500" />
                                {o.display_name}
                                {o.character_id === me ? " (you)" : ""}
                            </div>
                        ))
                    )}
                </div>
            )}

            {/* messages */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto px-2 py-2 space-y-1.5 min-h-0" data-testid="chat-messages">
                {loading && messages.length === 0 ? (
                    <div className="stat-label text-muted-foreground text-center py-6 text-[10px]">Tuning the aetheric channel…</div>
                ) : messages.length === 0 ? (
                    <div className="stat-label text-muted-foreground text-center py-6 text-[10px]">
                        No words yet. Be the first to speak.
                    </div>
                ) : (
                    messages.map((m) => {
                        if (m.kind === "system") {
                            return (
                                <div key={m.id} className="text-center py-0.5" data-testid="chat-system-msg">
                                    <span className="text-[10px] font-mono italic text-primary/70">— {m.text} —</span>
                                </div>
                            );
                        }
                        const mine = m.character_id && me && m.character_id === me;
                        return (
                            <div key={m.id} className={`flex flex-col ${mine ? "items-end" : "items-start"}`} data-testid="chat-user-msg">
                                <div className={`text-[9px] font-mono uppercase tracking-wide ${mine ? "text-primary" : "text-muted-foreground"}`}>
                                    {mine ? "You" : m.display_name}
                                </div>
                                <div className={`max-w-[85%] px-2 py-1 text-xs font-mono border break-words ${mine ? "border-primary bg-primary/10" : "border-border bg-muted/20"}`}>
                                    {m.text}
                                </div>
                            </div>
                        );
                    })
                )}
            </div>

            {/* input */}
            <form onSubmit={submit} className="border-t border-border p-1.5 flex gap-1.5 shrink-0">
                <input
                    data-testid="chat-input"
                    value={draft}
                    onChange={(e) => setDraft(e.target.value)}
                    maxLength={400}
                    placeholder="Type a message…"
                    className="flex-1 bg-background border border-border px-2 py-1 text-xs font-mono focus:border-primary outline-none"
                />
                <button
                    type="submit"
                    data-testid="chat-send"
                    disabled={sending || !draft.trim()}
                    className="press-btn font-pixel text-[10px] uppercase px-2 py-1 border-2 border-primary bg-primary text-primary-foreground disabled:opacity-40 flex items-center gap-1"
                >
                    <Send size={12} />
                </button>
            </form>
        </div>
    );
}
