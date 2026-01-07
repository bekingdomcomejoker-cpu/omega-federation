def summarize(text):
    lines = text.splitlines()
    return {"lines": len(lines), "first": lines[0] if lines else ""}
