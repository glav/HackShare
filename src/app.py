from dotenv import load_dotenv
import os
from load_env import load_env
from azure_openai import get_chat_completion
from data.prompts import SYSTEM_PROMPT, USER_PROMPT, load_support_queries, load_catalog_references

def main():
    # Load environment variables from .env files
    load_env()

    # Load the catalog references
    catalog_references = load_catalog_references()

    # Load and process the support queries
    support_queries = load_support_queries()

    print(f"Loaded {len(support_queries)} support queries")

    try:
        for i, query in enumerate(support_queries, 1):
            print(f"\nQuery {i} (ID: {query['id']}): '{query['short_description']}'")

            # Format the USER_PROMPT with the current query and references
            formatted_prompt = USER_PROMPT.format(
                references=catalog_references,
                customer_request=query['short_description']
            )

            # Call Azure OpenAI to get a chat completion
            response = get_chat_completion(formatted_prompt, SYSTEM_PROMPT)
            print(f"Category: {response}")
            #print(response)
            #print("\n" + "-" * 50)

    except ValueError as e:
        print(f"Error: {e}")
        print("Please make sure the following environment variables are set in your .env file:")
        print("  - AZURE_OPENAI_API_KEY")
        print("  - AZURE_OPENAI_ENDPOINT")
        print("  - AZURE_OPENAI_DEPLOYMENT")


if __name__ == "__main__":
    main()
