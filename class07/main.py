import rich
import asyncio
from connection import config
from pydantic import BaseModel

from agents import (Agent, OutputGuardrailTripwireTriggered, Runner, 
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered, output_guardrail
)

class PassengerOutput(BaseModel):
    response: str
    isWeightExceed: bool
     
airport_security_guard = Agent(
    name = "Airport Security Guard",
    instructions= """ 
        Your task is to check the passenger luggage.
        If passenger's luggage is more then 25KGs, gracefully stop them
    """,
    output_type = PassengerOutput
)

@input_guardrail
async def security_guardrail(ctx, agent, input):
    result = await Runner.run(airport_security_guard, 
                              input, 
                              run_config=config
                              )
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info= result.final_output.response,
        tripwire_triggered= result.final_output.isWeightExceed
    )

# Main agent
passenger_agent = Agent(
    name = 'Passenger',
    instructions="You are a passenger agent",
    input_guardrails=[security_guardrail]
)

async def main():
        try:
            result = await Runner.run(passenger_agent , 'My luggage weight is 20kgs', run_config=config)
            print("Passenger is onboarded")

        except InputGuardrailTripwireTriggered:
             print('Passenger cannot check-in')


######################## Output Guardrails ########################

class MessageOutput(BaseModel): # Model for Agent Output Type
    response: str

class PHDOutput(BaseModel): # Model to trigger the guardrail
    isPHDLevelResponse: bool

phd_guardrail_agent = Agent(
    name = "PHD Guardrail Agent",
    instructions="""
        You are a PHD Guardrail Agent that evaluates if text is too complex for 8th grade students. If the response if 
        very hard to read for an eight grade student deny the agent response
    """,
    output_type=PHDOutput
)

@output_guardrail
async def PHD_guardrail(ctx, agent: Agent, output) -> GuardrailFunctionOutput:

    result = await Runner.run(phd_guardrail_agent, output.response,  run_config=config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.isPHDLevelResponse
    )

# Main executor agent
eigth_grade_std = Agent(
    name = "Eight grade student",
    instructions="""
        1. You are an agent that answer query to a eight standard student. Keep your vocabulary simple and easy. 
        2. If asked to give answers in most difficult level use the most hardest english terms
    """,
    output_type=MessageOutput,
    output_guardrails=[PHD_guardrail]
)

async def og_main():
    query = "What are trees? Explain using the most complex scientific terminology possible"
    # query = "What are trees? Explain in simple words"
    try:
        result = await Runner.run(eigth_grade_std, query, run_config=config)
        print(result.final_output)

    except OutputGuardrailTripwireTriggered:
        print('Agent output is not according to the expectations')
        

if __name__ == "__main__":
    asyncio.run(og_main())
    asyncio.run(main())