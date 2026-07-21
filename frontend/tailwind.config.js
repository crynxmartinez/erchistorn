/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
        "./public/index.html",
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
                pixel: ['VT323', 'monospace'],
                mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
                narr: ['"Crimson Text"', 'Georgia', 'serif'],
            },
            keyframes: {
                'fade-in': {
                    from: { opacity: '0', transform: 'translateY(4px)' },
                    to: { opacity: '1', transform: 'translateY(0)' },
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
            },
        },
    },
    plugins: [require("tailwindcss-animate")],
};
