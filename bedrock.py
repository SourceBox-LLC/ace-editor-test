from langchain_aws import ChatBedrock
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve AWS credentials from Streamlit secrets
aws_access_key_id = st.secrets["aws"]["access_key_id"]
aws_secret_access_key = st.secrets["aws"]["secret_access_key"]
aws_region_name = st.secrets["aws"]["region_name"]

# Initialize the ChatBedrock LLM with credentials
llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs=dict(temperature=0),
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name,
    # Add other necessary parameters if needed
)

def generate_template(prompt):
    messages = [
        ("system", "You are a code template generator. Your output should be only valid code. Do not include any other text or comments."),
        ("human", prompt),
    ]
    try:
        # Invoke the ChatBedrock LLM
        ai_msg = llm.invoke(messages)
        # Log raw AI response for debugging
        logger.info(f"Raw AI response: {ai_msg}")

        # Extract the text content from the returned object.
        # Adjust the method to match the actual structure of ai_msg.
        content = ai_msg.content
        logger.info("Template generated successfully.")
        return content

    except Exception as e:
        logger.error(f"Error generating template: {e}")
        return None




def auto_edit_template(prompt, code):
    messages = [
        ("system", """
         You are a code template editor.
         Your goal is to edit the CODE provided based on the user PROMPT Your output should be only valid code. 
         Do not include any other text or comments."""),
        ("human", f"PROMPT: {prompt}\nCODE: {code}"),
    ]
    try:
        # Invoke the ChatBedrock LLM
        ai_msg = llm.invoke(messages)
        # Log raw AI response for debugging
        logger.info(f"Raw AI response: {ai_msg}")

        # Extract the text content from the returned object.
        # Adjust the method to match the actual structure of ai_msg.
        content = ai_msg.content
        logger.info("Template edited successfully.")
        return content

    except Exception as e:
        logger.error(f"Error generating templates: {e}")
        return None
    




