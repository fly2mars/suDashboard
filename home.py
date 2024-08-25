import os
import streamlit as st
from common.search_agent import SearchAgent
import re
import datetime
import hashlib

# --- Setup User Authentication ---
names = ["Alex"]
usernames = ["combust"]
# Replace with hashed passwords for security
passwords = ['d39bda2bb8268719d4bbd925b4940fd8209cb4688723bfdd88f64bbfa863e721']

# 初始化session state
if 'user' not in st.session_state:
    st.session_state.user = None


# 登录函数
def login(username, password):
    # 这里应该有实际的用户验证逻辑
    if username == "combust" and hashlib.sha256(password.encode()).hexdigest() == passwords[0]:
        st.session_state.user = username
        return True
    return False


def logout():
    st.session_state.user = None
    for key in list(st.session_state.keys()):
        if key.startswith('show_'):
            del st.session_state[key]


def get_common_links():
    # 这里可以从数据库或配置文件中获取常用链接
    return [
        {"name": "采招办", "url": "https://newsso.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE3MjQ1ODQ3ODk4OTAzODkxNjEsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IlV2MzhCeUdDWlU4V1AxOFBtbUlkY3BWbXgwMFFBM3hOIiwic2NvcGUiOiIiLCJyZWRpcmVjdFVyaSI6Imh0dHBzOi8vYmlkZGluZy5zaHUuZWR1LmNuL3Nzb2xvZ2luLmpzcCIsInN0YXRlIjoiIn0="},
        {"name": "实验设备管理处", "url": "https://sbc.shu.edu.cn/"},
        {"name": "研究生信息管理", "url": "https://gmis.shu.edu.cn/gmis/"},
        {"name": "机构知识库", "url": "https://ir.shu.edu.cn"},
        {"name": "教务系统", "url": "https://cj.shu.edu.cn/"}
    ]


def get_latest_news():
    agent = SearchAgent()
    # 获取当前日期
    today = datetime.date.today()

    # 计算前一个月的日期
    one_month_ago = today - datetime.timedelta(days=20)

    # 格式化日期为搜索字符串
    search_string = f"after:{one_month_ago.strftime('%Y-%m-%d')} before:{today.strftime('%Y-%m-%d')}"
    query = f"site:shu.edu.cn 项目 or 申报 or 自然科学 {search_string}"
    news = {}
    result = agent.run(query)
    for url, content in result.items():
        decoded_content = content.encode('latin1').decode('utf-8', errors='ignore')
        cleaned_text = re.sub(r"\s+", "", decoded_content[:40]).strip()
        news[url] = cleaned_text
    return news


def main():

    if st.session_state.user is None:
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        if st.button("登录"):
            if login(username, password):
                st.success("登录成功!")
                st.rerun()
            else:
                st.error("用户名或密码错误")
    else:
        # 侧边栏
        with st.sidebar:
            if st.session_state.user:
                st.write(f"当前用户: {st.session_state.user}")
                if st.button("登出"):
                    logout()
                    st.experimental_rerun()

        col1, col2 = st.columns(2)

        # 左列：常用链接
        with col1:
            st.subheader("常用链接")
            links = get_common_links()
            for link in links:
                st.markdown(f"[{link['name']}]({link['url']})")

        # 右列：最新消息
        with col2:
            st.subheader("最新消息")
            news = get_latest_news()
            for url, content in news.items():
                # st.markdown(f"<span style='font-size: 8px;'>[{content}]({url})</span>", unsafe_allow_html=True)
                st.html(f"<a style='font-size: 8px;' href={url}>{content}</a>")
                # st.write("---")

    # 隐藏/显示其他页面
    if st.session_state.user is None:
        # 隐藏其他页面
        hide_pages()
    else:
        # 显示其他页面
        show_pages()


def hide_pages():
    # 获取pages目录下的所有.py文件
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")
    for filename in os.listdir(pages_dir):
        if filename.endswith(".py"):
            page_name = filename[:-3]  # 移除.py后缀
            st.session_state[f"show_{page_name}"] = False


def show_pages():
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")
    for filename in os.listdir(pages_dir):
        if filename.endswith(".py"):
            page_name = filename[:-3]
            st.session_state[f"show_{page_name}"] = True


if __name__ == "__main__":
    main()
