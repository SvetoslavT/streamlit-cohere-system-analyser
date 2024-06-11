import streamlit as st
import cohere
import os

co = cohere.Client("Your Cohere API key here")

def analyze_and_solve(text):
    response = co.generate(
        model='command-r-plus',  
        prompt='Analyze the following scan results, identify problems, and suggest detailed solutions to all of the found problems. \
            give them to me in a structired was, no unnesessary comments abot them, only the problems and the solutions and theit prioripy. Make them also suitable for imporing ina a db table \
                Also calssicy them, system or network etc.. Give me onl them, no other text\n\n' + text,
        max_tokens=5000,
        temperature=0.5)
    return response.generations[0].text

st.title('System Health & Vulnerability Scan Analyzer')

directory = '/home/svrt/Documents/CohereChat/Monitoring'

txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

if txt_files:
    tab_container = st.tabs([f"{file_name}" for file_name in txt_files]) 
    for tab, file_name in zip(tab_container, txt_files):
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            content = file.read()
        with tab:
            st.write(f"Analysis and Solutions for {file_name}:")
            solutions = analyze_and_solve(content)
            st.text_area(f"Solutions for {file_name}", solutions, height=1000)
    st.error("No text files found in the directory.")
