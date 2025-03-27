import re
import requests
from lxml import etree as ET

# Liste der regulären Ausdrücke für Maskierung
# TODO Hier weitere Muster ergänzen
PATTERNS = [
    re.compile(r'\[\[\s*input\s*:\s*\w+\s*\]\]'), 
    re.compile(r'\[\[\s*validation\s*:\s*\w+\s*\]\]'),  
    re.compile(r'\[\[\s*feedback\s*:\s*\w+\s*\]\]'),
    # If-Blöcke
    re.compile(r'\[\[\s*if test\s*=\.+\s*\]\]'),
    re.compile(r'\[\[\s*elif test\s*=\.+\s*\]\]'),
    re.compile(r'\[\[\s*else\s*\]\]'),
    re.compile(r'\[\[\s*\/\s*if\s*\]\]'),
    # Reveal-Blöcke
    re.compile(r'\[\[\s*reveal\.+\s*\]\]'),
    re.compile(r'\[\[\s*\/\s*reveal\s*\]\]'),
    # JSXGraph-Blöcke
    re.compile(r'\[\[\s*jsxgraph\.*\s*\]\]'),
    re.compile(r'\[\[\s*\/\s*jsxgraph\s*\]\]'),
    # Hint-Blöcke
    re.compile(r'\[\[\s*facts\s*:\.+\s*\]\]')
    # TODO Hier weitere Blöcke ergänzen
]

def translate_text(url, text, source_lang, target_lang):
    """ Sendet einen Text zur Übersetzung an die API """
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
        return text  # Fallback: Originaltext zurückgeben

def translate_xml(socketio, app, url, temp_data):
    try:
        parser = ET.XMLParser(remove_blank_text=False, strip_cdata=False, resolve_entities=False)
        root = ET.fromstring(temp_data['original'], parser)

        # Gesamte Anzahl der Textknoten, die übersetzt werden müssen
        total_texts = len(root.findall(".//text"))
        translated_count = 0  # Anzahl der bereits übersetzten Textknoten

        # Iteriere durch alle Textelemente und übersetze sie
        for text_element in root.findall(".//text"):
            
            parent = text_element.find("..")

            # Fragevariablen und Feedbackvariablen nicht übersetzen
            if parent is not None and parent.tag in ("questionvariables", "feedbackvariables"):
                translated_count += 1
                continue

            src_text = text_element.text

            if src_text:
               
               # Maskieren
                masked_values = {}
                for pattern in PATTERNS:
                    matches = pattern.findall(src_text)
                    for match in matches:
                        placeholder = f"MASK#{len(masked_values)}"
                        src_text = src_text.replace(match, placeholder)
                        masked_values[placeholder] = match

                # Übersetzen
                dest_text = translate_text(url, src_text, temp_data['srcLang'], temp_data['destLang'])

                # Demaskieren
                if masked_values:
                    for placeholder, original in masked_values.items():
                        dest_text = dest_text.replace(placeholder, original)

            text_element.text = dest_text

            # Fortschritt berechnen
            translated_count += 1
            progress = (translated_count / total_texts) * 100

            # Sende Fortschritt über SocketIO an den Client
            socketio.emit('translation_progress', {'progress': progress, 'finished': False})

        # Umwandeln in String, Ersetzungen vornehmen und zurück in Bytes konvertieren
        result_str = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
        result_str = result_str.replace("&lt;", "<").replace("&gt;", ">")
        result = result_str.encode('utf-8') 
        
        return result, progress

    except Exception as e:
        raise ValueError(f"XML translation error: {e}")
