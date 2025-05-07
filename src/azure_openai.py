import os
import logging
from openai import AzureOpenAI
import httpx

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_chat_completion(user_prompt, system_prompt="I am an assistant", verify_ssl=True):
    """
    Get a chat completion from Azure OpenAI.

    Args:
        user_prompt (str): The user prompt to send to the model
        system_prompt (str): The system prompt to set the context
        verify_ssl (bool): Whether to verify SSL certificates. Set to False to disable SSL verification.

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

    logger.debug(f"Using Azure OpenAI endpoint: {endpoint}")
    logger.debug(f"Using deployment: {deployment}")
    logger.debug(f"Using API version: {api_version}")

    # Check if required environment variables exist
    if not api_key or not endpoint or not deployment:
        missing = []
        if not api_key:
            missing.append("AZURE_OPENAI_API_KEY")
        if not endpoint:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not deployment:
            missing.append("AZURE_OPENAI_DEPLOYMENT")
        error_msg = f"Warning: Missing required environment variables: {', '.join(missing)}"
        logger.error(error_msg)
        print(error_msg)
        #raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    try:
        # Configure HTTP client with SSL verification option
        http_client = httpx.Client(verify=verify_ssl)
        logger.debug(f"HTTP client configured with SSL verification: {verify_ssl}")

        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,  # Use the API version from environment variable
            azure_endpoint=endpoint,
            http_client=http_client
        )
        logger.debug("Azure OpenAI client initialized successfully")

        # Prepare default headers for the request
        extra_headers = {}

        # Add APIM subscription key to headers if available
        extra_headers["api-key"] = api_key
        logger.debug("Request headers prepared")

        logger.debug(f"Sending request to Azure OpenAI with system prompt: {system_prompt[:20]}...")

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
        logger.debug("Response received from Azure OpenAI")

        # Return the response content
        return response.choices[0].message.content
    except Exception as e:
        error_message = f"Error accessing Azure OpenAI: {str(e)}"
        logger.error(error_message, exc_info=True)
        return error_message
