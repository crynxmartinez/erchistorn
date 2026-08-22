# erchis-web — the public site

Server-rendered marketing site. The game client stays a SPA in [`../frontend`](../frontend).

## Why this exists

The CRA app served both the marketing pages and the game from one client-rendered
bundle. That is fine for an app and wrong for content: **nothing was in the HTML.**
Measured against the same running backend:

| Content | this app | `../frontend` (CRA) |
|---|---|---|
| Race names and perks | in HTML | absent |
| Continent names | in HTML | absent |
| Leaderboard | in HTML | absent |
| d6 outcome table | in HTML | absent |
| Per-route `<title>` | unique per page | same title on all 11 routes |

Googlebot will usually execute JS eventually. Link unfurlers — Discord, Slack,
Twitter, Facebook — do not, which is why every shared link showed the same generic
card no matter which page was posted.

## Running it

```bash
npm install
npm run dev            # http://localhost:3100
```

The FastAPI backend must be reachable. `/api/*` is rewritten to it, so the browser
stays same-origin and cookies keep behaving as the game client expects.

| Variable | Default | Purpose |
|---|---|---|
| `BACKEND_ORIGIN` | `http://127.0.0.1:8000` | FastAPI origin, used server-side and by the `/api` rewrite |
| `NEXT_PUBLIC_SITE_ORIGIN` | `https://erchis.online` | Canonical origin for metadata, sitemap and robots |
| `NEXT_PUBLIC_APP_ORIGIN` | `/app` | Where "Play free" and "Sign in" point — the game client |

```bash
npm run build && npm start
```

## Deployment — the one thing that needs a decision

**There are now two apps, and something has to route between them.** Nothing here
can make that choice; it depends on your host.

The intended split:

```
erchis.online/           -> this app        (marketing, server-rendered)
erchis.online/app/*      -> ../frontend     (the game client SPA)
```

Any of these works:

1. **Two services behind one proxy** (nginx/Caddy/Traefik): `/` to this app on 3100,
   `/app` to the CRA build. Set `NEXT_PUBLIC_APP_ORIGIN=/app`.
2. **Two hosts**: `erchis.online` here, `play.erchis.online` for the game. Set
   `NEXT_PUBLIC_APP_ORIGIN=https://play.erchis.online`. Simplest, but auth cookies
   need a parent-domain scope to be shared.
3. **Single host, subpath build**: serve the CRA build from `/app` as static files.

Until routing is configured, `../frontend` still serves its own copies of the public
pages. **They were deliberately left in place** — deleting them would break the
current deployment before the new one is wired up. Once routing is live, remove the
public routes from `frontend/src/App.js` and the pages under `frontend/src/pages/`
that are duplicated here.

## What is where

```
app/
  layout.jsx          fonts (self-hosted via next/font), default metadata
  page.jsx            home — server-fetches the ladder and latest posts
  mechanics/          the d6 outcome table and the systems around it
  races/              server-fetched races, beast aspects, marine adaptations
  world/              server-fetched continents (the deep browser stays in the game)
  blog/               index + [slug] with per-post metadata and Article JSON-LD
  leaderboard/        revalidates every 5 minutes
  changelog/ about/   static
  sitemap.js          generated — includes blog slugs, so publishing needs no edit
  robots.js           disallows the game, auth and guild routes
components/site/      shared with ../frontend; same components, next/link instead
lib/api.js            server-side reads, all fail-soft
```

## Two things worth knowing before editing

**Do not set `font-size` on `.font-pixel` or `.font-display`.** A rule doing exactly
that flattened all 149 headings on the old site to 20.7px — the hero ended up smaller
than the body copy. Sizes belong to the type scale in `tailwind.config.js`.

**Fonts load through `next/font`, not `@import`.** An `@import` inside CSS serialises
the request chain: the stylesheet must download before the font URL is even
discovered. That was the largest single contributor to LCP on the old site.

## Still to do

- **22 generated pages**: `/mastery/[id]` x11 and `/continent/[id]` x11. The highest
  -leverage SEO work left, and most of the copy already exists in
  `../MASTERY_PLANS.md`.
- Search Console + sitemap submission, once this is deployed.
- Blog search and tag filters, as real routes (`/blog/tag/[tag]`) rather than
  client-side filtering — each filter should be its own indexable page. Dropped from
  the CRA port on purpose: with zero posts they were premature.
