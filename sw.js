// 오프라인에서도 열리게: 앱 파일을 저장해 두고, 인터넷이 되면 새 버전으로 바꿔요
const VERSION = "cmt-study-7";
const FILES = ["./", "index.html", "data.js", "guide.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET" || new URL(r.url).origin !== location.origin) return;
  e.respondWith(fetch(r, { cache: "no-cache" }).then(res => { const c = res.clone(); caches.open(VERSION).then(x => x.put(r, c)); return res; }).catch(() => caches.match(r, { ignoreSearch: true }).then(m => m || caches.match("index.html"))));
});
