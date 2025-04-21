import streamlit as st
import pandas as pd
import openai

# New client object required by OpenAI v1+
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load and prepare Excel data as before...
# [your existing code up to the Ask button]

# Run on submit
if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            prompt = f'''
You are an assistant that helps summarize event tracking data for a healthcare organization.
Here is the event data:

{data_string}

Now, answer this question based on the data above:
{question}

Provide the answer in a clean, concise, readable summary.
'''
            try:
                response = client.chat.completions.create(  # ✅ New method
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for analyzing Excel event data."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                answer = response.choices[0].message.content
                st.success("✅ Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"OpenAI Error: {e}")
