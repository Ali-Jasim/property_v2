from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class OllamaChatBot:
    def __init__(
        self, model_name="llama3.1", base_url="http://localhost:11434", temperature=0.7
    ):
        """
        Initialize the Ollama chat bot.

        Args:
            model_name (str): The name of the Ollama model to use
            base_url (str): The URL of the Ollama API
            temperature (float): Controls randomness in responses (0.0 to 1.0)
        """
        try:
            self.chat_model = ChatOllama(
                model=model_name,
                base_url=base_url,
                temperature=temperature,
            )
            logger.info(f"Initialized ChatOllama with model {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize ChatOllama: {e}")
            raise

    def chat(self, message, system_prompt=None, chat_history=None):
        """
        Send a message to the chatbot and get a response.

        Args:
            message (str): The user message
            system_prompt (str, optional): System instructions for the model
            chat_history (list, optional): Previous conversation history

        Returns:
            str: The AI's response
        """
        messages = []

        # Add system message if provided
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history)

        # Add the current user message
        messages.append(HumanMessage(content=message))

        try:
            # Get response from the model
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    def stream_chat(self, message, system_prompt=None, chat_history=None):
        """
        Stream a chat response from the model.

        Args:
            message (str): The user message
            system_prompt (str, optional): System instructions for the model
            chat_history (list, optional): Previous conversation history

        Returns:
            generator: A generator yielding tokens as they're generated
        """
        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        if chat_history:
            messages.extend(chat_history)

        messages.append(HumanMessage(content=message))

        try:
            for chunk in self.chat_model.stream(messages):
                yield chunk.content
        except Exception as e:
            logger.error(f"Error in stream_chat: {e}")
            yield f"Sorry, I encountered an error: {str(e)}"


# Example usage
if __name__ == "__main__":
    # Initialize the chat bot
    chat_bot = OllamaChatBot(model_name="llama3.1")

    # Simple single-turn conversation
    response = chat_bot.chat(
        message="Hello! Can you explain what Ollama is?",
        system_prompt="You are a helpful assistant that provides brief and accurate information.",
    )
    print("Bot response:", response)

    # Example of a multi-turn conversation
    history = []

    # First turn
    user_message = "What are the benefits of using Ollama?"
    response = chat_bot.chat(message=user_message)
    print(f"User: {user_message}")
    print(f"Bot: {response}")

    # Update history
    history.extend([HumanMessage(content=user_message), AIMessage(content=response)])

    # Second turn with history
    user_message = "How does it compare to other local LLM solutions?"
    response = chat_bot.chat(message=user_message, chat_history=history)
    print(f"User: {user_message}")
    print(f"Bot: {response}")
