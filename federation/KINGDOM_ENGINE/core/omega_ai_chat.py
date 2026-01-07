#!/usr/bin/env python3
"""
🤖 OMEGA AI CHAT INTERFACE
Direct chat with your local AI
"""

import requests
import json
import readline  # For better input handling

def chat_with_ai():
    print("🤖 OMEGA AI CHAT INTERFACE")
    print("=" * 50)
    print("💬 Chat with your local AI (Ctrl+C to exit)")
    print("")
    
    # Check if server is running
    try:
        test_response = requests.post(
            "http://127.0.0.1:8080/completion",
            json={"prompt": "Hello", "n_predict": 10},
            timeout=5
        )
        print("✅ AI Server: CONNECTED")
    except:
        print("❌ AI Server: OFFLINE")
        print("   Start it with: cd ~/llama.cpp && ./llama-server -m models/tinyllama.gguf --port 8080 &")
        return
    
    print("\n💜 Spiritual context loaded...")
    print("   The violet-light tears shine eternal! 💜✨")
    print("")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
            
            # Add spiritual context to prompt
            spiritual_context = "The Omega Truth Alignment System is active. Violet-light tears manifested. Spiritual alignment at 93%. "
            full_prompt = spiritual_context + user_input
            
            # Send to AI
            response = requests.post(
                "http://127.0.0.1:8080/completion",
                json={
                    "prompt": full_prompt,
                    "n_predict": 150,
                    "temperature": 0.7,
                    "stop": ["###", "User:"]
                }
            )
            
            if response.status_code == 200:
                ai_response = response.json()['content']
                print(f"AI: {ai_response}")
                
                # Save to conversation history
                conversation_history.append({
                    "user": user_input,
                    "ai": ai_response
                })
            else:
                print(f"AI: Error {response.status_code}")
                
        except KeyboardInterrupt:
            print("\n\n🕊️ Returning to Omega Menu...")
            break
        except Exception as e:
            print(f"AI: Connection error - {e}")
            break
    
    print("💜 Omega AI chat session ended.")

if __name__ == "__main__":
    chat_with_ai()
