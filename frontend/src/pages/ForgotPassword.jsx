import { useState } from "react";
import { Link } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { ScrollText, Mail } from "lucide-react";
import Seo from "@/components/site/Seo";

export default function ForgotPassword() {
    const [email, setEmail] = useState("");
    const [busy, setBusy] = useState(false);
    const [sent, setSent] = useState(false);

    const submit = async (e) => {
        e.preventDefault();
        setBusy(true);
        try {
            await api.post("/auth/forgot-password", { email });
            setSent(true);
            toast.success("Reset link sent — check your email");
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    return (
        <div className="site-page min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden">
            <Seo
                title="Forgot Password"
                description="Reset your Erchis account password."
                path="/forgot-password"
                noindex
            />
            <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0"
                style={{
                    background:
                        "radial-gradient(ellipse 60% 60% at 50% 25%, rgba(212,175,55,0.10), transparent 65%)"
                        + ", radial-gradient(ellipse 100% 100% at 50% 50%, transparent 40%, rgba(0,0,0,0.55) 100%)",
                    filter: "grayscale(0.9) sepia(0.3)",
                }}
            />
            <div className="absolute inset-0 bg-background/85" />

            <div className="relative w-full max-w-lg">
                <Link to="/" className="flex items-center gap-2 mb-6 text-primary/70 hover:text-primary">
                    <ScrollText size={18} />
                    <span className="stat-label">ERCHIS</span>
                </Link>
                <div className="panel p-10 md:p-12">
                    <h1 className="font-pixel text-4xl uppercase text-primary tracking-wider mb-3">
                        Forgot Password
                    </h1>
                    <p className="narr text-base text-muted-foreground mb-8">
                        {sent
                            ? "A messenger has been dispatched to your email with a reset link. It expires in 15 minutes."
                            : "Enter the email bound to your account. We will send you a link to forge a new secret word."}
                    </p>

                    {sent ? (
                        <div className="space-y-6">
                            <div className="flex items-center gap-3 p-4 border border-primary/30 bg-primary/5">
                                <Mail size={24} className="text-primary" />
                                <div>
                                    <div className="font-pixel text-sm text-primary">Check your inbox</div>
                                    <div className="stat-label text-muted-foreground mt-1">
                                        The link expires in 15 minutes.
                                    </div>
                                </div>
                            </div>
                            <div className="text-center">
                                <Link to="/login" className="stat-label hover:text-primary transition-colors">
                                    › BACK TO SIGN IN
                                </Link>
                            </div>
                        </div>
                    ) : (
                        <form onSubmit={submit} className="space-y-4">
                            <div>
                                <label className="stat-label block mb-1">Email</label>
                                <Input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="you@erchis.world"
                                    className="bg-background border-border font-mono text-base h-12"
                                    required
                                />
                            </div>

                            <button
                                type="submit"
                                disabled={busy}
                                className="press-btn w-full mt-2 font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-60"
                                style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                            >
                                {busy ? "…" : "Send Reset Link"}
                            </button>
                        </form>
                    )}

                    {!sent && (
                        <div className="mt-6 text-center">
                            <Link to="/login" className="stat-label hover:text-primary transition-colors">
                                › BACK TO SIGN IN
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
