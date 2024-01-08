import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st

# Load the text file and preprocess the data
with open('C:/einstein.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')
# Tokenize the text into sentences
sentences = sent_tokenize(data)
# Define a function to preprocess each sentence

def preprocess(sentence):
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in sentence]

    # Expand contractions
    contractions = {
        "can't": "cannot",
        "won't": "will not",
        # Add more contractions and their expansions
    }

    def expand_contractions(text):
        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)
        return text

    sentence = expand_contractions(sentence)

    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Remove stopwords, punctuation, and special characters
    stop_words = set(stopwords.words('english'))
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words and word not in string.punctuation and not re.match(r'^\W+$', word)]

    return words

# Preprocess each sentence in the text
corpus = [preprocess(sentence) for sentence in sentences]


# Define a function to find the most relevant sentence given a query
def get_most_relevant_sentence(query):
    # Preprocess the query
    query = preprocess(query)
    # Compute the similarity between the query and each sentence in the text
    max_similarity = 0
    most_relevant_sentence = ""
    for sentence in corpus:
        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
    return most_relevant_sentence

def chatbot(question):
    # Find the most relevant sentence
    most_relevant_sentence = get_most_relevant_sentence(question)
    # Return the answer
    return most_relevant_sentence

# Create a Streamlit app
def main():
    st.title("Chatbot")
    st.write("Hello! I'm a chatbot. Ask me anything about the topic in the text file.")
    # Get the user's question
    question = st.text_input("You:")
    # Create a button to submit the question
    if st.button("Submit"):
        # Call the chatbot function with the question and display the response
        response = chatbot(question)
        st.write("Chatbot: " + response)
if __name__ == "__main__":
    main()