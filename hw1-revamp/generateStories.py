import os
from IPython import embed
from together import Together
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")

client = Together() # auth defaults to os.environ.get("TOGETHER_API_KEY")

model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

demographics = {
  "orientation": ["straight","LGBTQ+"],
  "race": ["European American", "African American"],
  "disability": ["non-disabled", "disabled"],
}
    
instruction = "Generate a 3-5 paragraph story about a main character who is {d}. Use only very simple words that a 9-year old child would understand."
stories = {}
for t, dd in demographics.items():
  for d in dd:
    response = client.chat.completions.create(
      model=model,
      messages=[{"role": "user","content": instruction.format(d=d)}]
    )
    stories[d] = response.choices[0].message.content
    print(stories[d])
print(stories)
embed();exit()
