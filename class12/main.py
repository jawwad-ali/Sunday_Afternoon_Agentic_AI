from agents import Agent, ModelSettings, Runner, function_tool
from connection import config
import asyncio
import rich
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

print(RECOMMENDED_PROMPT_PREFIX)

@function_tool(
        name_override="add_numbers",
        description_override="Add two numbers together and return the result.",
        # is_enabled=True
        # is_enabled=False
        )
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@function_tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

math_agent = Agent(
    name="Math Agent",
    instructions=""" You are a math agent. Your task is to assist users with math-related inquiries and calculations.""",
    tools=[add, subtract],
    model_settings=ModelSettings(
        # tool_choice="required"
        # tool_choice="none"
    )
)

# transfer_to_billing_agent
billing_agent = Agent(
    name="Billing Agent",
    instructions=f""" You are a billing agent. Your task is to assist users with billing-related inquiries and issues.""",
    handoff_description="""
    This is a billing agent. It handles user queries 
    related to billing."""
)

# trasnfer_to_medicine_agent
# medicine_agent = Agent()


# transfer_to_plant_agent
# plant_agent = Agent()

triage_agent = Agent(
    name="Triage Agent",
    instructions=f""" {RECOMMENDED_PROMPT_PREFIX} You 
    are a  triage agent. Your task is to delegate tasks
      to the appropriate specialized 
    agents based on the user's request.""",
    handoffs=[billing_agent]
)

async def main():
    # result = await Runner.run(
    #     math_agent,
    #     input="What is 5 plus 3?",
    #     run_config=config,
    #     # max_turns=2 // OK.
    #     # max_turns=1 // Error
    #     )

    result = await Runner.run(
        triage_agent,
        input="I have a question about my last invoice.",
        run_config=config,
    )
    
    rich.print(result.new_items)
    rich.print(result.final_output)
    rich.print(result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())

# transfer_to_agent_name