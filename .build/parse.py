import re, json, sys
src = open(sys.argv[1], encoding="utf-8").read()
pages = src.split("\f")
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮"
BOX = ["시험 포인트", "쉬운 예", "실전 사례", "문제 연습", "이번 주 학습목표", "주차 핵심 요약", "풀이"]
secs = []; cur = None; last = None; table = None
def add(b):
    global last, table
    if b["t"] != "table": table = None
    cur["blocks"].append(b); last = b
import re as _re
_st=lambda w:_re.sub(r'[^0-9A-Za-z가-힣]','',w)
VOC=set(_st(l.split("\t")[0]) for l in open("/tmp/claude-0/cmt/build/vocab.txt",encoding="utf-8"))
LOG=[]
END="게고며면서는은을를의에와과로도만나이가요지해며"
def join(a, b):
    if not a: return b
    if a.endswith(('"', "(", "“", "'", "·", "/", "-", "~")): return a + b
    A=a.split()[-1]; B=b.split()[0]
    hang=lambda c: "가"<=c<="힣"
    if hang(A[-1]) and hang(B[0]):
        sA,sB=_st(A),_st(B)
        if sA+sB in VOC or _st(A+B.split('"')[0]) in VOC: sp=False
        elif B.startswith(("입니다","이다","니다","다.","다,","습니다","습니까")): sp=False
        elif len(sB)==1 and sB in "지다요고게며서도에를은는이가의로": sp=False
        elif len(sA)>=3 and sA[-1] in END: sp=True
        elif len(sA)>=2 and sA in VOC and len(sB)>=3: sp=True
        elif sA in VOC and sB in VOC: sp=True
        elif sB not in VOC: sp=False
        else: sp=True
        LOG.append((A,B,sp))
        if not sp: return a+b
    return a + " " + b
for pi, pg in enumerate(pages):
    if pi < 4: continue
    lines = pg.split("\n")
    for raw in lines:
        if not raw.strip(): 
            if last and last["t"] in ("box",): last = {"t": "_gap"}
            continue
        s = raw.rstrip(); st = s.strip()
        if st.startswith("CMT Level I 기본 정리서"): continue
        if re.fullmatch(r"\d+", st): continue
        ind = len(s) - len(s.lstrip(" "))
        m = re.fullmatch(r"제(\d+)주차 (.+)", st)
        if m and ind < 8 and (not cur or int(m.group(1)) == cur["n"] + 1):
            cur = {"n": int(m.group(1)), "title": m.group(2).strip(), "blocks": []}; secs.append(cur); last = None; table = None; continue
        if cur is None: continue
        m = re.match(r"([ⅠⅡⅢⅣⅤⅥⅦⅧ])\. (.+)", st)
        if m and ind == 0: add({"t": "h2", "x": st}); continue
        m = re.match(r"(\d+)\. (.+)", st)
        if m and ind in (1, 2) : add({"t": "h3", "x": st}); continue
        m = re.match(r"\((\d+)\) (.+)", st)
        if m and 2 <= ind <= 4: add({"t": "h4", "x": st}); continue
        if st[0] in CIRC and 2 <= ind <= 5: add({"t": "li", "x": st}); continue
        bx = next((k for k in BOX if st.startswith(k + " ")), None)
        if bx and 3 <= ind <= 7:
            add({"t": "box", "k": bx, "x": st[len(bx) + 1:].strip()}); continue
        cells = re.split(r"\s{3,}", st)
        if len(cells) >= 2 and not (last and last["t"] in ("li", "box") and ind >= 4 and ind <= 6 and len(cells) < 2):
            if last and last["t"] == "li" and ind == 5 and len(cells) < 3:
                pass
            else:
                if table is None or last is not table:
                    table = {"t": "table", "rows": []}; cur["blocks"].append(table); last = table
                table["rows"].append(cells); continue
        if last and last["t"] in ("li", "box", "h4", "p"):
            last["x"] = join(last["x"], st); continue
        if last and last["t"] == "table" and last["rows"]:
            last["rows"][-1][-1] = join(last["rows"][-1][-1], st); continue
        add({"t": "p", "x": st})
for s in secs:
    s["blocks"] = [b for b in s["blocks"] if b["t"] != "_gap"]
import random;random.seed(3);open(sys.argv[2]+".log","w").write("\n".join(f"{x}|{y}|{z}" for x,y,z in LOG))
json.dump(secs, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for s in secs:
    c = {}
    for b in s["blocks"]: c[b["t"]] = c.get(b["t"], 0) + 1
    print(s["n"], s["title"], c)
