import streamlit as st
import google.generativeai as genai
from datetime import datetime

st.set_page_config(page_title="AI学習プラン作成アプリ", page_icon="📅", layout="centered")

st.title("📅 AI学習プラン作成アプリ")
st.caption("Gemini APIを使って、あなたの目標に合わせた学習プランやToDoを自動生成します。")

st.markdown("---")

# セッション状態の初期化
if "plan_output" not in st.session_state:
    st.session_state.plan_output = ""
if "todo_output" not in st.session_state:
    st.session_state.todo_output = ""

# 入力フォーム（常に上部に表示）
api_key = st.text_input(
    "🔑 Gemini APIキーを入力してください：",
    type="password",
    help="※ Google AI Studio で取得したAPIキーを入力してください。"
)

st.subheader("🎯 あなたの学習目標を教えてください")
goal = st.text_input("目標（例：ITパスポートに合格する）")
duration = st.text_input("達成したい期間（例：1ヶ月、30日、8週間など）")
study_days_per_week = st.slider("1週間に勉強できる日数", min_value=1, max_value=7, value=5)

# ボタンを横並びに表示
col1, col2 = st.columns(2)
with col1:
    make_plan = st.button("📝 学習プランを作成")
with col2:
    make_todo = st.button("📋 ToDoを作成")

# Geminiモデル初期化関数
def init_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

# 学習プラン生成処理
if make_plan:
    if not api_key:
        st.error("Gemini APIキーを入力してください。")
    elif not goal or not duration:
        st.warning("目標と期間を入力してください。")
    else:
        try:
            model = init_model(api_key)
            prompt = f"""
あなたは優秀な学習コーチです。
以下の情報に基づいて、最適な学習プランを作成してください。

【目標】{goal}
【期間】{duration}
【1週間に勉強できる日数】{study_days_per_week}日

学習プランには以下を含めてください：
1. 週間ごとのスケジュール（例：Week1〜Week4）
2. 毎週やるべき内容（わかりやすく段階的に）
3. モチベーションを維持するアドバイス
4. 最終確認の方法（模試・過去問など）

親しみやすい語り口でお願いします。
"""
            response = model.generate_content(prompt)
            st.session_state.plan_output = response.text
            st.success("✅ 学習プランが完成しました！")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# ToDo生成処理
if make_todo:
    if not api_key:
        st.error("Gemini APIキーを入力してください。")
    elif not goal:
        st.warning("まず学習目標を入力してください。")
    else:
        try:
            model = init_model(api_key)
            today = datetime.now().strftime("%Y年%m月%d日（%A）")

            todo_prompt = f"""
あなたは優秀な学習サポーターです。
以下の学習目標に向かって、今日（{today}）やるべき具体的なToDoリストを5項目以内で提案してください。

【目標】{goal}
【期間】{duration}
【1週間に勉強できる日数】{study_days_per_week}日

箇条書きで、シンプルかつ行動しやすく書いてください。
"""
            response = model.generate_content(todo_prompt)
            st.session_state.todo_output = response.text
            st.success("📋 今日のToDoリストを作成しました！")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# 出力表示（画面下部、左右2列に分割）
st.markdown("---")
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### ✨ あなたの学習プラン")
    if st.session_state.plan_output:
        st.markdown(st.session_state.plan_output)
    else:
        st.info("学習プランがここに表示されます。")

with right_col:
    st.markdown("### ✅ 今日やること（ToDo）")
    if st.session_state.todo_output:
        st.markdown(st.session_state.todo_output)
    else:
        st.info("ToDoリストがここに表示されます。")
