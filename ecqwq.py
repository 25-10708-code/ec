import streamlit as st
from openai import OpenAI

# 1. 웹 페이지 상단 탭 및 레이아웃 설정
st.set_page_config(page_title="오늘의 감정 영화 추천", page_icon="🎬", layout="centered")

# 2. [필수 수정] 여기에 본인의 OpenAI API 키를 입력하세요!
# 예시: OPENAI_API_KEY = "sk-proj-..." 
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"

# 3. 메인 화면 UI 디자인
st.title("🎬 오늘 어떤 하루를 보내셨나요?")
st.write("오늘 있었던 일을 한두 줄로 가볍게 적어주시면, 지금 감정에 딱 맞는 영화나 드라마를 찾아드릴게요.")
st.divider()

# 사용자 입력 받는 칸
user_diary = st.text_input(
    label="오늘 나의 하루 한 줄 요약", 
    placeholder="예: 오늘 중요한 면접을 망쳐서 너무 우울해...",
    label_visibility="collapsed"
)

# 버튼 클릭 시 작동하는 로직
if st.button("나에게 맞는 작품 추천받기 ✨", use_container_width=True):
    # 입력값이 비어있는 경우
    if not user_diary.strip():
        st.warning("오늘 하루를 아주 짧게라도 입력해 주세요!")
        
    # API 키를 수정하지 않고 그대로 둔 경우
    elif OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":moon
        st.error("코드 내 9번째 줄의 'YOUR_OPENAI_API_KEY_HERE' 부분을 본인의 실제 OpenAI API 키로 변경하셔야 작동합니다.")
        
    # 정상 작동
    else:
        with st.spinner("오늘의 감정을 분석해서 인생작을 고르는 중... 🍿"):
            try:
                # OpenAI 클라이언트 초기화
                client = OpenAI(api_key=OPENAI_API_KEY)
                
                # AI에게 줄 미션 지시사항
                system_instruction = (
                    "당신은 전 세계의 모든 영화와 드라마를 꿰뚫고 있는 다정한 문화 콘텐츠 전문가입니다. "
                    "사용자가 제공한 오늘 하루 일기(감정, 사건)를 깊이 공감하고 분석한 뒤, "
                    "그 감정을 위로해주거나 기쁨을 더해줄 수 있는 영화 또는 드라마를 2~3편 추천해주세요. "
                    "응답은 반드시 깔끔한 마크다운 양식을 사용하여 다음 내용을 포함해야 합니다:\n"
                    "1. 사용자의 감정에 대한 따뜻한 공감 한 줄\n"
                    "2. 추천 작품들의 제목, 유형(영화/드라마), 그리고 '이 작품을 추천하는 명확한 이유'"
                )
                
                # GPT-4o-mini 호출
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": f"사용자의 오늘 하루: {user_diary}"}
                    ],
                    temperature=0.75
                )
                
                # 결과창에 출력
                recommendation = response.choices[0].message.content
                st.success("🎉 분석 완료! 이런 작품들은 어떠신가요?")
                st.markdown(recommendation)
                
            except Exception as e:
                st.error(f"알 수 없는 오류가 발생했습니다. API 키가 만료되었거나 결제가 연동되어 있는지 확인해 주세요. (에러 내용: {e})")

# 하단 푸터 영역
st.caption("Powered by Streamlit & OpenAI GPT-4o-mini")
