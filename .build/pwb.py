import re, json, sys
sys.path.insert(0, "/tmp/claude-0/cmt/build")
src = open("/tmp/claude-0/cmt/b.txt", encoding="utf-8").read()
VOC = set()
for ln in open("/tmp/claude-0/cmt/build/vocab.txt", encoding="utf-8"): VOC.add(ln.split("\t")[0])
def KJ(a, b):
    if not a: return b
    A, B = a.split()[-1], b.split()[0]
    h = lambda c: "가" <= c <= "힣"
    if h(A[-1]) and h(B[0]) and (B.startswith(("다", "니다", "이다")) or len(B) == 1 or (A + B) in VOC): return a + b
    return a + " " + b
Q = {}; wk = None; mode = "q"; cur = None; q = None
for pg in src.split("\f")[2:]:
    for raw in pg.split("\n"):
        st = raw.strip(); ind = len(raw) - len(raw.lstrip())
        if not st or st.startswith("CMT Level I 문제집") or re.fullmatch(r"-\s*\d+\s*-", st): continue
        if st.startswith("제2부"): mode = "a"; continue
        m = re.match(r"제(\d+)주차 (.+?)( 정답 및 해설)?$", st)
        if m and ind <= 2: wk = int(m.group(1)); cur = None; continue
        if wk is None: continue
        if mode == "q":
            m = re.match(r"(\d+)\. (.+)", st)
            if m and ind <= 2: q = Q.setdefault((wk, int(m.group(1))), {"q": m.group(2), "o": []}); cur = "q"; continue
            m = re.match(r"([A-D])\) (.*)", st)
            if m and q is not None: q["o"].append(m.group(2)); cur = "o"; continue
            if q is None: continue
            if cur == "q": q["q"] = KJ(q["q"], st)
            elif cur == "o": q["o"][-1] = KJ(q["o"][-1], st)
        else:
            if re.fullmatch(r"[\d\s]+", st) or re.fullmatch(r"[A-D\s]+", st): continue
            m = re.match(r"(\d+)\. 정답 ([A-D])\s*(.*)", st)
            if m: q = Q.setdefault((wk, int(m.group(1))), {"q": "", "o": []}); q["a"] = "ABCD".index(m.group(2)); q["e"] = m.group(3); cur = "e"; continue
            if cur == "e" and q is not None: q["e"] = KJ(q["e"], st)
out = [{"id": f"w{w:02d}-{n:02d}", "w": w, "n": n, "q": v["q"], "o": v["o"], "a": v.get("a"), "e": v.get("e", "")} for (w, n), v in sorted(Q.items())]
bad = [o["id"] for o in out if len(o["o"]) != 4 or o["a"] is None or not o["q"] or not o["e"]]
print(len(out), "bad", bad[:20])
json.dump(out, open("/tmp/claude-0/cmt/w.json", "w", encoding="utf-8"), ensure_ascii=False)
