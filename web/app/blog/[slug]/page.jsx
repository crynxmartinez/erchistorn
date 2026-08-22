import { notFound } from "next/navigation";
import Link from "next/link";
import Section from "@/components/site/Section";
import { Prose, CTABand } from "@/components/site/Bits";
import { getPost, getPosts, fmtDate } from "@/lib/api";

/**
 * A single post.
 *
 * Two things this gets that the CRA version could not:
 *
 *  - **Per-post metadata in the HTML.** Every post previously inherited the one
 *    site-wide title, so sharing a post to Discord showed the generic card and a
 *    search result could not distinguish two articles.
 *  - **`Article` JSON-LD**, which only counts if it is server-rendered.
 *
 * `generateStaticParams` prerenders every known slug at build time; anything
 * published later is rendered on first request and then cached (`revalidate` in
 * lib/api), so publishing does not require a rebuild.
 */

export async function generateStaticParams() {
    const posts = await getPosts(200);
    return posts.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }) {
    const { slug } = await params;
    const data = await getPost(slug);
    const post = data?.post || data;
    if (!post?.title) {
        return { title: "Post not found", robots: { index: false } };
    }
    const description = post.excerpt || post.summary || undefined;
    return {
        title: post.title,
        description,
        alternates: { canonical: `/blog/${slug}` },
        openGraph: {
            type: "article",
            title: post.title,
            description,
            url: `/blog/${slug}`,
            publishedTime: post.published_at || post.created_at || undefined,
        },
        twitter: { card: "summary_large_image", title: post.title, description },
    };
}

export default async function BlogPostPage({ params }) {
    const { slug } = await params;
    const data = await getPost(slug);
    const post = data?.post || data;
    if (!post?.title) notFound();

    const published = post.published_at || post.created_at;
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Article",
        headline: post.title,
        description: post.excerpt || undefined,
        datePublished: published || undefined,
        author: { "@type": "Organization", name: "Erchis" },
        publisher: { "@type": "Organization", name: "Erchis" },
        mainEntityOfPage: `https://erchis.online/blog/${slug}`,
    };

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
            />

            <article>
                <header className="border-b border-border/60">
                    <div className="mx-auto w-full max-w-3xl px-6 py-16 md:py-20">
                        <Link
                            href="/blog"
                            className="font-mono text-label uppercase text-muted-foreground hover:text-primary"
                        >
                            ← All posts
                        </Link>
                        <p className="mt-8 font-mono text-label uppercase text-primary/70">
                            {fmtDate(published)}
                            {post.tag ? ` · ${post.tag}` : ""}
                        </p>
                        <h1 className="mt-3 font-display text-title uppercase text-foreground">
                            {post.title}
                        </h1>
                        {post.excerpt && (
                            <p className="mt-6 text-lede text-muted-foreground">{post.excerpt}</p>
                        )}
                    </div>
                </header>

                <Section variant="inset" label="Article">
                    {post.body_html ? (
                        <Prose>
                            <div dangerouslySetInnerHTML={{ __html: post.body_html }} />
                        </Prose>
                    ) : (
                        <Prose>
                            {/* Plain-text bodies: split on blank lines so paragraphs survive. */}
                            {String(post.body || post.content || "")
                                .split(/\n{2,}/)
                                .filter(Boolean)
                                .map((para, i) => (
                                    <p key={i}>{para}</p>
                                ))}
                        </Prose>
                    )}
                </Section>
            </article>

            <CTABand
                title="Roll for yourself."
                primary={{ to: "/mechanics", label: "How the die works" }}
                secondary={{ to: "/blog", label: "More dispatches" }}
            />
        </>
    );
}
