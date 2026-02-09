import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="我的第一个云端应用", page_icon="🌤️")

st.title("🚀 欢迎来到我的云端实验室")
st.write(f"当前服务器时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 创建一个互动的随机折线图
st.subheader("实时数据模拟")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['访问量', '转化率', '跳出率']
)
st.line_chart(chart_data)

# 简单的互动
name = st.text_input("留下你的大名：")
if name:
    st.success(f"你好 {name}！你的第一个 Streamlit 应用已部署成功！")