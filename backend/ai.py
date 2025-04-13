from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import json

# Import database components
from database import SessionLocal
from models.tenant import Tenant
from models.landlord import Landlord
from models.property import Property
from models.issue import Issue
from models.contractor import Contractor
from contextlib import contextmanager

# Define system prompt
system_prompt = """
You are an assistant that helps tenants with rental property issues.
You are friendly, helpful, and knowledgeable about property management.
Provide assistance without revealing any internal database details unless specifically requested.
Focus on understanding and responding to tenant inquiries while maintaining confidentiality.
"""


# Improved database session handling
@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_tenants_from_db() -> List[Dict[str, Any]]:
    """Retrieve all tenants from the database."""
    with get_db_session() as db:
        tenants = Tenant.get_all(db)
        result = []
        for tenant in tenants:
            result.append(
                {
                    "id": tenant.id,
                    "name": tenant.name,
                    "email": tenant.email,
                    "phone_number": tenant.phone_number,
                    "property_id": tenant.property_id,
                    "landlord_id": tenant.landlord_id,
                }
            )
        return result


def get_landlords_from_db() -> List[Dict[str, Any]]:
    """Retrieve all landlords from the database."""
    with get_db_session() as db:
        landlords = Landlord.get_all(db)
        result = []
        for landlord in landlords:
            result.append(
                {
                    "id": landlord.id,
                    "name": landlord.name,
                    "email": landlord.email,
                    "phone_number": landlord.phone_number,
                }
            )
        return result


def get_properties_from_db() -> List[Dict[str, Any]]:
    """Retrieve all properties from the database."""
    with get_db_session() as db:
        properties = Property.get_all(db)
        result = []
        for prop in properties:
            result.append(
                {
                    "id": prop.id,
                    "address": prop.address,
                    "landlord_id": prop.landlord_id,
                }
            )
        return result


def get_issues_from_db(resolved: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Retrieve issues from the database, optionally filtered by resolved status."""
    with get_db_session() as db:
        all_issues = Issue.get_all(db)
        result = []
        for issue in all_issues:
            if resolved is None or issue.resolved == resolved:
                result.append(
                    {
                        "id": issue.id,
                        "description": issue.description,
                        "location": issue.location,
                        "action": issue.action,
                        "resolved": issue.resolved,
                        "property_id": issue.property_id,
                    }
                )
        return result


# Fixed data retrieval functions to properly close sessions
def get_contractors_from_db() -> List[Dict[str, Any]]:
    """Retrieve all contractors from the database."""
    with get_db_session() as db:
        contractors = Contractor.get_all(db)
        result = []
        for contractor in contractors:
            result.append(
                {
                    "id": contractor.id,
                    "name": contractor.name,
                    "email": contractor.email,
                    "phone_number": contractor.phone_number,
                    "work": contractor.work,
                    "landlord_id": contractor.landlord_id,
                }
            )
        return result


# Fixed data retrieval functions to properly close sessions
def create_issue_in_db(
    description: str, location: str, action: str, property_id: Optional[int] = None
) -> Dict[str, Any]:
    """Create a new issue in the database."""
    with get_db_session() as db:
        # Validate property_id if provided
        if property_id is not None:
            property_obj = Property.get(db, property_id)
            if property_obj is None:
                return {"error": f"Property with ID {property_id} not found"}

        issue_data = {
            "description": description,
            "location": location,
            "action": action,
            "resolved": False,
        }

        if property_id is not None:
            issue_data["property_id"] = property_id

        try:
            issue = Issue.create(db, issue_data)
            return {
                "id": issue.id,
                "description": issue.description,
                "location": issue.location,
                "action": issue.action,
                "resolved": issue.resolved,
                "property_id": issue.property_id,
                "status": "created",
            }
        except Exception as e:
            return {"error": str(e)}


# Define more tools for database interaction
tools = [
    # Keeping only the create_issue tool, removing all get_*_from_db tools
    Tool(
        func=create_issue_in_db,
        name="create_issue_in_db",
        description="Creates a new issue in the database. Requires description, location, and action. Property ID is optional.",
        args_schema={
            "description": "str",
            "location": "str",
            "action": "str",
            "property_id": "Optional[int]",
        },
    ),
]


# Function to load all data at startup
def load_all_data():
    """Load all data from the database at startup and return a formatted string representation."""
    tenants = get_tenants_from_db()
    landlords = get_landlords_from_db()
    properties = get_properties_from_db()
    issues = get_issues_from_db()
    contractors = get_contractors_from_db()

    tenant_info = "\n".join(
        [
            f"- Tenant {t['id']}: {t['name']}, Email: {t['email']}, Phone: {t['phone_number']}, Property ID: {t['property_id']}, Landlord ID: {t['landlord_id']}"
            for t in tenants
        ]
    )

    landlord_info = "\n".join(
        [
            f"- Landlord {l['id']}: {l['name']}, Email: {l['email']}, Phone: {l['phone_number']}"
            for l in landlords
        ]
    )

    property_info = "\n".join(
        [
            f"- Property {p['id']}: {p['address']}, Landlord ID: {p['landlord_id']}"
            for p in properties
        ]
    )

    issue_info = "\n".join(
        [
            f"- Issue {i['id']}: {i['description']} at {i['location']}, Action: {i['action']}, Resolved: {i['resolved']}, Property ID: {i['property_id']}"
            for i in issues
        ]
    )

    contractor_info = "\n".join(
        [
            f"- Contractor {c['id']}: {c['name']}, Work: {c['work']}, Email: {c['email']}, Phone: {c['phone_number']}, Landlord ID: {c['landlord_id']}"
            for c in contractors
        ]
    )

    return f"""
DATABASE CONTENTS:

TENANTS:
{tenant_info}

LANDLORDS:
{landlord_info}

PROPERTIES:
{property_info}

ISSUES:
{issue_info}

CONTRACTORS:
{contractor_info}
"""


# Initialize memory
history = InMemoryChatMessageHistory()

# Load all data at startup
database_contents = load_all_data()

# Add database contents to system prompt
enhanced_system_prompt = f"""
{system_prompt}

Here is the current database information that you can reference:

{database_contents}

When asked about tenants, landlords, properties, issues, or contractors, use this information to respond.
Only use the create_issue_in_db tool when a user wants to create a new maintenance issue.
"""

# Set up the LLM with a prompt that supports tools and memory
tool_llm = ChatOllama(
    model="llama3.1",
    temperature=0,
    base_url="http://localhost:11434",
).bind_tools(tools)

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
    base_url="http://localhost:11434",
)

# Define a prompt template with the enhanced system prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", enhanced_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# Create a chain that combines prompt, LLM, and tools
chain = prompt | llm

# When starting a new conversation, add a system message with the database contents
history.add_message(SystemMessage(content=enhanced_system_prompt))


# Enhanced function to handle message sending and tool use
def send_message(user_message):
    try:
        # Add user message to history
        history.add_message(HumanMessage(content=user_message))

        # Invoke tool llm with the same input
        tool_response = tool_llm.invoke(input=user_message)

        # Check if a tool was called - now only the create_issue_in_db tool remains
        if tool_response.tool_calls:
            tool_call = tool_response.tool_calls[0]
            tool_name = tool_call["name"]

            if tool_name == "create_issue_in_db":
                args = tool_call.get("args", {})
                description = args.get("description", "")
                location = args.get("location", "")
                action = args.get("action", "")
                property_id = args.get("property_id")

                tool_result = create_issue_in_db(
                    description=description,
                    location=location,
                    action=action,
                    property_id=property_id,
                )

                if "error" in tool_result:
                    response_content = (
                        f"I couldn't create the issue: {tool_result['error']}"
                    )
                else:
                    response_content = f"I've created a new maintenance issue:\n- Description: {tool_result['description']}\n- Location: {tool_result['location']}\n- Action needed: {tool_result['action']}\n- Issue ID: {tool_result['id']}"

                history.add_message(AIMessage(content=response_content))

                # Reload database data after creating an issue to keep context up to date
                global database_contents, enhanced_system_prompt
                database_contents = load_all_data()
                enhanced_system_prompt = f"{system_prompt}\n\nHere is the current database information that you can reference:\n\n{database_contents}"

        # Invoke the chain with chat history and input
        response = chain.invoke(
            {
                "input": user_message,
                "chat_history": history.messages,
            }
        )
        history.add_message(AIMessage(content=response.content))
        return response.content

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history.add_message(AIMessage(content=error_msg))
        return error_msg


# Example usage
if __name__ == "__main__":
    print("Welcome to the Property Management Assistant!")
    print("Type 'exit' or 'quit' to leave the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break
        print("--------------------------------------------------")
        response = send_message(user_input)
        print(f"Assistant: {response}")
        print("--------------------------------------------------")
