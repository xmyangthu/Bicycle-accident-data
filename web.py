
#tdddggg
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def accident_data(choice):
    st.title(f"{choice}")
    st.write("[注]：所有数据均来自国家统计局（[点击访问国家统计局](https://www.stats.gov.cn/)）")
    df = pd.read_excel("自行车事故数据1.xlsx", engine="openpyxl")
    # 去除空列
    df = df.dropna(axis=1, how='all')
    bike_data = ['年份', '自行车交通事故发生数(起)', 
                    '自行车交通事故受伤人数(人)', 
                    '自行车交通事故死亡人数(人)', 
                    '自行车交通事故直接财产损失(万元)', 
                    '自行车交通事故伤亡总人数(人)'
                    ]
    
    data_for_chart = pd.DataFrame({
                '年份':df['年份'].values,
                '事故发生数':df['自行车交通事故发生数(起)'].values,
                '受伤人数':df['自行车交通事故受伤人数(人)'].values,
                '死亡人数':df['自行车交通事故死亡人数(人)'].values,
                '伤亡总人数':df['自行车交通事故伤亡总人数(人)'].values,
                '直接财产损失':df['自行车交通事故直接财产损失(万元)'].values,
            })
    
    if choice == "总体数据":
        st.write("")
        st.write("")
        st.write("")
        df = pd.read_excel("自行车事故数据1.xlsx", engine="openpyxl")
        # 去除空列
        df = df.dropna(axis=1, how='all')
        # 获取年份列表
        years = df['年份'].unique()
        all_data = ['年份', '交通事故发生数总计(起)',
                            '交通事故受伤人数总计(人)',
                            '交通事故死亡人数总计(人)',
                            '交通事故伤亡总人数(人)'
                            ]
        # 展示数据表格
        st.write("#### 自行车事故数据：")
        st.dataframe(df[bike_data])
        st.markdown("<hr>", unsafe_allow_html=True)

        st.write("#### 交通事故数据：")
        st.dataframe(df[all_data])
        st.markdown("<hr>", unsafe_allow_html=True)

        st.write("#### 自行车事故数据1996~2022年变化情况")
        
        # 使用Plotly展示折线图，并显示数据标签
        fig1 = px.line(data_for_chart, x='年份', y=['事故发生数', '受伤人数', '死亡人数'], title='事故发生数、伤亡情况')
        # 使用update_layout以调整图例位置
        fig1.update_layout(legend=dict(x=0.5, y=1, orientation='h', title_text='', traceorder='normal'))
        # 使用update_traces以显示具体数值，但好像显示不出来
        for trace in fig1.data:
            trace.update(text=trace.y, textposition='bottom center', hoverinfo='y+text')
        st.plotly_chart(fig1)


        # 使用Plotly Express创建柱状图
        fig2 = px.bar(data_for_chart, x='年份', y=['受伤人数', '死亡人数'], title='自行车事故伤亡情况')
        # 添加折线图
        total_casualties = data_for_chart['受伤人数'] + data_for_chart['死亡人数']
        fig2.add_trace(go.Scatter(x=data_for_chart['年份'], y=total_casualties, mode='lines+markers', name='伤亡总数'))
        # 使用update_layout以调整图例位置
        fig2.update_layout(legend=dict(x=0.5, y=1, orientation='h', title_text='', traceorder='normal'))
        # 显示图表
        st.plotly_chart(fig2)

        
        # 绘制折线图
        fig3 = px.line(data_for_chart, x='年份', y=['直接财产损失'], title='自行车事故直接财产损失(万元)')
        # 使用update_layout以调整图例位置
        fig3.update_layout(legend=dict(x=0.5, y=1, orientation='h', title_text='', traceorder='normal'))
        # 使用update_traces以显示具体数值，但好像显示不出来
        for trace in fig3.data:
            trace.update(text=trace.y, textposition='bottom center', hoverinfo='y+text')
        st.plotly_chart(fig3)
        
    elif choice == "各年份具体数据":
        st.write("")
        # 获取年份列表
        years = df['年份'].unique()

        # 创建多选框，默认选择所有年份
        selected_years = st.multiselect("选择年份(1996~2022年)", years, default=years)

        # 根据选择的年份过滤数据
        if selected_years:
            selected_data = df[df['年份'].isin(selected_years)]
            # 展示完整数据表格
            st.write("所选年份数据表格:")
            columns_to_display = ['年份', 
                                  '自行车交通事故发生数(起)', 
                                  '自行车交通事故受伤人数(人)', 
                                  '自行车交通事故死亡人数(人)', 
                                  '自行车交通事故直接财产损失(万元)', 
                                  '自行车交通事故伤亡总人数(人)'
                                  ]
            st.dataframe(selected_data[columns_to_display])
            # 数据处理：选择的年份的不同数据各占一列
            fig = paintbar(selected_data)
            
            st.write("所选年份柱状图:")
            st.plotly_chart(fig)
        else:
            # 显示所有年份的数据
            st.write("1996~2022年数据表格:")
            st.dataframe(df)
            fig = paintbar(df)
            st.write("1996~2022年柱状图:")
            st.plotly_chart(fig)

    elif choice == "与交通事故总体对比":
        st.write("")

        st.write("##### 事故发生数(起)")
        fig1,fig2 = compare('自行车交通事故发生数(起)', '交通事故发生数总计(起)')
        tab1, tab2 = st.tabs(["📈 折线图", "📊 柱状图"])
        tab1.plotly_chart(fig1)
        tab2.plotly_chart(fig2)
        st.markdown("<hr>", unsafe_allow_html=True)
        # TODO:
        st.write("##### 伤亡人数(人)")
        fig3, fig4 = compare('自行车交通事故伤亡总人数(人)', '交通事故伤亡总人数(人)')
        tab3, tab4 = st.tabs(["📈 折线图", "📊 柱状图"])
        tab3.plotly_chart(fig3)
        tab4.plotly_chart(fig4)
        st.markdown("<hr>", unsafe_allow_html=True)
        # TODO:
        st.write("##### 伤亡发生率(%)")
        st.write(r"本图中，$$ 伤亡发生率 = \frac{伤亡总人数}{事故发生起数} $$")
        fig5, fig6 = compare('自行车交通事故伤亡发生率(%)', '交通事故伤亡发生率(%)')
        fig5.update_yaxes(range=[0,200])
        tab5, tab6 = st.tabs(["📈 折线图", "📊 柱状图"])
        tab5.plotly_chart(fig5)
        tab6.plotly_chart(fig6)
        st.markdown("<hr>", unsafe_allow_html=True)
        # TODO:
        st.write("##### 死亡占总伤亡人数百分比(%)")
        fig7, fig8 = compare('自行车事故死亡占总伤亡百分比(%)', '交通事故死亡占总伤亡百分比(%)')
        fig7.update_yaxes(range=[0,80])
        tab7, tab8 = st.tabs(["📈 折线图", "📊 柱状图"])
        tab7.plotly_chart(fig7)
        tab8.plotly_chart(fig8)
        st.markdown("<hr>", unsafe_allow_html=True)




def compare(str1,str2):
    df = pd.read_excel("自行车事故数据1.xlsx", engine="openpyxl")
    # 去除空列
    df = df.dropna(axis=1, how='all')
    fig1 = px.line(df, x='年份', y=[f'{str1}', f'{str2}'])
    # 使用update_layout以调整图例位置
    fig1.update_layout(legend=dict(x=0.2, y=-0.2, orientation='h', title_text='', traceorder='normal'))
    # 使用update_traces以显示具体数值，但好像显示不出来
    for trace in fig1.data:
        trace.update(text=trace.y, textposition='bottom center', hoverinfo='y+text')

    fig2 = px.bar(df, x='年份', y=[f'{str1}', f'{str2}'], barmode='group')
    # 使用update_layout以调整图例位置
    fig2.update_layout(legend=dict(x=0.2, y=-0.2, orientation='h', title_text='', traceorder='normal'))
    # 使用update_traces以显示具体数值，但好像显示不出来
    for trace in fig2.data:
        trace.update(text=trace.y, textposition='outside', hoverinfo='y+text')
        

    return fig1,fig2


def paintbar(data):
    data_for_chart1 = pd.DataFrame({
        '年份':data['年份'].values,
        '事故发生数':data['自行车交通事故发生数(起)'].values,
        '受伤人数':data['自行车交通事故受伤人数(人)'].values,
        '死亡人数':data['自行车交通事故死亡人数(人)'].values,
        '伤亡总人数':data['自行车交通事故伤亡总人数(人)'].values,
        '直接财产损失':data['自行车交通事故直接财产损失(万元)'].values,
    })

    # 使用Plotly展示每种数据单独一列
    fig = px.bar(data_for_chart1, x='年份',y=['事故发生数','受伤人数','死亡人数','伤亡总人数','直接财产损失'], barmode='group')
    # 使用update_traces以显示具体数值
    for trace in fig.data:
        trace.update(text=trace.y, textposition='outside', hoverinfo='y+text')
    return fig


def main():
    st.sidebar.title("自行车交通事故数据")
    choicelist = ["总体数据", "各年份具体数据", "与交通事故总体对比"]
    choice = st.sidebar.selectbox("选择页面", choicelist)
    accident_data(choice)
    

if __name__ == "__main__":
    main()