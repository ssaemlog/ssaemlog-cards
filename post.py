"""schedule.json에서 게시 시간이 된 게시물을 인스타그램에 캐러셀로 올린다.

환경 변수
  IG_TOKEN     인스타그램 로그인 API 장기 액세스 토큰 (GitHub Secret)
  IG_USER_ID   인스타 프로페셔널 계정 ID (GitHub Secret)
  IMAGE_BASE   이미지 공개 URL 앞부분 (예: https://raw.githubusercontent.com/<user>/<repo>/main/cards/)
  DRY_RUN=1    실제 게시 없이 무엇을 올릴지만 출력
"""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
# 인스타 로그인 토큰(IG...)은 graph.instagram.com, 페이스북 쪽 토큰(EA...)은 graph.facebook.com
_HOST = "https://graph.instagram.com/" if os.environ.get("IG_TOKEN", "").startswith("IG") else "https://graph.facebook.com/"
API = _HOST + os.environ.get("GRAPH_VERSION", "v24.0")
ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEDULE = os.path.join(ROOT, "schedule.json")
POSTED = os.path.join(ROOT, "posted.json")


def call(method, path, **params):
    params["access_token"] = os.environ["IG_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path} 실패: {e.code} {e.read().decode()[:500]}")


def wait_ready(container_id):
    for _ in range(30):
        s = call("GET", container_id, fields="status_code").get("status_code")
        if s == "FINISHED":
            return
        if s in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"컨테이너 {container_id} 상태 {s}")
        time.sleep(5)
    raise RuntimeError(f"컨테이너 {container_id} 준비 시간 초과")


def images_of(post):
    """images 가 없으면 render.py 가 만든 cards/r/<id>_NN.jpg 를 쓴다"""
    if post.get("images"):
        return post["images"]
    return [f"r/{post['id']}_{i:02d}.jpg" for i in range(1, len(post["slides"]) + 1)]


def publish(post, user_id, base):
    children = []
    for img in images_of(post):
        c = call("POST", f"{user_id}/media", image_url=base + img, is_carousel_item="true")
        children.append(c["id"])
    for c in children:
        wait_ready(c)
    parent = call("POST", f"{user_id}/media", media_type="CAROUSEL",
                  children=",".join(children), caption=post["caption"])
    wait_ready(parent["id"])
    return call("POST", f"{user_id}/media_publish", creation_id=parent["id"])["id"]


def check():
    """게시하지 않고 연결만 확인: 계정 조회 + 첫 이미지로 컨테이너 생성(게시 안 함, 24시간 뒤 자동 만료)"""
    uid = os.environ["IG_USER_ID"]
    me = call("GET", uid, fields="username")
    print("계정 확인:", me.get("username"))
    first = json.load(open(SCHEDULE, encoding="utf-8"))[0]
    c = call("POST", f"{uid}/media", image_url=os.environ["IMAGE_BASE"] + images_of(first)[0], is_carousel_item="true")
    wait_ready(c["id"])
    print("이미지 업로드 확인: OK (게시하지 않음)")


def main():
    if os.environ.get("CHECK") == "1":
        return check()
    schedule = json.load(open(SCHEDULE, encoding="utf-8"))
    posted = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}
    now = datetime.now(KST)
    dry = os.environ.get("DRY_RUN") == "1"
    due = [p for p in schedule
           if p["id"] not in posted and datetime.fromisoformat(p["publish_at"]) <= now]
    if not due:
        print(f"{now:%m/%d %H:%M} 올릴 게시물 없음")
        return
    # 한 번 실행에 1개만 올린다 (밀린 게 여러 개여도 몰아서 올리지 않음)
    post = sorted(due, key=lambda p: p["publish_at"])[0]
    print(f"게시 대상: {post['id']} ({len(images_of(post))}장)")
    if dry:
        print(post["caption"])
        return
    media_id = publish(post, os.environ["IG_USER_ID"], os.environ["IMAGE_BASE"])
    posted[post["id"]] = {"media_id": media_id, "posted_at": now.isoformat()}
    json.dump(posted, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"게시 완료: {post['id']} → {media_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("오류:", e)
        sys.exit(1)
