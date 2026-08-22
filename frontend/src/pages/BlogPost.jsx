import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import { ArrowLeft, Newspaper, Calendar, User } from "lucide-react";

function fmtDate(s) {
    if (!s) return "";
    return new Date(s).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
}

function renderMarkdown(body) {
    if (!body) return null;
    const lines = body.split("\n");
    const elements = [];
    let inList = false;
    let listItems = [];

    const flushList = () => {
        if (listItems.length) {
            elements.push(<ul key={`ul-${elements.length}`} className="list-disc pl-6 space-y-1 my-3">{listItems}</ul>);
            listItems = [];
            inList = false;
        }
    };

    lines.forEach((line, i) => {
        if (line.startsWith("### ")) {
            flushList();
            elements.push(<h3 key={i} className="font-display text-card uppercase text-primary mt-8 mb-3">{line.slice(4)}</h3>);
        } else if (line.startsWith("## ")) {
            flushList();
            elements.push(<h2 key={i} className="font-display text-card uppercase text-primary mt-10 mb-4">{line.slice(3)}</h2>);
        } else if (line.startsWith("# ")) {
            flushList();
            elements.push(<h1 key={i} className="font-display text-subtitle uppercase text-primary mt-10 mb-5">{line.slice(2)}</h1>);
        } else if (line.startsWith("- ") || line.startsWith("* ")) {
            inList = true;
            listItems.push(<li key={i} className="text-base text-foreground/85">{line.slice(2)}</li>);
        } else if (line.startsWith("> ")) {
            flushList();
            elements.push(<blockquote key={i} className="border-l-2 border-primary pl-5 italic text-muted-foreground my-4 text-base">{line.slice(2)}</blockquote>);
        } else if (line.trim() === "") {
            flushList();
        } else {
            flushList();
            elements.push(<p key={i} className="text-base text-foreground/85 leading-relaxed my-3">{line}</p>);
        }
    });
    flushList();
    return elements;
}

export default function BlogPost() {
    const { slug } = useParams();
    const [post, setPost] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        api.get(`/blog/${slug}`)
            .then(r => setPost(r.data.post))
            .catch(e => setError(extractError(e)))
            .finally(() => setLoading(false));
    }, [slug]);

    return (
        <SiteLayout>
            <div className="max-w-4xl mx-auto px-4 md:px-8 py-16">
                <Link to="/blog" className="stat-label text-primary/70 hover:text-primary flex items-center gap-1 mb-8">
                    <ArrowLeft size={12} /> Back to Blog
                </Link>

                {loading && <div className="stat-label text-muted-foreground py-20 text-center">Reading the page…</div>}
                {error && <div className="stat-label text-destructive py-20 text-center">{error}</div>}

                {post && (
                    <>
                        {/* Hero image */}
                        {post.hero_image && (
                            <div className="mb-8 h-72 md:h-96 overflow-hidden border-2 border-border">
                                <img src={post.hero_image} alt={post.title} className="w-full h-full object-cover" />
                            </div>
                        )}

                        {/* Meta */}
                        <div className="stat-label text-primary/70 mb-2">{post.category}</div>
                        <h1 className="font-display text-subtitle md:text-4xl uppercase text-primary tracking-wider mb-4 leading-tight">
                            {post.title}
                        </h1>
                        <div className="flex items-center gap-4 stat-label text-muted-foreground mb-8 flex-wrap">
                            <span className="flex items-center gap-1"><User size={12} /> {post.author_name}</span>
                            <span className="flex items-center gap-1"><Calendar size={12} /> {fmtDate(post.published_at)}</span>
                        </div>

                        {/* Tags */}
                        {post.tags?.length > 0 && (
                            <div className="flex gap-2 mb-8 flex-wrap">
                                {post.tags.map(t => (
                                    <span key={t} className="stat-label px-2 py-0.5 border border-border text-muted-foreground">#{t}</span>
                                ))}
                            </div>
                        )}

                        {/* Body */}
                        <article className="prose prose-sm max-w-none">
                            {renderMarkdown(post.body)}
                        </article>

                        {/* Share / back */}
                        <div className="mt-12 pt-6 border-t border-border flex items-center justify-between">
                            <Link to="/blog" className="stat-label text-primary hover:underline flex items-center gap-1">
                                <ArrowLeft size={12} /> All posts
                            </Link>
                            <div className="flex gap-2">
                                <a
                                    href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(window.location.href)}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="press-btn stat-label px-3 py-1.5 border border-border text-muted-foreground hover:text-primary hover:border-primary"
                                >
                                    Share on X
                                </a>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </SiteLayout>
    );
}
