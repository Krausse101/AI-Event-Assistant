import streamlit as st
import pandas as pd
import openai

# Set API key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# App layout
st.set_page_config(page_title="AI Event Assistant", layout="wide")
st.title("🤖 AI Event Assistant")
st.write("Ask questions about the event data stored in the Master Schedule Excel file.")

# Load Excel data from "Data" and "Home" sheets
try:
    sheet_names = ["Data", "Home"]
    data_string = ""

    for name in sheet_names:
        df = pd.read_excel("Master Schedule.xlsm", sheet_name=name)
        data_string += f"\n\n--- Sheet: {name} ---\n\n"
        data_string += df.to_string(index=False)

except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# User input
question = st.text_input("🔍 What would you like to know?", placeholder="e.g., What is the actual YTD spending for Alante?")

# Handle user question
if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            prompt = f"""
You are an assistant that helps summarize event tracking and financial data for a healthcare organization.
Here is the information from two Excel sheets:

{data_string}

Now, answer this question based on the data above:
{question}

Provide the answer in a clean, concise, readable summary.
"""
            try:
                response = client.chat.completions.create(
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

