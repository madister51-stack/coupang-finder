import streamlit as st
import urllib.parse
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# ----------------- 기본 설정 -----------------
st.set_page_config(
    page_title="쿠팡 → 중국마켓 자동검색기",
    page_icon="🛒",
    layout="centered"
)

# ----------------- 유틸 함수 -----------------
def translate_ko_to_zh(text: str) -> str:
    """한글을 중국어(간체)로 번역. 실패 시 원문 그대로 반환."""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        return GoogleTranslator(source="ko", target="zh-CN").translate(text)
    except Exception:
        return text  # 번역 실패해도 앱이 죽지 않도록

def make_links(keyword_zh: str):
    """중국어 키워드로 각 마켓 검색 링크 생성."""
    q = urllib.parse.quote(keyword_zh)
    st.markdown("#### 🔎 중국/글로벌 마켓 바로검색")
    st.markdown(f"- 🐉 **[1688 검색](https://s.1688.com/selloffer/offer_search.htm?keywords={q})**")
    st.markdown(f"- 🧡 **[타오바오 검색](https://s.taobao.com/search?q={q})**")
    st.markdown(f"- 🌏 **[알리익스프레스 검색](https://www.aliexpress.com/wholesale?SearchText={q})**")
    st.markdown(f"- 🏢 **[알리바바 검색](https://www.alibaba.com/trade/search?searchText={q})**")
    st.markdown(f"- 🛍 **[테무 검색](https://www.temu.com/search.html?q={q})**")

def extract_title_from_coupang(url: str) -> str:
    """쿠팡 상품 URL에서 og:title 또는 title을 읽어 상품명 추출."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            return og["content"].strip()

        if soup.title and soup.title.text:
            return soup.title.text.replace("쿠팡!", "").strip()
    except Exception:
        pass
    return ""

# ----------------- UI -----------------
st.title("쿠팡 → 중국마켓 자동검색기")
st.caption("한글 상품명을 중국어(간체)로 자동 번역하고, 중국/글로벌 마켓에서 바로 검색할 수 있게 링크를 만들어줘요.")

tab1, tab2 = st.tabs(["문구로 검색", "쿠팡 URL로 검색"])

with tab1:
    name_ko = st.text_input("한글 상품명", placeholder="예) 무선 청소기, 욕실 선반, 창문 청소기")
    # 버튼을 누르거나, 입력이 있으면 바로 동작
    run = st.button("번역하고 검색 링크 만들기", key="btn1") or bool(name_ko.strip())
    if run:
        if name_ko.strip():
            name_zh = translate_ko_to_zh(name_ko)
            st.markdown("#### ✅ 번역 결과")
            st.code(name_zh or "(번역 실패 — 원문으로 검색합니다)", language="text")
            make_links(name_zh or name_ko)
        else:
            st.warning("검색어를 입력해 주세요.")

with tab2:
    url = st.text_input("쿠팡 상품 URL 붙여넣기", placeholder="예) https://www.coupang.com/vp/products/...")
    if st.button("URL에서 제목 가져와 번역 + 검색", key="btn2"):
        if not url.strip():
            st.warning("URL을 입력해 주세요.")
        else:
            title_ko = extract_title_from_coupang(url.strip())
            if not title_ko:
                st.warning("상품 제목을 가져오지 못했어요. URL이 맞는지 확인해 주세요.")
            else:
                st.markdown("#### 📌 쿠팡 제목")
                st.code(title_ko, language="text")
                name_zh = translate_ko_to_zh(title_ko)
                st.markdown("#### ✅ 번역 결과")
                st.code(name_zh or "(번역 실패 — 원문으로 검색합니다)", language="text")
                make_links(name_zh or title_ko)

st.info("TIP: 너무 길면 핵심어 2~3개만 넣는 게 검색 품질이 좋아요. 예) '무선 청소기 헤파필터'")
