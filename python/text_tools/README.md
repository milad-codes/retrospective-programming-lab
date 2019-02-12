# Text tools

| File | Contents |
| --- | --- |
| `word_count.py` | word frequencies with a Unicode-aware tokenizer; also a command-line tool |
| `ciphers.py` | Caesar and Vigenère ciphers, plus breaking a Caesar shift with a chi-squared test against English letter frequencies |
| `rle.py` | run-length encoding with input validation |

```bash
python3 -m text_tools.word_count --top 5 README.md   # from the python/ folder
python3 -m unittest discover -s text_tools -t .
```

The tokenizer uses `[^\W_]` (a word character that is not an underscore), so "Müller" and "café" are single words, and
an apostrophe or hyphen inside a word keeps "don't" and "state-of-the-art" together.
