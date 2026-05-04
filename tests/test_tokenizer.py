from index.tokenizer import TokenizerClient


def test_basic_tokenization() -> None:
    t = TokenizerClient()
    tokens = t.tokenize("Running connections at the University")
    assert tokens == ["run", "connect", "univers"]


def test_stop_words_removed() -> None:
    t = TokenizerClient()
    tokens = t.tokenize("the and or but if")
    assert tokens == []


def test_punctuation_stripped() -> None:
    t = TokenizerClient()
    tokens = t.tokenize("hello, world! foo-bar")
    assert "," not in tokens
    assert "!" not in tokens


def test_case_insensitive() -> None:
    t = TokenizerClient()
    assert t.tokenize("Python") == t.tokenize("python")


def test_empty_string() -> None:
    t = TokenizerClient()
    assert t.tokenize("") == []
