/**
 * Server-side reads from the FastAPI backend.
 *
 * These run at build time (or on revalidation), so the data is baked into the HTML
 * the crawler receives. That is the whole reason this app exists: on the CRA site
 * the blog was fetched in a `useEffect`, so posts existed only after JS executed and
 * were invisible to every crawler that does not run it.
 *
 * Every helper fails soft and returns an empty shape. A marketing page must render
 * with the backend down — an unreachable API should cost you a section, not the
 * whole page.
 */

const BACKEND = process.env.BACKEND_ORIGIN || "http://127.0.0.1:8000";

/** Seconds before a cached fetch is considered stale. */
export const REVALIDATE = {
    content: 3600, // blog, changelog — changes when you publish
    world: 86400, // races, continents — changes when the game data changes
    live: 300, // leaderboard — changes constantly, but not per-request
};

async function get(path, revalidate) {
    try {
        const res = await fetch(`${BACKEND}/api${path}`, {
            next: { revalidate },
            headers: { accept: "application/json" },
        });
        if (!res.ok) return null;
        return await res.json();
    } catch {
        // Build must not fail because the backend is asleep.
        return null;
    }
}

export async function getPosts(limit = 12) {
    const d = await get(`/blog?limit=${limit}`, REVALIDATE.content);
    return d?.posts || [];
}

export async function getPost(slug) {
    return await get(`/blog/${encodeURIComponent(slug)}`, REVALIDATE.content);
}

export async function getLeaderboard() {
    const d = await get("/public/leaderboard", REVALIDATE.live);
    return d?.leaderboard || d?.players || [];
}

export async function getRaces() {
    const d = await get("/public/races", REVALIDATE.world);
    return d?.races || [];
}

export async function getBeastAspects() {
    const d = await get("/public/beast_aspects", REVALIDATE.world);
    return d?.beast_aspects || [];
}

export async function getMarineAdaptations() {
    const d = await get("/public/marine_adaptations", REVALIDATE.world);
    return d?.marine_adaptations || [];
}

export async function getWorld() {
    return await get("/public/world", REVALIDATE.world);
}

export function fmtDate(s) {
    if (!s) return "";
    try {
        return new Date(s).toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
            year: "numeric",
        });
    } catch {
        return "";
    }
}
