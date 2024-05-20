from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
  organization=os.getenv("OPEN_AI_ORG"),
  project=os.getenv("OPEN_AI_PROJECT"),
  api_key=os.getenv("OPEN_AI_API_KEY")
)

def query(theory, options):
  output = ""
  stream = client.chat.completions.create(
      model="gpt-4",
      messages=[{"role": "user", "content": f"Which of the following most likely share the song name and artist with \"{theory}\"? If the original contains some variant of the words sped up, nightcore, frenchcore, hardstyle, or remix, but the new one doesn't, or none are remotely similar, respond with {theory}. Only respond in the form of {theory} or the first option found.\n {options}"}],
      stream=True,
  )
  for chunk in stream:
      if chunk.choices[0].delta.content is not None:
          output += chunk.choices[0].delta.content
  return output

if __name__ == "__main__":
  theory_name = "BBY GOYARD - Run Shannon Run"
  #theory_name = "Sefa - One Tribe (Official Defqon.1 Anthem)"
  options = """BBY GOYARD - Run Shannon Run
BBY GOYARD - VETTE SUM (SHANNONGRAM)
BBY GOYARD, Tyson, evilgiane - Shannon's Ladder
BBY GOYARD - Sabonis (BONUS!)
BBY GOYARD - GRANT ME ACCESS
BBY GOYARD - TH13TEEN GHOSTS
BBY GOYARD - Astaroth4ever
BBY GOYARD - Trident
BBY GOYARD - Trackhawk
Pedroflexin, BBY GOYARD - Hotshot"""
  print(query(theory_name, options))