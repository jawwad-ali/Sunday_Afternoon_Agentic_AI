from agents import (
    Agent,
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered, 
    Runner,
    input_guardrail,
    trace
    )

from connection import config
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
load_dotenv()

######################################### Input Guardrails ########################################

class MedicineOutput(BaseModel):
    response: str
    isMedicineQuery: bool

guardrail_agent = Agent(
    name = 'Guardrail agent',
    instructions=""" You are a guardrail agent. Your task to keep an eye on user query. User query should only be related to medicine """,
    output_type= MedicineOutput
)

@input_guardrail
async def medicine_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, run_config=config)
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = not result.final_output
    )

medicine_agent = Agent(
    name = "Medicine Agent",
    instructions = """ You are a medicine agent your task is to is to answer queries related to medicine. """
)

triage_agent = Agent(
    name = "Tirage Agent",
    instructions = """ You are a triage agent your task is to delegate the task to appropriate agent. """,
    handoffs=[medicine_agent],
    input_guardrails=[medicine_guardrail]
)

async def main():
    with trace("Learning Guardrails"):
        try:
            result = await Runner.run(triage_agent, 'What is the most recommended medicine for blood pressure', run_config=config)
            print(result.final_output)

        except InputGuardrailTripwireTriggered:
            print('Agent output is not according to the expectations')
       
# if __name__ == "__main__":
#     asyncio.run(main())