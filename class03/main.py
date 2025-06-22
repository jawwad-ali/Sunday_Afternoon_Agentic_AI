import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import asyncio
import datetime


# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

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
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

@function_tool
def get_date_time():
    return datetime.date.today()

agent = Agent(
    name="Haiku agent",
    # instructions="Always respond in haiku form",
    instructions="You are an helpfull assistant",
    model=model,
    tools=[get_weather, get_date_time],
)

async def main():
    result = await Runner.run(agent, "What is Date today?", 
                              run_config=config
                              )
    print(result.new_items[2])


if __name__ == "__main__":
    asyncio.run(main())