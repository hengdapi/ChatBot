from openai import OpenAI
import streamlit as st,base64

st.title("AI Chatbot")

encoded_str = "c2stb3ItdjEtNTQ4NmUyODc3N2Q3MWQ0NmM0ZDRmZDc5MTdlMTUxNWZkMjlhNTYzYjdkZjViYjcyNzc0MDc2ZGZhMWQ4NTJiOA=="
decoded_bytes = base64.b64decode(encoded_str.encode())
decoded_str = decoded_bytes.decode()

client = OpenAI(base_url='https://openrouter.ai/api/v1',
                api_key=decoded_str)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "qwen/qwen3-235b-a22b:free"

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