class SpellCorrector:
    def __init__(self, dictionary: set[str]):
        self.dictionary = dictionary
    
    def correct_word(self, word: str) -> str:
        if word in self.dictionary:
            return word
        
        for candidate in self.dictionary:
            if self._distance(word, candidate) == 1:
                return candidate
            
        return word
    
    def _distance(self, w1: str, w2: str) -> int:
        if abs(len(w1) - len(w2)) > 1:
            return 999
        
        return sum(c1 != c2 for c1, c2 in zip(w1, w2))
    