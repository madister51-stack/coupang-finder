import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from urllib.parse import quote_plus

# 언어 선택
LANGS = {
    "한국어 (ko)": "ko",
    "중국어 간체 (zh-CN)": "zh-CN",
    "영어 (en)": "en",
    "일본어 (ja)": "ja",
    "베트남어 (vi)": "vi",
    "태국어 (th)": "th",
}

# 번역 함수
def translate_any(text: str, src_code: str, tgt_code: str) -> str:
    """원하는 언어 → 원하는 언어 번역 (실패 시 원문 반환)"""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        return GoogleTranslator(source=src_code, target=tgt_code).translate(text)
    except Exception:
        return text


# 검색 링크 생성 함수
def make_links(query):
    query_encoded = quote_plus(query)
    st.markdown("### 🌏 검색 결과 링크")
    st.write(f"[🔍 알리익스프레스 검색](https://ko.aliexpress.com/wholesale?catId=0&SearchText={query_encoded})")
    st.write(f"[🛍️ 타오바오 검색](https://s.taobao.com/search?q={query_encoded})")
    st.write(f"[🧾 1688 검색](https://s.1688.com/selloffer/offer_search.htm?keywords={query_encoded})")


# -------------------------------
# Streamlit 화면 시작
# -------------------------------

st.set_page_config(page_title="쿠팡 → 중국마켓 자동검색기", page_icon="🛒", layout="centered")

st.title("🇰🇷 쿠팡 ➜ 중국마켓 자동검색기")
st.write("쿠팡 상품명(또는 핵심 키워드)을 입력하면 중국/글로벌 마켓 검색 링크를 자동 생성합니다.")

st.markdown("---")

# 입력창
st.subheader("🔎 쿠팡 상품명 입력")
product_name = st.text_input("예: 무선 청소기, 욕실 선반, 창문 청소기")

if product_name:
    # 한글 → 중국어 번역
    translated = translate_any(product_name, "ko", "zh-CN")
    st.success(f"자동 번역된 중국어: **{translated}**")
    make_links(translated)

st.markdown("---")

# 🔤 수동 번역기 기능
st.subheader("🔤 빠른 번역기 (수동)")

with st.form("manual_translator"):
    c1, c2 = st.columns(2)
    with c1:
        src_label = st.selectbox("원문 언어", list(LANGS.keys()), index=0)
    with c2:
        tgt_label = st.selectbox("번역 언어", list(LANGS.keys()), index=1)

    src = st.text_area("원문 입력", placeholder="여기에 번역할 문장을 입력하세요.", height=100)
    submitted = st.form_submit_button("번역하기")

if submitted:
    src_code = LANGS[src_label]
    tgt_code = LANGS[tgt_label]
    out = translate_any(src, src_code, tgt_code)

    st.markdown("#### ✅ 번역 결과")
    st.text_area("결과", value=out, height=100)

    if out.strip():
        if st.button("이 결과로 검색 링크 만들기"):
            make_links(out)
