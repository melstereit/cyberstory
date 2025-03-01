import os
import unittest

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

class MyTestCase(unittest.TestCase):

    def test_api_key(self):
        assert api_key is not None and api_key != "", "GOOGLE_API_KEY is not set or is empty"
        print("API key loaded successfully.")

    def test_new_gemini_sdk(self):
        try:
            prompt = "What are three interesting facts about the planet Mars?"

            # Generate a response
            response = client.models.generate_content(
                model='gemini-2.0-flash-lite',
                contents=prompt
            )

            print(response.model_dump_json(exclude_none=True, indent=2))

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    unittest.main()
