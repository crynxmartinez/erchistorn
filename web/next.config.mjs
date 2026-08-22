/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    // The FastAPI backend. Proxied through /api so the browser stays same-origin
    // (no CORS preflight, and cookies keep working the way the game client
    // already expects).
    async rewrites() {
        const backend = process.env.BACKEND_ORIGIN || "http://127.0.0.1:8000";
        return [{ source: "/api/:path*", destination: `${backend}/api/:path*` }];
    },
};
export default nextConfig;
