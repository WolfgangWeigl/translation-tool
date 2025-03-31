import os
import shutil
import requests
from lxml import etree as ET
from flask_socketio import emit

def translate_text(url: str, text: str, source_lang: str, target_lang: str) -> str:
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "html"
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()["translatedText"]
    except Exception as e:
        print(f"Translation error: {e}")
        return
    
def translate_xml_element(url: str, element: ET._Element, source_lang: str, target_lang: str):
    try:
        if element.text and element.text.strip():
            if not "<script" in element.text and not "</script>" in element.text:
                element.text = translate_text(url=url, text=element.text, source_lang=source_lang, target_lang=target_lang)
        for child in element:
            translate_xml_element(url=url, element=child, source_lang=source_lang, target_lang=target_lang)
    except Exception as e:
        print(f"Error translating XML element for url: {url}: {e}")

def translate_xml_file(url: str, input_path: str, output_path: str, source_lang: str, target_lang: str):
    try:
        # Parse XML
        parser = ET.XMLParser(remove_blank_text=True)
        tree: ET._ElementTree = ET.parse(input_path, parser)
        root = tree.getroot()

        # Translate
        translate_xml_element(url=url, element=root, source_lang=source_lang, target_lang=target_lang)

        # Save with XML declaration
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as file:
            file.write(ET.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True))
        print(f"Translated XML file saved to {output_path}")

    except ET.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")
    except Exception as e:
        print(f"Error processing XML file: {e}")

def translate_mbz(app, src_lang, dest_lang):
        url = app.config['LT_URL'] + "/translate"
        total_files = sum(len(files) for _, _, files in os.walk(app.config['EXTRACTION_FOLDER']))
        processed_files = 0
        for (root, dirs, files) in os.walk(app.config['EXTRACTION_FOLDER']):
            for file in files:
                total_files += 1
                input_path = os.path.join(root, file)
                output_path = os.path.join(app.config['TRANSLATION_FOLDER'], os.path.relpath(input_path, app.config['EXTRACTION_FOLDER']))
                if file.endswith('.xml'):
                    translate_xml_file(url, input_path, output_path, src_lang, dest_lang)
                else:
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    shutil.copy2(input_path, output_path)
                processed_files +=1
                progress = (processed_files / total_files) * 100
                print(f"Fortschritt: {processed_files}/{total_files} Dateien verarbeitet ({progress:.2f}%)", end='\r')
                emit('translation_progress', {'progress': progress, 'finished': processed_files == total_files})