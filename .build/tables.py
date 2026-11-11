import pdfplumber, json, re
pdf = pdfplumber.open('/tmp/claude-0/cmt/a.pdf')
T = []
for i, p in enumerate(pdf.pages):
    for t in sorted(p.find_tables(), key=lambda t: t.bbox[1]):
        rows = t.extract()
        if rows and max(len(r) for r in rows) >= 2: T.append([[re.sub(r"\s*\n\s*", " ", c or "").strip() for c in r] for r in rows])
B = json.load(open('/tmp/claude-0/cmt/book_clean.json'))
k = 0; fixed = 0; dropped = 0
norm = lambda s: re.sub(r"\s", "", s)[:4]
for s in B:
    out = []
    for b in s["blocks"]:
        if b["t"] == "table":
            hit = next((j for j in range(k, min(k + 3, len(T))) if norm(T[j][0][0]) == norm(b["rows"][0][0])), None)
            if hit is not None: b["rows"] = T[hit]; k = hit + 1; fixed += 1; out.append(b)
            else: out.append({"t": "p", "x": " ".join(" ".join(r) for r in b["rows"])}); dropped += 1
        else: out.append(b)
    s["blocks"] = out
json.dump(B, open('/tmp/claude-0/cmt/book_final.json', 'w'), ensure_ascii=False)
print("tables", fixed, "as text", dropped, "unused", len(T) - k)
