# -*- coding: utf-8 -*-
# @Project: webframework_wenfengyang
# @Date    : 2021/6/7
# @Author  : Wenfeng
# @FileName: test_plotly.py
# @contact : wenfengyangchn@gmail.com

import plotly.express as px

df = px.data.gapminder().query("continent != 'Asia'") # remove Asia for visibility
fig = px.line(df, x="year", y="lifeExp", color="continent",
              line_group="country", hover_name="country")
fig.show()
