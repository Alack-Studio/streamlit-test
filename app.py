import streamlit as st

# 设置页面
st.set_page_config(page_title="AI 读心术 - 猜人物", page_icon="🔮")

st.title("🔮 AI 读心术：猜猜我想谁？")
st.write("请在心中想一个著名人物（现实或虚构），我会通过几个问题猜出他/她！")

# 初始化会话状态，用于存储回答记录
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# 人物数据库（简化版，你可以不断扩充）
# 逻辑：特征组合 -> 目标人物
DATABASE = [
    {"name": "孙悟空", "real": False, "male": True, "china": True, "magic": True},
    {"name": "周杰伦", "real": True, "male": True, "china": True, "magic": False},
    {"name": "爱因斯坦", "real": True, "male": True, "china": False, "magic": False},
    {"name": "艾莎 (Elsa)", "real": False, "male": False, "china": False, "magic": True},
    {"name": "花木兰", "real": False, "male": False, "china": True, "magic": False},
    {"name": "马斯克", "real": True, "male": True, "china": False, "magic": False}
]

# 问题列表
QUESTIONS = [
    {"key": "real", "text": "该人物是真实存在的吗？"},
    {"key": "male", "text": "该人物是男性吗？"},
    {"key": "china", "text": "该人物是中国人/源自中国文化吗？"},
    {"key": "magic", "text": "该人物拥有超能力或魔法吗？"}
]

def reset_game():
    st.session_state.step = 0
    st.session_state.answers = {}

# 游戏主逻辑
if st.session_state.step < len(QUESTIONS):
    current_q = QUESTIONS[st.session_state.step]
    st.subheader(f"问题 {st.session_state.step + 1}:")
    st.write(f"### {current_q['text']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 是的", use_container_width=True):
            st.session_state.answers[current_q['key']] = True
            st.session_state.step += 1
            st.rerun()
    with col2:
        if st.button("👎 不是", use_container_width=True):
            st.session_state.answers[current_q['key']] = False
            st.session_state.step += 1
            st.rerun()

else:
    # 计算匹配度
    best_match = None
    max_score = -1

    for person in DATABASE:
        score = sum(1 for k, v in st.session_state.answers.items() if person.get(k) == v)
        if score > max_score:
            max_score = score
            best_match = person['name']

    st.balloons()
    st.success(f"### 我猜到了！你心里想的候选人可能是：**{best_match}**")
    st.write("（匹配度越高，结果越准。如果不对，可能是我的数据库还不够大！）")
    
    if st.button("再玩一次"):
        reset_game()
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("这个应用展示了决策树算法的基本原理。你可以通过增加 `DATABASE` 里的词条来让它变得更聪明！")
