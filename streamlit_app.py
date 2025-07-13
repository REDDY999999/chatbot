import streamlit as st
from openai import OpenAI
from pathlib import Path


@st.cache_data
def load_docs(directory: str = "docs"):
    docs = []
    for path in Path(directory).glob("*.txt"):
        docs.append({"text": path.read_text()})
    return docs


def simple_retrieve(query: str, docs, k: int = 2):
    query_words = set(query.lower().split())
    scored = []
    for doc in docs:
        words = set(doc["text"].lower().split())
        score = len(query_words & words)
        scored.append((score, doc["text"]))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [text for score, text in scored[:k] if score > 0]


docs = load_docs()

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Retrieve relevant documents and add them to the prompt.
        context_docs = simple_retrieve(prompt, docs)
        message_list = [
            {"role": "system", "content": "Use the following documents to answer the question."},
        ]
        for doc_text in context_docs:
            message_list.append({"role": "system", "content": doc_text})
        message_list.extend(
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        )

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_list,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

