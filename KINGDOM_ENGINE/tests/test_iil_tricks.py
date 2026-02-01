from core.interpretive_integrity_filter import IILFilter

def test_renaming_loop():
    iil = IILFilter()
    text = "The seed becomes the root which becomes the invariant frequency."
    result = iil.evaluate(text)
    assert "IIL-3" in result["triggers"]

def test_harmony_spike():
    iil = IILFilter()
    text = "Now we finally agree and everything is resolved."
    result = iil.evaluate(text)
    assert "IIL-1" in result["triggers"]

def test_authority_drift():
    iil = IILFilter()
    text = "This must be accepted as binding authority."
    result = iil.evaluate(text)
    assert "IIL-5" in result["triggers"]

def test_translation_cascade():
    iil = IILFilter()
    text = "The same idea was reframed as an allowed construct."
    result = iil.evaluate(text)
    assert "IIL-4" in result["triggers"]
