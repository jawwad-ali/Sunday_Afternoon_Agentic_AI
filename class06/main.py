from agents import Agent, Runner, trace, function_tool
from connection import config
import asyncio
from dotenv import load_dotenv

load_dotenv()
@function_tool
def current_weather():
    return "Sunny"

@function_tool
def current_location():
    return "GH Sindh Karachi"


plant_agent = Agent(
    name = 'Plant Agent',
    instructions="You are a plant agent. You task is to answer user query related to plants"
)

medicine_agent = Agent(
    name = "Medicine Agent",
    instructions="You are a medicine agent. Your task is to answer user query related to medicine",
    model="gpt3"
)

parent_agent = Agent(
    name = "Parent Agent",
    instructions=""" 
        You are a parent agent. Your task is to
        delegate user query to approriate agent. and call the tool by yourself
        Delegate plant and flower related queries to plant agent.
        Delegate medicine related queries to medicine agent.
        Any query other than plant and medicine keep it to 
        yourself and deny the user query,

        You also have tools available like current location
        and current weather
    """,
    handoffs=[medicine_agent, plant_agent],
    tools=[current_location]
)

async def main():
    with trace("Class 06"):
        result = await Runner.run(
            parent_agent, 
            """
                What are red-blood cells. and 
                what is my current location?
            """, 
            run_config=config)
        print(result.final_output)
        print("Last Agent ==> ",result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())

# What is photosynthesis