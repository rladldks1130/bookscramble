import streamlit as st
import random
import pandas as pd
import time

@st.cache
def load_books():
    df = pd.read_excel("https://github.com/rladldks1130/bookscramble/raw/main/book_list.xlsx")
    return df['Book Titles'].tolist()

book_list = load_books()

st.markdown(f"<h2 style='font-size: 70px;'> 북스크램블 </h2>", unsafe_allow_html=True)

if "start" not in st.session_state:
    st.session_state.start = False
    st.session_state.current_index = 0
    st.session_state.quiz_book = []
    st.session_state.score = 0

if st.button("start"):
    st.session_state.start = True
    st.session_state.quiz_book = random.sample(book_list, 10)
    st.session_state.current_index = 0
    st.session_state.score = 0

if st.session_state.start:
    if st.session_state.current_index < 10:
        book = st.session_state.quiz_book[st.session_state.current_index].replace(" ", "")
        scramble = random.sample(book, len(book))
        quiz = " ".join(scramble)
        st.markdown(f"<h2 style='font-size: 24px;'>문제 {st.session_state.current_index + 1}: {quiz}</h2>", unsafe_allow_html=True)
        
        current_time = int(time.time())  # 현재 시간을 기반으로 키 생성
        answer = st.text_input("정답을 입력하세요:", key=f"input{current_time}")

        if st.button("정답 제출", key=f"submit{current_time}"):
            answer = answer.replace(" ", "")
            if answer == book:
                st.session_state.score += 1
                st.markdown(f"<h3 style='font-size: 20px;'>정답입니다! {st.session_state.score}/10</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 style='font-size: 20px;'>오답입니다! {st.session_state.score}/10</h3>", unsafe_allow_html=True)

            if st.session_state.current_index < 9:
                st.session_state.current_index += 1
                time.sleep(1)
                st.experimental_rerun()
            else:
                if st.session_state.score >= 7:
                    st.balloons()
                st.markdown(f"<h3 style='font-size: 24px;'>총 {st.session_state.score}문제 맞췄습니다. {'' if st.session_state.score >= 7 else '실패'}입니다!</h3>", unsafe_allow_html=True)
                st.session_state.start = False  # 게임 종료
