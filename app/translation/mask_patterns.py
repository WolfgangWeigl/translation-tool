# translation/mask_patterns.py

import re

PATTERNS = [
    re.compile(r'\[\[\s*input\s*:\s*\w+\s*\]\]'),
    re.compile(r'\[\[\s*validation\s*:\s*\w+\s*\]\]'),
    re.compile(r'\[\[\s*feedback\s*:\s*\w+\s*\]\]'),
    re.compile(r'\[\[\s*if test\s*=\.+\s*\]\]'),
    re.compile(r'\[\[\s*elif test\s*=\.+\s*\]\]'),
    re.compile(r'\[\[\s*else\s*\]\]'),
    re.compile(r'\[\[\s*/\s*if\s*\]\]'),
    re.compile(r'\[\[\s*reveal\.+\s*\]\]'),
    re.compile(r'\[\[\s*/\s*reveal\s*\]\]'),
    re.compile(r'\[\[\s*jsxgraph\.*\s*\]\]'),
    re.compile(r'\[\[\s*/\s*jsxgraph\s*\]\]'),
    re.compile(r'\[\[\s*facts\s*:\.+\s*\]\]')
]

def mask_text(text):
    masks = {}
    for pattern in PATTERNS:
        for match in pattern.findall(text):
            placeholder = f"MASK#{len(masks)}"
            text = text.replace(match, placeholder)
            masks[placeholder] = match
    return text, masks

def unmask_text(text, masks):
    for placeholder, original in masks.items():
        text = text.replace(placeholder, original)
    return text
