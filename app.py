from CodeReviewer import CodeReviewer
import streamlit as st

MAX_CHARS = 4000

st.set_page_config(
    page_title=" AI Code Review Assistant",
    page_icon="🤖",
    layout="wide"
)

try:
    code_reviewer = CodeReviewer()
    if "api_key_toast_shown" not in st.session_state:
            st.toast("OpenAI Key successfully loaded!", icon="✅")
            st.session_state.api_key_toast_shown = True
except Exception as e:
        st.error(f"🛑 Could not initialize CodeReviewer: {e}")
        st.stop()

st.title("🤖 AI Code Review Assistant")
st.write("Welcome to your AI Code Review Assistant")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("✍️ Paste your code here")
    language_choice = st.selectbox(
        "🧠 Choose a programming language",
        ["Python", "PHP", "Javascript", "Java", "C", "C#"]
    )
    tone_choice = st.selectbox("🎭 Choose feedback tone", ["Supportive", "Direct", "Humorous", "Sarcastic"])
    code_input = st.text_area("Paste your code here", height=200)
    uploaded_file = st.file_uploader("Or upload a code file", type=["py", "txt"])

    if uploaded_file is not None:
        try:
            code_input = uploaded_file.read().decode("utf-8")
            st.text_area("File Content", code_input, height=300)
        except Exception:
            st.error("🛑 Could not read the uploaded file. Please upload a valid text-based file.")

with col2:
    st.subheader("📋 Review Output")

    if st.session_state.get("feedback"):
        st.markdown(" ### AI Code Review")
        st.markdown(st.session_state["feedback"])
    elif code_input:
        st.write("Code Review will appear here.")
    else:
        st.info("Paste some code to get started.")



if st.button("⚙️ Get Review"):
    if not code_input.strip():
        st.warning("⚠️ Please paste or upload some code before requesting a review.")
    elif not language_choice:
        st.warning("⚠️ Please select one programming language before requesting a review.")
    elif len(code_input) > MAX_CHARS:
        st.error(f"🛑 Entered code is too long. Please input code under {MAX_CHARS} characters")
    else:
        with st.spinner("Reviewing your code..."):
            try:
                response = code_reviewer.get_code_feedback(code_input, language_choice, tone_choice='Supportive')
                st.session_state["feedback"] = response['feedback']
                st.toast(
                    f"Total tokens cost: {response['tokens_prompt']}\n"
                    f"Total cost in USD: {response['cost_usd']}",
                    icon="✅"
                )
                st.rerun()
            except Exception as e:
                st.error(f"🛑 Error during review: {e}")
