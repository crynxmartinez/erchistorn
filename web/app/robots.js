const ORIGIN = process.env.NEXT_PUBLIC_SITE_ORIGIN || "https://erchis.online";

/**
 * The game client and auth screens are an application, not content: they render
 * nothing useful without a session, so they should not compete for crawl budget or
 * surface in results.
 */
export default function robots() {
    return {
        rules: [
            {
                userAgent: "*",
                allow: "/",
                disallow: ["/app/", "/game", "/create", "/login", "/register", "/auth", "/guild/"],
            },
        ],
        sitemap: `${ORIGIN}/sitemap.xml`,
        host: ORIGIN,
    };
}
