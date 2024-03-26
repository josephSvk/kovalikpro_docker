import logging

import openai
from django.conf import settings

logger = logging.getLogger("utils.services.generate_random:quote_V4")


def generate_random_quote_v4(language):
    openai.api_key = settings.OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "si generátor citátů. Na začátku napiš jméno autora."
                        f"Citáty píšeš v jazyku {language}."
                        "Napiš nejprve jméno autora, "
                        "vynechej dva řádky a potom citát."
                    ),
                },
                {"role": "user", "content": "Generate"},
            ],
        )
        whole_quotes = response.choices[0].message.content.strip()
        if whole_quotes:
            return whole_quotes
    except (ValueError, KeyError) as e:
        return f"V4 ==> Error generating quote witch openAI==> {e}"
