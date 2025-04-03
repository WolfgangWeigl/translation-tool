import pytest
from unittest.mock import patch, MagicMock
from app.translation.xml_translator import process_xml_translation, translate_xml, merge_xml, parse_xml, finalize_xml, skip_element
from lxml import etree as ET

@pytest.mark.unit
def test_process_xml_translation_success():
    # Test für den "single" Übersetzungstyp
    temp_data = {
        'original': b"<xml>original</xml>",
        'translation': b"<xml>translated</xml>",  # Erwartete Übersetzung
        'srcLang': 'en',
        'destLang': 'de',
        'transType': 'single'
    }

    expected_results = {
        'original': b"<xml>original</xml>",
        'translation': b"<xml>translated</xml>",  # Erwartetes Ergebnis
        'merged': None,
        'progress': 100
    }

    # Mock für die translate_xml Funktion, um die Übersetzungslogik zu isolieren
    with patch('app.translation.xml_translator.translate_xml') as mock_translate_xml:
        mock_translate_xml.return_value = (b"<xml>translated</xml>", 100, [])

        result = process_xml_translation(temp_data, socketio=None)

        assert result['original'] == expected_results['original']
        assert result['translation'] == expected_results['translation']
        assert result['merged'] == expected_results['merged']
        assert result['progress'] == expected_results['progress']

@pytest.mark.unit
def test_process_xml_translation_multiple():
    # Test für den "multiple" Übersetzungstyp
    temp_data = {
        'original': b"<xml>original</xml>",
        'translation': b"<xml>translated</xml>",  # Erwartete Übersetzung
        'srcLang': 'en',
        'destLang': 'de',
        'transType': 'multiple'
    }

    expected_results = {
        'original': b"<xml>original</xml>",
        'translation': b"<xml>translated</xml>",  # Erwartetes Ergebnis
        'merged': b"<xml>merged</xml>",
        'progress': 100
    }

    # Mock für die translate_xml und merge_xml Funktionen
    with patch('app.translation.xml_translator.translate_xml') as mock_translate_xml, \
         patch('app.translation.xml_translator.merge_xml') as mock_merge_xml:
        mock_translate_xml.return_value = (b"<xml>translated</xml>", 100, ['translated_text'])
        mock_merge_xml.return_value = (b"<xml>merged</xml>", 100)

        result = process_xml_translation(temp_data, socketio=None)

        assert result['original'] == expected_results['original']
        assert result['translation'] == expected_results['translation']
        assert result['merged'] == expected_results['merged']
        assert result['progress'] == expected_results['progress']

@pytest.mark.unit
def test_process_xml_translation_invalid_trans_type():
    # Test für ungültigen Übersetzungstyp
    temp_data = {
        'original': b"<xml>original</xml>",
        'translation': b"<xml>translated</xml>",
        'srcLang': 'en',
        'destLang': 'de',
        'transType': 'invalid'
    }

    with pytest.raises(ValueError, match="Unbekannter Übersetzungstyp: invalid"):
        process_xml_translation(temp_data, socketio=None)

@pytest.mark.unit
def test_translate_xml():
    # Test für die translate_xml Funktion
    temp_data = {
        'original': b"<xml><text>original</text></xml>",
        'srcLang': 'en',
        'destLang': 'de',
        'url': 'http://fake-url'
    }

    # Mock der externen Übersetzungsfunktion
    with patch('app.translation.xml_translator.translate_text') as mock_translate_text:
        mock_translate_text.return_value = "translated"

        result, progress, translated_map = translate_xml(temp_data, socketio=None)

        assert progress == 100
        assert translated_map == ['translated']
        assert result == b"<xml><text><![CDATA[translated]]></text></xml>"

@pytest.mark.unit
def test_merge_xml():
    # Test für die merge_xml Funktion
    temp_data = {
        'original': b"<xml><text>original</text></xml>",
        'srcLang': 'en',
        'destLang': 'de'
    }

    translated_texts = ['translated']

    # Mock der merge_text_blocks Funktion
    with patch('app.translation.xml_translator.merge_text_blocks') as mock_merge_text_blocks:
        mock_merge_text_blocks.return_value = "merged"
        
        result, progress = merge_xml(temp_data, translated_texts)

        assert progress == 100
        assert result == b"<xml><text><![CDATA[merged]]></text></xml>"

@pytest.mark.unit
def test_parse_xml():
    # Test für die parse_xml Funktion
    xml_bytes = b"<xml><text>content</text></xml>"

    result = parse_xml(xml_bytes)

    assert result.tag == "xml"
    assert len(result.findall(".//text")) == 1

@pytest.mark.unit
def test_finalize_xml():
    # Test für die finalize_xml Funktion
    root = ET.Element("xml")
    el = ET.SubElement(root, "text")
    el.text = "content"

    result = finalize_xml(root)

    assert b"<xml><text><![CDATA[content]]></text></xml>" in result or b"<xml><text>content</text></xml>" in result


@pytest.mark.unit
def test_skip_element():
    # Test für die skip_element Funktion
    el = MagicMock()
    el.getparent.return_value = MagicMock(tag="questionvariables")
    
    result = skip_element(el)

    assert result is True

    el.getparent.return_value = MagicMock(tag="other")
    
    result = skip_element(el)

    assert result is False
