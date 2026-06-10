import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load the environment variables from the .env file (local development)
load_dotenv()

# 2. Get the Groq API key — check environment variable directly.
#    Works on Render (env vars set in dashboard), Streamlit Cloud (secrets),
#    and local development (.env file).
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Set it as an environment variable on Render "
        "(or create a .env file with GROQ_API_KEY=your_key for local development)."
    )

# Initialize the Groq LLM globally
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key=groq_api_key,
)


def resturant_name_and_menu(cuisine):
    # 2. Define the individual prompts
    prompt_name = PromptTemplate.from_template(
        "I want to open a restaurant for {cuisine} food. Suggest only one fancy name for this."
    )

    prompt_menu = PromptTemplate.from_template(
        "Suggest a 10-item menu for a restaurant named: {restaurant_name}. "
        "For each menu item, provide a menu name and a short description. "
        "Format each menu item as:\n"
        "1. **Menu Name** - Description of the menu\n"
        "2. **Menu Name** - Description of the menu\n"
        "3. **Menu Name** - Description of the menu\n"
        "4. **Menu Name** - Description of the menu\n"
        "5. **Menu Name** - Description of the menu\n"
        "6. **Menu Name** - Description of the menu\n"
        "7. **Menu Name** - Description of the menu\n"
        "8. **Menu Name** - Description of the menu\n"
        "9. **Menu Name** - Description of the menu\n"
        "10. **Menu Name** - Description of the menu"
    )

    # 3. Create independent executable sub-chains
    name_chain = prompt_name | llm | StrOutputParser()
    menu_chain = prompt_menu | llm

    # 4. Step 1: Generate and capture the clean restaurant name string
    generated_name = name_chain.invoke({"cuisine": cuisine})

    # 5. Step 2: Feed that generated name right into the menu prompt execution
    menu_response = menu_chain.invoke({"restaurant_name": generated_name})

    # 6. Return both items perfectly structured for your Streamlit UI
    return {
        "restaurant_name": generated_name.strip(),
        "menu": menu_response.content,
    }
