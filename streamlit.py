import streamlit as st
from qna_with_rag import question, Qna, Question


st.set_page_config(page_title="Rag with Streamlit", layout="wide")
with st.sidebar:
    st.title("Rag with Streamlit")


def generate_response(input):
    return question(Question(question=input))


if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome, let's find capital cities of countries!",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Getting your answer from knowledge base..."):
            response = generate_response(input)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
