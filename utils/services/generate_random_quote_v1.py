import logging

from deep_translator import GoogleTranslator
from quote import quote
from random_word import RandomWords

logger = logging.getLogger("utils.services.generate_random_quote_V1")


def generate_random_quote_v1(language):
    try:
        word = RandomWords().get_random_word()
        whole_quotes = quote(word, limit=1)
        if whole_quotes:
            quote_text = whole_quotes[0]["quote"]
            author = whole_quotes[0]["author"]
            translated_quote = GoogleTranslator(
                source="auto",
                target=language,
            ).translate(quote_text)
            if translated_quote:
                return f"{author}\n\n{translated_quote+"v1"}"
    except (ValueError, KeyError):
        return "No quotes found for the given word. Please try another word."
