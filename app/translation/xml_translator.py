# app/translation/xml_translator.py

from lxml import etree as ET
from app.translation.mask_patterns import mask_text, unmask_text
from app.translation.libretranslate_api import translate_text
from app.translation.merge_utils import merge_text_blocks
from app.utils.progress import emit_progress
from flask import current_app

def process_xml_translation(data, socketio=None):
    if data['transType'] == 'single':
        translated, progress, _ = translate_xml(data, socketio)
        return {
            "original": data['original'],
            "translation": translated,
            "merged": None,
            "progress": progress
        }

    elif data['transType'] == 'multiple':
        translated, progress, translated_texts = translate_xml(data, socketio)
        merged, _ = merge_xml(data, translated_texts)

        return {
            "original": data['original'],
            "translation": translated,
            "merged": merged,
            "progress": progress
        }

    else:
        raise ValueError(f"Unbekannter Übersetzungstyp: {data['transType']}")


def translate_xml(data, socketio=None):
    root = parse_xml(data['original'])
    total = len(root.findall(".//text"))
    count = 0
    translated_map = []

    for el in root.findall(".//text"):
        if skip_element(el):
            translated_map.append(None)
            continue

        src_text = el.text or ""
        masked_text, masks = mask_text(src_text)
        translated = translate_text(data['url'], masked_text, data['srcLang'], data['destLang'])
        translated = unmask_text(translated, masks)

        if translated is None:
            translated = ""

        el.text = ET.CDATA(translated)
        translated_map.append(translated)

        count += 1
        emit_progress(socketio, count, total)

    return finalize_xml(root), 100, translated_map


def merge_xml(data, translated_texts):
    root = parse_xml(data['original'])

    for i, el in enumerate(root.findall(".//text")):
        if skip_element(el):
            continue

        src_text = el.text or ""
        translated = translated_texts[i]

        if translated is None:
            continue

        merged = merge_text_blocks(src_text, translated, data['srcLang'], data['destLang'])
        el.text = ET.CDATA(merged)

    return finalize_xml(root), 100


def parse_xml(xml_bytes):
    parser = ET.XMLParser(remove_blank_text=False, strip_cdata=False, resolve_entities=False)
    return ET.fromstring(xml_bytes, parser)

def finalize_xml(root):
    xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
    return xml_str.replace("&lt;", "<").replace("&gt;", ">").encode('utf-8')

def skip_element(el):
    parent = el.getparent()
    return parent is not None and parent.tag in ("questionvariables", "feedbackvariables")
