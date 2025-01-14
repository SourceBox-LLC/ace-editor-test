from langchain_aws import ChatBedrock
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the ChatBedrock LLM
llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs=dict(temperature=0),
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










