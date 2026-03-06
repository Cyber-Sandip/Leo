# commands/phase1_engine.py

import re


def phase1_engine(text):

    text = text.lower()

    # OPEN APP
    if "open chrome" in text or "launch chrome" in text:
        return {
            "intent": "OPEN_APP",
            "entities": {"app": "chrome"},
            "confidence": 1.0
        }

    if "open notepad" in text:
        return {
            "intent": "OPEN_APP",
            "entities": {"app": "notepad"},
            "confidence": 1.0
        }

    if "open calculator" in text:
        return {
            "intent": "OPEN_APP",
            "entities": {"app": "calculator"},
            "confidence": 1.0
        }

    # TIME
    if "time" in text:
        return {
            "intent": "GET_TIME",
            "entities": {},
            "confidence": 1.0
        }

    # DATE
    if "date" in text or "today" in text:
        return {
            "intent": "GET_DATE",
            "entities": {},
            "confidence": 1.0
        }

    # SEARCH
    if "search" in text:
        query = text.replace("search", "").strip()

        return {
            "intent": "SEARCH_WEB",
            "entities": {"query": query},
            "confidence": 1.0
        }

    # EXIT
    if "exit" in text or "quit" in text:
        return {
            "intent": "EXIT",
            "entities": {},
            "confidence": 1.0
        }

    return {
        "intent": "UNKNOWN",
        "entities": {},
        "confidence": 0.0
    }