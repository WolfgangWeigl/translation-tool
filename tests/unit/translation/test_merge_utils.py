# tests/unit/translation/test_merge_utils.py

import pytest
from app.translation.merge_utils import merge_text_blocks

@pytest.mark.unit
def test_merge_text_blocks_basic():
    original = "Dies ist ein Test."
    translated = "This is a test."
    src_lang = "de"
    dest_lang = "en"

    result = merge_text_blocks(original, translated, src_lang, dest_lang)

    expected = (
        '[[lang code="de"]]\n'
        'Dies ist ein Test.\n'
        '[[/lang]]\n'
        '[[lang code="en"]]\n'
        'This is a test.\n'
        '[[/lang]]'
    )

    assert result == expected

@pytest.mark.unit
def test_merge_text_blocks_handles_empty_original():
    result = merge_text_blocks("", "Hello", "xx", "yy")

    assert '[[lang code="xx"]]\n\n[[/lang]]' in result
    assert '[[lang code="yy"]]\nHello\n[[/lang]]' in result

@pytest.mark.unit
def test_merge_text_blocks_handles_empty_translation():
    result = merge_text_blocks("Hallo", "", "de", "en")

    assert '[[lang code="de"]]\nHallo\n[[/lang]]' in result
    assert '[[lang code="en"]]\n\n[[/lang]]' in result
