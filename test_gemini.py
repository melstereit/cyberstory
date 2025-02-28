import unittest
import json
from google.generativeai import configure, list_models
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def list_available_models(api_key):
    configure(api_key=api_key)
    for m in list_models():
        print(m.name)

api_key = os.getenv("GOOGLE_API_KEY")
configure(api_key=api_key)
client = genai.Client(api_key=api_key)

class MyTestCase(unittest.TestCase):

    def test_api_key(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        assert api_key is not None and api_key != "", "GOOGLE_API_KEY is not set or is empty"
        print("API key loaded successfully.")
        return api_key

    @unittest.skip("This test is currently disabled")
    def test_gemini(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            print("Error: GOOGLE_API_KEY not found in environment variables.")
            return

        try:
            # Initialize the Gemini model
            genai.configure(api_key=api_key)
            llm = genai.GenerativeModel("models/gemini-2.0-flash-lite")

            # Test prompt
            prompt = "What are three interesting facts about the planet Mars?"

            # Generate a response
            response = llm.generate_content(prompt)

            print(response.text)
            # Assert that the response starts with the expected phrase
            assert response.text.strip().startswith("Here are three interesting facts about the planet Mars:"), \
                "Response does not start with the expected phrase"
            print("Assertion passed: Response starts with the expected phrase.")

        except AssertionError as ae:
            print(f"Assertion Error: {ae}")

        except Exception as e:
            print(f"An error occurred: {e}")

    @unittest.skip("This test is currently disabled")
    def test_gemini_response_json_dump(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            print("Error: GOOGLE_API_KEY not found in environment variables.")
            return

        try:
            # Initialize the Gemini model
            genai.configure(api_key=api_key)
            llm = genai.GenerativeModel("models/gemini-2.0-flash-lite")

            # Test prompt
            prompt = "What are three interesting facts about the planet Mars?"

            # Generate a response
            response = llm.generate_content(prompt)

            print(json.dumps(response.to_dict(), indent=2, sort_keys=True))

        except Exception as e:
            print(f"An error occurred: {e}")

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
    print("Available models:")
    api_key = os.getenv("GOOGLE_API_KEY")
    list_available_models(api_key)

    unittest.main()
