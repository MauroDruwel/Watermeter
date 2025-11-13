import os
from openai import OpenAI
import requests
import base64

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

# Fetch the image from the camera
image_path = "http://192.168.1.127/capture"
image_bytes = requests.get(image_path).content

# Convert image to base64 for OpenAI API
image_base64 = base64.b64encode(image_bytes).decode('utf-8')

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
    temperature=1.0,
    top_p=1.0,
    model=model
)

print(response.choices[0].message.content)
"""

prompt = "Bekijk de foto van de watermeter heel zorgvuldig en vergroot waar nodig. De vier zwarte cijfers (witte wieltjes) geven het aantal kubieke meters (m³) — dat is het gehele getal vóór de komma. De vier witte cijfers (rode wijzertjes) geven de cijfers ná de komma (de decimale cijfers) Oppassen het laatste cijfer is niet altijd even goed zichtbaar, door een soort wijzer die ervoor zit, tel dus goed het aantal cijfers dat je ziet. Lees alle 8 cijfers exact en geef alleen de meterstand terug in één regel, zonder extra woorden of eenheid, in het format met een punt als decimaalscheiding: XXXX.YYYY (bijvoorbeeld 0123.4567). Als één of meer cijfers onleesbaar zijn of de foto onvoldoende kwaliteit heeft om de volledige acht cijfers betrouwbaar te bepalen, antwoord dan precies met: ERROR (uitroepende letters, met toelichting), tenzij het enkel over het laatste cijfer gaat, deze is minder belangrijk, dus probeer dan in te schatten wat het getal zou zijn."

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ],
    temperature=1.0,
    top_p=1.0,
    model=model
)

print(float(response.choices[0].message.content))
#print(response.choices[0].message.content)

"""