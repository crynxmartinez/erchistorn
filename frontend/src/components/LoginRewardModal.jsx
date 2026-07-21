import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function LoginRewardModal({ reward, onClose }) {
    const [open, setOpen] = useState(false);

    useEffect(() => {
        if (reward) setOpen(true);
    }, [reward]);

    if (!open || !reward) return null;

    return (
        <div className="fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4" data-testid="login-reward-modal">
            <div className="panel max-w-md w-full p-8 text-center relative">
                <div className="stat-label text-primary/70 mb-2">DAILY LOGIN REWARD</div>
                <h2 className="font-pixel text-4xl uppercase text-primary mb-2">Day {reward.day}</h2>
                <div className="narr text-sm text-muted-foreground mb-6">Erchis remembers those who return.</div>

                <div className="border-2 border-primary p-6 bg-primary/5 mb-6">
                    <div className="stat-label mb-2">CLAIMED</div>
                    <div className="font-pixel text-2xl uppercase text-primary">
                        +{reward.reward?.gold || 0} GOLD
                    </div>
                    {reward.reward?.item && (
                        <div className="font-pixel text-lg uppercase text-primary mt-2">
                            + {reward.reward.item[0].replace(/_/g, " ")} × {reward.reward.item[1]}
                        </div>
                    )}
                </div>

                <button
                    data-testid="login-reward-close"
                    onClick={() => { setOpen(false); onClose?.(); }}
                    className="press-btn font-pixel text-xl uppercase px-8 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                    style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                >
                    Accept
                </button>
            </div>
        </div>
    );
}
