import re


def phase1_engine(text):

    text = text.lower().strip()

    # OPEN ANY APP
    match = re.search(r"(open|launch|start)\s+(.*)", text)

    if match:
        app = match.group(2)

        return {
            "intent": "OPEN_APP",
            "entities": {"app": app},
            "confidence": 1.0
        }

    # OPEN CAMERA
    if "camera" in text:
        return {
            "intent": "OPEN_CAMERA",
            "entities": {},
            "confidence": 1.0
        }

    # VOLUME UP
    if "volume up" in text:
        return {
            "intent": "VOLUME_UP",
            "entities": {},
            "confidence": 1.0
        }

    # VOLUME DOWN
    if "volume down" in text:
        return {
            "intent": "VOLUME_DOWN",
            "entities": {},
            "confidence": 1.0
        }

    # RESTART
    if "restart" in text:
        return {
            "intent": "RESTART",
            "entities": {},
            "confidence": 1.0
        }

    # SHUTDOWN
    if "shutdown" in text:
        return {
            "intent": "SHUTDOWN",
            "entities": {},
            "confidence": 1.0
        }

    # SCREENSHOT
    if "screenshot" in text:
        return {
            "intent": "SCREENSHOT",
            "entities": {},
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
    if "exit" in text or "quit" in text or "stop" in text:
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