import streamlit as st
import random
import time

# 책 목록
book_list = [r"C:\Python_Project\bookscramble\book_list.xlsx"]

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
	st.session_state.quiz_book = random.sample(book_list, 10)
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
		if answer == st.session_state.quiz_book[st.session_state.current_index]:
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
			st.write(f"{st.session_state.score}/10")
			if st.session_state.score >= 7:
				st.balloons()
				st.success(f"총 {st.session_state.score}문제 맞췄습니다. 통과입니다!")
			else:
				st.error(f"총 {st.session_state.score}문제 맞췄습니다. 실패입니다")
			st.session_state.start = False  # 게임 종료
