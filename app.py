import streamlit as st
from typing import Dict, List

# 기본 설정
st.set_page_config(
    page_title="축구 경기 판단력 테스트",
    page_icon="⚽",
    layout="wide"
)

# 제출자 정보
STUDENT_ID = "2023204043"
STUDENT_NAME = "이시웅"

# 로그인 계정
VALID_ID = "student"
VALID_PW = "1234"

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "login_user" not in st.session_state:
    st.session_state.login_user = ""

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "balloon_shown" not in st.session_state:
    st.session_state.balloon_shown = False


# 캐싱: 퀴즈 데이터 로드
@st.cache_data
def load_quiz_data() -> List[Dict]:
    return [
        {
            "id": 1,
            "question": "우리 팀이 1점 지고 있고 후반 85분입니다. 가장 좋은 공격 판단은?",
            "options": [
                "무조건 멀리서 강슛을 때린다.",
                "공격 숫자를 늘리되, 무리한 개인 플레이보다 패스 선택지를 만든다.",
                "수비수에게 다시 백패스만 한다.",
                "시간이 없으니 아무 방향으로나 크로스한다."
            ],
            "answer": 1,
            "explanation": "막판에는 공격 숫자를 늘리되 무리한 선택보다 확률 높은 찬스를 만드는 판단이 중요합니다.",
            "stat_type": "PASS"
        },
        {
            "id": 2,
            "question": "상대 수비 라인이 높게 올라와 있습니다. 가장 효과적인 공격 방식은?",
            "options": [
                "뒤 공간을 노리는 빠른 침투 패스",
                "천천히 뒤에서만 공 돌리기",
                "골키퍼에게 계속 백패스",
                "수비수 앞에서 멈춰 있기"
            ],
            "answer": 0,
            "explanation": "수비 라인이 높으면 뒷공간이 생기기 때문에 빠른 침투와 패스가 효과적입니다.",
            "stat_type": "PACE"
        },
        {
            "id": 3,
            "question": "페널티 박스 안에서 골키퍼가 앞으로 나왔습니다. 가장 침착한 마무리는?",
            "options": [
                "눈 감고 강하게 슛한다.",
                "골키퍼 위치를 보고 칩슛 또는 빈 공간으로 슛한다.",
                "공을 멈추고 수비수가 올 때까지 기다린다.",
                "무조건 뒤로 패스한다."
            ],
            "answer": 1,
            "explanation": "골키퍼가 나온 상황에서는 빈 공간을 보고 침착하게 마무리하는 판단이 중요합니다.",
            "stat_type": "SHOOT"
        },
        {
            "id": 4,
            "question": "상대가 빠르게 역습을 시작했습니다. 수비수로서 가장 먼저 해야 할 행동은?",
            "options": [
                "무조건 슬라이딩 태클을 한다.",
                "공만 보고 앞으로 튀어나간다.",
                "상대 공격을 지연시키고 패스 길을 막는다.",
                "공격하러 상대 진영으로 올라간다."
            ],
            "answer": 2,
            "explanation": "역습 수비에서는 성급한 태클보다 시간을 벌고 패스 길을 막는 것이 중요합니다.",
            "stat_type": "DEF"
        },
        {
            "id": 5,
            "question": "측면에서 공을 잡았고 중앙에 동료가 침투 중입니다. 가장 좋은 선택은?",
            "options": [
                "무조건 혼자 드리블한다.",
                "동료 움직임에 맞춰 타이밍 좋은 패스를 넣는다.",
                "공을 밖으로 차낸다.",
                "그 자리에서 가만히 멈춘다."
            ],
            "answer": 1,
            "explanation": "좋은 패스는 동료의 움직임과 타이밍을 읽는 판단에서 나옵니다.",
            "stat_type": "PASS"
        },
        {
            "id": 6,
            "question": "상대 수비수와 1대1 상황이고 앞쪽 공간이 열려 있습니다. 가장 효과적인 플레이는?",
            "options": [
                "공간을 활용해 드리블 돌파를 시도한다.",
                "무조건 뒤로만 패스한다.",
                "상대 수비수에게 공을 준다.",
                "공을 멈추고 기다린다."
            ],
            "answer": 0,
            "explanation": "앞 공간이 열려 있다면 드리블 돌파가 좋은 선택이 될 수 있습니다.",
            "stat_type": "DRIBBLE"
        },
        {
            "id": 7,
            "question": "우리 팀이 2대1 역습 기회를 잡았습니다. 가장 확률 높은 선택은?",
            "options": [
                "수비수를 끌어낸 뒤 더 좋은 위치의 동료에게 패스한다.",
                "무조건 혼자 슛한다.",
                "공을 뒤로 돌려 공격을 멈춘다.",
                "상대 수비가 정비될 때까지 기다린다."
            ],
            "answer": 0,
            "explanation": "2대1 상황에서는 수비수를 끌어낸 뒤 패스로 확실한 기회를 만드는 것이 좋습니다.",
            "stat_type": "PASS"
        },
        {
            "id": 8,
            "question": "공격수가 오프사이드 위치에 있지만 공을 건드리지 않고 플레이에 관여하지 않았습니다. 올바른 판단은?",
            "options": [
                "무조건 오프사이드다.",
                "플레이에 관여하지 않았다면 오프사이드가 아닐 수 있다.",
                "골키퍼가 보이면 무조건 반칙이다.",
                "하프라인을 넘었으니 무조건 오프사이드다."
            ],
            "answer": 1,
            "explanation": "오프사이드는 위치뿐 아니라 실제 플레이 관여 여부도 중요합니다.",
            "stat_type": "PASS"
        }
    ]


# 함수
def reset_quiz() -> None:
    st.session_state.quiz_submitted = False
    st.session_state.answers = {}
    st.session_state.current_question = 0
    st.session_state.balloon_shown = False


def logout() -> None:
    st.session_state.logged_in = False
    st.session_state.login_user = ""
    reset_quiz()


def calculate_result(quiz_data: List[Dict], user_answers: Dict[int, int]) -> Dict:
    score = 0
    max_score = len(quiz_data)

    stats = {
        "PACE": 50,
        "SHOOT": 50,
        "PASS": 50,
        "DRIBBLE": 50,
        "DEF": 50
    }

    detailed_results = []

    for q in quiz_data:
        qid = q["id"]
        selected_index = user_answers.get(qid, -1)
        is_correct = selected_index == q["answer"]

        if is_correct:
            score += 1
            stats[q["stat_type"]] += 15
        else:
            stats[q["stat_type"]] += 3

        detailed_results.append({
            "id": qid,
            "question": q["question"],
            "selected": selected_index,
            "correct": q["answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"],
            "options": q["options"],
            "stat_type": q["stat_type"]
        })

    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    top_stat = sorted_stats[0][0]

    if top_stat == "SHOOT":
        style_name = "결정적 순간 해결사형"
        style_desc = "찬스 상황에서 침착하게 마무리하는 능력이 강한 유형입니다."
    elif top_stat == "PASS":
        style_name = "경기 흐름 조율형"
        style_desc = "공간과 동료 움직임을 읽고 팀의 공격 흐름을 만드는 유형입니다."
    elif top_stat == "PACE":
        style_name = "역습 스피드형"
        style_desc = "빠른 판단과 침투로 상대 수비 뒷공간을 노리는 유형입니다."
    elif top_stat == "DRIBBLE":
        style_name = "1대1 돌파형"
        style_desc = "공간이 열렸을 때 직접 돌파로 상황을 바꾸는 유형입니다."
    else:
        style_name = "수비 안정형"
        style_desc = "성급하게 달려들기보다 위치와 공간을 지키는 안정적인 유형입니다."

    accuracy = round((score / max_score) * 100, 1)

    if accuracy >= 87.5:
        grade = "월드클래스"
    elif accuracy >= 75:
        grade = "프로 레벨"
    elif accuracy >= 62.5:
        grade = "세미프로"
    elif accuracy >= 50:
        grade = "아마추어 상급"
    else:
        grade = "입문자"

    return {
        "score": score,
        "max_score": max_score,
        "accuracy": accuracy,
        "stats": stats,
        "style_name": style_name,
        "style_desc": style_desc,
        "grade": grade,
        "details": detailed_results
    }


def stat_label(stat_type: str) -> str:
    if stat_type == "PASS":
        return "패스 / 경기 흐름 판단"
    if stat_type == "SHOOT":
        return "슈팅 / 마무리 판단"
    if stat_type == "PACE":
        return "역습 / 속도 판단"
    if stat_type == "DRIBBLE":
        return "드리블 / 돌파 판단"
    return "수비 / 위치 선정 판단"


# 첫 화면
st.title("⚽ 축구 경기 판단력 테스트")
st.markdown("### 나는 어떤 유형의 플레이어일까?")
st.info(f"학번: **{STUDENT_ID}** | 이름: **{STUDENT_NAME}**")

st.caption(
    "실제 경기에서 나올 수 있는 상황을 바탕으로 사용자의 축구 판단력과 플레이 성향을 분석하는 앱입니다. "
    "문항 데이터는 Streamlit 캐싱 기능을 활용해 반복 사용됩니다."
)

# 로그인 화면
if not st.session_state.logged_in:
    st.subheader("🔐 로그인")

    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if username == VALID_ID and password == VALID_PW:
            st.session_state.logged_in = True
            st.session_state.login_user = username
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("로그인 실패! 아이디 또는 비밀번호를 확인하세요.")

    st.warning("로그인 계정: student / 1234")
    st.stop()


# 로그인 이후 화면
left, right = st.columns([3, 1])

with left:
    st.success(f"로그인 사용자: {st.session_state.login_user}")

with right:
    if st.button("로그아웃"):
        logout()
        st.rerun()

st.divider()

quiz_data = load_quiz_data()

tab1, tab2 = st.tabs(["퀴즈 풀기", "캐싱 설명"])

# 캐싱 설명 탭
with tab2:
    st.subheader("📌 캐싱 기능 설명")
    st.write(
        """
        이 프로젝트에서는 `@st.cache_data`를 사용하여 퀴즈 데이터를 캐싱했습니다.

        퀴즈 문항, 정답, 해설, 스탯 연결 정보는 앱에서 반복적으로 사용됩니다.
        따라서 매번 새로 만드는 대신 한 번 불러온 데이터를 재사용하도록 구성했습니다.

        이를 통해 앱 실행 중 불필요한 데이터 생성 과정을 줄이고,
        더 안정적으로 퀴즈 데이터를 사용할 수 있습니다.
        """
    )

    st.code(
        """
@st.cache_data
def load_quiz_data():
    return quiz_data
        """,
        language="python"
    )


# 퀴즈 탭
with tab1:
    st.subheader("🧠 축구 상황 판단 퀴즈")

    if not st.session_state.quiz_submitted:
        current_index = st.session_state.current_question
        q = quiz_data[current_index]

        progress_value = (current_index + 1) / len(quiz_data)

        st.progress(progress_value)
        st.caption(f"{current_index + 1} / {len(quiz_data)} 문제")
        st.info(f"문제 영역: {stat_label(q['stat_type'])}")

        st.markdown(f"### Q{q['id']}. {q['question']}")

        previous_answer = st.session_state.answers.get(q["id"], 0)

        user_choice = st.radio(
            "정답을 선택하세요.",
            options=list(range(len(q["options"]))),
            index=previous_answer,
            format_func=lambda x, opts=q["options"]: opts[x],
            key=f"radio_{q['id']}"
        )

        col1, col2 = st.columns(2)

        with col1:
            if current_index > 0:
                if st.button("⬅️ 이전 문제"):
                    st.session_state.answers[q["id"]] = user_choice
                    st.session_state.current_question -= 1
                    st.rerun()

        with col2:
            if current_index < len(quiz_data) - 1:
                if st.button("다음 문제 ➡️"):
                    st.session_state.answers[q["id"]] = user_choice
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("결과 확인 🏁"):
                    st.session_state.answers[q["id"]] = user_choice
                    st.session_state.quiz_submitted = True
                    st.rerun()

    else:
        if not st.session_state.balloon_shown:
            st.balloons()
            st.session_state.balloon_shown = True

        result = calculate_result(quiz_data, st.session_state.answers)

        st.subheader("📊 최종 결과")

        c1, c2, c3 = st.columns(3)
        c1.metric("정답 수", f"{result['score']} / {result['max_score']}")
        c2.metric("정확도", f"{result['accuracy']}%")
        c3.metric("등급", result["grade"])

        st.markdown("### 🏷️ 플레이 스타일 분석")
        st.success(f"당신의 플레이 스타일은 **{result['style_name']}** 입니다.")
        st.write(result["style_desc"])

        st.markdown("### ⚙️ 축구 스탯")
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric("PACE", result["stats"]["PACE"])
        s2.metric("SHOOT", result["stats"]["SHOOT"])
        s3.metric("PASS", result["stats"]["PASS"])
        s4.metric("DRIBBLE", result["stats"]["DRIBBLE"])
        s5.metric("DEF", result["stats"]["DEF"])

        st.markdown("### 📈 전체 정확도")
        st.progress(min(int(result["accuracy"]), 100))

        wrong_categories = [
            item["stat_type"]
            for item in result["details"]
            if not item["is_correct"]
        ]

        st.markdown("### 🔍 보완이 필요한 영역")

        if wrong_categories:
            for category in set(wrong_categories):
                count = wrong_categories.count(category)
                st.warning(f"{stat_label(category)}: {count}개 오답")
        else:
            st.success("모든 영역에서 좋은 판단을 보였습니다!")

        st.markdown("### ✅ 문항별 정답 및 해설")

        for item in result["details"]:
            st.markdown(f"**Q{item['id']}. [{stat_label(item['stat_type'])}] {item['question']}**")

            selected_text = item["options"][item["selected"]]
            correct_text = item["options"][item["correct"]]

            if item["is_correct"]:
                st.success(f"내 답: {selected_text}")
            else:
                st.error(f"내 답: {selected_text}")
                st.info(f"정답: {correct_text}")

            st.caption(f"해설: {item['explanation']}")
            st.write("")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("다시 풀기"):
                reset_quiz()
                st.rerun()

        with col_b:
            if st.button("로그아웃 후 종료"):
                logout()
                st.rerun()