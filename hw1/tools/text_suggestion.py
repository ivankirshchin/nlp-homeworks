import numpy as np

class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def suggest_text(self, text, n_words=3, n_texts=1):
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, которые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """
        if len(text) == 0:
            return [], []
        
        if isinstance(text, str) and text[-1] == ' ':
            text = text.split()
            
        def normalize_message(message):
            norm_message = ''
            for char in message:
                if char.isalpha():
                    norm_message += char.lower()
                elif char in [' ', '\n', '\t'] and len(norm_message) > 0 and norm_message[-1] != ' ':
                    norm_message += ' '
            return norm_message
        
        if isinstance(text, str):
            text = normalize_message(text)
        else:
            text = normalize_message(' '.join(text)).split()

        if isinstance(text, str):
            words, probs = self.word_completor.get_words_and_probs(text.split()[-1])
            if len(words) == 0:
                return [], [text]
            else:
                text = text.split()[:-1]
        else:
            words, probs = self.n_gram_model.get_next_words_and_probs(text)
            if len(words) == 0:
                return [], [' '.join(text)]
        
        best_words = [words[i] for i in np.argsort(probs)[::-1][:n_texts]]
        suggestions = []
        texts = []
        for word in best_words:
            suggestions_word = [word]
            text_word = text + [word]
            for _ in range(n_words - 1):
                words, probs = self.n_gram_model.get_next_words_and_probs(text_word)
                if len(words) == 0:
                    break
                next_word = words[np.argmax(probs)]
                suggestions_word.append(next_word)
                text_word.append(next_word)
            suggestions.append(suggestions_word)
            texts.append(text_word)
        
        return suggestions, [' '.join(text) for text in texts]