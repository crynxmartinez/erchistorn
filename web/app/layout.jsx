import { VT323, Crimson_Text, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import SiteChrome from "@/components/site/SiteChrome";

/**
 * Root layout.
 *
 * Fonts come through `next/font`, which self-hosts them at build time. That removes
 * the render-blocking round trip to fonts.googleapis.com entirely — the CRA site
 * loaded three families via an `@import` inside CSS, which serialises the chain
 * (the stylesheet has to download before the font URL is even discovered) and was
 * the largest single contributor to LCP.
 *
 * `display: "swap"` plus `adjustFontFallback` also stops the 96px VT323 headline
 * from causing a visible layout shift when it swaps in.
 */

const display = VT323({
    weight: "400",
    subsets: ["latin"],
    variable: "--font-display",
    display: "swap",
});

const body = Crimson_Text({
    weight: ["400", "700"],
    style: ["normal", "italic"],
    subsets: ["latin"],
    variable: "--font-body",
    display: "swap",
});

const mono = JetBrains_Mono({
    weight: ["400", "700"],
    subsets: ["latin"],
    variable: "--font-mono",
    display: "swap",
});

const ORIGIN = process.env.NEXT_PUBLIC_SITE_ORIGIN || "https://erchis.online";

/**
 * Defaults every page inherits. Pages override title/description/canonical via
 * their own `generateMetadata`; because this runs on the server, the values land in
 * the HTML that link unfurlers actually read — which the client-side version could
 * never fix.
 */
export const metadata = {
    metadataBase: new URL(ORIGIN),
    title: {
        default: "Erchis — A Fantasy Dice RPG",
        template: "%s — Erchis",
    },
    description:
        "A free browser-based fantasy RPG decided by a single weighted six-sided die. " +
        "Eight races, eleven continents, eleven masteries. No energy caps — play at your own pace.",
    applicationName: "Erchis",
    alternates: { canonical: "/" },
    openGraph: {
        type: "website",
        siteName: "Erchis",
        url: "/",
        title: "Erchis — A Fantasy Dice RPG",
        description:
            "Eight races. Eleven continents. One six-sided die that will decide whether you become legend — or footnote.",
        images: [
            {
                url: "/og-image.png",
                width: 1200,
                height: 630,
                alt: "Erchis — a six-sided die on black, amber pips showing six.",
            },
        ],
    },
    twitter: {
        card: "summary_large_image",
        title: "Erchis — A Fantasy Dice RPG",
        description:
            "Eight races. Eleven continents. One six-sided die that will decide whether you become legend — or footnote.",
        images: ["/og-image.png"],
    },
    icons: {
        icon: [{ url: "/favicon.svg", type: "image/svg+xml" }],
        apple: [{ url: "/apple-touch-icon.png" }],
    },
};

export const viewport = {
    themeColor: "#0C0A09",
};

export default function RootLayout({ children }) {
    return (
        <html
            lang="en"
            className={`${display.variable} ${body.variable} ${mono.variable}`}
        >
            <body className="site-page flex min-h-screen flex-col bg-background">
                <SiteChrome>{children}</SiteChrome>
            </body>
        </html>
    );
}
