import { useEffect, useRef, useState } from "react";
import { Send, Users } from "lucide-react";

// Presentational country-chat panel. All live state comes from useCountryChat (held
// at the Game page level so presence keeps beating even when this panel is closed).
export default function CountryChat({
    continentName,
    messages = [],
    online = [],
    onlineCount = 0,
    me,
    loading = false,
    sending = false,
    onSend,
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

    return (
        <div className="panel flex flex-col h-[calc(100vh-11rem)] min-h-[440px]" data-testid="country-chat">
            {/* header */}
            <div className="flex items-center justify-between border-b border-border p-3">
                <div>
                    <div className="stat-label text-muted-foreground">Country Chat</div>
                    <div className="font-pixel text-lg uppercase text-primary tracking-wider" data-testid="chat-continent-name">
                        {continentName || "—"}
                    </div>
                </div>
                <button
                    onClick={() => setShowOnline((v) => !v)}
                    data-testid="chat-online-toggle"
                    className="flex items-center gap-1.5 border-2 border-border px-2 py-1 text-xs font-mono hover:border-primary"
                >
                    <span className="inline-block w-2 h-2 rounded-full bg-green-500" />
                    <Users size={13} /> {onlineCount} online
                </button>
            </div>

            {showOnline && (
                <div className="border-b border-border p-2 max-h-36 overflow-y-auto bg-muted/20" data-testid="chat-online-list">
                    {online.length === 0 ? (
                        <div className="stat-label text-muted-foreground px-1">Nobody here yet.</div>
                    ) : (
                        online.map((o) => (
                            <div key={o.character_id} className="text-xs font-mono py-0.5 px-1 flex items-center gap-1.5">
                                <span className="inline-block w-1.5 h-1.5 rounded-full bg-green-500" />
                                {o.display_name}
                                {o.character_id === me ? " (you)" : ""}
                            </div>
                        ))
                    )}
                </div>
            )}

            {/* messages */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-3 space-y-2" data-testid="chat-messages">
                {loading && messages.length === 0 ? (
                    <div className="stat-label text-muted-foreground text-center py-8">Tuning the aetheric channel…</div>
                ) : messages.length === 0 ? (
                    <div className="stat-label text-muted-foreground text-center py-8">
                        No words yet. Be the first to speak in {continentName}.
                    </div>
                ) : (
                    messages.map((m) => {
                        if (m.kind === "system") {
                            return (
                                <div key={m.id} className="text-center py-0.5" data-testid="chat-system-msg">
                                    <span className="text-[11px] font-mono italic text-primary/70">— {m.text} —</span>
                                </div>
                            );
                        }
                        const mine = m.character_id && me && m.character_id === me;
                        return (
                            <div key={m.id} className={`flex flex-col ${mine ? "items-end" : "items-start"}`} data-testid="chat-user-msg">
                                <div className={`text-[10px] font-mono uppercase tracking-wide ${mine ? "text-primary" : "text-muted-foreground"}`}>
                                    {mine ? "You" : m.display_name}
                                </div>
                                <div className={`max-w-[85%] px-2.5 py-1.5 text-sm font-mono border-2 break-words ${mine ? "border-primary bg-primary/10" : "border-border bg-muted/20"}`}>
                                    {m.text}
                                </div>
                            </div>
                        );
                    })
                )}
            </div>

            {/* input */}
            <form onSubmit={submit} className="border-t border-border p-2 flex gap-2">
                <input
                    data-testid="chat-input"
                    value={draft}
                    onChange={(e) => setDraft(e.target.value)}
                    maxLength={400}
                    placeholder={`Speak to ${continentName || "the country"}\u2026`}
                    className="flex-1 bg-background border-2 border-border px-2 py-1.5 text-sm font-mono focus:border-primary outline-none"
                />
                <button
                    type="submit"
                    data-testid="chat-send"
                    disabled={sending || !draft.trim()}
                    className="press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 border-primary bg-primary text-primary-foreground disabled:opacity-40 flex items-center gap-1.5"
                >
                    <Send size={14} /> Send
                </button>
            </form>
        </div>
    );
}
