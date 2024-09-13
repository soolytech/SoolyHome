# page1 : 투자자문 서비스

import streamlit as st
import pandas as pd
import altair as alt
from math import sqrt
import sqlite3
import plotly.graph_objects as go


st.markdown("#### :one: 투자자문")

# soft 줄바꿈 하려면 space를 넣어야함. 아래 첫줄 끝에 공백 필요
st.markdown('''
- 주가가 일정 수준 하락해도 수익을 보는 Buffer 전략      
>> 해외에서 구조화 상품을 ETF로 변환한 Buffer ETF 인기있음    

- 긴 투자기간 동안 안정적인 수익추구: 퇴직연금에 적합

- ELS 복제 전략을 개선한 Buffer 전략     
>> 운용 및 마케팅 지원 시스템으로 업무 효율화
''' )

st.divider()

items = ['SK하이닉스','삼성전자','현대차','기아','KB금융','NAVER', '삼성생명', '셀트리온']


st.markdown("##### :a: Market watch (예시)")
############################# 종목 선택 (입력)
item_name = st.selectbox("종목을 선택하세요", items)

conn= sqlite3.connect('soolyDB.db')

sql_query = pd.read_sql_query(
    ('select * from hist_data where name = :value'),
    conn,
    params={'value': item_name}
)

############################### chart data preparing
df = pd.DataFrame(sql_query)

chart_data = pd.DataFrame(df.head(210), columns=["date", "open", "high", "low", "close"])
chart_data['date'] = pd.to_datetime(chart_data['date'], format="%Y%m%d")

############################# 변동성 구하기
chart_data['daily_return'] = chart_data['close'].pct_change()
chart_data['7d_vol'] = chart_data['daily_return'].rolling(window=7).std() * sqrt(252)
chart_data['15d_vol'] = chart_data['daily_return'].rolling(window=15).std() * sqrt(252)
chart_data['30d_vol'] = chart_data['daily_return'].rolling(window=30).std() * sqrt(252)
chart_data['60d_vol'] = chart_data['daily_return'].rolling(window=60).std() * sqrt(252)

vol_data = pd.DataFrame(chart_data.head(150), columns=["date", "7d_vol", "15d_vol", "30d_vol", "60d_vol"])

#####################################
subtitle = str(item_name) + " 주가 그래프"
st.markdown(subtitle)

domain_max = max(chart_data['close']) * 1.1
domain_min = min(chart_data['close']) * 0.9

chart = alt.Chart(chart_data).mark_line().encode(
    x='date',
    y=alt.Y('close', scale=alt.Scale(domain=[domain_min,domain_max]))
)

st.altair_chart(chart, use_container_width=True)

################################
subtitle = str(item_name) + " 캔들스틱 차트"
st.markdown(subtitle)

fig = go.Figure()
fig.add_trace(go.Candlestick(x=chart_data['date'], open=chart_data['open'], high=chart_data['high'], low = chart_data['low'], close=chart_data['close']))

st.plotly_chart(fig)

################################
subtitle = str(item_name) + " 변동성 그래프 (검증 중)"
st.markdown(subtitle)

chart = alt.Chart(vol_data).transform_fold(['7d_vol', '15d_vol', '30d_vol', '60d_vol']).mark_line().encode(
    x='date',
    y='value:Q',
    color='key:N'
)

st.altair_chart(chart, use_container_width=True)
st.divider()
##############################
st.markdown("Main Book 정보")
bookinfo ={
    '상품코드': ['2024001', '2024002', '2024003'],
    '발행일' :['2023-10-5', '2023-11-5', '2024-05-02'],
    '발행금액' : ['100,000,000', '250,000,000', '120,000,000'],
    '기초자산' : ['KOSPI200', '삼성전자', 'SK하이닉스'],
    '목표수익률' : ['6%', '7%', '10%'],
    '상품명' : ['Buffer 1호', 'Buffer 2호', 'Buffer 3호'],
    'NAV' : ['101.4', '103.3', '105.2']
}
df = pd.DataFrame(bookinfo)

st.dataframe(df)
st.divider()
################# 상품 설명서

if st.button("상품설명서 생성"):
    st.image('samsungELS.PNG', caption='삼성증권 ELS 상품 예시')

st.button("Reset(다시시작)", type="primary")
st.divider()
################# working on

st.markdown('백테스팅, 운용관리 등 working on ... :sun_with_face:')
