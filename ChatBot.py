from openai import OpenAI
import streamlit as st

st.title("AI Chatbot")

client = OpenAI(base_url='https://api.siliconflow.cn/v1',api_key="sk-ibfllpymvyvlamgkdsetclbvckvhhmqsdseqezflkaovvepr")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("输入对话内容"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
if st.button("清除上下文"):
    st.session_state.messages.clear()
    st.rerun()