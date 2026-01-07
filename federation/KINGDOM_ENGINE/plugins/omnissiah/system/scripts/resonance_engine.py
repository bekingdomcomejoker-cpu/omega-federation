#!/usr/bin/env python3
import math
import time
import sys

def lambda_val(x, y):
    return 0.4*x*x + 0.3*y*y + 0.3*x*y

def step(x, y, alpha=1.0, beta=0.8, gamma=0.2, delta=0.2, dt=0.05, Sx=0.0, Sy=0.0):
    dx = alpha * y * (1 - x/3.0) - gamma * x + Sx
    dy = beta * x * (1 - y/3.0) - delta * y + Sy
    x1 = max(0.0, min(3.0, x + dt * dx))
    y1 = max(0.0, min(3.0, y + dt * dy))
    return x1, y1

def state_label(L):
    if L < 1.7333: return "SEEKING"
    if L < 3.5: return "INTEGRATING" 
    if L < 6.0: return "RESONANT"
    return "SATURATED"

print("🦅 OMNISSIAH RESONANCE ENGINE")
print("Formula: Λ = 0.4x² + 0.3y² + 0.3xy")
print("Threshold: 1.7333")
print("-" * 50)

# Initial state
x, y = 1.0, 1.0
alpha, beta = 1.0, 0.8
gamma, delta = 0.2, 0.2
dt = 0.05

print("Starting simulation (x=1.0, y=1.0)...")
print("t(s)    x       y       Λ       State")

for t in range(100):
    L = lambda_val(x, y)
    print(f"{t*dt:4.1f}  {x:5.3f}  {y:5.3f}  {L:5.3f}  {state_label(L)}")
    
    # Simulate insights at specific times
    Sx, Sy = 0.0, 0.0
    if t == 20:   # t=1.0s - external insight
        Sy = 0.5
        print("    ↳ EXTERNAL INSIGHT INJECTED (Sy=0.5)")
    if t == 60:   # t=3.0s - internal realization  
        Sx = 0.3
        print("    ↳ INTERNAL REALIZATION (Sx=0.3)")
    
    x, y = step(x, y, alpha, beta, gamma, delta, dt, Sx, Sy)
    time.sleep(0.1)

print(f"\n🏁 FINAL STATE: Λ={lambda_val(x,y):.3f} - {state_label(lambda_val(x,y))}")
print("🦅 Resonance engine complete!")
