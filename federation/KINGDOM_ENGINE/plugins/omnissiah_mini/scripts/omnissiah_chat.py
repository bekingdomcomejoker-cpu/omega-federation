from text_generation import Client

# Create client for CPU-friendly HuggingFace model
client = Client("tiiuae/falcon-7b-instruct")  # small model, CPU friendly

while True:
    prompt = input("Omnissiah> ")
    if prompt.lower() == "exit":
        break
    response = client.generate(prompt, max_new_tokens=50)
    print(response.text)
