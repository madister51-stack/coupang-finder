import streamlit as st
import urllib.parse

st.set_page_config(page_title="쿠팡 → 중국마켓 자동검색기", page_icon="🛒", layout="centered")

st.title("쿠팡 → 중국마켓 자동검색기")
st.caption("쿠팡 상품명(또는 핵심 키워드)을 입력하면 중국/글로벌 마켓 검색 링크를 자동 생성합니다.")

def make_links(keyword: str):
    q = urllib.parse.quote(keyword)
    st.markdown("#### 🔎 검색 링크")
    st.markdown(f"- 🐉 [1688](https://s.1688.com/selloffer/{q}.html)")
    st.markdown(f"- 🧡 [타오바오](https://world.taobao.com/search?q={q})")
    st.markdown(f"- 🌏 [알리익스프레스](https://www.aliexpress.com/wholesale?SearchText={q})")
    st.markdown(f"- 🏢 [알리바바](https://www.alibaba.com/trade/search?searchText={q})")
    st.markdown(f"- 🛍 [테무](https://www.temu.com/search.html?q={q})")
    st.info("TIP: '무선 청소기', '욕실 선반'처럼 핵심어를 짧게 넣으면 결과가 더 잘 나와요.")

# 입력창
name = st.text_input("쿠팡 상품명(또는 핵심 키워드)", placeholder="예: 무선 청소기, 욕실 선반, 창문 청소기")

# ✅ 버튼 없이도, 글자를 입력하면 즉시 링크가 보이도록
if name.strip():
    make_links(name.strip())

# 테스트용 예시 버튼(옵션)
with st.expander("예시로 테스트하기 (동작 확인용)"):
    if st.button("예시 실행: 무선 청소기"):
        make_links("무선 청소기")
