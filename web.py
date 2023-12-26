import pandas as pd
import streamlit as st

df = pd.read_excel("自行车事故数据1.xlsx")

# 创建一个新的 DataFrame 包含要绘制的列
selected_columns1 = ['发生数（起）', '死亡人数（人）', '受伤人数（人）']
chart_data = df.set_index('年份')[selected_columns1]

# 绘制折线图
st.line_chart(chart_data)


selected_columns2 = ['发生数（起）', '死亡人数（人）', '受伤人数（人）']
st.bar_chart(chart_data)