import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { ScrollText } from "lucide-react";
import Seo from "@/components/site/Seo";
import OAuthButtons from "@/components/OAuthButtons";

function pwStrength(pw) {
    let s = 0;
    if (pw.length >= 6) s++;
    if (pw.length >= 10) s++;
    if (/[A-Z]/.test(pw)) s++;
    if (/[0-9]/.test(pw)) s++;
    if (/[^A-Za-z0-9]/.test(pw)) s++;
    return s;
}

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [displayName, setDisplayName] = useState("");
    const [busy, setBusy] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const strength = pwStrength(password);
    const strengthLabels = ["Too short", "Weak", "Fair", "Good", "Strong", "Fortified"];
    const strengthColors = ["text-muted-foreground", "text-destructive", "text-destructive", "text-yellow-500", "text-primary", "text-primary"];

    const submit = async (e) => {
        e.preventDefault();
        if (password !== confirm) {
            toast.error("Passwords do not match");
            return;
        }
        if (!displayName.trim()) {
            toast.error("Choose a display name");
            return;
        }
        setBusy(true);
        try {
            const user = await register(email, password, displayName);
            toast.success("Your name is now known in Erchis");
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
                title="Create an account"
                description="Create a free Erchis account and roll your first character."
                path="/register"
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
                        Enter Erchis
                    </h1>
                    <p className="narr text-base text-muted-foreground mb-8">
                        A new name inscribed in the ledgers of the old kingdoms.
                    </p>

                    <form onSubmit={submit} className="space-y-4">
                        <div>
                            <label className="stat-label block mb-1">Display Name</label>
                            <Input
                                data-testid="register-input-displayname"
                                value={displayName}
                                onChange={(e) => setDisplayName(e.target.value)}
                                placeholder="How the world will know you"
                                className="bg-background border-border font-mono text-base h-12"
                                required
                                maxLength={30}
                            />
                        </div>
                        <div>
                            <label className="stat-label block mb-1">Email</label>
                            <Input
                                data-testid="register-input-email"
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
                                data-testid="register-input-password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="At least six letters"
                                className="bg-background border-border font-mono text-base h-12"
                                required
                                minLength={6}
                            />
                            {password.length > 0 && (
                                <div className={`stat-label mt-1 ${strengthColors[strength]}`}>
                                    {strengthLabels[strength]}
                                </div>
                            )}
                        </div>
                        <div>
                            <label className="stat-label block mb-1">Confirm Password</label>
                            <Input
                                data-testid="register-input-confirm"
                                type="password"
                                value={confirm}
                                onChange={(e) => setConfirm(e.target.value)}
                                placeholder="Repeat your secret word"
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
                            data-testid="register-submit"
                            disabled={busy || (confirm.length > 0 && password !== confirm)}
                            className="press-btn w-full mt-2 font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-60"
                            style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                        >
                            {busy ? "…" : "Create Account"}
                        </button>
                    </form>

                    <OAuthButtons onError={(msg) => toast.error(msg)} />

                    <div className="mt-6 text-center">
                        <Link to="/login" className="stat-label hover:text-primary transition-colors" data-testid="register-to-login">
                            › ALREADY HAVE AN ACCOUNT? SIGN IN
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
