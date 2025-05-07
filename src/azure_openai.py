import os
from openai import AzureOpenAI

def get_chat_completion(user_prompt, system_prompt="I am an assistant"):
    """
    Get a chat completion from Azure OpenAI.

    Args:
        user_prompt (str): The user prompt to send to the model
        system_prompt (str): The system prompt to set the context

    Returns:
        str: The response from the model
    """
    # Get required environment variables
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")  # Get API version from env with default
    # Get APIM subscription key if available
    apim_subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY")

    # Check if required environment variables exist
    if not api_key or not endpoint or not deployment:
        missing = []
        if not api_key:
            missing.append("AZURE_OPENAI_API_KEY")
        if not endpoint:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not deployment:
            missing.append("AZURE_OPENAI_DEPLOYMENT")
        print(f"Warning: Missing required environment variables: {', '.join(missing)}")
        #raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,  # Use the API version from environment variable
            azure_endpoint=endpoint
        )

        # Prepare default headers for the request
        extra_headers = {}

        # Add APIM subscription key to headers if available
        if apim_subscription_key and apim_subscription_key.strip():
            extra_headers["api-key"] = apim_subscription_key
            #print("Using APIM subscription key")

        # Create chat completion request
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            extra_headers=extra_headers if extra_headers else None
        )

        # Return the response content
        return response.choices[0].message.content
    except Exception as e:
        return f"Error accessing Azure OpenAI: {str(e)}"
