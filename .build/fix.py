import json, re
B = json.load(open('/tmp/claude-0/cmt/book.json'))
for s in B:
    out = []
    for b in s['blocks']:
        if b['t'] == 'h4' and re.search(r'\s①\s', b['x']):
            parts = re.split(r'\s(?=[①-⑳]\s)', b['x'])
            out.append({'t': 'h4', 'x': parts[0]})
            out += [{'t': 'li', 'x': p} for p in parts[1:]]
            continue
        if b['t'] == 'table':
            extra = []
            last = b['rows'][-1]
            m = re.search(r'\s(기출 포인트|쉬운 예|실제 사례)\s', last[-1])
            if m:
                tail = last[-1][m.start():].strip(); last[-1] = last[-1][:m.start()].strip()
                for k, x in re.findall(r'(기출 포인트|쉬운 예|실제 사례) (.*?)(?=\s(?:기출 포인트|쉬운 예|실제 사례) |$)', tail):
                    extra.append({'t': 'box', 'k': k, 'x': x.strip()})
            if s['n'] == 8 and b['rows'][0][0] == '약제':
                b['rows'] = [["약제", "성질", "주로 쓰는 얼룩", "주의"],
                    ["중성세제", "계면활성제", "간장·주스·땀 등 수용성 전반, 마무리", "충분히 헹굼"],
                    ["탄닌계 오점제거제", "탄닌 분해·분산", "커피·홍차·녹차·과즙·포도주", "견뢰도 확인"],
                    ["산소계 표백제", "약한 산화 표백", "남은 색소, 혈액 자국, 땀 황변", "금속 장식 주의"],
                    ["수산(옥살산)", "산", "녹(쇳물), 잉크 속 철분", "사용 후 충분히 헹굼"],
                    ["시너", "유기용제", "페인트, 그리스, 유성 매직·기름", "인화성, 일부 섬유 손상"],
                    ["아세톤", "강한 유기용제", "매니큐어, 접착제", "아세테이트·트리아세테이트 금지"],
                    ["메틸알코올", "알코올 용제", "유성 볼펜 잉크, 일부 색소, 약품", "인화성·독성, 환기"],
                    ["로트유", "술폰화 피마자유(유화성 기름)", "굳은 유성 얼룩을 풀어 물로 씻겨 나오게 돕는 보조제", "남지 않게 헹굼"]]
            out.append(b); out += extra; continue
        out.append(b)
    s['blocks'] = out
# 표 머리줄 끊어진 같은 표 반복 제거(8절 2차 처리표 중복 헤더)
for s in B:
    for b in s['blocks']:
        if b['t'] == 'table':
            hdr = b['rows'][0]; b['rows'] = [hdr] + [r for r in b['rows'][1:] if r != hdr]
for s in B:
    for b in s['blocks']:
        if 'x' in b: b['x']=re.sub(r'\(\s{3,},\s*','(',b['x'])
json.dump(B, open('/tmp/claude-0/cmt/book_clean.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(sum(len(s['blocks']) for s in B), "blocks;", sum(1 for s in B for b in s['blocks'] if b['t']=='box' and b['k']=='기출 포인트'), "기출 포인트")
