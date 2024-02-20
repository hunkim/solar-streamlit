from openai import OpenAI
import streamlit as st

st.title("Solar Mini Chatbot")
st.write(
    """ Use the `@` symbol to switch between different models: 
         `@enko` will switch to the Solar-mini-en-ko model, 
         and `@koen` will switch to the Solar-mini-ko-en.
        You can also use `@chat` to switch back to the default chat model."""
)
st.write("Visit https://console.upstage.ai to get your Solar API key.")

tags = {
    "enko": "upstage/solar-1-mini-translate-enko",
    "koen": "upstage/solar-1-mini-translate-koen",
    "chat": "upstage/solar-1-mini-chat",
}

client = OpenAI(
    api_key=st.secrets["SOLAR_API_KEY"], base_url="https://api.upstage.ai/v1/solar"
)

if "model_name" not in st.session_state:
    st.session_state["model_name"] = tags["chat"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        if prompt.startswith("@"):
            model_tag = prompt[1:].split()[0]
            if model_tag in tags:
                st.session_state["model_name"] = tags[model_tag]
                st.markdown(f"**Switched to `{st.session_state['model_name']}`**")
                prompt = prompt.replace(f"@{model_tag}", "").strip()
        st.markdown(prompt)
        
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["model_name"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.messages and st.button("Clear chat"):
    st.session_state.messages = []
    # refresh the page
    st.rerun()