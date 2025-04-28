# 실행 streamlit streamlit_basic.py
import streamlit as st 

# -------------------------
# 1. Session State
# -------------------------
st.title("Session State 예제")

if 'count' not in st.session_state:
    st.session_state['count'] = 0

if st.button('세션 카운트 증가'):
    st.session_state['count'] += 1

st.write(f"현재 카운트: {st.session_state['count']}")

st.divider()

# -------------------------
# 2. Title, Write, Text Input, Text Area
# -------------------------
st.title("기본 출력 예제")

name = st.text_input("이름을 입력하세요:")
comment = st.text_area("하고 싶은 말을 적어주세요:")

st.write(f"**입력한 이름:** {name}")
st.write(f"**남긴 말:** {comment}")

st.divider()

# -------------------------
# 3. Checkbox, Button
# -------------------------
st.title("Checkbox와 Button 예제")

agree = st.checkbox("~~위 내용을 확인했습니다.~~")

if agree:
    if st.button("제출하기"):
        st.success("제출이 완료되었습니다!")

st.divider()

# -------------------------
# 4. Container, Expander, Columns
# -------------------------
st.title("Container, Expander, Columns 예제")

with st.container():
    st.write("여기는 컨테이너 안입니다.")

with st.expander("더 많은 정보 보기"):
    st.write("이곳은 확장 가능한 영역입니다.")

col1, col2 = st.columns(2)

with col1:
    st.write("왼쪽 칸입니다.")

with col2:
    st.write("오른쪽 칸입니다.")

st.divider()

# -------------------------
# 5. Success, Error 메시지
# -------------------------
st.title("Success와 Error 메시지 예제")

st.success("처리가 성공했습니다!")
st.error("문제가 발생했습니다. 다시 시도하세요.")

# -------------------------
# 6. File Uploader
# -------------------------
st.title("파일 업로더 예제")

uploaded_file = st.file_uploader("파일을 업로드하세요", type=["txt", "wav", "mp3"])

if uploaded_file is not None:
    st.success(f"업로드된 파일 이름: {uploaded_file.name}")
    # 파일 타입에 따라 다르게 처리 가능
    if uploaded_file.type.startswith("text/"):
        content = uploaded_file.read().decode("utf-8")
        st.text_area("파일 내용", content, height=200)
    else:
        st.write("음성 파일이 업로드되었습니다!")

# -------------------------
# 7. Calendar
# -------------------------
st.title("파일 업로더 예제")

from streamlit_calendar import calendar

event_data = [
  {
     "title": "프로젝트 기간",
     "start": "2025-05-01T10:00:00",
     "end": "2025-05-05T11:00:00",
     "allDay": True
  },
  {
     "title": "회의",
     "start": "2025-05-02T10:00:00",
     "end": "2025-05-02T11:00:00",
     "allDay": False
  }
]

event = calendar(
    events=event_data,
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