import streamlit as st
import requests
from bs4 import BeautifulSoup


# 检查是否应该显示这个页面
if st.session_state.user is None:
    st.error("请先登录以访问此页面")
    st.stop()

st.title("Web Entry Interface")

st.write("### Common Links")
st.write("[Submission](#)")
st.write("[Office](#)")
st.write("[Information Query](#)")

st.write("### Latest Technology News")
st.write("Extracting latest news...")
# Example: Extracting news from a website (replace with actual URLs)
response = requests.get("https://tech.sina.com.cn")
soup = BeautifulSoup(response.text, 'html.parser')

# Parsing and displaying news (modify according to the structure of the target website)
news_list = soup.find_all('div', class_='news-item')
for news in news_list:
    st.write(news.text)

st.write("### Notifications")
st.write("No new notifications.")
