# Website Redo — Design System, Rebuild, and SEO

Full rebuild of the public site. **The theme stays.** Written after auditing the
live site in a browser and measuring computed styles rather than eyeballing it.

---

## Scope: what "redo" means here

This is a rebuild of structure, not a reinvention of identity.

### Stays — the theme contract

Treat these as fixed. Every new page must satisfy them.

| Element | Value | Why it stays |
|---|---|---|
| Palette | near-black `#0C0A09`, bone `#E9E7E2`, amber `#D4AF37`, six rarity colours | Coherent, well-chosen dark fantasy. Not the problem. |
| `border-radius` | `0` everywhere | Deliberate, consistent with the pixel identity |
| VT323 | display and headings | It *is* the identity — it has just never been shown above 20.7px |
| Crimson Text | reading copy and narrative | The best-looking thing on the site today |
| JetBrains Mono | labels, stats, numbers | Correct for HUD-flavoured UI |
| Voice | "Eight races. Eleven continents. One six-sided die that will decide whether you become legend — or footnote." | Strong writing. Keep the copy; change how it renders. |
| The d6 | central motif | The game's core mechanic and its natural logo |

### Gets rebuilt

- Information architecture and page set (§3)
- The layout and spacing system (§4) — currently ad-hoc per component
- Every public page's composition (§5)
- The entire SEO foundation (§6) — currently absent
- `public/index.html` — still the CRA scaffolding

### Deleted

- `Landing.jsx` — a dead duplicate of `Home.jsx`, imported nowhere. It already
  caused a fix to be applied to the wrong file.

---

## 1. Why it looks bad: four defects, not taste

| # | Defect | Severity |
|---|---|---|
| 1 | One CSS rule collapses **every heading on every public page to 20.7px** | Critical |
| 2 | Title is still `Emergent | Fullstack App`, description `A product of emergent.sh` | Critical |
| 3 | **Zero artwork.** `public/` contains only `index.html` | High |
| 4 | `Landing.jsx` dead duplicate | Low |

### The typography bug  **[fixed]**

```css
.site-page             { font-size: 18px; }
.site-page .font-pixel { font-size: 1.15em; }   /* 18 x 1.15 = 20.7px */
```

`.site-page .font-pixel` is specificity **0-2-0**; every Tailwind size utility is
**0-1-0**. The class beats all of them, overriding **149 heading and button
declarations** across the public pages.

| Element | Markup asks for | Rendered |
|---|---|---|
| Hero `h1` | `text-5xl md:text-7xl lg:text-8xl` (48/72/96px) | **20.7px** |
| Every section `h2` | `text-3xl md:text-5xl` | **20.7px** |
| Body paragraph | — | **24px** |

Distinct heading sizes on the home page: **one**. The hero was smaller than the
body copy.

**The fix.** The first attempt wrapped the selector in `:where()` to drop its
specificity. **That was wrong, and it is worth recording why.** `:where()` zeroes
only its own argument — `.site-page` still counts — so the selector becomes 0-1-0,
which *ties* with `.text-5xl`. Ties break on source order, and this file is emitted
after the utilities layer, so the override still won.

It looked fixed because the home hero uses a responsive variant (`lg:text-8xl`)
that lands after the rule and escaped, while `/leaderboard`'s plain `text-5xl` did
not. Verified on one page, generalised to all — precisely the mistake this repo
keeps punishing.

The correct fix is to stop setting `font-size` on that class at all. The rule
existed to compensate for VT323 rendering small for its point size; that belongs in
the type scale (§4.1), not in a blanket override on the class every heading uses.

**Verified after, across all eight public pages** (real router navigation):

| Page | h1 | Distinct heading sizes |
|---|---|---|
| `/` | **96px** | 96 / 60 / 48 |
| `/mechanics` | 60px | 60 / 30 |
| `/races` | 60px | 60 / 30 |
| `/world` | 60px | 60 / 36 |
| `/blog`, `/leaderboard`, `/changelog`, `/about` | 48px | 48 |

Headings under 24px: **0** on every page except `/about`, where four are deliberate
`text-xl` sub-headings beneath a 48px `h1`.

---

## 2. The SEO blocker you need to decide first

**The public site is a pure client-side CRA bundle.** Measured: no SSR, no
prerendering, no `react-helmet`, **no per-page `<title>`**, and the blog is fetched
client-side via `api.get('/blog')` inside a `useEffect`.

Consequences today:

- All 11 routes share one title: `Emergent | Fullstack App`
- No `robots.txt`, no `sitemap.xml` — `public/` holds only `index.html`
- No `og:` or `twitter:` tags, so every shared link renders as a grey box
- Blog posts exist only after JS executes. Googlebot can render JS, but slowly and
  unreliably; most social and secondary crawlers do not render at all.

**The timing is lucky: the blog has 0 posts.** There is nothing to rank yet, and
nothing to migrate. That argues strongly for building the foundation properly
*before* writing content, rather than retrofitting SEO onto an indexed site later.

### Three options

| Option | Effort | SEO result | Notes |
|---|---|---|---|
| **A. Prerender the CRA at build** (`react-snap`-style) | ~1 day | Good for static pages, poor for the blog | Cheapest. Puppeteer-at-build is fragile and the tooling is under-maintained. Blog needs a rebuild per post. |
| **B. Split: Next.js public site + keep CRA for the game** | ~1 week | Best | Marketing pages become SSG/ISR with real per-page metadata; the game app stays a SPA, which is correct for an app. Matches the existing two-repo split. |
| **C. Server-render public pages from FastAPI (Jinja)** | ~4 days | Good | Reuses the backend you already run, but duplicates the design system across two stacks — Tailwind classes in Python templates. |

**Recommendation: B**, and do it *now* while there is no content to migrate.
Marketing sites and web apps have genuinely different requirements — one needs
crawlable HTML and fast first paint, the other needs a persistent client. Fighting
that with one bundle is why the current site has neither.

If you want visible results this week instead, do **A** as an interim and treat B
as the Phase 3 target. Do not do A *after* publishing content.

---

## 3. Information architecture

Current routes: `/`, `/login`, `/register`, `/auth`, `/world`, `/races`,
`/mechanics`, `/blog`, `/blog/:slug`, `/leaderboard`, `/about`, `/changelog`.

That set is sound. What is missing is a **purpose and a target query per page** —
right now every page is a wall of the same boxes with the same title.

| Route | Job | Primary CTA | Target query |
|---|---|---|---|
| `/` | Convince in 5 seconds; sell the d6 hook | Begin Your Saga | `text based rpg`, `browser fantasy rpg` |
| `/mechanics` | The differentiator: weighted d6, 11 masteries | Register | `dice based rpg combat`, `turn based browser rpg` |
| `/races` | Build-planning fantasy; 8 races x perks | Register | `<race> rpg builds`, `fantasy rpg races` |
| `/world` | Scale: 11 continents, biomes, monsters | Explore | `open world text rpg`, continent names |
| `/blog` + `/blog/:slug` | **The SEO engine.** Dev logs, guides, patch notes | Register | long-tail guides, `erchis <topic>` |
| `/leaderboard` | Social proof; live and changing | Register | `erchis leaderboard` (brand) |
| `/changelog` | Signals an actively developed game | — | brand + `updates` |
| `/about` | Trust, the solo-dev story | — | brand |
| `/login`, `/register` | Convert | — | `noindex` |

Two additions worth making:

- **`/mastery/:id`** — 11 pages, one per mastery (Knight, Mage, Alchemist…). Each
  is a genuine long-tail landing page with content you already have in
  `MASTERY_PLANS.md`. This is the single highest-leverage SEO addition: 11 real
  pages from existing material.
- **`/continent/:id`** — same argument, 11 more pages from world data.

---

## 4. Design system

### 4.1 Type scale

One scale, used everywhere. Currently sizes are ad-hoc per component.

| Role | Desktop / mobile | Font | Case |
|---|---|---|---|
| Hero | 96 / 48 | VT323 | as written |
| Section title | 48 / 32 | VT323 | UPPER |
| Card title | 24 / 20 | VT323 | UPPER |
| Eyebrow, label | 13 | JetBrains Mono | UPPER, +0.15em |
| Body | 19 / 17 | Crimson Text | sentence |
| Pull-quote | 24 / 20 | Crimson Text italic | sentence |
| Caption, meta | 14 | JetBrains Mono | sentence |

Roughly 1.5x between steps — wide enough that hierarchy is obvious at a glance.

**Font role change:** demote JetBrains Mono from body copy to labels only.
Monospace prose reads as a terminal, not a game. Promote Crimson Text to body.

**Uppercase:** currently **18 of 38** headings and controls are uppercase, with
extra letter-spacing, in a pixel font — close to unreadable at small sizes. Keep
uppercase for labels and eyebrows; drop it above roughly four words.

### 4.2 Spacing and layout

- Section rhythm: `128px` desktop / `72px` mobile between sections; `24px` grid gap
- Measure: cap body text at `68ch` (currently 672px at 24px, about 55 chars — right)
- **Reduce visible boxes.** Every card currently has a 1px border, which reads as a
  wireframe. Keep `border-radius: 0`; group with whitespace and let borders mark
  only genuinely interactive surfaces.

### 4.3 Component inventory to build

`SiteNav` · `SiteFooter` · `Hero` · `SectionHeader` · `FeatureCard` ·
`RaceCard` · `ContinentCard` · `StatStrip` · `PullQuote` · `CTABand` ·
`PostCard` · `Prose` (blog body) · `Seo` (per-page meta)

Twelve components covers every page. Today each page hand-rolls its own markup,
which is why they all drift.

### 4.4 Art direction — the "nothing to look at" problem

**Measured:** 0 `<img>`, 0 background images, 11 lucide icons, 4,428px of text.
A dark-fantasy RPG page with no art cannot look good however well the type is set.

Cheapest paths, no artist required:

1. **Animated d6 hero.** Inline SVG die that settles on load. Your central
   mechanic and natural logo, in code rather than paint.
2. **Use the sprite system you already have.** `PixelSprite` and `.sprite-slot`
   exist for the game UI and appear on **zero** public pages, while 8 race cards
   and 11 continents sit empty.
3. **Texture over flat fill.** `index.css` already defines an amber scanline
   gradient used in one place. As a section background with a vignette it reads as
   art direction rather than an empty div.
4. **Typographic art.** At 96px, VT323 over a hairline amber rule *is* a visual.

Commissioned key art only after the above.

---

## 5. Page specs

**`/` Home** — Hero (d6 + 96px headline + two CTAs) → StatStrip (live: players,
kills, continents — pulled from `/leaderboard`, proves the game is real) → three
FeatureCards, not six → Race strip with sprites → live ladder top 5 → CTABand.
Cut the page from 4,428px to about 2,800px by removing repetition, not content.

**`/mechanics`** — The d6 explained with an actual rolled-outcome table; the
weighted-dice diagram; masteries grid linking to the 11 new mastery pages.

**`/races`** — 8 cards with sprites, perk, and a "plays like" line. Links to
mastery pages.

**`/world`** — 11 continents, each with biome count and signature monster.
Full-bleed alternating rows rather than a uniform grid.

**`/blog`** — PostCard list, tag filter, real dates. Currently empty; §6.4 covers
what to write.

**`/leaderboard`** — the only genuinely live page. Give it prominence; it is the
strongest proof of a real game.

---

## 6. SEO plan

### 6.1 Technical foundation

| Item | Status | Action |
|---|---|---|
| Per-page `<title>` | **none** | `Seo` component per route. Pattern: `{Page} — Erchis` / home: `Erchis — A Fantasy Dice RPG` |
| Meta description | boilerplate | Unique, 150-160 chars, per page |
| `og:` / `twitter:` | **none** | `og:title/description/image/url/type`, `twitter:card=summary_large_image` |
| Social image | **none** | 1200x630 per page type. The 96px VT323 headline on near-black renders beautifully at that size — generate them from the type system |
| Favicon | **none** | Full set incl. `apple-touch-icon`, `theme-color: #0C0A09` |
| `robots.txt` | **none** | Allow all; `Disallow: /game`, `/create`, `/login`, `/register`; point to sitemap |
| `sitemap.xml` | **none** | Generate at build: static routes + blog slugs + 11 masteries + 11 continents |
| Canonical URLs | **none** | Self-referencing canonical on every page |
| `noindex` | — | On `/login`, `/register`, `/auth`, `/game`, `/create` |
| Structured data | **none** | `VideoGame` on `/`, `Article` on posts, `BreadcrumbList` on nested, `Organization` in footer |
| `lang` attribute | check | `<html lang="en">` |

### 6.2 Crawlability

Everything above is worthless while the HTML ships empty — resolve §2 first.
`VideoGame` JSON-LD on a client-rendered page is invisible.

Order: **§2 decision → server-rendered HTML → metadata → sitemap → content.**

### 6.3 Performance (Core Web Vitals are a ranking input)

- **Three Google font families** (VT323, JetBrains Mono, Crimson Text with 5
  weights) load via a single render-blocking `@import` in CSS — the worst possible
  form. Move to `<link rel="preconnect">` + `preload`, subset to the weights
  actually used, and add `font-display: swap`.
- `@import` in CSS serialises the request chain: CSS must download before the font
  request even starts. This is likely the largest LCP contributor.
- Measure LCP/CLS/INP before and after. A pixel font swapping in late causes
  visible CLS on a 96px headline — reserve space with `size-adjust`.

### 6.4 Content strategy — the actual SEO engine

The blog is built and **empty**. Technical SEO makes a site indexable; content is
what ranks. Three streams, all from material you already have:

1. **Dev logs** — you have a genuinely interesting build story (the bug hunts in
   this repo alone). Ranks on brand + attracts the indie-game audience.
2. **Guides** — one per mastery (11), one per continent (11), plus systems
   (crafting, resolve, professions). This is the long-tail volume, and
   `MASTERY_PLANS.md` is most of the first draft already.
3. **Patch notes** — `/changelog` already exists. Consistent, dated updates signal
   an actively maintained game to both players and crawlers.

Realistic cadence for a solo dev: one post a week. Twelve posts plus 22 generated
mastery/continent pages is a real content footprint within a quarter.

### 6.5 Measurement

Search Console + sitemap submission on day one of Phase 2. Track: indexed page
count, impressions per query cluster, and registration conversion by landing page.
Without the last one you cannot tell which content actually recruits players.

---

## 7. Build order

### Phase 0 — corrections  **[COMPLETE]**

1. **Typography override removed** — hierarchy restored on all 8 public pages
2. **Identity** — `<title>Erchis — A Fantasy Dice RPG</title>`, real meta
   description, canonical, full Open Graph + Twitter card, `theme-color: #0C0A09`
3. **Assets created** — `favicon.svg` (a d6 showing six, zero-radius to match the
   site), `og-image.png` (1200x630, rendered with the real VT323 face),
   `apple-touch-icon.png`, `robots.txt` (game routes disallowed), `sitemap.xml`
   (8 static routes, valid against the sitemaps.org schema)
4. **Font loading** — the `@import` moved out of `index.css` into a `<link>` in the
   head behind the existing preconnect. An `@import` serialises the chain: the
   stylesheet must download before the font URL is even discovered.
5. **Dropped an unused fourth font** — `Inter:wght@600` loaded on every page and
   referenced nowhere in `src/` or the Tailwind config
6. **Deleted `Landing.jsx`**, and renamed `Home.jsx`'s component from `Landing()`
   to `Home()` — that mismatch is what caused a fix to land in the dead file

Left alone deliberately: `assets.emergent.sh/scripts/emergent-main.js` in the head.
It may be required by the hosting platform, and removing deploy infrastructure on a
guess is not worth the risk. Flagged for you to confirm.

Known remaining noise: a logged-out visitor triggers one `401` on `/api/auth/me`
per page as the session check runs. Functionally correct, cosmetically noisy;
silence it when the auth-state work lands in Phase 2.

### Phase 1 — design system  **[COMPLETE]**

- Type scale as Tailwind `fontSize` tokens, using `clamp()` so one class is
  responsive. This also removes the `text-5xl md:text-7xl lg:text-8xl` pile-up that
  let a single stray override flatten 149 headings unnoticed.
- Font roles separated: VT323 display, Crimson Text reading copy, JetBrains Mono
  labels. The serif is scoped to `.site-page`, **not** `body` — the game client has
  no opt-out hook, so a global swap would have put a serif in the HUD.
- 13 components in `src/components/site/`: Die, Section, SectionHeader, Button,
  Hero, StatStrip, FeatureCard, RaceCard, ContinentRow, PostCard, PullQuote,
  CTABand, Prose.

### Phase 2 — page rebuild  **[COMPLETE]**

- **Home** rebuilt: asymmetric two-column hero with the rolling d6, live StatStrip,
  three features instead of six, pull-quote band, dense race strip, live ladder,
  one closing CTA. Alternates contained/band so consecutive sections differ
  structurally. 4,890 → 4,521px after making the race strip compact.
- **Mechanics** rebuilt around the actual d6 outcome table — six faces and what each
  means. That table is the most useful thing the page can show and it did not exist.
- **Races** rebuilt: numbered index, then alternating detail rows using the pixel
  sprite slot that already shipped for the game UI and appeared on zero public pages.
- **World** kept its tabbed browser (a genuinely good interactive page) and had its
  hero, tab styling and measure rebuilt. Tabs moved off 14px VT323.
- **Blog, About, Changelog, Leaderboard** normalised onto the type scale.
- **Hotlinked Unsplash photos removed from five pages.** Each was a 2000px external
  JPEG at 15–20% opacity: full download cost, external dependency, no license
  record, and a photograph in a pixel-art game. *This corrects the "zero artwork"
  claim in §3 — it was wrong. JSX uses camelCase `backgroundImage`, so the grep
  missed them.*
- **Per-route metadata**: unique title, description, canonical, OG/Twitter per page;
  `VideoGame` JSON-LD on home; `noindex` on the three auth routes.

Verified in-browser on all eight public pages: h1 96px desktop / 48px mobile, body
Crimson Text, zero headings under 24px, no horizontal overflow at 375px, mobile menu
works, production build passes with no new warnings.

### Phase 3 — server-rendered public site  **[COMPLETE — one decision left for you]**

Option B, built in `web/` (Next.js 15, App Router, SSG). The game client stays a SPA
in `frontend/`. Measured against the same running backend:

| Content | `web/` (SSR) | `frontend/` (CRA) |
|---|---|---|
| Race names and perks | **in HTML** | absent |
| Continent names | **in HTML** | absent |
| Leaderboard | **in HTML** | absent |
| d6 outcome table | **in HTML** | absent |
| Per-route `<title>` | **unique** | same title on all 11 routes |

**30 routes prerendered at build time**, including the 22 generated pages:
`/mastery/[id]` x11 and `/continent/[id]` x11. Both sets are linked from
`/mechanics` and `/world` respectively and listed in the generated sitemap — a
generated page that is unlinked and unannounced is a page nothing crawls.

Also shipped: `Article` JSON-LD per blog post, `VideoGame` JSON-LD on home, generated
`sitemap.xml` (30 URLs, blog slugs included so publishing needs no edit) and
`robots.txt`. Fonts moved to `next/font`, which self-hosts them and removes the
external round trip the old `@import` chain caused.

Theme verified identical at 1272px: h1 96px VT323, body Crimson Text, background
`rgb(12,10,9)`, no overflow. The palette block is **copied verbatim** from
`frontend/src/index.css` rather than retyped, so the two apps cannot drift.

**What still needs you:** there are two apps now and something has to route between
them (`/` → `web/`, `/app` → `frontend/`). Three options with their auth-cookie
implications are documented in `web/README.md`. That depends on your host, so it is
not a call I should make. Until it is wired, `frontend/` deliberately keeps serving
its own copies of the public pages — deleting them first would break the live site.

**Deliberately not ported:**
- World's tabbed browser (continents/biomes/towns/bestiary/materials). That is an app
  feature — six interacting pieces of client state, useful while playing, not what
  should rank. `/world` server-renders the eleven continents as indexable text and
  leaves the browser in the game.
- Blog search and tag filters. Client-side filtering would put the archive back behind
  JavaScript; they should return as real routes (`/blog/tag/[tag]`) so each filter is
  its own indexable page.

### Phase 4 — content (ongoing)
15. One post a week; guides first, dev logs for reach

**Phases 0-2 are about a week** and produce a site that looks deliberate.
Phase 3 is what makes it findable. Phase 4 is what makes it grow.

---

## 8. Risks

- **The Next.js split is the only large-effort item.** If it stalls, Phase 0-2
  still leaves a much better-looking site — just an unfindable one. Do not let
  Phase 3 block Phase 0.
- **Prerendering after publishing content** means re-indexing churn. Decide §2
  before writing posts.
- **Art remains the gap code cannot close.** The four cheap paths in §4.4 get the
  site to "deliberate and clean". "Striking" needs an artist, and that is a
  spending decision, not an engineering one.
- **Three fonts is already the ceiling.** Do not add a fourth for the redo.
