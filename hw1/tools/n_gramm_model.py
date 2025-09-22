class NGramLanguageModel:
    def __init__(self, corpus, n):
        self.n = n
        self.freq = {}
        den = {}
        for sentence in corpus:
            for i in range(max(len(sentence) - n, 0)):
                if tuple(sentence[i:i + n]) not in self.freq:
                    self.freq[tuple(sentence[i:i + n])] = {}
                if sentence[i + n] not in self.freq[tuple(sentence[i:i + n])]:
                    self.freq[tuple(sentence[i:i + n])][sentence[i + n]] = 0
                self.freq[tuple(sentence[i:i + n])][sentence[i + n]] += 1
                
                if tuple(sentence[i:i + n]) not in den:
                    den[tuple(sentence[i:i + n])] = 0
                den[tuple(sentence[i:i + n])] += 1
                
        for sent in self.freq:
            for word in self.freq[sent]:
                self.freq[sent][word] = self.freq[sent][word] / den[sent]

    def get_next_words_and_probs(self, prefix: list):
        """
        Возвращает список слов, которые могут идти после prefix,
        а так же список вероятностей этих слов
        """

        next_words, probs = [], []
        prefix = prefix[-self.n:]
        
        if tuple(prefix) not in self.freq:
            return next_words, probs
        
        for word in self.freq[tuple(prefix)]:
            next_words.append(word)
            probs.append(self.freq[tuple(prefix)][word])

        return next_words, probs