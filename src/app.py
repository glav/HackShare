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

    print(f"\nLoaded {len(support_queries)} support queries\nProcessing...")

    try:
        for i, query in enumerate(support_queries, 1):
            # Remove "generalised IT request" from short description (ignoring case)
            customer_query = f"{query['Brief summary']} - {query['Further details']}"
            query_number = query['Number']
            expected_category = query['category']

            print(f"\nQuery {i} (ID: {query_number}): '{customer_query}'")

            # Format the USER_PROMPT with the current query and references
            formatted_prompt = USER_PROMPT.format(
                references=catalog_references,
                customer_request=customer_query
            )

            # Call Azure OpenAI to get a chat completion
            response = get_chat_completion(formatted_prompt, SYSTEM_PROMPT)
            print(f"Generated Category: {response}")
            print(f"Expected Category: {expected_category}")
            if response != expected_category:
                print(f"FAIL!")
            else:
                print(f"Pass")
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
