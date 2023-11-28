import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import requests
from bs4 import BeautifulSoup
from collections import Counter
import pdfplumber

def summarize_text(text, ratio):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in STOP_WORDS:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens) * ratio)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    return summary

def scrape_wikipedia(keywords, sections):
    text_output = ""
    for keyword in keywords:
        url = f"https://en.wikipedia.org/wiki/{keyword}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        text_output += f"Text excerpt for {keyword}:\n"
        
        content = soup.find(id="content")
        text = ""
        for paragraph in content.find_all("p"):
            text += paragraph.get_text() + "\n"
            if len(text.split()) >= 1000:
                break
        
        text_output += " ".join(text.split()[:1000]) + "...read more.\n"
        
        text_output += f"\nLink to full article: {url}\n"
    
    return text_output

def is_connected():
    try:
        response = requests.get("https://www.wikipedia.com", timeout=5)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    return False

def keyword(text, num_keywords=5):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    words = [token.text for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    word_freq = Counter(words)
    keyword_threshold = 2
    keyword_freq_tuples = [(word, freq) for word, freq in word_freq.items() if freq >= keyword_threshold]
    sorted_keywords = sorted(keyword_freq_tuples, key=lambda x: x[1], reverse=True)
    keywords = [f"{word}: {freq}" for word, freq in sorted_keywords[:num_keywords]]
    return keywords


def extract_text_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text



# Streamlit code
'''st.title("Text Summarization and Information Extraction")

st.text("Please select your option")

option = st.radio("Select an option:", ("Help", "Summarize text", "Keyword finder", "Information extraction", "File Summary(.txt)", "File Summary(.pdf)"))

if option == "Help":
    st.subheader("Summarize text")
    st.write("1) Input text into the text box.")
    st.write("2) Select the summary percentage from the slider bar.")
    st.write('3) Click on "Generate Summary" button to generate the summary of the given text with respect to the provided summary percentage.' )
    
    st.subheader("Keyword finder")
    st.write("1) Input text into the text box.")
    st.write('2) Click on the "Generate keyword(s)" button to generate the keywords from the given text.')
    st.write('3) The keywords so obtained can be used to find more information in the "Information extraction" section.')

    st.subheader("Information extraction")
    st.write('1) Insert the keyword you want the information on (can be obtained from the "Keyword finder" section or can be a user input ).')
    st.write("2) The first 1000 words of the information will be displayed on the screen. A link will be displayed, and on clicking it, you will be redirected to the wikipedia page.")

    st.subheader("File Summary")
    st.write("1) We advise you to use this feature if you have a large text. ")
    st.write("2) You can drag and drop the file or browse the file from the required directories.")
    st.write("3) Select the required summary percentage from the slider. ")
    st.write('4) Click on the "Generate File Summary" to generate the summary of the file contents.')
    st.write("**NOTE: AT PRESENT, THE PROGRAM ONLY ACCEPTS .TXT AND .PDF FILES**")

elif option == "Summarize text":
    st.text("Please enter the text you want to summarize:")
    input_text = st.text_area("Input text", height=200, max_chars=10000)

    st.text("Please enter the Summary Percentage:" )
    input_percentage = st.slider("Percentage between 0 and 100", min_value = 0, max_value = 100, step = 1)
    summary_percentage = f"Summary Percentage {input_percentage}%"
    input_percentage = input_percentage / 100
    st.write(summary_percentage)

    if st.button("Generate Summary"):
        if input_text and input_percentage:
            try:
                input_percentage = float(input_percentage)
                if input_percentage > 0 and input_percentage <= 100:
                    summary_result = summarize_text(input_text, input_percentage)
                    if(summary_result is None) or (summary_result.strip() == ""):
                        st.warning("The input text is very small with respect to the ratio. Either increase the input text or the ratio to resolve this issue")
                    else:
                        st.subheader("Summary:")
                        st.write(summary_result)
                else:
                    st.warning("Please enter a valid summary percentage between 0 and 100.")
            except ValueError:
                st.warning("Please enter a valid summary percentage as a number.")
        
        else:
            st.warning("Fill the required fields")
    
elif option == "Keyword finder":
    st.write("Please enter the text you want to find the keyword from: ")
    input_text_keyword = st.text_area("Input text", height=200, max_chars=10000)
    if(st.button("Generate keyword(s)")):
        if input_text_keyword:
            try:
                keywords = keyword(input_text_keyword)
                st.subheader("Keyword(s): ")
                for i, keyword in enumerate(keywords):
                    st.write(f"{i + 1}. {keyword}")
                #keywords_text = ', '.join(keywords)
                #st.write(keywords_text)
            except ValueError:
                st.error("please give a valid input text")


elif option == "Information extraction":
    if is_connected():
        st.text("Please enter the keyword for information extraction:")
        input_keyword = st.text_input("Input keyword")
        input_keyword = input_keyword.replace(" ", "_")
    elif not is_connected():
        st.error("Connection failed. Make sure to connect to the network.")
        st.stop()

    if st.button("Extract Information"):
        if input_keyword:
            sections_to_extract = ["Overview", "History", "Approaches"]
            extraction_result = scrape_wikipedia([input_keyword], sections_to_extract)
            st.subheader("Information Extracted from Wikipedia:")
            st.write(extraction_result)
        else:
            st.error("Fill the required fields")

elif option == "File Summary(.txt)":

    uploaded_file_txt = st.file_uploader("Upload a file", type=["txt"])

    input_percentage_file = st.slider("Select a percentage between 0 and 100", min_value=0, max_value=100, step=1)
    summary_percentage_file = f"Summary Percentage {input_percentage_file}%"
    st.write(summary_percentage_file)
    input_percentage_file = input_percentage_file / 100

    if uploaded_file_txt:
        file_contents = str(uploaded_file_txt.read())
        if st.button("Generate File Summary"):
            if uploaded_file_txt and input_percentage_file:
                try:
                    input_percentage_file = float(input_percentage_file)
                    if input_percentage_file > 0 and input_percentage_file <= 100:
                        summary_result_file = summarize_text(file_contents, input_percentage_file)
                        if (summary_result_file is None) or (summary_result_file.strip() == ""):
                            st.warning("The text inside the file is very small with respect to the ratio. Either increase the input text in the file or the ratio to resolve this issue")
                        else:
                            file_name_txt = uploaded_file_txt.name.rsplit('.', 1)[0]
                            file_name_txt = str(file_name_txt)
                            #st.write(file_name_txt)
                            st.subheader("Summary:")
                            #st.write(summary_result_file)
                            download_link = f"{file_name_txt}_summary.txt"
                            txt_summary = summary_result_file.encode("utf-8")
                            download_key = f"{file_name_txt}_summary.txt"
                            
                            st.download_button(label=download_link, data=txt_summary,  file_name=f"{file_name_txt}_summary.txt", mime='text/plain', key=download_key, on_click=None)
                    else:
                        st.warning("Please enter a valid summary ratio between 0 and 1.")
                except ValueError:
                    st.warning("Please enter a valid summary ratio as a number.")
            else:
                st.warning("Drop the file to be summarized")

elif option == "File Summary(.pdf)":
    uploaded_file_pdf = st.file_uploader("Upload a file", type=["pdf"])
    input_percentage_pdf = st.slider("Select a percentage between 0 and 100", min_value=0, max_value=100, step=1)
    summary_percentage_pdf = f"Summary Percentage {input_percentage_pdf}%"
    st.write(summary_percentage_pdf)
    input_percentage_pdf = input_percentage_pdf / 100
    if uploaded_file_pdf:
        file_contents_pdf = extract_text_pdf(uploaded_file_pdf) 
        if st.button("Generate File Summary"):
            if uploaded_file_pdf and input_percentage_pdf:
                try:
                    input_percentage_pdf = float(input_percentage_pdf)
                    if input_percentage_pdf > 0 and input_percentage_pdf <= 100:
                        summary_result_file = summarize_text(file_contents_pdf, input_percentage_pdf)
                        if not summary_result_file.strip():
                            st.warning("The text inside the PDF is very small with respect to the percentage. Either increase the text in the PDF or the percentage to resolve this issue.")
                        else:
                            file_name_pdf = uploaded_file_pdf.name.rsplit('.', 1)[0]
                            file_name_pdf = str(file_name_pdf)
                            #st.write(file_name_pdf)
                            st.subheader("Summary:")
                            #st.write(summary_result_file)
                            download_link = f"{file_name_pdf}_summary.pdf"
                            pdf_summary = summary_result_file.encode("utf-8")
                            download_key = f"{file_name_pdf}_summary.pdf"
                            st.download_button(label=download_link, data=pdf_summary,  file_name=f"{file_name_pdf}_summary.txt", mime='text/plain', key=download_key, on_click=None)
                    else:
                        st.warning("Please enter a valid summary percentage between 0 and 100.")
                except ValueError:
                    st.warning("Please enter a valid summary percentage as a number.")
            else:
                st.warning("The uploaded PDF is empty or the percentage is missing.")'''
