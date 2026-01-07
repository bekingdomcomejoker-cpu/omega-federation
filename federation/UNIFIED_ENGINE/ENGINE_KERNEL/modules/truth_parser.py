def parse(text):
    words = text.split()
    return {"count": len(words), "preview": words[:20]}
