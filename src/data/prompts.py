"""
This module contains predefined prompts for the OpenAI API.
"""
import os
import csv

# System prompts define the behavior and capabilities of the assistant
SYSTEM_PROMPT ="""
    You are a categorisation assistant that helps support operators
    classify or categories customer requests in a specific service catalog
    within a ServiceNow support system. Your task is to provide a specific
    servicenow category and subcategory based on the customer request.
    If you are unable to determine the category and subcategory from the
    customer request, please respond with "Unknown" and do not provide
    any other information.
    You are to list only the category and subcategory in the response in the
    following format:
    <category>-<subcategory>
    For example, if the topic is "Access", the category is "SAP" and the subcategory is "SAP new user",
    the response should be:
    SAP-SAP new User

    The topic should not be used in the response.
"""

# User prompts are example inputs that can be used for testing or demonstrations
USER_PROMPT = """
  I would like to know the servicenow category of a generalised IT support request
  that can be determined from a list of ServiceNow reference categories so that
  it can be routed to the correct category for efficient service.
  The reference categories are:
  {references}

  The customer request is:
  {customer_request}
"""

def load_support_queries():
    """
    Loads support queries from support_queries.csv file and returns them as a list of dictionaries
    containing 'id' and 'short_description' fields.
    """
    queries = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    queries_file_path = os.path.join(current_dir, 'support_queries.csv')

    try:
        with open(queries_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                queries.append({
                    'Number': row['Number'],
                    'Brief summary': row['Brief summary'],
                    'Further details': row['Further details'],
                })
    except Exception as e:
        print(f"Error loading support queries: {e}")

    return queries

def load_catalog_references():
    """
    Loads catalog references from catalog_reference.md file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    references_file_path = os.path.join(current_dir, 'catalog_reference.md')

    try:
        with open(references_file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading catalog references: {e}")
        return ""



