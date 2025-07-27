from agents import Agent, Runner, trace
from class06.connection import config
import asyncio
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from dotenv import load_dotenv

load_dotenv()

waiter_agent = Agent(
    name="Waiter Agent",
    instructions="""
    You are a waiter agent and provide a list of pizzas to the customer.
        ## Your pizza list:
        1. Margherita - $12
        2. Pepperoni - $15  
        3. Vegetarian - $14
    """
)

welcome_Agent = Agent(
    name="Welcome Agent",
    instructions=f"""
        You are a Welcome agent in a Pizza Restuarant you task is to greet user and handoffs to waiter agent
        1. Welcome user politely.
        2. Ask them to have a seat.
        3. Handoffs to the waiter agent to show the the menu
        """,
    handoffs=[waiter_agent],
    handoff_description="You need to handsoff to waiter agent after welcome message appears"
)

async def main():
    while True:
        msg = input("Enter your message")

        with trace("Class 05"):

            result = await Runner.run(welcome_Agent, msg, run_config=config)
            print(result.last_agent.name)
            print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
