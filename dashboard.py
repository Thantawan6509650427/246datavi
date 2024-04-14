# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wFd0Tk3bb0XzQt8CLDddjJBdC1G6LbJ1

# Dashboard
"""

import streamlit as st
import pandas as pd
import altair as alt

url = 'https://drive.google.com/file/d/1QPBjNIxIwrMsOpTBQbvquOPyCWbbtkqF/view?usp=sharing'
csv_url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(csv_url, on_bad_lines='skip')

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:

# กำหนดค่าที่ต้องการเปลี่ยนใน column 'คุณเป็นนักศึกษาชั้นปีที่'
replace_values = {'ชั้นปีที่ 1': 'ชั้นปีที่ 1',
                  'ชั้นปีที่ 2': 'ชั้นปีที่ 2',
                  'ชั้นปีที่ 3': 'ชั้นปีที่ 3',
                  'ชั้นปีที่ 4': 'ชั้นปีที่ 4',
                  'ชั้นปีที่ 5': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 6': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 7': 'ชั้นปีที่ 5-8',
                  'ชั้นปีที่ 8': 'ชั้นปีที่ 5-8'
                  }

# เปลี่ยนค่าใน column 'คุณเป็นนักศึกษาชั้นปีที่' ใน DataFrame ใหม่
df_new = df.replace({'คุณเป็นนักศึกษาชั้นปีที่': replace_values})

# กำหนดลำดับของรายได้ต่อเดือน
price_order = ['มากกว่า 9,999 บาท',
               '9,000 - 9,999 บาท',
               '8,000 - 8,999 บาท',
               '7,000 - 7,999 บาท',
               'น้อยกว่า 7,000 บาท']

# กำหนดลำดับของชั้นปีที่ศึกษา
year_order = ['ชั้นปีที่ 1',
              'ชั้นปีที่ 2',
              'ชั้นปีที่ 3',
              'ชั้นปีที่ 4',
              'ชั้นปีที่ 5-8'
              ]

# สร้างกราฟแท่ง
chart = alt.Chart(df_new).mark_bar().encode(
    x=alt.X('count():Q', title='จำนวนนักศึกษา'),
    y=alt.Y('คุณมีรายได้ต่อเดือนเท่าไหร่ ?:N', sort=price_order, title='รายได้ต่อเดือน (บาท)'),
    color=alt.Color('คุณเป็นนักศึกษาชั้นปีที่:N', sort=year_order, legend=alt.Legend(title='ชั้นปีที่')),
    tooltip=['คุณมีรายได้ต่อเดือนเท่าไหร่ ?', 'คุณเป็นนักศึกษาชั้นปีที่', 'count()']
).properties(
    width=700,
    height=400,
    title='แนวโน้มรายได้ต่อเดือนของนักศึกษา โดยแบ่งตามชั้นปีที่ศึกษา'
)

st.altair_chart(chart, use_container_width=True)
