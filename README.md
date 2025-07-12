# 💬 Chatbot template

A simple Streamlit app that shows how to build a chatbot using OpenAI's GPT-3.5.
This version also demonstrates a minimal retrieval-augmented generation (RAG)
setup. The app searches text files in the `docs/` folder and sends the most
relevant snippets along with the conversation to the language model.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

You can add your own knowledge sources by placing text files in the `docs/`
folder. The chatbot will search these files and use the retrieved text to help
answer your questions.
