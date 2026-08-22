"use client";

import Link from "next/link";

/**
 * The site's two button treatments, in one place.
 *
 * Previously every CTA hand-rolled its own eight Tailwind classes, so hover
 * behaviour and padding drifted between pages. Zero border radius is inherited
 * from the global reset — do not add one here.
 */
const VARIANTS = {
    primary:
        "bg-primary text-primary-foreground border-2 border-primary " +
        "hover:bg-transparent hover:text-primary",
    ghost:
        "bg-transparent text-primary border-2 border-primary " +
        "hover:bg-primary hover:text-primary-foreground",
};

const SIZES = {
    lg: "px-8 py-3.5 text-card",
    md: "px-6 py-2.5 text-[1.125rem]",
};

export default function Button({
    to,
    href,
    variant = "primary",
    size = "lg",
    className = "",
    children,
    ...rest
}) {
    const cls =
        `inline-flex items-center justify-center gap-2 font-display uppercase ` +
        `tracking-wide transition-colors duration-150 ${VARIANTS[variant]} ${SIZES[size]} ${className}`;

    if (to) {
        return (
            <Link href={to} className={cls} {...rest}>
                {children}
            </Link>
        );
    }
    if (href) {
        return (
            <a href={href} className={cls} {...rest}>
                {children}
            </a>
        );
    }
    return (
        <button type="button" className={cls} {...rest}>
            {children}
        </button>
    );
}
