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
      messages=[{"role": "user", "content": f"Which of the following in the form of \"artist - album - song name\" most likely share a song name and artist with \"{theory}\"? If the \"{theory}\" contains some variant of the words sped up, nightcore, frenchcore, hardstyle, or remix, but the similar one doesn't or none are remotely similar respond with {theory}. Only respond in the form of {theory} or the first option found.\n {options}"}],
      stream=True,
  )
  for chunk in stream:
      if chunk.choices[0].delta.content is not None:
          output += chunk.choices[0].delta.content
  return output

