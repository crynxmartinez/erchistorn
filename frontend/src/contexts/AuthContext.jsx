import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";

const AuthCtx = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null); // null = checking, false = anon, obj = user
    const [error, setError] = useState("");

    const checkSession = useCallback(async () => {
        try {
            const { data } = await api.get("/auth/me");
            setUser(data);
        } catch {
            setUser(false);
        }
    }, []);

    useEffect(() => {
        checkSession();
    }, [checkSession]);

    const login = async (email, password) => {
        setError("");
        try {
            const { data } = await api.post("/auth/login", { email, password });
            setUser(data);
            return data;
        } catch (e) {
            const msg = extractError(e);
            setError(msg);
            throw new Error(msg);
        }
    };

    const register = async (email, password, display_name) => {
        setError("");
        try {
            const { data } = await api.post("/auth/register", { email, password, display_name });
            setUser(data);
            return data;
        } catch (e) {
            const msg = extractError(e);
            setError(msg);
            throw new Error(msg);
        }
    };

    const logout = async () => {
        try {
            await api.post("/auth/logout");
        } catch {
            /* ignore */
        }
        setUser(false);
    };

    const refresh = async () => await checkSession();

    return (
        <AuthCtx.Provider value={{ user, error, login, register, logout, refresh }}>
            {children}
        </AuthCtx.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthCtx);
    if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
    return ctx;
}
