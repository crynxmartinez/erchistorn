/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: [
        "./app/**/*.{js,jsx}",
        "./components/**/*.{js,jsx}",
    ],
    theme: {
        extend: {
            borderRadius: {
                lg: '0',
                md: '0',
                sm: '0',
            },
            colors: {
                background: 'hsl(var(--background))',
                foreground: 'hsl(var(--foreground))',
                card: {
                    DEFAULT: 'hsl(var(--card))',
                    foreground: 'hsl(var(--card-foreground))',
                },
                popover: {
                    DEFAULT: 'hsl(var(--popover))',
                    foreground: 'hsl(var(--popover-foreground))',
                },
                primary: {
                    DEFAULT: 'hsl(var(--primary))',
                    foreground: 'hsl(var(--primary-foreground))',
                },
                secondary: {
                    DEFAULT: 'hsl(var(--secondary))',
                    foreground: 'hsl(var(--secondary-foreground))',
                },
                muted: {
                    DEFAULT: 'hsl(var(--muted))',
                    foreground: 'hsl(var(--muted-foreground))',
                },
                accent: {
                    DEFAULT: 'hsl(var(--accent))',
                    foreground: 'hsl(var(--accent-foreground))',
                },
                destructive: {
                    DEFAULT: 'hsl(var(--destructive))',
                    foreground: 'hsl(var(--destructive-foreground))',
                },
                border: 'hsl(var(--border))',
                input: 'hsl(var(--input))',
                ring: 'hsl(var(--ring))',
                rarity: {
                    common: 'hsl(var(--rarity-common))',
                    uncommon: 'hsl(var(--rarity-uncommon))',
                    rare: 'hsl(var(--rarity-rare))',
                    epic: 'hsl(var(--rarity-epic))',
                    legendary: 'hsl(var(--rarity-legendary))',
                    mythic: 'hsl(var(--rarity-mythic))',
                },
            },
            fontFamily: {
                // Three roles, not three competing voices.
                //   display -> VT323        headings only
                //   body    -> Crimson Text all reading copy
                //   mono    -> JetBrains    labels, stats, numbers
                display: ['VT323', 'monospace'],
                body: ['"Crimson Text"', 'Georgia', 'serif'],
                mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
                // Kept as aliases so existing game-UI markup keeps working.
                pixel: ['VT323', 'monospace'],
                narr: ['"Crimson Text"', 'Georgia', 'serif'],
            },
            // One type scale for the whole public site. Sizes use clamp() so a
            // single class is responsive -- the previous approach needed
            // `text-5xl md:text-7xl lg:text-8xl` on every heading, and that
            // class pile-up is what let a stray font-size override flatten all
            // 149 of them without anyone noticing.
            fontSize: {
                display: ['clamp(3rem, 9vw, 6rem)', { lineHeight: '0.9', letterSpacing: '0.02em' }],
                title: ['clamp(2rem, 5.5vw, 3rem)', { lineHeight: '1.0', letterSpacing: '0.04em' }],
                subtitle: ['clamp(1.5rem, 3.5vw, 2.25rem)', { lineHeight: '1.1', letterSpacing: '0.03em' }],
                card: ['1.5rem', { lineHeight: '1.15', letterSpacing: '0.04em' }],
                lede: ['clamp(1.125rem, 2vw, 1.375rem)', { lineHeight: '1.6' }],
                body: ['1.1875rem', { lineHeight: '1.7' }],
                'body-sm': ['1.0625rem', { lineHeight: '1.65' }],
                quote: ['clamp(1.25rem, 2.5vw, 1.625rem)', { lineHeight: '1.55' }],
                label: ['0.8125rem', { lineHeight: '1.2', letterSpacing: '0.15em' }],
                caption: ['0.875rem', { lineHeight: '1.5' }],
                stat: ['clamp(2rem, 4vw, 2.75rem)', { lineHeight: '1' }],
            },
            spacing: {
                // Section rhythm: 128px desktop / 72px mobile.
                section: '8rem',
                'section-sm': '4.5rem',
            },
            maxWidth: {
                prose: '68ch',
            },
            keyframes: {
                'fade-in': {
                    from: { opacity: '0', transform: 'translateY(4px)' },
                    to: { opacity: '1', transform: 'translateY(0)' },
                },
                // The hero die's single roll: a short tumble that settles.
                'die-tumble': {
                    '0%':   { transform: 'rotate(-14deg) scale(0.92)' },
                    '35%':  { transform: 'rotate(10deg) scale(1.04)' },
                    '65%':  { transform: 'rotate(-6deg) scale(0.98)' },
                    '100%': { transform: 'rotate(0deg) scale(1)' },
                },
                'flash': {
                    '0%': { opacity: '1' },
                    '50%': { opacity: '0.2' },
                    '100%': { opacity: '1' },
                },
            },
            animation: {
                'fade-in': 'fade-in 0.4s ease-out',
                'flash': 'flash 0.5s steps(2, end)',
                'die-tumble': 'die-tumble 1.1s cubic-bezier(0.2, 0.8, 0.2, 1) 1',
            },
        },
    },
    plugins: [],
};
