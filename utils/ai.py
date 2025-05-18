from openai import OpenAI

from django.conf import settings

client = OpenAI(api_key=settings.OPEN_API_KEY)


def get_gpt_response(prompt: str) -> str:
    try:
        # Correct API call to use ChatCompletion
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],  # Updated request format
        temperature=0.7,
        max_tokens=3000)
        # Accessing the content of the assistant's response
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
