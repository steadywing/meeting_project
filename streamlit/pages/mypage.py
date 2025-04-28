import streamlit as st 
from streamlit_calendar import calendar

#================================================
# 1. 사용자 정보
#================================================
meeting_info = st.session_state.meeting_info
name = meeting_info["name"]
department = meeting_info["department"]
st.title(f"{name}({department})")

#================================================
# 2. To Do List
#================================================
st.subheader("내가 할 일")

for todo in st.session_state.todo_value:
    st.checkbox(todo)

#================================================
# 3. Calendar
#================================================
st.divider()

schedule_data = st.session_state.edited_schedule_data
# 캘린더 컴포넌트 띄우기
event = calendar(
    events=schedule_data.to_dict(orient="records"),
    options={
        "editable": False,
        "selectable": False,
        "eventTimeFormat": {
            "hour": "2-digit",
            "minute": "2-digit",
            "meridiem": False  # 오전/오후(a/p) 없이 24시간제 표시
        }
    },
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """
)

st.dataframe(
    data=st.session_state.schedule_data,
    hide_index=True
)