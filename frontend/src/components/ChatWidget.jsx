import { useState, useMemo, useEffect } from "react";
import { createPortal } from "react-dom";
import { MessageSquare, X, Globe, MapPin, Shield, Minimize2 } from "lucide-react";
import { useChatChannel } from "@/hooks/useChatChannel";
import ChatChannel from "@/components/ChatChannel";

/**
 * Floating chat widget — sits at bottom-right of the screen.
 * Collapsed: circular icon button with unread badge.
 * Expanded: panel with channel tabs (World / Country / Guild) and ChatChannel view.
 */
export default function ChatWidget({ character }) {
    const [open, setOpen] = useState(false);
    const [activeChannel, setActiveChannel] = useState("world");
    const [ready, setReady] = useState(false);

    useEffect(() => { setReady(true); }, []);

    const hasGuild = !!character?.guild_id;
    const myId = character?.id;
    const myName = character?.name;

    // Each channel polls independently.
    const world = useChatChannel({
        enabled: !!character,
        active: open && activeChannel === "world",
        channel: "world",
        myId,
        myName,
    });
    const country = useChatChannel({
        enabled: !!character,
        active: open && activeChannel === "country",
        channel: "country",
        myId,
        myName,
    });
    const guild = useChatChannel({
        enabled: !!character && hasGuild,
        active: open && activeChannel === "guild",
        channel: "guild",
        myId,
        myName,
    });

    const channels = useMemo(() => ({
        world,
        country,
        guild,
    }), [world, country, guild]);

    const totalUnread = world.unread + country.unread + (hasGuild ? guild.unread : 0);

    const tabs = [
        { id: "world", label: "World", icon: Globe, color: "text-blue-400", border: "border-blue-400", bg: "bg-blue-500/10" },
        { id: "country", label: "Country", icon: MapPin, color: "text-green-400", border: "border-green-400", bg: "bg-green-500/10" },
    ];
    if (hasGuild) {
        tabs.push({ id: "guild", label: "Guild", icon: Shield, color: "text-purple-400", border: "border-purple-400", bg: "bg-purple-500/10" });
    }

    const active = channels[activeChannel];
    const activeTab = tabs.find((t) => t.id === activeChannel) || tabs[0];

    if (!character || !ready) return null;

    return createPortal(
        <>
            {/* Collapsed FAB */}
            {!open && (
                <button
                    onClick={() => setOpen(true)}
                    data-testid="chat-widget-fab"
                    style={{
                        position: "fixed",
                        bottom: "1rem",
                        right: "1rem",
                        zIndex: 9999,
                        width: "48px",
                        height: "48px",
                        borderRadius: "9999px",
                        border: "2px solid hsl(var(--primary))",
                        background: "hsl(var(--primary))",
                        color: "hsl(var(--primary-foreground))",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        boxShadow: "0 4px 12px rgba(0,0,0,0.4)",
                        cursor: "pointer",
                    }}
                    aria-label="Open chat"
                >
                    <MessageSquare size={22} />
                    {totalUnread > 0 && (
                        <span
                            data-testid="chat-widget-unread"
                            style={{
                                position: "absolute",
                                top: "-4px",
                                right: "-4px",
                                minWidth: "20px",
                                height: "20px",
                                padding: "0 4px",
                                borderRadius: "9999px",
                                background: "hsl(var(--destructive))",
                                color: "hsl(var(--destructive-foreground))",
                                fontSize: "10px",
                                fontFamily: "monospace",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                border: "2px solid hsl(var(--background))",
                            }}
                        >
                            {totalUnread > 9 ? "9+" : totalUnread}
                        </span>
                    )}
                </button>
            )}

            {/* Expanded panel */}
            {open && (
                <div
                    style={{
                        position: "fixed",
                        bottom: "1rem",
                        right: "1rem",
                        zIndex: 9999,
                        width: "360px",
                        maxWidth: "calc(100vw - 2rem)",
                        height: "480px",
                        maxHeight: "calc(100vh - 2rem)",
                        background: "linear-gradient(180deg, hsl(var(--card)) 0%, hsl(var(--popover)) 100%)",
                        border: "1px solid hsl(var(--border))",
                        display: "flex",
                        flexDirection: "column",
                        boxShadow: "0 8px 32px rgba(0,0,0,0.6)",
                    }}
                    data-testid="chat-widget-panel"
                >
                    {/* Title bar */}
                    <div className="flex items-center justify-between border-b border-border px-2 py-1.5 shrink-0">
                        <div className="flex items-center gap-1.5">
                            {/* Channel tabs */}
                            {tabs.map((tab) => {
                                const Icon = tab.icon;
                                const ch = channels[tab.id];
                                const isActive = activeChannel === tab.id;
                                return (
                                    <button
                                        key={tab.id}
                                        onClick={() => setActiveChannel(tab.id)}
                                        data-testid={`chat-tab-${tab.id}`}
                                        className={`flex items-center gap-1 px-2 py-1 text-[10px] font-pixel uppercase border ${
                                            isActive
                                                ? `${tab.border} ${tab.bg} ${tab.color}`
                                                : "border-border text-muted-foreground hover:border-primary"
                                        }`}
                                    >
                                        <Icon size={11} />
                                        {tab.label}
                                        {ch.unread > 0 && !isActive && (
                                            <span className="ml-0.5 min-w-[14px] h-[14px] px-0.5 rounded-full bg-destructive text-destructive-foreground text-[8px] font-mono flex items-center justify-center">
                                                {ch.unread > 9 ? "9+" : ch.unread}
                                            </span>
                                        )}
                                    </button>
                                );
                            })}
                        </div>
                        <button
                            onClick={() => setOpen(false)}
                            data-testid="chat-widget-close"
                            className="text-muted-foreground hover:text-primary p-1"
                            aria-label="Close chat"
                        >
                            <Minimize2 size={14} />
                        </button>
                    </div>

                    {/* Channel content */}
                    <div className="flex-1 min-h-0 overflow-hidden">
                        <ChatChannel
                            label={active.label}
                            messages={active.messages}
                            online={active.online}
                            onlineCount={active.onlineCount}
                            me={active.me}
                            loading={active.loading}
                            sending={active.sending}
                            error={active.error}
                            onSend={active.send}
                            accentColor={activeTab.color}
                            borderColor={activeTab.border}
                            bgColor={activeTab.bg}
                        />
                    </div>
                </div>
            )}
        </>
    , document.body);
}
