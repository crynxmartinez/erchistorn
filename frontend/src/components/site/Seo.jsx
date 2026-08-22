import { useEffect } from "react";

/**
 * Per-route document metadata.
 *
 * All eleven routes previously shared one `<title>`, so every tab, bookmark and
 * search result said the same thing. This sets title, description, canonical and
 * the Open Graph / Twitter pair per page, plus optional JSON-LD.
 *
 * **An honest limit:** this runs on the client. It fixes tab titles, bookmarks and
 * anything that executes JS, and Googlebot will generally see it — but link
 * unfurlers (Discord, Slack, Twitter, Facebook) read the raw HTML and will keep
 * showing the defaults baked into `public/index.html` until the public pages are
 * server-rendered. That is the Phase 3 decision in WEBSITE_DESIGN_PLAN.md §2, and
 * this component is written so the migration only has to move these values into
 * the server response — the call sites will not change.
 *
 * No react-helmet: a ~15kB dependency to set six tags is not worth it, and it
 * would have to be replaced during the SSR migration anyway.
 */

const SITE = "Erchis";
const ORIGIN = "https://erchis.online";
const DEFAULT_IMAGE = `${ORIGIN}/og-image.png`;

/** Set or create a meta/link tag, and report whether we created it. */
function put(selector, make) {
    let el = document.head.querySelector(selector);
    let created = false;
    if (!el) {
        el = make();
        document.head.appendChild(el);
        created = true;
    }
    return { el, created };
}

function metaByName(name, content) {
    const { el, created } = put(`meta[name="${name}"]`, () => {
        const m = document.createElement("meta");
        m.setAttribute("name", name);
        return m;
    });
    el.setAttribute("content", content);
    return created ? el : null;
}

function metaByProp(prop, content) {
    const { el, created } = put(`meta[property="${prop}"]`, () => {
        const m = document.createElement("meta");
        m.setAttribute("property", prop);
        return m;
    });
    el.setAttribute("content", content);
    return created ? el : null;
}

export default function Seo({
    title,
    description,
    path = "",
    image = DEFAULT_IMAGE,
    type = "website",
    noindex = false,
    jsonLd = null,
}) {
    const fullTitle = title ? `${title} — ${SITE}` : `${SITE} — A Fantasy Dice RPG`;
    const url = `${ORIGIN}${path}`;

    useEffect(() => {
        const previousTitle = document.title;
        document.title = fullTitle;

        // Track only the nodes we create, so cleanup never removes the defaults
        // that public/index.html ships for the crawlers that do not run JS.
        const created = [];
        const track = (node) => node && created.push(node);

        if (description) {
            track(metaByName("description", description));
            const d = document.head.querySelector('meta[name="description"]');
            if (d) d.setAttribute("content", description);
            track(metaByProp("og:description", description));
            track(metaByName("twitter:description", description));
        }
        track(metaByProp("og:title", fullTitle));
        track(metaByName("twitter:title", fullTitle));
        track(metaByProp("og:url", url));
        track(metaByProp("og:type", type));
        track(metaByProp("og:image", image));
        track(metaByName("twitter:image", image));

        const canonical = document.head.querySelector('link[rel="canonical"]');
        const previousCanonical = canonical?.getAttribute("href");
        if (canonical) canonical.setAttribute("href", url);

        let robots = null;
        if (noindex) {
            robots = document.createElement("meta");
            robots.setAttribute("name", "robots");
            robots.setAttribute("content", "noindex, nofollow");
            document.head.appendChild(robots);
        }

        let ld = null;
        if (jsonLd) {
            ld = document.createElement("script");
            ld.type = "application/ld+json";
            ld.textContent = JSON.stringify(jsonLd);
            document.head.appendChild(ld);
        }

        return () => {
            document.title = previousTitle;
            if (canonical && previousCanonical) canonical.setAttribute("href", previousCanonical);
            robots?.remove();
            ld?.remove();
            created.forEach((n) => n.remove());
        };
    }, [fullTitle, description, url, image, type, noindex, jsonLd]);

    return null;
}

/** Schema.org VideoGame, for the home page. */
export const GAME_JSON_LD = {
    "@context": "https://schema.org",
    "@type": "VideoGame",
    name: "Erchis",
    url: ORIGIN,
    description:
        "A free browser-based fantasy RPG decided by a single weighted six-sided die. Eight races, eleven continents, eleven masteries.",
    image: DEFAULT_IMAGE,
    genre: ["Role-playing game", "Text-based game", "MMORPG"],
    gamePlatform: "Web browser",
    applicationCategory: "Game",
    playMode: "MultiPlayer",
    operatingSystem: "Any",
    offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
};

export { ORIGIN, DEFAULT_IMAGE };
