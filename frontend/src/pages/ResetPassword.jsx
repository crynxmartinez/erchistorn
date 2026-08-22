import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { ScrollText } from "lucide-react";
import Seo from "@/components/site/Seo";

export default function ResetPassword() {
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [busy, setBusy] = useState(false);
    const [done, setDone] = useState(false);
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token") || "";

    const submit = async (e) => {
        e.preventDefault();
        if (password !== confirm) {
            toast.error("Passwords do not match");
            return;
        }
        if (password.length < 6) {
            toast.error("Password must be at least 6 characters");
            return;
        }
        setBusy(true);
        try {
            await api.post("/auth/reset-password", { token, new_password: password });
            setDone(true);
            toast.success("Password reset successfully");
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const noToken = !token;

    return (
        <div className="site-page min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden">
            <Seo
                title="Reset Password"
                description="Set a new password for your Erchis account."
                path="/reset-password"
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
                        Reset Password
                    </h1>

                    {noToken ? (
                        <div className="space-y-6">
                            <p className="narr text-base text-muted-foreground">
                                No reset token found. Request a new reset link from the forgot password page.
                            </p>
                            <div className="text-center">
                                <Link to="/forgot-password" className="stat-label hover:text-primary transition-colors">
                                    › REQUEST RESET LINK
                                </Link>
                            </div>
                        </div>
                    ) : done ? (
                        <div className="space-y-6">
                            <p className="narr text-base text-muted-foreground">
                                Your password has been forged anew. You may now sign in with your new secret word.
                            </p>
                            <button
                                onClick={() => navigate("/login")}
                                className="press-btn w-full font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                                style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                            >
                                Sign In
                            </button>
                        </div>
                    ) : (
                        <>
                            <p className="narr text-base text-muted-foreground mb-8">
                                Choose a new secret word. It must be at least six letters long.
                            </p>
                            <form onSubmit={submit} className="space-y-4">
                                <div>
                                    <label className="stat-label block mb-1">New Password</label>
                                    <Input
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        placeholder="At least six letters"
                                        className="bg-background border-border font-mono text-base h-12"
                                        required
                                        minLength={6}
                                    />
                                </div>
                                <div>
                                    <label className="stat-label block mb-1">Confirm Password</label>
                                    <Input
                                        type="password"
                                        value={confirm}
                                        onChange={(e) => setConfirm(e.target.value)}
                                        placeholder="Repeat your new secret word"
                                        className="bg-background border-border font-mono text-base h-12"
                                        required
                                        minLength={6}
                                    />
                                    {confirm.length > 0 && password !== confirm && (
                                        <div className="stat-label text-destructive mt-1">Passwords do not match</div>
                                    )}
                                </div>

                                <button
                                    type="submit"
                                    disabled={busy || (confirm.length > 0 && password !== confirm)}
                                    className="press-btn w-full mt-2 font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-60"
                                    style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                                >
                                    {busy ? "…" : "Reset Password"}
                                </button>
                            </form>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
