import streamlit as st

# 检查是否应该显示这个页面
if st.session_state.user is None:
    st.error("请先登录以访问此页面")
    st.stop()

st.title("Research Testing Interface")
st.write("This is the research testing page.")

# Example: Add widgets for running experiments, visualizing data, etc.
st.write("Add your research tools and widgets here.")
