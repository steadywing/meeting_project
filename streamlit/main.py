# streamlit/main.py
import streamlit as st
import pandas as pd

# print(st.session_state)
#================================================
# 0. Session State 초기화
#================================================
if "stt_expander" not in st.session_state:
    st.session_state.stt_expander = False
if "summary_expander" not in st.session_state:
    st.session_state.summary_expander = False
if "todo_expander" not in st.session_state:
    st.session_state.todo_expander = False
if "schedule_expander" not in st.session_state:
    st.session_state.schedule_expander = False

if "meeting_info" not in st.session_state:
    st.session_state.meeting_info = None   

if "stt_value" not in st.session_state:
    st.session_state.stt_value = ""
if "summary_value" not in st.session_state:
    st.session_state.summary_value = ""
if "todo_value" not in st.session_state:
    st.session_state.todo_value = ""
if "schedule_data" not in st.session_state:
    columns = ["title","start","end","allDay"]
    st.session_state.schedule_data = pd.DataFrame(columns=columns)
#================================================
# 1. 사이드 바 만들기
#================================================
pages = [
    st.Page("pages/manage_meeting.py", title="회의록 관리", icon=":material/group:", default=True),
    st.Page("pages/mypage.py", icon=":material/calendar_month:", title="마이페이지"),
    st.Page("pages/streamlit_basic.py", icon=":material/search:", title="Streamlit 예제"),
]

pg = st.navigation(pages)
pg.run()

