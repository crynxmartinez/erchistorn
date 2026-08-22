import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import { Newspaper, Search, ArrowLeft, ArrowRight } from "lucide-react";

const CATEGORIES = ["All", "Devlog", "Lore", "Patch Notes", "Community", "Guides"];

function fmtDate(s) {
    if (!s) return "";
    return new Date(s).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export default function Blog() {
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(1);
    const [pages, setPages] = useState(1);
    const [category, setCategory] = useState("All");
    const [search, setSearch] = useState("");
    const [loading, setLoading] = useState(true);
    const [total, setTotal] = useState(0);

    const load = useCallback(async () => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (category !== "All") params.set("category", category);
            params.set("page", page);
            params.set("limit", 9);
            const { data } = await api.get(`/blog?${params}`);
            setPosts(data.posts);
            setPages(data.pages);
            setTotal(data.total);
        } catch {
            setPosts([]);
        } finally {
            setLoading(false);
        }
    }, [category, page]);

    useEffect(() => { load(); }, [load]);

    const filtered = search
        ? posts.filter(p => p.title.toLowerCase().includes(search.toLowerCase()) || (p.excerpt || "").toLowerCase().includes(search.toLowerCase()))
        : posts;

    return (
        <SiteLayout>
            <div className="max-w-6xl mx-auto px-4 md:px-8 py-16">
                {/* Header */}
                <div className="mb-10">
                    <div className="stat-label text-primary/70 mb-2 flex items-center gap-2">
                        <Newspaper size={14} /> CHRONICLES
                    </div>
                    <h1 className="font-pixel text-4xl md:text-5xl uppercase text-primary tracking-wider mb-3">The Erchis Blog</h1>
                    <p className="narr text-lg text-muted-foreground max-w-2xl">
                        Devlogs, lore entries, patch notes, and community stories from the world of Erchis.
                    </p>
                </div>

                {/* Filters */}
                <div className="flex flex-wrap gap-3 items-center mb-8">
                    <div className="flex gap-1 flex-wrap">
                        {CATEGORIES.map(c => (
                            <button
                                key={c}
                                onClick={() => { setCategory(c); setPage(1); }}
                                className={`press-btn stat-label px-3 py-1.5 border transition-colors ${
                                    category === c
                                        ? "border-primary bg-primary text-primary-foreground"
                                        : "border-border text-muted-foreground hover:text-primary hover:border-primary"
                                }`}
                            >
                                {c}
                            </button>
                        ))}
                    </div>
                    <div className="relative flex-1 min-w-[200px]">
                        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                        <input
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="w-full bg-background border border-border pl-10 pr-4 py-3 font-mono text-base"
                            placeholder="Search posts…"
                        />
                    </div>
                </div>

                {/* Posts */}
                {loading ? (
                    <div className="stat-label text-muted-foreground py-20 text-center">Unfurling the pages…</div>
                ) : filtered.length === 0 ? (
                    <div className="stat-label text-muted-foreground py-20 text-center">
                        {total === 0 ? "No posts yet. Check back soon." : "No posts match your search."}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filtered.map((p) => (
                            <Link
                                key={p.slug}
                                to={`/blog/${p.slug}`}
                                className="panel p-8 hover:border-primary transition-colors block flex flex-col"
                            >
                                {p.hero_image ? (
                                    <div className="mb-5 -mx-8 -mt-8 h-48 overflow-hidden border-b border-border">
                                        <img src={p.hero_image} alt={p.title} className="w-full h-full object-cover" />
                                    </div>
                                ) : (
                                    <div className="mb-5 -mx-8 -mt-8 h-48 border-b border-border bg-primary/5 flex items-center justify-center">
                                        <Newspaper size={40} className="text-primary/30" />
                                    </div>
                                )}
                                <div className="stat-label text-primary/70 mb-2">{p.category}</div>
                                <div className="font-pixel text-lg uppercase text-primary mb-3 leading-tight">{p.title}</div>
                                <div className="text-base text-muted-foreground line-clamp-3 flex-1">{p.excerpt}</div>
                                <div className="stat-label text-muted-foreground/60 mt-5 flex items-center justify-between">
                                    <span>{p.author_name}</span>
                                    <span>{fmtDate(p.published_at)}</span>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}

                {/* Pagination */}
                {pages > 1 && (
                    <div className="flex items-center justify-center gap-2 mt-10">
                        <button
                            onClick={() => setPage(Math.max(1, page - 1))}
                            disabled={page === 1}
                            className="press-btn stat-label px-3 py-1.5 border border-border text-muted-foreground hover:text-primary disabled:opacity-40 flex items-center gap-1"
                        >
                            <ArrowLeft size={12} /> Prev
                        </button>
                        <span className="stat-label text-muted-foreground">Page {page} of {pages}</span>
                        <button
                            onClick={() => setPage(Math.min(pages, page + 1))}
                            disabled={page === pages}
                            className="press-btn stat-label px-3 py-1.5 border border-border text-muted-foreground hover:text-primary disabled:opacity-40 flex items-center gap-1"
                        >
                            Next <ArrowRight size={12} />
                        </button>
                    </div>
                )}
            </div>
        </SiteLayout>
    );
}
