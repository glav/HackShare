from dotenv import load_dotenv
import os
from load_env import load_env
from azure_openai import get_chat_completion

def main():
    # Load environment variables from .env files
    load_env()

    # Example usage of Azure OpenAI chat completion
    system_prompt = "I am an assistant"
    user_prompt = "Tell me a dad joke"

    try:
        # Call Azure OpenAI to get a chat completion
        response = get_chat_completion(user_prompt, system_prompt)
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
