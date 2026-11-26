"""schedule.json 에서 slides(카드 문구)가 있는 게시물을 1080x1350 JPG 카드로 그린다.

- 결과: cards/r/<게시물id>_NN.jpg  (이미 있으면 건너뜀)
- 사진: slide 의 "photo": {"url": 직접 다운로드 URL, "credit": "작가 / 사이트"}
- --check : 그릴 게 있으면 GITHUB_OUTPUT 에 need=1 (설치 단계 생략용)
- --only <id> / --force : 미리보기·재렌더용
"""
import base64, hashlib, html, json, os, sys, asyncio, pathlib, urllib.request, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "render"))
from art import ART  # noqa: E402

OUT = ROOT / "cards" / "r"


def image_names(post):
    return [f"r/{post['id']}_{i:02d}.jpg" for i in range(1, len(post["slides"]) + 1)]


def fingerprint(post):
    return hashlib.sha256(json.dumps(post["slides"], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def todo(schedule, only=None, force=False):
    """그린 적 없거나, 카드 문구·사진이 바뀐 게시물 (cards/r/<id>.hash 로 비교)"""
    res = []
    for p in schedule:
        if "slides" not in p or (only and p["id"] != only):
            continue
        h = OUT / f"{p['id']}.hash"
        same = h.exists() and h.read_text().strip() == fingerprint(p)
        if force or not same or not all((ROOT / "cards" / n).exists() for n in image_names(p)):
            res.append(p)
    return res


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;color:#2A2A2A;background:#F5F0E8;position:relative;overflow:hidden}
.wrap{position:absolute;inset:0;padding:110px 100px 150px;display:flex;flex-direction:column}
.tag{display:inline-block;align-self:flex-start;font-size:30px;font-weight:700;color:#FBF8F3;background:#5E7B6A;border-radius:40px;padding:10px 26px;margin-bottom:40px;letter-spacing:1px}
h1{font-weight:900;line-height:1.3;white-space:pre-line;letter-spacing:-1.5px}
p{font-size:40px;line-height:1.65;font-weight:500;white-space:pre-wrap}
.art{display:flex;justify-content:center}
.art svg{max-width:100%;height:auto}
.cover h1{font-size:84px}
.cover .sub{font-size:38px;color:#5E7B6A;font-weight:700;margin-top:36px}
.cover .art{margin-bottom:60px}
.reason h1,.body h1,.tip h1{font-size:64px;margin-bottom:44px}
.reason .art{margin:10px 0 50px}
.reason .art svg{width:520px}
.tip{background:#EDE6DA}
.quote h1{font-size:56px;margin-bottom:50px}
.bubble{background:#FBF8F3;border:6px solid #2A2A2A;border-radius:44px;padding:56px;position:relative;box-shadow:14px 14px 0 #DCE5DE}
.bubble p{font-size:44px;line-height:1.7;font-weight:700}
.bubble:after{content:"";position:absolute;left:90px;bottom:-46px;width:60px;height:46px;background:#FBF8F3;border-left:6px solid #2A2A2A;border-bottom:6px solid #2A2A2A;transform:skewX(30deg)}
.speaker{display:flex;align-items:center;gap:20px;margin-top:80px;font-size:34px;font-weight:700;color:#5E7B6A}
.speaker i{width:64px;height:64px;border-radius:50%;background:#5E7B6A;display:block}
.question{background:#5E7B6A;color:#FBF8F3}
.question .tag{background:#FBF8F3;color:#5E7B6A}
.question h1{font-size:82px}
.question p{color:#E6EDE8;font-size:38px;margin-top:50px}
.qmark{position:absolute;right:80px;top:80px;width:220px;height:220px;border-radius:50%;border:8px solid #9CB5A6;display:flex;align-items:center;justify-content:center;font-size:150px;font-weight:900;color:#9CB5A6}
.photo{width:100%;border-radius:36px;overflow:hidden;position:relative;background:#DCE5DE}
.photo img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(0.85)}
.photo:after{content:"";position:absolute;inset:0;background:#5E7B6A;opacity:0.08}
.cover .photo{height:620px;margin-bottom:56px}
.reason .photo,.body .photo,.tip .photo{height:440px;margin:0 0 48px}
.credit{position:absolute;right:18px;bottom:14px;font-size:20px;color:#FBF8F3;z-index:2;text-shadow:0 1px 3px rgba(0,0,0,.5)}
.foot{position:absolute;bottom:64px;left:100px;right:100px;display:flex;justify-content:space-between;font-size:28px;color:#8C857B}
.question .foot{color:#CFDCD3}
"""


def fetch_photo(url, tmp):
    path = pathlib.Path(tmp) / (str(abs(hash(url))) + ".jpg")
    if not path.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 ssaemlog-cards"})
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
    data = path.read_bytes()
    mime = "image/png" if data[:4] == b"\x89PNG" else "image/webp" if data[8:12] == b"WEBP" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(data).decode()


def card_html(s, idx, total, photo_uri=None):
    kind = s.get("kind", "body")
    tag = html.escape(s.get("tag", ""))
    t = html.escape(s.get("title", ""))
    lines = s.get("lines", [])
    ps = "".join(f"<p>{html.escape(l) or '&nbsp;'}</p>" for l in lines)
    art = s.get("art")
    a = f'<div class="art">{ART[art]()}</div>' if art in ART else ""
    if photo_uri:
        credit = html.escape(s.get("photo", {}).get("credit", ""))
        a = f'<div class="photo"><img src="{photo_uri}">' + (f'<span class="credit">Photo: {credit}</span>' if credit else "") + "</div>"
    if kind == "cover":
        sub = f'<div class="sub">{html.escape(lines[0])}</div>' if lines else ""
        inner = f'<div style="margin-top:auto"></div>{a}<h1>{t}</h1>{sub}'
    elif kind == "question":
        sub = f"<p>{html.escape(lines[0])}</p>" if lines else ""
        inner = f'<div class="qmark">?</div><div class="tag">{tag or "QUESTION"}</div><div style="margin:auto 0"><h1>{t}</h1>{sub}</div>'
    elif kind == "quote":
        inner = f'<div class="tag">{tag}</div><h1>{t}</h1><div class="bubble">{ps}</div><div class="speaker"><i></i>{html.escape(s.get("speaker", "강사님"))}</div>'
    else:
        inner = (f'<div class="tag">{tag}</div>' if tag else "") + f"<h1>{t}</h1>{a}{ps}"
    right = "넘겨보기 →" if idx < total else "댓글·DM 환영해요"
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{kind}">'
            f'<div class="wrap">{inner}</div><div class="foot"><span>{idx} / {total}</span><span>{right}</span></div></body></html>')


async def render(posts, out_dir=OUT, chrome=None):
    from playwright.async_api import async_playwright
    out_dir.mkdir(parents=True, exist_ok=True)
    chrome = chrome or os.environ.get("CHROME_PATH") or next(
        (c for c in ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium"] if os.path.exists(c)), None)
    with tempfile.TemporaryDirectory() as tmp:
        async with async_playwright() as pw:
            b = await pw.chromium.launch(executable_path=chrome) if chrome else await pw.chromium.launch()
            pg = await b.new_page(viewport={"width": 1080, "height": 1350})
            for p in posts:
                n = len(p["slides"])
                for i, s in enumerate(p["slides"], 1):
                    uri = fetch_photo(s["photo"]["url"], tmp) if s.get("photo", {}).get("url") else None
                    await pg.set_content(card_html(s, i, n, uri), wait_until="load")
                    await pg.wait_for_timeout(150)
                    target = out_dir / f"{p['id']}_{i:02d}.jpg"
                    await pg.screenshot(path=str(target), type="jpeg", quality=90)
                    print("렌더:", target.name)
                for old in out_dir.glob(f"{p['id']}_*.jpg"):   # 장수가 줄었으면 남은 옛 파일 정리
                    if int(old.stem.rsplit("_", 1)[1]) > n:
                        old.unlink()
                (out_dir / f"{p['id']}.hash").write_text(fingerprint(p))
            await b.close()


def main():
    args = sys.argv[1:]
    schedule = json.load(open(ROOT / "schedule.json", encoding="utf-8"))
    only = args[args.index("--only") + 1] if "--only" in args else None
    posts = todo(schedule, only, "--force" in args)
    if "--check" in args:
        need = "1" if posts else "0"
        print("렌더 필요:", [p["id"] for p in posts] or "없음")
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"need={need}\n")
        return
    if posts:
        asyncio.run(render(posts))


if __name__ == "__main__":
    main()
