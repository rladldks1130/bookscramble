import streamlit as st
import random
import pandas as pd  # 엑셀 파일을 읽기 위해 pandas 사용
import time

# 엑셀 파일에서 책 목록 불러오기
@st.cache_data
def load_books():
    # 엑셀 파일에서 데이터를 읽고, 'Book Titles'라는 컬럼을 리스트로 변환
    df = pd.read_excel("https://github.com/rladldks1130/bookscramble/raw/main/book_list.xlsx")
    return df['Book Titles'].tolist()

# 책 목록 불러오기
book_list = load_books()

st.markdown(f"<h2 style='font-size: 70px;'> 북스크램블 </h2>", unsafe_allow_html=True)

# 세션 상태 초기화
if "start" not in st.session_state:
	st.session_state.start = False
	st.session_state.current_index = 0
	st.session_state.quiz_book = []
	st.session_state.score = 0
	st.session_state.key_suffix = 0  # key_suffix를 추가합니다.

# 시작 버튼
if st.button("start"):
	st.session_state.start = True
	st.session_state.quiz_book = random.sample(book_list, 5)  # 엑셀에서 불러온 책 목록 중 10개 샘플
	st.session_state.current_index = 0
	st.session_state.score = 0
	st.session_state.key_suffix = 0  # 게임을 시작할 때 key_suffix를 0으로 초기화합니다.
	answer = ""

if st.session_state.start:
	if st.session_state.current_index < 5:
		# 현재 문제
		book = st.session_state.quiz_book[st.session_state.current_index].replace(" ", "")
		scramble = random.sample(book, len(book))
		quiz = " ".join(scramble)
		st.markdown(f"<h2 style='font-size: 35px;'>문제 {st.session_state.current_index + 1}: {quiz}</h2>", unsafe_allow_html=True)

		# 사용자 입력 받기
		answer = st.text_input("정답을 입력하세요:", placeholder=None, key=f"input{st.session_state.current_index}{st.session_state.key_suffix}")

		# 정답 제출 버튼
	if st.button("정답 제출", key=f"submit{st.session_state.current_index}"):
		answer = answer.replace(" ", "")
		if answer == book:
			st.session_state.score += 1
			st.markdown(f"<h3 style='font-size: 25px;'>정답입니다! {st.session_state.score}/10</h3>", unsafe_allow_html=True)
		else:
			st.markdown(f"<h3 style='font-size: 25px;'>오답입니다! {st.session_state.score}/10</h3>", unsafe_allow_html=True)

		# 다음 문제로 넘어가기 전에 인덱스와 key_suffix를 증가시킨 후 1초 대기
		if st.session_state.current_index < 4:
			st.session_state.current_index += 1
			st.session_state.key_suffix += 1  # key_suffix를 증가시킵니다.
			time.sleep(1)
			st.rerun()  # 인덱스를 증가시킨 후 페이지 다시 로드
		else:
			if st.session_state.score >= 3:
				st.balloons()
				st.markdown(f"<h3 style='font-size: 24px;'>총 {st.session_state.score}문제 맞췄습니다. 통과입니다!</h3>", unsafe_allow_html=True)
			else:
				st.markdown(f"<h3 style='font-size: 24px;'>총 {st.session_state.score}문제 맞췄습니다. 실패입니다</h3>", unsafe_allow_html=True)
			st.session_state.start = False  # 게임 종료
