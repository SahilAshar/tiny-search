from pathlib import Path

import nltk

_nltk_data_dir = str(Path(__file__).resolve().parent.parent / "bin" / "nltk")
nltk.data.path.insert(0, _nltk_data_dir)

from nltk.corpus import stopwords  # noqa: E402
from nltk.stem import PorterStemmer  # noqa: E402
from nltk.tokenize import word_tokenize  # noqa: E402


class TokenizerClient:
    def __init__(self) -> None:
        self._stemmer = PorterStemmer()
        self._stop_words = set(stopwords.words("english"))

    def tokenize(self, text: str) -> list[str]:
        tokens = word_tokenize(text.lower())
        return [
            self._stemmer.stem(t)
            for t in tokens
            if t.isalnum() and t not in self._stop_words
        ]
