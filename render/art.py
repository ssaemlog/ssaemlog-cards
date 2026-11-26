"""카드용 SVG 일러스트 (선화 스타일, 세이지 포인트). 모두 직접 그린 도형."""
S = "#5E7B6A"   # sage
D = "#2A2A2A"   # dark
L = "#DCE5DE"   # light sage fill
C = "#E9DFD0"   # warm fill
W = "#FBF8F3"


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">{body}</svg>'


def reformer():
    # 필라테스 리포머 선화 + 매트
    b = f'''
    <ellipse cx="430" cy="372" rx="400" ry="22" fill="{C}"/>
    <rect x="70" y="250" width="720" height="40" rx="12" fill="none" stroke="{D}" stroke-width="7"/>
    <line x1="110" y1="290" x2="110" y2="360" stroke="{D}" stroke-width="7" stroke-linecap="round"/>
    <line x1="750" y1="290" x2="750" y2="360" stroke="{D}" stroke-width="7" stroke-linecap="round"/>
    <rect x="330" y="205" width="230" height="45" rx="14" fill="{L}" stroke="{S}" stroke-width="7"/>
    <rect x="530" y="168" width="22" height="40" rx="6" fill="{S}"/>
    <rect x="490" y="168" width="22" height="40" rx="6" fill="{S}"/>
    <rect x="345" y="182" width="70" height="25" rx="10" fill="{W}" stroke="{S}" stroke-width="5"/>
    <path d="M120 250 L120 150 Q120 130 140 130 L175 130" fill="none" stroke="{D}" stroke-width="7" stroke-linecap="round"/>
    <path d="M250 270 q12 -14 24 0 q12 14 24 0 q12 -14 24 0" fill="none" stroke="{S}" stroke-width="6" stroke-linecap="round"/>
    <line x1="790" y1="250" x2="790" y2="170" stroke="{D}" stroke-width="7" stroke-linecap="round"/>
    <line x1="690" y1="170" x2="790" y2="170" stroke="{D}" stroke-width="7" stroke-linecap="round"/>
    <circle cx="700" cy="170" r="10" fill="{S}"/>
    '''
    return svg(860, 400, b)


def calendar_q():
    b = f'''
    <rect x="40" y="50" width="300" height="270" rx="26" fill="{W}" stroke="{D}" stroke-width="7"/>
    <rect x="40" y="50" width="300" height="70" rx="26" fill="{S}"/>
    <rect x="40" y="95" width="300" height="25" fill="{S}"/>
    <line x1="110" y1="30" x2="110" y2="80" stroke="{D}" stroke-width="8" stroke-linecap="round"/>
    <line x1="270" y1="30" x2="270" y2="80" stroke="{D}" stroke-width="8" stroke-linecap="round"/>
    ''' + "".join(
        f'<circle cx="{90 + (i % 5) * 50}" cy="{165 + (i // 5) * 50}" r="11" fill="{S if i < 9 else L}"/>'
        for i in range(15)) + f'''
    <circle cx="390" cy="250" r="78" fill="{C}" stroke="{D}" stroke-width="7"/>
    <path d="M362 228 q0 -30 30 -30 q30 0 30 28 q0 20 -26 28 v16" fill="none" stroke="{D}" stroke-width="10" stroke-linecap="round"/>
    <circle cx="396" cy="300" r="7" fill="{D}"/>
    '''
    return svg(500, 360, b)


def flat_chart():   # 효과를 못 느낌
    b = f'''
    <rect x="30" y="30" width="340" height="250" rx="24" fill="{W}" stroke="{D}" stroke-width="6"/>
    <line x1="70" y1="230" x2="330" y2="230" stroke="{D}" stroke-width="5"/>
    <line x1="70" y1="70" x2="70" y2="230" stroke="{D}" stroke-width="5"/>
    <path d="M80 175 L140 168 L200 172 L260 166 L320 170" fill="none" stroke="{S}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="320" cy="170" r="10" fill="{S}"/>
    <text x="200" y="120" text-anchor="middle" font-family="Noto Sans CJK KR" font-weight="900" font-size="44" fill="{D}">?</text>
    '''
    return svg(400, 310, b)


def wallet():
    b = f'''
    <rect x="50" y="90" width="300" height="190" rx="28" fill="{W}" stroke="{D}" stroke-width="7"/>
    <path d="M50 130 L300 60 L320 90" fill="none" stroke="{D}" stroke-width="7" stroke-linejoin="round"/>
    <rect x="250" y="160" width="100" height="56" rx="16" fill="{L}" stroke="{S}" stroke-width="6"/>
    <circle cx="282" cy="188" r="9" fill="{S}"/>
    <circle cx="140" cy="60" r="32" fill="{C}" stroke="{D}" stroke-width="6"/>
    <text x="140" y="74" text-anchor="middle" font-family="Noto Sans CJK KR" font-weight="900" font-size="38" fill="{D}">₩</text>
    '''
    return svg(400, 310, b)


def clock_cal():
    b = f'''
    <rect x="40" y="70" width="230" height="210" rx="22" fill="{W}" stroke="{D}" stroke-width="6"/>
    <rect x="40" y="70" width="230" height="50" rx="22" fill="{L}" stroke="{D}" stroke-width="6"/>
    <path d="M90 170 l100 70 M190 170 l-100 70" stroke="{S}" stroke-width="9" stroke-linecap="round"/>
    <circle cx="290" cy="110" r="75" fill="{C}" stroke="{D}" stroke-width="6"/>
    <path d="M290 65 V110 L325 130" fill="none" stroke="{D}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    '''
    return svg(400, 310, b)


def bubbles_dots():   # 관계 - 말 못한 불편
    b = f'''
    <path d="M40 60 h200 a24 24 0 0 1 24 24 v90 a24 24 0 0 1 -24 24 h-120 l-40 34 v-34 h-40 a24 24 0 0 1 -24 -24 v-90 a24 24 0 0 1 24 -24z" fill="{W}" stroke="{D}" stroke-width="6"/>
    <circle cx="100" cy="130" r="10" fill="{D}"/><circle cx="140" cy="130" r="10" fill="{D}"/><circle cx="180" cy="130" r="10" fill="{D}"/>
    <path d="M190 150 h170 a24 24 0 0 1 24 24 v70 a24 24 0 0 1 -24 24 h-30 v30 l-36 -30 h-104 a24 24 0 0 1 -24 -24 v-70 a24 24 0 0 1 24 -24z" fill="{L}" stroke="{S}" stroke-width="6"/>
    <circle cx="245" cy="210" r="9" fill="{S}"/><circle cx="280" cy="210" r="9" fill="{S}"/><circle cx="315" cy="210" r="9" fill="{S}"/>
    '''
    return svg(400, 310, b)


def target():
    b = f'''
    <circle cx="190" cy="160" r="120" fill="{W}" stroke="{D}" stroke-width="7"/>
    <circle cx="190" cy="160" r="80" fill="{L}" stroke="{S}" stroke-width="7"/>
    <circle cx="190" cy="160" r="38" fill="{S}"/>
    <line x1="190" y1="160" x2="330" y2="40" stroke="{D}" stroke-width="8" stroke-linecap="round"/>
    <path d="M330 40 l-6 -30 M330 40 l30 6" stroke="{D}" stroke-width="8" stroke-linecap="round"/>
    '''
    return svg(400, 310, b)


def before_after():
    b = f'''
    <rect x="30" y="50" width="160" height="220" rx="20" fill="{W}" stroke="{D}" stroke-width="6"/>
    <rect x="210" y="50" width="160" height="220" rx="20" fill="{L}" stroke="{S}" stroke-width="6"/>
    <circle cx="110" cy="110" r="22" fill="{C}" stroke="{D}" stroke-width="5"/>
    <path d="M110 132 Q96 180 104 240" fill="none" stroke="{D}" stroke-width="8" stroke-linecap="round"/>
    <circle cx="290" cy="105" r="22" fill="{W}" stroke="{S}" stroke-width="5"/>
    <line x1="290" y1="127" x2="290" y2="240" stroke="{S}" stroke-width="8" stroke-linecap="round"/>
    <text x="110" y="300" text-anchor="middle" font-family="Noto Sans CJK KR" font-weight="700" font-size="26" fill="{D}">1개월 전</text>
    <text x="290" y="300" text-anchor="middle" font-family="Noto Sans CJK KR" font-weight="700" font-size="26" fill="{S}">오늘</text>
    '''
    return svg(400, 310, b)


def checklist():
    b = f'''
    <rect x="80" y="30" width="240" height="270" rx="22" fill="{W}" stroke="{D}" stroke-width="6"/>
    <rect x="150" y="14" width="100" height="36" rx="12" fill="{S}"/>
    ''' + "".join(f'''
    <rect x="112" y="{86 + i * 66}" width="36" height="36" rx="8" fill="{L if i < 2 else W}" stroke="{S}" stroke-width="5"/>
    {'<path d="M120 %d l9 10 l16 -20" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>' % (106 + i * 66, S) if i < 2 else ''}
    <line x1="168" y1="{104 + i * 66}" x2="{290 - i * 30}" y2="{104 + i * 66}" stroke="{D}" stroke-width="7" stroke-linecap="round"/>''' for i in range(3))
    return svg(400, 310, b)


def two_people():   # 상담 장면 (추상 인물)
    b = f'''
    <ellipse cx="400" cy="345" rx="360" ry="18" fill="{C}"/>
    <circle cx="230" cy="120" r="46" fill="{C}" stroke="{D}" stroke-width="7"/>
    <path d="M150 340 Q150 200 230 190 Q310 200 310 340" fill="{S}"/>
    <circle cx="570" cy="120" r="46" fill="{W}" stroke="{D}" stroke-width="7"/>
    <path d="M490 340 Q490 200 570 190 Q650 200 650 340" fill="{L}" stroke="{S}" stroke-width="6"/>
    <path d="M330 60 h140 a20 20 0 0 1 20 20 v50 a20 20 0 0 1 -20 20 h-60 l-30 26 v-26 h-50 a20 20 0 0 1 -20 -20 v-50 a20 20 0 0 1 20 -20z" fill="{W}" stroke="{D}" stroke-width="6"/>
    <path d="M370 106 h60" stroke="{S}" stroke-width="8" stroke-linecap="round"/>
    <path d="M370 86 h80" stroke="{D}" stroke-width="8" stroke-linecap="round"/>
    '''
    return svg(800, 370, b)


def stairs():   # 공통점 표지: 계단 + 깃발
    b = f'''
    <path d="M60 330 H250 V250 H440 V170 H630 V90 H760 V330 Z" fill="{L}" stroke="{S}" stroke-width="7" stroke-linejoin="round"/>
    <line x1="700" y1="90" x2="700" y2="10" stroke="{D}" stroke-width="7" stroke-linecap="round"/>
    <path d="M700 14 h60 l-14 18 l14 18 h-60z" fill="{S}"/>
    <circle cx="150" cy="300" r="14" fill="{D}"/><circle cx="345" cy="220" r="14" fill="{D}"/><circle cx="535" cy="140" r="14" fill="{D}"/>
    <ellipse cx="410" cy="345" rx="380" ry="14" fill="{C}"/>
    '''
    return svg(820, 370, b)


def ban_bubble():   # 피해야 할 표현
    b = f'''
    <path d="M40 60 h280 a24 24 0 0 1 24 24 v110 a24 24 0 0 1 -24 24 h-180 l-46 38 v-38 h-54 a24 24 0 0 1 -24 -24 v-110 a24 24 0 0 1 24 -24z" fill="{W}" stroke="{D}" stroke-width="6"/>
    <text x="180" y="158" text-anchor="middle" font-family="Noto Sans CJK KR" font-weight="900" font-size="54" fill="{D}">₩?!</text>
    <circle cx="320" cy="90" r="52" fill="#F3E3DE" stroke="#9A5B4B" stroke-width="7"/>
    <line x1="284" y1="126" x2="356" y2="54" stroke="#9A5B4B" stroke-width="9" stroke-linecap="round"/>
    '''
    return svg(400, 310, b)


ART = {k: v for k, v in globals().items() if callable(v) and k not in ("svg",)}
