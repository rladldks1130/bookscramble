import streamlit as st
import random
import pandas as pd  # 엑셀 파일을 읽기 위해 pandas 사용
import time

# 엑셀 파일에서 책 목록 불러오기
@st.cache_data
def load_books():
    # 엑셀 파일에서 데이터를 읽고, 'Book Titles'라는 컬럼을 리스트로 변환
    df = pd.read_excel("book_list.xlsx")
    return df['Book Titles'].tolist()

# 책 목록 불러오기
book_list = load_books()

st.title("북스크램블")

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
	st.session_state.quiz_book = random.sample(book_list, 10)  # 엑셀에서 불러온 책 목록 중 10개 샘플
	st.session_state.current_index = 0
	st.session_state.score = 0
	st.session_state.key_suffix = 0  # 게임을 시작할 때 key_suffix를 0으로 초기화합니다.
	answer = ""

if st.session_state.start:
	if st.session_state.current_index < 10:
		# 현재 문제
		book = st.session_state.quiz_book[st.session_state.current_index].replace(" ", "")
		scramble = random.sample(book, len(book))
		quiz = " ".join(scramble)
		st.write(f"문제 {st.session_state.current_index + 1}: {quiz}")

		# 사용자 입력 받기
		answer = st.text_input("정답을 입력하세요:", key=f"input{st.session_state.current_index}{st.session_state.key_suffix}")

		# 정답 제출 버튼
	if st.button("정답 제출", key=f"submit{st.session_state.current_index}"):
		answer = answer.replace(" ", "")
		if answer == book:
			st.session_state.score += 1
			st.success(f"정답입니다! {st.session_state.score}/10")
		else:
			st.error(f"오답입니다! {st.session_state.score}/10")

		# 다음 문제로 넘어가기 전에 인덱스와 key_suffix를 증가시킨 후 1초 대기
		if st.session_state.current_index < 9:
			st.session_state.current_index += 1
			st.session_state.key_suffix += 1  # key_suffix를 증가시킵니다.
			time.sleep(1)
			st.rerun()  # 인덱스를 증가시킨 후 페이지 다시 로드
		else:
			if st.session_state.score >= 7:
				st.balloons()
				st.success(f"총 {st.session_state.score}문제 맞췄습니다. 통과입니다!")
			else:
				st.error(f"총 {st.session_state.score}문제 맞췄습니다. 실패입니다")
			st.session_state.start = False  # 게임 종료
