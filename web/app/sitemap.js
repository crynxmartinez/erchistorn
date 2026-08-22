import { getPosts, getWorld } from "@/lib/api";
import { MASTERIES } from "@/content/masteries";

const ORIGIN = process.env.NEXT_PUBLIC_SITE_ORIGIN || "https://erchis.online";

/**
 * Generated, not hand-written.
 *
 * The static sitemap.xml added in Phase 0 listed eight routes and would have gone
 * stale the day the first blog post shipped. This one reads the post list at build
 * (and on revalidation), so publishing a post adds it to the sitemap with no other
 * action.
 *
 * The game client, auth screens and guild pages are absent on purpose — they render
 * nothing without a session, so indexing them wastes crawl budget. robots.js
 * disallows them too.
 */
export default async function sitemap() {
    const now = new Date();

    const staticRoutes = [
        { path: "/", changeFrequency: "weekly", priority: 1.0 },
        { path: "/mechanics", changeFrequency: "monthly", priority: 0.9 },
        { path: "/races", changeFrequency: "monthly", priority: 0.9 },
        { path: "/world", changeFrequency: "monthly", priority: 0.9 },
        { path: "/blog", changeFrequency: "weekly", priority: 0.8 },
        { path: "/leaderboard", changeFrequency: "daily", priority: 0.6 },
        { path: "/changelog", changeFrequency: "weekly", priority: 0.5 },
        { path: "/about", changeFrequency: "yearly", priority: 0.4 },
    ].map((r) => ({
        url: `${ORIGIN}${r.path}`,
        lastModified: now,
        changeFrequency: r.changeFrequency,
        priority: r.priority,
    }));

    // The eleven mastery and eleven continent pages. Generated pages that are not
    // in the sitemap are pages nothing knows to crawl.
    const masteryRoutes = MASTERIES.map((m) => ({
        url: `${ORIGIN}/mastery/${m.id}`,
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.8,
    }));

    const world = await getWorld();
    const continentRoutes = (world?.continents || []).map((c) => ({
        url: `${ORIGIN}/continent/${c.id}`,
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.8,
    }));

    const posts = await getPosts(500);
    const postRoutes = posts.map((p) => ({
        url: `${ORIGIN}/blog/${p.slug}`,
        lastModified: p.updated_at || p.published_at || p.created_at || now,
        changeFrequency: "yearly",
        priority: 0.7,
    }));

    return [...staticRoutes, ...masteryRoutes, ...continentRoutes, ...postRoutes];
}
