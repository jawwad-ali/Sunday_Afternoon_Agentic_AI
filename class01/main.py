# pip install openai-agents
# pip install python-dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
print(gemini_api_key)
# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def get_weather(city: str):
    return f'The current in {city} weather is 42 degrees'

# Write Agent
# writer = Agent(
#     name = 'Writer Agent',
#     instructions= 
#     """You are a writer agent. Generate poem,
#     stories, essay, email etc."""
# )

async def main():
    agent = Agent(
        name = 'Weather Agent',
        instructions = 'Your task is to answer user query. If you do not have the answer to the user query just deny the query do not hallucinate',
        tools = [get_weather]
    )

    response = await  Runner.run(
        agent,
        input = 'Do you have access to json placeholder api available on the internet?',
        run_config = config
        )
    print(response)

if __name__ == '__main__':
    asyncio.run(main())