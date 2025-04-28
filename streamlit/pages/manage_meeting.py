# streamlit/main.py
import streamlit as st
from streamlit_calendar import calendar
import tempfile
import pandas as pd
import datetime

# 내가 만든 모듈 불러오기
from services.whisper_service import model, transcribe_audio
from services.prompt_service import summary_chain, todo_chain, schedule_chain
#================================================
# 1. 제목
#================================================
st.title("📝 회의록 관리 시스템")

#================================================
# 2. File Uploader 
#================================================
uploaded_file = st.file_uploader(
    "회의 음성 파일(mp3, wav)을 업로드하세요.", 
    type=["mp3", "wav"],
    key="upload_file"
)

if uploaded_file is not None:
    filename = uploaded_file.name
    if filename.endswith("wav"):
        suffix = ".wav"
    elif filename.endswith("mp3"):
        suffix = ".mp3"
    
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    st.success("파일 업로드 완료!")

#================================================
# 3. 회의 정보 입력
#================================================
with st.expander(label="👥 회의 정보", expanded=True):
    col1, col2 = st.columns(2)
    name = col1.text_input(label="담당자 이름", value="김나래")
    department = col2.text_input(label="담당자 부서명", value="개발팀")
    meeting_date = st.date_input(label="회의 날짜", value=datetime.date(2025, 4, 22))

    st.session_state.meeting_info = {
        "name": name,
        "department": department,
        "meeting_date": meeting_date.strftime(format="%Y-%m-%d %A")
    }

#================================================
# 4. 버튼 만들기
#================================================
col1, col2, col3, col4 = st.columns(4)

stt_button = col1.button(label="🎙️ 음성 텍스트 변환", use_container_width=True, type="primary")
if stt_button:
    st.session_state.stt_expander=True
    st.session_state.summary_expander=False
    st.session_state.todo_expander=False
    st.session_state.schedule_expander=False

summary_button = col2.button(label="📝 회의록 요약", use_container_width=True, type="primary")
if summary_button:
    st.session_state.stt_expander=False
    st.session_state.summary_expander=True
    st.session_state.todo_expander=False
    st.session_state.schedule_expander=False

todo_button = col3.button(label="✅ To Do List 생성", use_container_width=True, type="primary")
if todo_button:
    st.session_state.stt_expander=False
    st.session_state.summary_expander=False
    st.session_state.todo_expander=True
    st.session_state.schedule_expander=False

schedule_button = col4.button(label="📅 일정 추출", use_container_width=True, type="primary")
if schedule_button:
    st.session_state.stt_expander=False
    st.session_state.summary_expander=False
    st.session_state.todo_expander=False
    st.session_state.schedule_expander=True

#================================================
# 5. 컨테이너 만들기
#================================================
# 5-1. 음성 텍스트 변환
with st.expander(label="1️⃣ 음성 텍스트 변환", expanded=st.session_state.stt_expander):
    if stt_button and st.session_state.upload_file:
        with st.spinner(text="음성을 텍스트로 변환 중입니다."):
            st.session_state.stt_value = transcribe_audio(
                model=model,
                file_path=tmp_file_path
            )
    
    st.text_area(
        label="회의록",
        value=st.session_state.stt_value,
        height=300
    )
    script_download = st.download_button(
        label="회의록 스크립트 다운로드",
        data=st.session_state.stt_value,
        file_name="meeting_transcript.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary"
    )
#------------------------------------------------
# 5-2. 희의록 요약
with st.expander(label="2️⃣ 회의록 요약", expanded=st.session_state.summary_expander):
    if summary_button and st.session_state.upload_file:
        with st.spinner(text="회의록을 요약 중입니다."):
            st.session_state.summary_value = summary_chain.invoke(
                {"meeting_transcript": st.session_state.stt_value}
            )

    st.text_area(
        label="희외록 요약",
        value = st.session_state.summary_value,
        height=300
    )
    summary_download = st.download_button(
        label="요약된 회의록 다운로드",
        data=st.session_state.summary_value,
        file_name="meeting_summary.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary"
    )
#------------------------------------------------
# 5-3. To Do List 생성
with st.expander(label="3️⃣ To Do List", expanded=st.session_state.todo_expander):
    if todo_button and st.session_state.upload_file:
        with st.spinner(text="To do List를 추출 입니다."):
            st.session_state.todo_value = todo_chain.invoke(
                {
                    "meeting_info": st.session_state.meeting_info,
                    "meeting_transcript": st.session_state.stt_value
                }
            )
    
    # 기존 할 일 수정
    text = ""
    for todo in st.session_state.todo_value:
        text += f"- {todo}\n"
        # st.checkbox(todo)
    st.text_area(label="To-Do List", value=text)
#------------------------------------------------
# 5-4. 일정 추출 및 등록
with st.expander(label="4️⃣ 일정 추출", expanded=st.session_state.schedule_expander):
    if schedule_button and st.session_state.upload_file:
        with st.spinner(text="일정을 추출 입니다."):
            schedule_list = schedule_chain.invoke(
                {
                    "meeting_info": st.session_state.meeting_info,
                    "meeting_transcript": st.session_state.stt_value
                }
            )
            st.session_state.schedule_data = pd.DataFrame(schedule_list)
    
    st.session_state.edited_schedule_data = st.data_editor(
        data=st.session_state.schedule_data,
        hide_index=True
    )
    enroll = st.button(
        label="일정 등록",
        use_container_width=True,
        type="primary"
    )
    if enroll:
        st.session_state.schedule_expander=True
        st.success("✅ 일정 등록이 완료되었습니다.")
