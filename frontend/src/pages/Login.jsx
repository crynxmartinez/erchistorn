import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { ScrollText } from "lucide-react";
import Seo from "@/components/site/Seo";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [remember, setRemember] = useState(true);
    const [busy, setBusy] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const submit = async (e) => {
        e.preventDefault();
        setBusy(true);
        try {
            const user = await login(email, password);
            toast.success("Welcome back to Erchis");
            if (user.has_character) navigate("/game");
            else navigate("/create");
        } catch (e) {
            toast.error(e.message || "Something went wrong");
        } finally {
            setBusy(false);
        }
    };

    return (
        <div className="site-page min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden">
            <Seo
                title="Sign in"
                description="Return to Erchis."
                path="/login"
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
                        Return to Erchis
                    </h1>
                    <p className="narr text-base text-muted-foreground mb-8">
                        Your name is remembered. Speak it, and the world awakens.
                    </p>

                    <form onSubmit={submit} className="space-y-4">
                        <div>
                            <label className="stat-label block mb-1">Email</label>
                            <Input
                                data-testid="login-input-email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="you@erchis.world"
                                className="bg-background border-border font-mono text-base h-12"
                                required
                            />
                        </div>
                        <div>
                            <label className="stat-label block mb-1">Password</label>
                            <Input
                                data-testid="login-input-password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Your secret word"
                                className="bg-background border-border font-mono text-base h-12"
                                required
                                minLength={6}
                            />
                        </div>

                        <label className="flex items-center gap-2 stat-label text-muted-foreground cursor-pointer">
                            <input
                                type="checkbox"
                                checked={remember}
                                onChange={(e) => setRemember(e.target.checked)}
                                className="accent-primary"
                            />
                            Remember me
                        </label>

                        <button
                            type="submit"
                            data-testid="login-submit"
                            disabled={busy}
                            className="press-btn w-full mt-2 font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-60"
                            style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                        >
                            {busy ? "…" : "Sign In"}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <Link to="/register" className="stat-label hover:text-primary transition-colors" data-testid="login-to-register">
                            › NEW TO ERCHIS? CREATE AN ACCOUNT
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
