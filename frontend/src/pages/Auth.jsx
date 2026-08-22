import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import Seo from "@/components/site/Seo";

export default function Auth() {
    const [mode, setMode] = useState("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [displayName, setDisplayName] = useState("");
    const [busy, setBusy] = useState(false);
    const { login, register } = useAuth();
    const navigate = useNavigate();

    const submit = async (e) => {
        e.preventDefault();
        setBusy(true);
        try {
            let user;
            if (mode === "login") {
                user = await login(email, password);
                toast.success("Welcome back to Erchis");
            } else {
                if (!displayName.trim()) throw new Error("Choose a display name");
                user = await register(email, password, displayName);
                toast.success("Your name is now known in Erchis");
            }
            if (user.has_character) navigate("/game");
            else navigate("/create");
        } catch (e) {
            toast.error(e.message || "Something went wrong");
        } finally {
            setBusy(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden" data-testid="auth-root">
            <Seo
                title="Sign in"
                description="Sign in or create an Erchis account."
                path="/auth"
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

            <div className="relative w-full max-w-md">
                <Link to="/" className="stat-label text-primary/70 hover:text-primary block mb-6" data-testid="auth-back-link">
                    ← ERCHIS
                </Link>
                <div className="panel p-10">
                    <h1 className="font-pixel text-4xl uppercase text-primary tracking-wider mb-2">
                        {mode === "login" ? "Return to Erchis" : "Enter Erchis"}
                    </h1>
                    <p className="narr text-muted-foreground mb-8">
                        {mode === "login"
                            ? "Your name is remembered. Speak it, and the world awakens."
                            : "A new name inscribed in the ledgers of the old kingdoms."}
                    </p>

                    <form onSubmit={submit} className="space-y-4">
                        {mode === "register" && (
                            <div>
                                <label className="stat-label block mb-1">Display Name</label>
                                <Input
                                    data-testid="auth-input-displayname"
                                    value={displayName}
                                    onChange={(e) => setDisplayName(e.target.value)}
                                    placeholder="How the world will know you"
                                    className="bg-background border-border font-mono"
                                    required
                                />
                            </div>
                        )}
                        <div>
                            <label className="stat-label block mb-1">Email</label>
                            <Input
                                data-testid="auth-input-email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="you@erchis.world"
                                className="bg-background border-border font-mono"
                                required
                            />
                        </div>
                        <div>
                            <label className="stat-label block mb-1">Password</label>
                            <Input
                                data-testid="auth-input-password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="At least six letters"
                                className="bg-background border-border font-mono"
                                required
                                minLength={6}
                            />
                        </div>

                        <button
                            type="submit"
                            data-testid="auth-submit"
                            disabled={busy}
                            className="press-btn w-full mt-4 font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-60"
                            style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                        >
                            {busy ? "…" : mode === "login" ? "Sign In" : "Create Account"}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <button
                            data-testid="auth-toggle-mode"
                            onClick={() => setMode(mode === "login" ? "register" : "login")}
                            className="stat-label hover:text-primary transition-colors"
                        >
                            {mode === "login" ? "› NEW TO ERCHIS? CREATE AN ACCOUNT" : "› ALREADY HAVE AN ACCOUNT? SIGN IN"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
