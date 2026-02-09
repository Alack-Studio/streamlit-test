import streamlit as st
import pandas as pd

# --- 1. 核心知识库 (这里你可以尽情扩展特征) ---
# 特征定义：1代表是，-1代表不是，0代表不确定
@st.cache_data
def get_knowledge_base():
    return pd.DataFrame([
        {"人物": "孙悟空", "虚构": 1, "男性": 1, "中国": 1, "战斗力强": 1, "现代": -1, "科学家": -1},
        {"人物": "周杰伦", "虚构": -1, "男性": 1, "中国": 1, "战斗力强": -1, "现代": 1, "科学家": -1},
        {"人物": "居里夫人", "虚构": -1, "男性": -1, "中国": -1, "战斗力强": -1, "现代": -1, "科学家": 1},
        {"人物": "马斯克", "虚构": -1, "男性": 1, "中国": -1, "战斗力强": -1, "现代": 1, "科学家": 1},
        {"人物": "那鲁多(鸣人)", "虚构": 1, "男性": 1, "中国": -1, "战斗力强": 1, "现代": -1, "科学家": -1},
        {"人物": "林黛玉", "虚构": 1, "男性": -1, "中国": 1, "战斗力强": -1, "现代": -1, "科学家": -1},
    ])

# --- 2. 初始化游戏状态 ---
if 'scores' not in st.session_state:
    kb = get_knowledge_base()
    st.session_state.kb = kb
    st.session_state.scores = {name: 0 for name in kb["人物"]}
    st.session_state.asked_questions = []
    st.session_state.game_over = False

# --- 3. 页面布局 ---
st.set_page_config(page_title="Pro级 AI 读心术", page_icon="🧠")
st.title("🧠 深度 AI 读心术 (Pro)")
st.write("想一个名人，我将通过逻辑推理锁定他。")

# --- 4. 自动选择最佳问题的逻辑 ---
def get_best_question():
    # 找出还没问过的特征列
    all_features = [c for c in st.session_state.kb.columns if c != "人物"]
    remaining_features = [f for f in all_features if f not in st.session_state.asked_questions]
    
    if not remaining_features:
        return None
    
    # 这里简单使用第一个，进阶版可以计算信息增益(Information Gain)
    return remaining_features[0]

# --- 5. 游戏交互主循环 ---
if not st.session_state.game_over:
    current_q = get_best_question()
    
    if current_q:
        st.subheader(f"分析中... 当前目标特征：**{current_q}**")
        progress = len(st.session_state.asked_questions) / (len(st.session_state.kb.columns)-1)
        st.progress(progress)
        
        q_text = f"请问该人物是否具有【{current_q}】的特征？"
        st.markdown(f"### {q_text}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ 是的", use_container_width=True):
                for idx, row in st.session_state.kb.iterrows():
                    st.session_state.scores[row["人物"]] += row[current_q]
                st.session_state.asked_questions.append(current_q)
                st.rerun()
        with col2:
            if st.button("❌ 不是", use_container_width=True):
                for idx, row in st.session_state.kb.iterrows():
                    st.session_state.scores[row["人物"]] -= row[current_q]
                st.session_state.asked_questions.append(current_q)
                st.rerun()
        with col3:
            if st.button("❔ 不确定", use_container_width=True):
                st.session_state.asked_questions.append(current_q)
                st.rerun()
    else:
        st.session_state.game_over = True
        st.rerun()

# --- 6. 结算界面 ---
else:
    # 按分数排序
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    winner, score = sorted_scores[0]
    
    st.balloons()
    st
