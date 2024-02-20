from openai import OpenAI
import streamlit as st

st.title("Solar Mini Chatbot")
st.write("""This is a mini chatbot that uses the Solar API to generate responses. 
            You can use the `@` symbol to switch between different models. 
         For example, `@enko` will switch to the Solar-mini-en-ko model, 
         and `@koen` will switch to the Solar-mini-ko-en.
        You can also use `@chat` to switch back to the default chat model.""")

tags = {"enko": "upstage/solar-1-mini-translate-enko", 
        "koen": "upstage/solar-1-mini-translate-koen", 
        "chat": "upstage/solar-1-mini-chat"}

model_name = tags['chat']

client = OpenAI(api_key=st.secrets["SOLAR_API_KEY"], 
        base_url="https://api.upstage.ai/v1/solar"
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        if prompt.startswith("@"):
            model_tag = prompt[1:].split()[0]
            if model_tag in tags:
                model_name = tags[model_tag]
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})