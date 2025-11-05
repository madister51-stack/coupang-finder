
import streamlit as st
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

st.set_page_config(page_title="쿠팡 → 중국마켓 자동검색기", page_icon="🛒")

st.title("쿠팡 상품 중국 사이트 자동 검색기 🇨🇳")
st.write("쿠팡 상품 이름을 입력하면 타오바오, 알리익스프레스, 1688에서 자동으로 검색합니다.")

query = st.text_input("🔍 쿠팡 상품명을 입력하세요")

if st.button("검색하기"):
    if query:
        translator = Translator()
        translated = translator.translate(query, src='ko', dest='zh-cn').text
        st.write(f"**중국어 번역:** {translated}")
        st.markdown("---")
        st.subheader("검색 결과 바로가기:")
        st.write(f"[🛍️ 타오바오 검색](https://s.taobao.com/search?q={translated})")
        st.write(f"[💎 알리익스프레스 검색](https://www.aliexpress.com/wholesale?catId=0&SearchText={translated})")
        st.write(f"[🏭 1688 검색](https://s.1688.com/selloffer/offer_search.htm?keywords={translated})")
    else:
        st.warning("상품명을 입력해주세요!")
