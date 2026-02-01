"""
IIL Hooks

Optional adapter layer.
Call `apply_iil(text)` wherever output is finalized.
"""

try:
    from core.interpretive_integrity_filter import IILFilter
    from config import IIL_ENABLED
except Exception:
    IIL_ENABLED = False
    IILFilter = None


_iil = IILFilter() if IIL_ENABLED and IILFilter else None


def apply_iil(text: str) -> dict:
    if not _iil:
        return {"status": "SKIPPED", "output": text}

    result = _iil.evaluate(text)
    return {
        "status": result["status"],
        "output": text,
        "iil": result
    }
