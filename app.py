import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from urllib.parse import quote_plus

# =========================
# 언어 코드
# =========================
LANGS = {
    "한국어 (ko)": "ko",
    "중국어 간체 (zh-CN)": "zh-CN",
    "영어 (en)": "en",
    "일본어 (ja)": "ja",
    "베트남어 (vi)": "vi",
    "태국어 (th)": "th",
}

# =========================
# 공통 함수
# =========================
def translate_any(text: str, src_code: str, tgt_code: str) -> str:
    """원하는 언어 ↔ 원하는 언어 번역 (실패 시 원문 반환)"""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        return GoogleTranslator(source=src_code, target=tgt_code).translate(text)
    except Exception:
        return text

def build_url(base: str, q: str) -> str:
    return f"{base}{quote_plus(q or '')}"

# 사이트별 (표시이름, 기본URL, 검색어 언어코드)
SITE_LINKS = [
    ("알리익스프레스 검색", "https://www.aliexpress.com/wholesale?SearchText=", "en"),
    ("타오바오 검색",       "https://s.taobao.com/search?q=",                    "zh-CN"),
    ("티몰(Tmall) 검색",   "https://list.tmall.com/search_product.htm?q=",      "zh-CN"),
    ("1688 검색",          "https://s.1688.com/selloffer/offer_search.htm?keywords=", "zh-CN"),
    ("알리바바 글로벌 검색","https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText=", "en"),
    ("테무 검색",           "https://www.temu.com/search_result.html?search_key=", "en"),
    ("징둥(JD) 검색",      "https://search.jd.com/Search?keyword=",             "zh-CN"),
    ("쿠팡 검색",           "https://www.coupang.com/np/search?q=",             "ko"),   # ✅ 항상 한글
]

# =========================
# UI 시작
# =========================
st.title("🌍 다국어 상품 검색 도우미")

# -------------------------
# 섹션 1) 검색 링크 생성기
# -------------------------
st.header("1) 플랫폼별 검색 링크 만들기")
col1, col2 = st.columns([1, 2])
with col1:
    src_lang_label = st.selectbox("입력(원본) 언어", list(LANGS.keys()), index=0)  # 기본 한국어
    src_code = LANGS[src_lang_label]
with col2:
    keyword = st.text_input("🔍 검색어를 입력하세요", placeholder="예: 욕실선반 / 浴室置物架 / bathroom shelf")

if keyword:
    st.write("---")
    # 필요한 언어만 번역 (중복 번역 방지)
    needed_langs = {lang for _, _, lang in SITE_LINKS}
    text_by_lang = {}
    for lang in needed_langs:
        if lang == src_code:
            text_by_lang[lang] = keyword.strip()
        else:
            text_by_lang[lang] = translate_any(keyword, src_code, lang)

    # 참고용으로 번역 결과 미리보기
    with st.expander("번역 미리보기 (사이트별로 실제로 사용되는 검색어)", expanded=False):
        for lang in sorted(needed_langs):
            st.write(f"- {lang}: {text_by_lang.get(lang, '')}")

    # 링크 출력
    st.subheader("🌐 검색 결과 링크")
    lines = []
    for label, base, lang in SITE_LINKS:
        try:
            q = text_by_lang.get(lang, keyword.strip())
            url = build_url(base, q)
            lines.append(f"- [{label}]({url})")
        except Exception as e:
            lines.append(f"- {label}: 링크 생성 실패 ({e})")
    st.markdown("\n".join(lines))

# -------------------------
# 섹션 2) 간단 번역기
# -------------------------
st.write("---")
st.header("2) 간단 번역기")

tcol1, tcol2 = st.columns(2)
with tcol1:
    trans_src_label = st.selectbox("원문 언어", list(LANGS.keys()), index=0, key="t_src")
    trans_src = LANGS[trans_src_label]
with tcol2:
    trans_tgt_label = st.selectbox("번역 언어", list(LANGS.keys()), index=1, key="t_tgt")
    trans_tgt = LANGS[trans_tgt_label]

src_text = st.text_area("원문 입력", height=120, placeholder="번역할 문장을 입력하세요.")
if src_text:
    result = translate_any(src_text, trans_src, trans_tgt)
    st.markdown("**번역 결과**")
    st.text_area("Result", value=result, height=120)
