# translation/merge_utils.py

def merge_text_blocks(original: str, translated: str, src_lang: str, dest_lang: str) -> str:
    return (
        f"[[lang code=\"{src_lang}\"]]\n"
        f"{original}\n"
        f"[[/lang]]\n"
        f"[[lang code=\"{dest_lang}\"]]\n"
        f"{translated}\n"
        f"[[/lang]]"
    )