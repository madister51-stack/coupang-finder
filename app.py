import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from urllib.parse import quote_plus

# -----------------------------
# 언어 선택
# -----------------------------
LANGS = {
    "한국어 (ko)": "ko",
    "중국어 간체 (zh-CN)": "zh-CN",
    "영어 (en)": "en",
    "일본어 (ja)": "ja",
    "베트남어 (vi)": "vi",
    "태국어 (th)": "th"
}

# -----------------------------
# 번역 함수
# -----------------------------
def translate_any(text: str, src_code: str, tgt_code: str) -> str:
    """원하는 언어 ↔ 원하는 언어 번역 (실패 시 원문 반환)"""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        result = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
        return result
    except Exception:
        return text

# -----------------------------
# 검색 링크 생성 함수
# -----------------------------
def build_url(base, q):
    return f"{base}{quote_plus(q)}"

LINKS = {
    "알리익스프레스 검색": lambda q: build_url("https://www.aliexpress.com/wholesale?SearchText=", q),
    "타오바오 검색":       lambda q: build_url("https://s.taobao.com/search?q=", q),
    "티몰(Tmall) 검색":   lambda q: build_url("https://list.tmall.com/search_product.htm?q=", q),
    "1688 검색":          lambda q: build_url("https://s.1688.com/selloffer/offer_search.htm?keywords=", q),
    "알리바바 글로벌 검색": lambda q: build_url("https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText=", q),
    "테무 검색":           lambda q: build_url("https://www.temu.com/search_result.html?search_key=", q),
    "징둥(JD) 검색":      lambda q: build_url("https://search.jd.com/Search?keyword=", q),
    "쿠팡 검색":           lambda q: build_url("https://www.coupang.com/np/search?q=", q),
}

# -----------------------------
# Streamlit 인터페이스
# -----------------------------
st.title("🌍 다국어 상품 검색 도우미")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("원본 언어", list(LANGS.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("번역 언어", list(LANGS.keys()), index=1)

keyword = st.text_input("🔍 검색어를 입력하세요", placeholder="예: 블루투스 이어폰")

if keyword:
    st.write("---")
    # 번역 결과
    translated = translate_any(keyword, LANGS[src_lang], LANGS[tgt_lang])
    st.write(f"**번역 결과 ({tgt_lang}) →** {translated}")
    st.write("---")

    # 검색 링크 생성
    st.subheader("🌐 검색 결과 링크")
    for label, make in LINKS.items():
        try:
            url = make(translated)
            st.markdown(f"- [{label}]({url})")
        except Exception as e:
            st.warning(f"{label} 링크 생성 실패: {e}")
