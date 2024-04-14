# -*- coding: utf-8 -*-
"""Dashboard

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UyGdk4cTw5or3eR3QggcinZxj3aNxAz8

# Import Library And Font
"""

!wget -q https://github.com/Phonbopit/sarabun-webfont/raw/master/fonts/thsarabunnew-webfont.ttf

!wget -q https://github.com/google/fonts/blob/main/ofl/chonburi/Chonburi-Regular.ttf

!pip install pythainlp

import gspread
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib as mpl
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from google.auth import default
from google.colab import auth
import matplotlib.font_manager as fm
from wordcloud import WordCloud
from pythainlp.tokenize import word_tokenize # เป็นตัวตัดคำของภาษาไทย
from pythainlp.corpus import thai_stopwords # เป็นคลัง Stop Words ของภาษาไทย
from collections import Counter
import random

mpl.font_manager.fontManager.addfont('thsarabunnew-webfont.ttf')
mpl.rc('font', family='TH Sarabun New')

font_path = '/usr/share/fonts/truetype/tlwg/THSarabunNew.ttf'  # Adjust if you downloaded directly
font = fm.FontProperties(fname=font_path, size=16)

"""#Import csv"""

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/แบบสำรวจพฤติกรรมการใช้จ่ายของนักศึกษามหาวิทยาลัยธรรมศาสตร์.csv')
# Code for making the first row as header. Remove if not needed.
df

"""#Data Cleaning"""

#df['คุณเป็นนักศึกษาชั้นปีที่'] = df['คุณเป็นนักศึกษาชั้นปีที่'].str.extract(r'(\d+)').astype(int)
df['คุณเป็นนักศึกษาชั้นปีที่'] = df['คุณเป็นนักศึกษาชั้นปีที่'].str.replace(r'\s*\([^()]*\)', '', regex=True)
df

# Clean values in the 'column_name' by removing strings in parentheses
df['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1'] = df['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 1'].str.replace(r'\s*\([^()]*\)', '', regex=True)
df['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2'] = df['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2'].str.replace(r'\s*\([^()]*\)', '', regex=True)
df['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3'] = df['ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3'].str.replace(r'\s*\([^()]*\)', '', regex=True)
df

df['คุณเคยเผชิญปัญหาทางการเงินหรือไม่?'] = df['คุณเคยเผชิญปัญหาทางการเงินหรือไม่?'].map({'เคย': True, 'ไม่เคย': False})

# Replace the values in col2 with null if the corresponding value in col1 is 'ไม่มีค่าใช้จ่ายในอันดับนี้'
df.loc[df["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 2"] == 'ไม่มีค่าใช้จ่ายในอันดับนี้', "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"] = np.nan
df.loc[df["ในหนึ่งเดือนคุณใช้เงินในส่วนใดมากที่สุดอันดับที่ 3"] == 'ไม่มีค่าใช้จ่ายในอันดับนี้', "จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"] = np.nan
df

# สร้าง dictionary เก็บลำดับใหม่
reorder_map_money = {
    "NaN" : 0,
    "ต่ำกว่า 500 บาท": 1,
    "500 - 1,500 บาท": 2,
    "1,501 - 2,500 บาท": 3,
    "2,501 - 3,500 บาท": 4,
    "3,501 - 4,500 บาท": 5,
    "4,501 - 5,500 บาท": 6,
    "มากกว่า 5,500 บาท" : 7
}

df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'] = df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'].map(reorder_map_money)
df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'] = df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'].map(reorder_map_money)
df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'] = df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'].map(reorder_map_money)

df = df.drop(df[(df["จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"] > df["จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"]) & (df["จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"] > df["จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"])].index)

df = df.drop(df[(df["จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"] > df["จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?"])].index)

reorder_map_money_back = {
    0 : "NaN",
    1 : "ต่ำกว่า 500 บาท",
    2 : "500 - 1,500 บาท",
    3 : "1,501 - 2,500 บาท",
    4 : "2,501 - 3,500 บาท",
    5 : "3,501 - 4,500 บาท",
    6 : "4,501 - 5,500 บาท",
    7 : "มากกว่า 5,500 บาท"
}

df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'] = df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 1 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'].map(reorder_map_money_back)
df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'] = df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 2 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'].map(reorder_map_money_back)
df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'] = df['จากตัวเลือกข้างต้นที่คุณเลือกเป็นอันดับ 3 คุณใช้จ่ายในส่วนนี้ไปประมาณเท่าไหร่ต่อเดือน ?'].map(reorder_map_money_back)

# Reorder the index
df = df.reset_index(drop=True)
# Make index start with 1
df.index = df.index + 1

df

"""# Install Dashboard"""

pip install streamlit-shadcn-ui

pip install streamlit-extras

pip install streamlit-elements==0.1.*

"""# 1. แผนภูมิโดนัท แสดงแนวโน้มสัดส่วนประชากรผู้ตอบแบบสอบถาม โดยแบ่งตามแต่ละชั้นปี คณะ และเพศ

"""

# นับจำนวนข้อมูลในแต่ละกลุ่ม
grouped = df.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คณะที่คุณกำลังศึกษา"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เก็บลำดับใหม่
reorder_map = {
    "ชั้นปีที่ 1": 0,
    "ชั้นปีที่ 2": 1,
    "ชั้นปีที่ 3": 2,
    "ชั้นปีที่ 4": 3,
    "ชั้นปีที่ 5-8": 4
}

# รวมชั้นปีที่ 5 ถึง 8
grouped['คุณเป็นนักศึกษาชั้นปีที่'] = grouped['คุณเป็นนักศึกษาชั้นปีที่'].replace(['ชั้นปีที่ 5', 'ชั้นปีที่ 6', 'ชั้นปีที่ 7', 'ชั้นปีที่ 8'], 'ชั้นปีที่ 5-8')

# นับจำนวนนักศึกษาใหม่
grouped = grouped.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คณะที่คุณกำลังศึกษา"]).agg({'จำนวนนักศึกษา': 'sum'}).reset_index()

# เพิ่มคอลัมน์ลำดับใหม่
grouped["ลำดับ"] = grouped["คุณเป็นนักศึกษาชั้นปีที่"].map(reorder_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ"
grouped = grouped.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# แสดงผล
grouped

# นับจำนวนข้อมูลในแต่ละกลุ่ม
grouped2 = df.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "เพศ", "คณะที่คุณกำลังศึกษา"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เก็บลำดับใหม่
reorder_map = {
    "ชั้นปีที่ 1": 0,
    "ชั้นปีที่ 2": 1,
    "ชั้นปีที่ 3": 2,
    "ชั้นปีที่ 4": 3,
    "ชั้นปีที่ 5-8": 4
}

# รวมชั้นปีที่ 5 ถึง 8
grouped2['คุณเป็นนักศึกษาชั้นปีที่'] = grouped2['คุณเป็นนักศึกษาชั้นปีที่'].replace(['ชั้นปีที่ 5', 'ชั้นปีที่ 6', 'ชั้นปีที่ 7', 'ชั้นปีที่ 8'], 'ชั้นปีที่ 5-8')

# นับจำนวนนักศึกษาใหม่
grouped2 = grouped2.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "เพศ","คณะที่คุณกำลังศึกษา"]).agg({'จำนวนนักศึกษา': 'sum'}).reset_index()

# เพิ่มคอลัมน์ลำดับใหม่
grouped2["ลำดับ"] = grouped2["คุณเป็นนักศึกษาชั้นปีที่"].map(reorder_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ"
grouped2 = grouped2.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# แสดงผล
grouped2

# ทำการกรุ๊ป 'คุณเป็นนักศึกษาชั้นปีที่' และรวม 'จำนวนนักศึกษา' เข้าด้วยกัน
sum_by_year = grouped.groupby('คุณเป็นนักศึกษาชั้นปีที่')['จำนวนนักศึกษา'].sum()

print(sum_by_year)

def faculty_student_count(grouped, selected_year, selected_faculty):
  """
  ฟังก์ชันนี้ใช้สำหรับพิมพ์ค่าจากคอลัมน์ "จำนวนนักศึกษา" โดยเลือกชื่อคอลัมน์ "คุณเป็นนักศึกษาชั้นปีที่" และ "เพศ"
  และจะคืนค่า 0 ถ้าไม่มีข้อมูลตามที่เลือก

  Args:
    grouped: DataFrame ที่ได้จากการ groupby คอลัมน์ "คุณเป็นนักศึกษาชั้นปีที่" และ "เพศ"
    selected_year: ปีการศึกษาที่ต้องการ
    selected_gender: เพศที่ต้องการ

  Returns:
    int: จำนวนนักศึกษา หรือ 0 ถ้าไม่มีข้อมูลตามที่เลือก
  """

  # กรอง DataFrame ตามปีการศึกษาที่เลือก
  filtered_df = grouped.loc[grouped['คุณเป็นนักศึกษาชั้นปีที่'] == selected_year]

  # กรอง DataFrame ตามเพศที่เลือก
  filtered_df = filtered_df.loc[filtered_df['คณะที่คุณกำลังศึกษา'] == selected_faculty]

  # กรณีมีข้อมูล
  if not filtered_df.empty:
      return filtered_df['จำนวนนักศึกษา'].values[0]
  else:  # กรณีไม่มีข้อมูล
      return 0

def gender_student_count(grouped, selected_year, selected_faculty, selected_gender):
  """
  ฟังก์ชันนี้ใช้สำหรับพิมพ์ค่าจากคอลัมน์ "จำนวนนักศึกษา" โดยเลือกชื่อคอลัมน์ "คุณเป็นนักศึกษาชั้นปีที่" และ "เพศ"
  และจะคืนค่า 0 ถ้าไม่มีข้อมูลตามที่เลือก

  Args:
    grouped: DataFrame ที่ได้จากการ groupby คอลัมน์ "คุณเป็นนักศึกษาชั้นปีที่" และ "เพศ"
    selected_year: ปีการศึกษาที่ต้องการ
    selected_gender: เพศที่ต้องการ

  Returns:
    int: จำนวนนักศึกษา หรือ 0 ถ้าไม่มีข้อมูลตามที่เลือก
  """

  # กรอง DataFrame ตามปีการศึกษาที่เลือก
  filtered_df = grouped2.loc[grouped2['คุณเป็นนักศึกษาชั้นปีที่'] == selected_year]

  # กรอง DataFrame ตามเพศที่เลือก
  filtered_df = filtered_df.loc[filtered_df['คณะที่คุณกำลังศึกษา'] == selected_faculty]

  # กรอง DataFrame ตามเพศที่เลือก
  filtered_df = filtered_df.loc[filtered_df['เพศ'] == selected_gender]

  # กรณีมีข้อมูล
  if not filtered_df.empty:
      return filtered_df['จำนวนนักศึกษา'].values[0]
  else:  # กรณีไม่มีข้อมูล
      return 0

# รายละเอียดข้อมูล ได้แก้ ชื่อ, และจำนวนข้อมูล
group_names=['ชั้นปีที่ 1 (รหัสนักศึกษาขึ้นต้นด้วย 66)', 'ชั้นปีที่ 2 (รหัสนักศึกษาขึ้นต้นด้วย 65)', 'ชั้นปีที่ 3 (รหัสนักศึกษาขึ้นต้นด้วย 64)', 'ชั้นปีที่ 4 (รหัสนักศึกษาขึ้นต้นด้วย 63)', 'ชั้นปีที่ 5-8 (รหัสนักศึกษาขึ้นต้นด้วย 59-62)'] # ชื่อ group ของ chart นอกสุด
group_size=[sum_by_year[0], sum_by_year[1], sum_by_year[2], sum_by_year[3], sum_by_year[4]] # ค่าภาย

faculties = ["คณะนิติศาสตร์", "คณะพาณิชยศาสตร์และการบัญชี", "คณะรัฐศาสตร์", "คณะเศรษฐศาสตร์", "คณะสังคมสงเคราะห์ศาสตร์", "คณะสังคมวิทยาและมานุษยวิทยา",
           "คณะศิลปศาสตร์", "คณะวารสารศาสตร์และสื่อสารมวลชน", "คณะวิทยาศาสตร์และเทคโนโลยี", "คณะวิศวกรรมศาสตร์", "คณะสถาปัตยกรรมศาสตร์และการผังเมือง",
           "คณะศิลปกรรมศาสตร์", "คณะแพทยศาสตร์", "คณะสหเวชศาสตร์", "คณะทันตแพทยศาสตร์", "คณะพยาบาลศาสตร์", "คณะสาธารณสุขศาสตร์", "คณะเภสัชศาสตร์",
           "คณะวิทยาการเรียนรู้และศึกษาศาสตร์", "วิทยาลัยพัฒนศาสตร์ ป๋วย อึ๊งภากรณ์", "วิทยาลัยนวัตกรรม", "วิทยาลัยสหวิทยาการ", "วิทยาลัยโลกคดีศึกษา", "สถาบันเทคโนโลยีนานาชาติสิรินธร",
           "วิทยาลัยนานาชาติ ปรีดี พนมยงค์", "วิทยาลัยแพทยศาสตร์นานาชาติจุฬาภรณ์", "สถาบันเสริมศึกษาและทรัพยากรมนุษย์", "สถาบันไทยคดีศึกษา", "สถาบันเอเชียตะวันออกศึกษา", "สถาบันภาษา", "สถาบันอาณาบริเวณศึกษา"]
faculty_colors = ['#FFD700', '#FF69B4', '#87CEEB', '#32CD32', '#FFA500', '#800080', '#FF4500', '#008000', '#FF6347', '#00CED1', '#FF8C00', '#4B0082', '#FF0000', '#8A2BE2', '#FF1493', '#228B22', '#FFFF00', '#1E90FF', '#FF00FF', '#00FF00', '#FF7F50', '#FFD700', '#FF69B4', '#87CEEB', '#32CD32', '#FFA500', '#800080', '#FF4500', '#008000', '#FF6347', '#00CED1', '#FF8C00', '#4B0082', '#FF0000', '#8A2BE2', '#FF1493', '#228B22', '#FFFF00', '#1E90FF', '#FF00FF', '#00FF00', '#FF7F50']
faculty_color_dict = {faculty: color for faculty, color in zip(faculties, faculty_colors)}

year_levels = ["1", "2", "3", "4", "5-8"]

genders = ["ชาย", "หญิง", "LGBTQIA+", "ไม่ต้องการระบุ"]
gender_colors = ["#2F63B8", "#E445E9", "#FF3737", "#B6B6B6"]
gender_color_dict = {gender: color for gender, color in zip(genders, gender_colors)}

subgroup_names = [f"ชั้นปีที่ {year}.{faculty}" for year in year_levels for faculty in faculties]
subgroup_size = [faculty_student_count(grouped, f"ชั้นปีที่ {year}", faculty) for year in year_levels for faculty in faculties]

# Create a dictionary mapping each subgroup_name to a color
name_to_color = {name: color for name, color in zip(subgroup_names, faculty_colors)}

subgroup2_names = [f"ชั้นปีที่ {year}.{faculty}.{gender}" for year in year_levels for faculty in faculties for gender in genders]
subgroup2_size = [gender_student_count(grouped, f"ชั้นปีที่ {year}", faculty, gender) for year in year_levels for faculty in faculties for gender in genders]

# กำหนดสีภายใน chart
gender_colors = [gender_color_dict[label.split('.')[-1]] for label in subgroup2_names]
faculty_colors = [faculty_color_dict[label.split('.')[-1]] for label in subgroup_names]

new_color_palette = sns.color_palette("hsv")
# Shuffle the color palette
outsidechartcolor = [new_color_palette[2], new_color_palette[1] ,new_color_palette[3], new_color_palette[4], new_color_palette[5]]
outsidechartcolor = [(r, g, b, 0.8) for r, g, b in outsidechartcolor]

# กำหนดฟังก์ชันสำหรับการระบุจำนวนในแต่ละช่อง chart
def absolute_value(val, total):
    return int(round(val * total / 100))

# สร้างวง donut chart ข้างนอกสุด
fig, ax = plt.subplots(figsize=(29, 12))
ax.axis('equal')
total = sum(group_size)
mypie, texts, autotexts = ax.pie(group_size, radius=1.3, labels=group_names, colors=outsidechartcolor,
                                 autopct=lambda val: f"{absolute_value(val, total):,}" if val != 0 else "", pctdistance=0.878)
plt.setp(mypie, width=0.5, edgecolor='white')

# Create the donut chart with custom colors
mypie2, texts2, autotexts2 = ax.pie(subgroup_size, radius=1.3-0.3, colors=faculty_colors,
                                   autopct=lambda val: f"{absolute_value(val, total):,}" if val != 0 else "", pctdistance=0.85)
plt.setp(mypie2, width=0.4, edgecolor='white')
plt.margins(0, 0)

# สร้างวง donut chart ข้างใน
total_sub = sum(subgroup2_size)
mypie3, texts3, autotexts3 = ax.pie(subgroup2_size, radius=1.3-0.3-0.3, colors=gender_colors,
                                   autopct=lambda val: f"{absolute_value(val, total):,}" if val > 0.5 else "", pctdistance=0.77)
plt.setp(mypie3, width=0.3, edgecolor='white')
plt.margins(0, 0)


# กำหนดตำแหน่งของ legends
legend1_loc = "lower left"
legend2_loc = "upper left"

# กำหนดขนาดของกล่องข้อความ
bbox_to_anchor = (0.0, 0.0, 0.5, 0.5)

# กำหนดขนาดของตัวอักษร
fontsize = 10

# กำหนดสไตล์ของเส้นขอบ
handlelength = 0.5
borderpad = 0.3

# Create handles and labels for each faculty
handles = []
labels = []
for faculty, color in zip(faculties, faculty_colors):
    handles.append(matplotlib.patches.Patch(color=color, label=faculty))
    labels.append(faculty)

# เพิ่ม legends
lgnd1 = plt.legend(handles, labels, loc=legend1_loc, bbox_to_anchor=bbox_to_anchor, fontsize=fontsize,
          handlelength=handlelength, borderpad=borderpad)

handles2 = []
labels2 = []
for gender, color in zip(genders, gender_colors):
    handles2.append(matplotlib.patches.Patch(color=color, label=gender))
    labels2.append(gender)

# เพิ่ม legends
lgnd2 = plt.legend(handles2, labels2, loc=legend2_loc, fontsize=fontsize,
          handlelength=handlelength, borderpad=borderpad)

ax.add_artist(lgnd1)
ax.add_artist(lgnd2)

ax.set_title('แนวโน้มสัดส่วนประชากรผู้ตอบแบบสอบถามในแต่ละชั้นปี', pad=30, fontsize=15)

# แสดงผลลัพธ์
donut = plt.show()

"""#4. Word Cloud แสดงปัจจัยที่สำคัญของนักศึกษาในการเลือกซื้อสินค้าและบริการ"""

data = df['อะไรคือปัจจัยสำคัญของคุณในการตัดสินใจเลือกใช้จ่ายสินค้าและบริการ']
text = ''
for row in data:       # ให้ python อ่านข้อมูลรีวิวจากทุก row ของ data
    text = text + row.lower() + ' ' # เก็บข้อมูลรีวิวของเราทั้งหมดเป็น String ในตัวแปร text
fixed_text = {'/' : '',
              '(' : '',
              ')' : '',
              '-' : '',
              ',' : '',
              'สินค้า' : '',
              'บริการ' : '',
              'ซื้อ' : '',
              'ดู' : '',
              'รูปลักษณื': 'รูปลักษณ์',
              'แะ' : 'และ',
              'คสาม' : 'ความ',
              'หิว' : 'ความต้องการ',
              'กิเลส' : 'ความต้องการ',
              'ปัจจัย4' : 'ความต้องการ',
              'ความอยากได้' : 'ความต้องการ',
              'ความอยาก' : 'ความต้องการ',
              'ความอยากได้ต่อสินค้า' : 'ความต้องการ',
              'อยากได้' : 'ความต้องการ',
              'ความจำเป็นของสินค้า' : 'ความจำเป็น',
              'จำเป็น' : 'ความจำเป็น',
              'ต้องมี' : 'ความจำเป็น',
              'ความพอใจ' : 'ความคุ้มค่า',
              'ดี' : 'ความคุ้มค่า',
              'ราคาของสินค้า' : 'ราคา',
              'ถูก' : 'ราคา',
              'ชอบ' : 'ความชอบ',
              'เหมาะสม' : 'ความเหมาะสม'
              }
for old_word, new_word in fixed_text.items():
    text = text.replace(old_word, new_word)
wt = word_tokenize(text, engine='multi_cut', keep_whitespace=False) # ตัดคำที่ได้จากตัวแปร text
path = 'thsarabunnew-webfont.ttf' # ตั้ง path ไปหา font ที่เราต้องการใช้แสดงผล
wordcloud = WordCloud(
                      font_path=path, # font ที่เราต้องการใช้ในการแสดงผล
                      stopwords=thai_stopwords(), # stop words ที่ใช้ซึ่งจะโดนตัดออกและไม่แสดงบน words cloud
                      relative_scaling=0.3,
                      min_font_size=1,
                      background_color = "#F4EDDA",
                      width=1000,
                      height=800,
                      max_words=8, # จำนวนคำที่เราต้องการจะแสดงใน Word Cloud
                      colormap='hsv',
                      scale=3,
                      font_step=4,
                      collocations=False,
                      regexp=r"[ก-๙a-zA-Z']+", # Regular expression to split the input text into token
                      margin=2,
                      contour_width=2, # Add this line
                      contour_color='black' # Add this line
                      ).generate(' '.join(wt)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string
fig, ax= plt.subplots(1, 1, figsize=(8, 8))
fig.patch.set_facecolor("#F4EDDA")
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
ax.set_title('ปัจจัยสำคัญในการเลือกซื้อสินค้าและบริการ', color='white', fontsize=24, bbox={'facecolor': '#153d52', 'alpha': 1, 'pad': 2, 'boxstyle': 'round,pad=0.5'}, y=1.05)
fig.show()

"""#5. Word Cloud แสดงสาเหตุของคนที่เคยเผชิญปัญหาทางการเงิน"""

targetColumn = 'เพราะเหตุใด คุณถึงเคย/ไม่เคยเผชิญปัญหาทางการเงิน'

selectRowTrue = df[df['คุณเคยเผชิญปัญหาทางการเงินหรือไม่?'] == True]

# สี
background_color = '#F4EDDA'
colors = ['#96312e', '#d1675a', '#ffbf6b', '#398eb2', '#153d52']
def color_func(word, font_size, position, orientation, **kwargs):
    return colors[position[0] % len(colors)]

# คำ
spendingTooMuch = ["เกิน","ชาบู","เกินไป","มากเกินไป","หักห้ามใจ","ฟุ่มเฟือย","Shopee","เกินตัว","ฟุ่ม","เพลิน","โลภ","ระงับ","คำนึงถึง","กิเลส","ห้ามใจ","ใช้ชีวิต","สอดคล้องกัน","ลืมตัว","อยากได้","ลืม","เยอะ","วู่วาม","ความจำเป็น",]
manageMoney = ["บริหาร","คำนวณ","หมุนเงิน","การวางแผน","การบริหาร","วางแผนการ","จด","จัด","เป็นระบบ","การออม","จัดสรร","วางแผน","จัดสรรเงิน","จัดการ","หมด","หาเงิน",]
moneyNotEnough = ["เงินไม่พอ","พอใช้","พอ","จำกัด","มีจำกัด","มากกว่า","น้อยกว่า","น้อยกว่า","จำเป็นต้อง","ค่าเดินทาง","กว่า","มีเงิน","จน",]
highCostOfLiving = ["ค่าครองชีพ","แพง","มีราคา",]
familyProblem = ["ครอบครัว","ผู้ปกครอง",]
society = ["เพื่อน"]
emergency = ["เหตุฉุกเฉิน","ฉุกเฉิน","นอกเหนือ","บาง","ตั้งตัว","ควบคุม","สุขภาพ"]
problem = ["การงาน","ตรง",]

word_cloud_filter = []
for str in selectRowTrue[targetColumn]:
  word_array = word_tokenize(str, engine='newmm')
  key_word = []
  for word in word_array:
    if word in spendingTooMuch:
      key_word.append("ใช้จ่ายเกินตัว")
    if word in highCostOfLiving:
      key_word.append("มีค่าครองชีพที่สูง")
    if word in moneyNotEnough:
      key_word.append("มีรายได้น้อย")
    if word in manageMoney:
      key_word.append("บริหารเงินไม่ดี")
    if word in familyProblem:
      key_word.append("มีปัญหาครอบครัว")
    if word in society:
      key_word.append("มีปัญหาสังคม")
    if word in problem:
      key_word.append("มีปัญหาจากปัจจัยภายนอก")
    if word in emergency:
      key_word.append("มีค่าใช้จ่ายฉุกเฉิน")
  word_cloud_filter.extend(list(set(key_word)))
  # print("key : ",list(set(key_word)),"------>",word_array,)
print("word_cloud_filter : ",word_cloud_filter)

word_counts_true = Counter(word_cloud_filter)
print(word_counts_true)

path = 'thsarabunnew-webfont.ttf' # ตั้ง path ไปหา font ที่เราต้องการใช้แสดงผล
wordcloudTrue = WordCloud(
                      font_path=path, # font ที่เราต้องการใช้ในการแสดงผล
                      stopwords=thai_stopwords(), # stop words ที่ใช้ซึ่งจะโดนตัดออกและไม่แสดงบน words cloud
                      relative_scaling=0,
                      min_font_size=1,
                      background_color = "#F4EDDA",
                      width=1000,
                      height=800,
                      max_words=20, # จำนวนคำที่เราต้องการจะแสดงใน Word Cloud
                      colormap='hsv',
                      scale=1,
                      font_step=2,
                      collocations=False,
                      regexp=r"[ก-๙a-zA-Z']+", # Regular expression to split the input text into token
                      margin=2,
                      contour_width=2, # Add this line
                      contour_color='black' # Add this line
                      ).generate(' '.join(wt)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string

# .generate(' '.join(word_cloud_filter)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string
wordcloudTrue.generate_from_frequencies(word_counts_true)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.patch.set_facecolor("#F4EDDA")
ax.imshow(wordcloudTrue, interpolation='bilinear')
ax.axis("off")
ax.set_title('เคยเผชิญปัญหาทางการเงิน', color='white', fontsize=24, bbox={'facecolor': '#153d52', 'alpha': 1, 'pad': 2, 'boxstyle': 'round,pad=0.5'}, y=1.05)
fig.show()

"""#6. แผนภูมิแท่ง แสดงจำนวนนักศึกษาแต่ละชั้นปีตามค่าใช้จ่ายเฉลี่ยในแต่ละวัน"""

# นับจำนวนข้อมูลในแต่ละกลุ่ม
grouped_6 = df.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?"]).size().reset_index(name="จำนวนนักศึกษา")

# สร้าง dictionary เก็บลำดับใหม่
reorder_map = {
    "ชั้นปีที่ 1": 0,
    "ชั้นปีที่ 2": 1,
    "ชั้นปีที่ 3": 2,
    "ชั้นปีที่ 4": 3,
    "ชั้นปีที่ 5-8": 4
}

# รวมชั้นปีที่ 5 ถึง 8
grouped_6['คุณเป็นนักศึกษาชั้นปีที่'] = grouped_6['คุณเป็นนักศึกษาชั้นปีที่'].replace(['ชั้นปีที่ 5', 'ชั้นปีที่ 6', 'ชั้นปีที่ 7', 'ชั้นปีที่ 8'], 'ชั้นปีที่ 5-8')

# นับจำนวนนักศึกษาใหม่
grouped_6 = grouped_6.groupby(["คุณเป็นนักศึกษาชั้นปีที่", "คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?"]).agg({'จำนวนนักศึกษา': 'sum'}).reset_index()

# เพิ่มคอลัมน์ลำดับใหม่
grouped_6["ลำดับ"] = grouped_6["คุณเป็นนักศึกษาชั้นปีที่"].map(reorder_map)

# เรียงลำดับตามคอลัมน์ "ลำดับ"
grouped_6 = grouped_6.sort_values(by="ลำดับ").drop(columns=["ลำดับ"])

# แสดงผล
grouped_6

del str

# สร้างกราฟแท่ง
plt.figure(figsize=(12, 8), facecolor='lightgrey')

# กำหนดสีแต่ละกลุ่ม
colors_6 = sns.color_palette("hsv")

# สร้างกราฟแท่ง
for i, (ค่าใช้จ่าย, group6) in enumerate(grouped_6.groupby("คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?")):
    plt.bar(group6["คุณเป็นนักศึกษาชั้นปีที่"], group6["จำนวนนักศึกษา"], label=ค่าใช้จ่าย, color=colors_6[i], edgecolor='blue', alpha=0.8)
    # เพิ่มจำนวนคนลงบนกราฟ
    for x, y in zip(group6["คุณเป็นนักศึกษาชั้นปีที่"], group6["จำนวนนักศึกษา"]):
      plt.text(x, y, str(y), ha="center", va="bottom")

# เพิ่มป้ายชื่อและตกแต่งกราฟ
plt.xlabel('ชั้นปี')
plt.ylabel('จำนวนนักศึกษา (คน)')
plt.title('จำนวนนักศึกษาในแต่ละชั้นปีตามค่าใช้จ่ายเฉลี่ยต่อวัน')
plt.legend()

# แสดงกราฟ
plt.show()

"""# Dashboard"""

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Number of students in each year according to average daily expenses')
    # สร้างกราฟแท่ง
    plt.figure(figsize=(12, 8), facecolor='lightgrey')

    # กำหนดสีแต่ละกลุ่ม
    colors_6 = sns.color_palette("hsv")

    # สร้างกราฟแท่ง
    for i, (ค่าใช้จ่าย, group6) in enumerate(grouped_6.groupby("คุณใช้จ่ายเงินเฉลี่ยเท่าไหร่ต่อวันในมหาวิทยาลัย ?")):
        plt.bar(group6["คุณเป็นนักศึกษาชั้นปีที่"], group6["จำนวนนักศึกษา"], label=ค่าใช้จ่าย, color=colors_6[i], edgecolor='blue', alpha=0.8)
        # เพิ่มจำนวนคนลงบนกราฟ
        for x, y in zip(group6["คุณเป็นนักศึกษาชั้นปีที่"], group6["จำนวนนักศึกษา"]):
          plt.text(x, y, str(y), ha="center", va="bottom")

    # เพิ่มป้ายชื่อและตกแต่งกราฟ
    plt.xlabel('ชั้นปี')
    plt.ylabel('จำนวนนักศึกษา (คน)')
    plt.title('จำนวนนักศึกษาในแต่ละชั้นปีตามค่าใช้จ่ายเฉลี่ยต่อวัน')
    plt.legend()

    # แสดงกราฟ
    plt.show()

with col[1]:
    st.markdown('#### Important factors in choosing products and services')

    path = 'thsarabunnew-webfont.ttf' # ตั้ง path ไปหา font ที่เราต้องการใช้แสดงผล
    wordcloud = WordCloud(
                          font_path=path, # font ที่เราต้องการใช้ในการแสดงผล
                          stopwords=thai_stopwords(), # stop words ที่ใช้ซึ่งจะโดนตัดออกและไม่แสดงบน words cloud
                          relative_scaling=0.3,
                          min_font_size=1,
                          background_color = "#F4EDDA",
                          width=1000,
                          height=800,
                          max_words=8, # จำนวนคำที่เราต้องการจะแสดงใน Word Cloud
                          colormap='hsv',
                          scale=3,
                          font_step=4,
                          collocations=False,
                          regexp=r"[ก-๙a-zA-Z']+", # Regular expression to split the input text into token
                          margin=2,
                          contour_width=2, # Add this line
                          contour_color='black' # Add this line
                          ).generate(' '.join(wt)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    fig.patch.set_facecolor("#F4EDDA")
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    ax.set_title('ปัจจัยสำคัญในการเลือกซื้อสินค้าและบริการ', color='white', fontsize=24, bbox={'facecolor': '#153d52', 'alpha': 1, 'pad': 2, 'boxstyle': 'round,pad=0.5'}, y=1.05)
    fig.show()

    st.markdown('#### Total Population')

    word_counts_true = Counter(word_cloud_filter)
    print(word_counts_true)

    path = 'thsarabunnew-webfont.ttf' # ตั้ง path ไปหา font ที่เราต้องการใช้แสดงผล
    wordcloudTrue = WordCloud(
                              font_path=path, # font ที่เราต้องการใช้ในการแสดงผล
                              stopwords=thai_stopwords(), # stop words ที่ใช้ซึ่งจะโดนตัดออกและไม่แสดงบน words cloud
                              relative_scaling=0,
                              min_font_size=1,
                              background_color = "#F4EDDA",
                              width=1000,
                              height=800,
                              max_words=20, # จำนวนคำที่เราต้องการจะแสดงใน Word Cloud
                              colormap='hsv',
                              scale=1,
                              font_step=2,
                              collocations=False,
                              regexp=r"[ก-๙a-zA-Z']+", # Regular expression to split the input text into token
                              margin=2,
                              contour_width=2, # Add this line
                              contour_color='black' # Add this line
                              ).generate(' '.join(wt)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string

    # .generate(' '.join(word_cloud_filter)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string
    wordcloudTrue.generate_from_frequencies(word_counts_true)

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    fig.patch.set_facecolor("#F4EDDA")
    ax.imshow(wordcloudTrue, interpolation='bilinear')
    ax.axis("off")
    ax.set_title('เคยเผชิญปัญหาทางการเงิน', color='white', fontsize=24, bbox={'facecolor': '#153d52', 'alpha': 1, 'pad': 2, 'boxstyle': 'round,pad=0.5'}, y=1.05)
    fig.show()