from typing import List

class PrefixTreeNode:
    def __init__(self):
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False

class PrefixTree:
    def __init__(self, vocabulary):
        """
        vocabulary: список всех уникальных токенов в корпусе
        """
        self.root = PrefixTreeNode()
        
        for word in vocabulary:
            self.insert(word)
            
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = PrefixTreeNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        """
        Возвращает все слова, начинающиеся на prefix
        prefix: str – префикс слова
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        result = []
        def dfs(curr, path):
            if curr.is_end_of_word:
                result.append(path)
            for ch, child in curr.children.items():
                dfs(child, path + ch)

        dfs(node, prefix)
        return result
    
class WordCompletor:
    def __init__(self, corpus):
        """
        corpus: list – корпус текстов
        """
        self.freq = {}
        den = 0
        for sentence in corpus:
            for word in sentence:
                if word not in self.freq:
                    self.freq[word] = 0
                self.freq[word] += 1
                den += 1
        for word in self.freq:
            self.freq[word] = self.freq[word] / den
        self.prefix_tree = PrefixTree(self.freq.keys())

    def get_words_and_probs(self, prefix: str):
        """
        Возвращает список слов, начинающихся на prefix,
        с их вероятностями (нормировать ничего не нужно)
        """
        words, probs = [], []
        possible_words = self.prefix_tree.search_prefix(prefix)
        for w in possible_words:
            words.append(w)
            probs.append(self.freq[w])
        return words, probs