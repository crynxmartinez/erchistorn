import Section from "@/components/site/Section";
import { PostCard } from "@/components/site/Cards";
import { CTABand } from "@/components/site/Bits";
import { getPosts, fmtDate } from "@/lib/api";

/**
 * Blog index — server-rendered.
 *
 * This is the page that most needed moving off the client. The CRA version fetched
 * posts in a `useEffect` with search and tag filters in query params, so the entire
 * content archive — the thing a content-marketing strategy exists to get indexed —
 * was invisible to anything that does not execute JS.
 *
 * Search and tag filtering are deliberately dropped here rather than ported. With
 * zero posts they are premature, and client-side filtering would push the list back
 * behind JavaScript. Reinstate them as real routes (`/blog/tag/[tag]`) when there is
 * enough content to need them — then each filter is its own indexable page.
 */

export const metadata = {
    title: "Dev log",
    description:
        "Devlogs, lore entries and patch notes from the world of Erchis — how a solo-built browser RPG gets made.",
    alternates: { canonical: "/blog" },
};

export default async function BlogPage() {
    const posts = await getPosts(50);

    return (
        <>
            <section className="relative overflow-hidden border-b border-border/60">
                <div
                    aria-hidden="true"
                    className="pointer-events-none absolute inset-0"
                    style={{
                        background:
                            "radial-gradient(ellipse 60% 60% at 30% 30%, rgba(212,175,55,0.08), transparent 65%)",
                    }}
                />
                <div className="relative mx-auto w-full max-w-6xl px-6 py-20 md:py-24">
                    <p className="mb-5 font-mono text-label uppercase text-primary/70">Dispatches</p>
                    <h1 className="font-display text-display uppercase text-foreground">
                        The Erchis <span className="text-primary">dev log</span>
                    </h1>
                    <p className="mt-7 max-w-prose text-lede text-muted-foreground">
                        Devlogs, lore entries and patch notes from the world of Erchis.
                    </p>
                </div>
            </section>

            <Section variant="plain" label="Posts">
                {posts.length === 0 ? (
                    <div className="max-w-prose">
                        <p className="font-display text-subtitle uppercase text-foreground">
                            Nothing published yet
                        </p>
                        <p className="mt-4 text-body text-muted-foreground">
                            The first dispatch is being written. In the meantime, the changelog has
                            every change shipped so far.
                        </p>
                    </div>
                ) : (
                    <div className="grid gap-12 md:grid-cols-2">
                        {posts.map((p) => (
                            <PostCard
                                key={p.slug}
                                slug={p.slug}
                                title={p.title}
                                excerpt={p.excerpt}
                                date={fmtDate(p.published_at || p.created_at)}
                                tag={p.tag}
                            />
                        ))}
                    </div>
                )}
            </Section>

            <CTABand
                title="Read the dice instead."
                lede="The systems make more sense once you have rolled a few."
                primary={{ to: "/mechanics", label: "How the die works" }}
            />
        </>
    );
}
