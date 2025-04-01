# translation/libretranslate_api.py

import requests

def translate_text(url, text, source_lang, target_lang):
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "html"
    }

    try:
        res = requests.post(url, data=payload)
        res.raise_for_status()
        return res.json()['translatedText']
    except Exception as e:
        print(f"Übersetzungsfehler: {e}")
        return text  # Fallback
