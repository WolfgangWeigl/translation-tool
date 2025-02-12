import requests
from lxml import etree as ET

def translate_text(url, text, source_lang, target_lang):
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
        return None
    
def translate_xml(app, url, temp_data):
    try:
        parser = ET.XMLParser(remove_blank_text=True)
        root = ET.fromstring(temp_data['original'], parser)

        for text_element in root.findall(".//text"):
            parent = text_element.find("..")
            if parent is not None and (parent.tag == "questionvariables" or parent.tag == "feedbackvariables"):
                continue # Skip translation of questionvariables

            original_text = text_element.text
            if original_text:
                    translated_text = translate_text(url=url, text=original_text, source_lang=temp_data['srcLang'], target_lang=temp_data['destLang'])
                    text_element.text = translated_text

        return ET.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)
    
    except Exception as e:
        app.logger.error(f"XML translation error: {e}")
        raise ValueError(f"XML translation error: {e}")    

# TODO: Mask Text

# TODO: Translate XML

# TODO: Demask Text

