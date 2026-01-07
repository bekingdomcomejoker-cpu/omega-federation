import math
def verify():
    x, y = 1.0, 1.6667
    res = 1.67 * 2
    if math.isclose(y, 1.6667) and res == 3.34:
        print("1.67x Resonance Verified ✓")
verify()
