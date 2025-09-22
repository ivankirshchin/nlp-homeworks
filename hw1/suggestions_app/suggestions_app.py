import reflex as rx
from tools.word_completor import WordCompletor
from tools.n_gramm_model import NGramLanguageModel
from tools.text_suggestion import TextSuggestion
import pandas as pd
import numpy as np

corpus = pd.read_csv('data/corpus_sample.csv', dtype=str)
corp = [str(msg).split() for msg in corpus['message_norm']]

word_completor = WordCompletor(corp)
n_gram_model = NGramLanguageModel(corpus=corp, n=3)
text_suggestion = TextSuggestion(word_completor, n_gram_model)

class State(rx.State):
    query = ""
    text1 = ""
    text2 = ""
    text3 = ""
    text4 = ""
    text5 = ""

    def get_suggestions(self):
        sugg_texts = text_suggestion.suggest_text(self.query, n_words=3, n_texts=5)[1]
        while len(sugg_texts) < 5:
            sugg_texts.append('')
        self.text1 = sugg_texts[0]
        self.text2 = sugg_texts[1]
        self.text3 = sugg_texts[2]
        self.text4 = sugg_texts[3]
        self.text5 = sugg_texts[4]


def index():
    return rx.center(
        rx.vstack(
            rx.heading("Suggestions", font_size="1.5em"),
            rx.input(
                placeholder="Enter your query",
                on_change=[State.set_query, State.get_suggestions],
                width="25em",
            ),
            rx.flex(
                rx.text(
                    State.text1
                ),
                rx.text(
                    State.text2
                ),
                rx.text(
                    State.text3
                ),
                rx.text(
                    State.text4
                ),
                rx.text(
                    State.text5
                ),
                direction="column",
                spacing="3",
            ),
            align="center",
        ),
        width="100%",
        height="100vh",
    )

# Add state and page to the app.
app = rx.App()
app.add_page(index, title="Suggestions")