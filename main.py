import streamlit as st
import pandas as pd
import random
from faker import Faker
from io import BytesIO

fake = Faker()

def generate_fake_data(num_records, questions):
    """
    Generate a DataFrame with the following columns:
      - "Timestamp"
      - "Name"
      - One column per question (using the question text as the header)
    
    For each record, a random timestamp and a random name are generated,
    and for each question, a random answer (from the provided options) is chosen.
    """
    # Create header: Timestamp, Name + each question text
    columns = ["Timestamp", "Name"] + [q["question"] for q in questions]
    data_rows = []
    
    for _ in range(num_records):
        row = {}
        row["Timestamp"] = str(fake.date_time_this_year())
        row["Name"] = fake.name()
        for q in questions:
            row[q["question"]] = random.choice(q["options"])
        data_rows.append(row)
    
    return pd.DataFrame(data_rows, columns=columns)

def main():
    st.title("Dynamic MCQ Generator with Fake Data")
    
    # Initialize questions list in session state if not already present
    if "questions" not in st.session_state:
        st.session_state["questions"] = []
    
    st.header("Add a New Question")
    with st.form("add_question_form"):
        question_text = st.text_input("Enter question text (e.g., 'What is your favorite color?')")
        options_text = st.text_input("Enter comma-separated options (e.g., 'Red,Green,Blue')")
        submitted = st.form_submit_button("Add Question")
        if submitted:
            if question_text.strip() and options_text.strip():
                options_list = [opt.strip() for opt in options_text.split(",") if opt.strip()]
                st.session_state["questions"].append({
                    "question": question_text,
                    "options": options_list
                })
                st.success(f"Question added: {question_text}")
            else:
                st.warning("Please enter both question text and options.")
    
    st.subheader("Current Questions")
    if st.session_state["questions"]:
        for idx, q in enumerate(st.session_state["questions"], start=1):
            st.write(f"**Question {idx}:** {q['question']}")
            st.write(f"**Options:** {', '.join(q['options'])}")
    else:
        st.write("No questions added yet.")
    
    st.header("Generate Fake Data")
    num_records = st.number_input("Number of records to generate:", min_value=1, value=5, step=1)
    
    if st.button("Generate Fake Data"):
        if not st.session_state["questions"]:
            st.error("Please add at least one question.")
        else:
            df = generate_fake_data(num_records, st.session_state["questions"])
            st.dataframe(df)
            
            # Download CSV option
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv_data, "fake_data.csv", "text/csv")
            
            # Download Excel option
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="FakeData")
            st.download_button("Download Excel", excel_buffer.getvalue(), "fake_data.xlsx", 
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()
