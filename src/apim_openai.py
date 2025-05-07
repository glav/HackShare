import os
import requests
import json

def get_chat_completion(user_prompt, system_prompt="I am an assistant"):
    """
    Get a chat completion from Azure OpenAI via an API Management endpoint.

    Args:
        user_prompt (str): The user prompt to send to the model
        system_prompt (str): The system prompt to set the context

    Returns:
        str: The response from the model
    """
    # The fixed APIM endpoint
    apim_endpoint = "http://apim-pacedev-openaiptu-mlops.riotinto.org/icc-azopenai-hackathon-2025-t4"

    # Get required environment variables
    subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # We still need the deployment name

    # Check if required environment variables exist
    if not subscription_key or not deployment:
        missing = []
        if not subscription_key:
            missing.append("APIM_SUBSCRIPTION_KEY")
        if not deployment:
            missing.append("AZURE_OPENAI_DEPLOYMENT")
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    try:
        # Construct the API endpoint URL
        api_url = f"{apim_endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-02-01"

        # Prepare the request headers
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": subscription_key
        }

        # Prepare the request payload
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }

        # Send the request to the APIM endpoint
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Parse the response
        response_data = response.json()

        # Extract and return the generated content
        return response_data["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as http_err:
        error_detail = ""
        try:
            error_detail = response.json()
        except:
            error_detail = response.text
        return f"HTTP error occurred: {http_err}. Details: {error_detail}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error occurred: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    except Exception as e:
        return f"Error accessing Azure OpenAI via APIM: {str(e)}"
