from dotenv import load_dotenv
import os
from load_env import load_env
from azure_openai import get_chat_completion
from data.prompts import SYSTEM_PROMPT, USER_PROMPT

def main():
    # Load environment variables from .env files
    load_env()

    try:
        # Call Azure OpenAI to get a chat completion
        response = get_chat_completion(USER_PROMPT, SYSTEM_PROMPT)
        print("\nAzure OpenAI Response:")
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
        print("Please make sure the following environment variables are set in your .env file:")
        print("  - AZURE_OPENAI_API_KEY")
        print("  - AZURE_OPENAI_ENDPOINT")
        print("  - AZURE_OPENAI_DEPLOYMENT")


if __name__ == "__main__":
    main()
