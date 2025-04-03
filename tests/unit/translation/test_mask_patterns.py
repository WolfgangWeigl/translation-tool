# tests/unit/translation/test_mask_patterns.py

import pytest
from app.translation.mask_patterns import mask_text, unmask_text

@pytest.mark.unit
def test_mask_text_replaces_patterns_with_placeholders():
    input_text = (
        "Start [[ input:username ]] middle [[ feedback:hint ]] end [[ /if ]]."
    )
    masked_text, masks = mask_text(input_text)

    # Überprüfe Platzhalter
    assert "MASK#0" in masked_text
    assert "MASK#1" in masked_text
    assert "MASK#2" in masked_text

    # Stelle sicher, dass die ursprünglichen Texte korrekt gemerkt wurden
    assert masks["MASK#0"] == "[[ input:username ]]"
    assert masks["MASK#1"] == "[[ feedback:hint ]]"
    assert masks["MASK#2"] == "[[ /if ]]"

@pytest.mark.unit
def test_unmask_text_restores_original_text():
    input_text = "Start MASK#0 middle MASK#1 end MASK#2."
    masks = {
        "MASK#0": "[[ input:username ]]",
        "MASK#1": "[[ feedback:hint ]]",
        "MASK#2": "[[ /if ]]"
    }

    restored_text = unmask_text(input_text, masks)

    expected = "Start [[ input:username ]] middle [[ feedback:hint ]] end [[ /if ]]."
    assert restored_text == expected

@pytest.mark.unit
def test_mask_text_with_no_patterns_returns_original():
    text = "This text has no special patterns."
    masked_text, masks = mask_text(text)

    assert masked_text == text
    assert masks == {}
