from google import genai
from google.genai import types

import requests

image_path = "http://192.168.1.127/capture"
image_bytes = requests.get(image_path).content
image = types.Part.from_bytes(
  data=image_bytes, mime_type="image/jpeg"
)

client = genai.Client()
prompt = "Bekijk de foto van de watermeter heel zorgvuldig en vergroot waar nodig. De vier witte cijfers (wieltjes) geven het aantal kubieke meters (m³) — dat is het gehele getal vóór de komma. De vier rode wijzertjes geven de cijfers ná de komma (de decimale cijfers). Lees alle 8 cijfers exact en geef alleen de meterstand terug in één regel, zonder extra woorden of eenheid, in het format met een punt als decimaalscheiding: XXXX.YYYY (bijvoorbeeld 0123.4567). Als één of meer cijfers onleesbaar zijn of de foto onvoldoende kwaliteit heeft om de volledige acht cijfers betrouwbaar te bepalen, antwoord dan precies met: ERROR (uitroepende letters, zonder toelichting)."
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-09-2025",
    contents=["Wat zieje op de foto?", image],
)

#print(float(response.text))
print(response.text)