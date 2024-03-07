import streamlit as st
from textblob import TextBlob
from language_tool_python import LanguageTool
from PyPDF2 import PdfReader
from io import BytesIO

class SpellCheckerModule:
    def __init__(self):
        self.spell_check = TextBlob("")
        self.grammar_check = LanguageTool('en-US')

    def correct_spell(self, text):
        words = text.split()
        corrected_words = []
        for word in words:
            corrected_word = str(TextBlob(word).correct())
            corrected_words.append(corrected_word)
        return " ".join(corrected_words)

    def correct_grammar(self, text):
        matches = self.grammar_check.check(text)
        found_mistakes = []
        for mistake in matches:
            found_mistakes.append(mistake.ruleId)
        found_mistakes_count = len(found_mistakes)
        corrected_text = self.grammar_check.correct(text)
        return found_mistakes, found_mistakes_count, corrected_text

def read_text_from_file(uploaded_file):
    if uploaded_file is not None:
        content = uploaded_file.getvalue()
        if uploaded_file.name.endswith('.txt'):
            return content.decode('utf-8')
        elif uploaded_file.name.endswith('.pdf'):
            pdf_reader = PdfReader(BytesIO(content))
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    return None

def main():
    st.title("Grammar And Spell Checker App")

    # Input box for typing text
    input_text = st.text_area("Type your text here")

    # File uploader for uploading .txt or .pdf file
    uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])

    if input_text or uploaded_file:
        if input_text:
            text = input_text
        else:
            text = read_text_from_file(uploaded_file)
            if text:
                st.subheader("Text from Uploaded File:")
                st.write(text)

        if text:
            spell_checker_module = SpellCheckerModule()

            if st.button("Correct"):
                found_mistakes, _, corrected_text = spell_checker_module.correct_grammar(text)
                corrected_text_spell = spell_checker_module.correct_spell(corrected_text)
                
                st.subheader("Corrected Text:")
                st.write(corrected_text_spell)

                st.subheader("Grammar Mistakes:")
                st.write(found_mistakes)
        else:
            st.write("Error: Unsupported file format. Please upload a .txt or .pdf file.")

if __name__ == "__main__":
    main()