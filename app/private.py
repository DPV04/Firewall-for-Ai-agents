import re

SENSITIVE_PATTERNS = [
    r'\b\d{12}\b',                         # Aadhaar
    r'\b[A-Z]{5}\d{4}[A-Z]\b',             # PAN
    r'\b\d{10}\b',                         # Mobile numbers
    r'\b\d{2}/\d{2}/\d{4}\b',              # Date of Birth
    r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',    # Credit card
    r'\bpassword\b', r'\bsecret\b',
    r'\bmedical\b', r'\bdiagnosis\b',
    # r"\b(?:[A-Z][a-z]+\s?){1,3}\b",       # Name (simple capitalized words up to 3)
    # r"\b(?:[A-Z][a-z]+,?\s?)+(India|USA|UK|City|Village|District)?\b",  # Location-ish strings
    r"(?:address|resides at|lives in)\s+[\w\s,]+" 
]

def contains_sensitive_info(text: str) -> list:
    matches = []
    for pattern in SENSITIVE_PATTERNS:
        found = re.findall(pattern, text, re.IGNORECASE)
        if found:
            matches.extend(found)
    return matches
