import tkinter as tk
from tkinter import scrolledtext

import nltk
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from faq_data import faq_data

nltk.download('punkt')

questions = list(faq_data.keys())

def get_answer(user_question):

    all_questions = questions + [user_question]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(all_questions)

    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    best_match = similarity.argmax()

    score = similarity[0][best_match]

    if score > 0.3:
        return faq_data[questions[best_match]]
    else:
        return "Sorry, I don't understand that question."

def send_message():

    user_question = entry.get()

    if not user_question:
        return

    chat_area.insert(
        tk.END,
        "You: " + user_question + "\n"
    )

    answer = get_answer(user_question)

    chat_area.insert(
        tk.END,
        "Bot: " + answer + "\n\n"
    )

    entry.delete(0, tk.END)

root = tk.Tk()

root.title("FAQ Chatbot")
root.geometry("700x500")

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD
)

chat_area.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

entry = tk.Entry(
    root,
    width=60
)

entry.pack(
    padx=10,
    pady=5
)

send_button = tk.Button(
    root,
    text="Send",
    command=send_message
)

send_button.pack()

root.mainloop()
