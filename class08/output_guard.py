from agents import (
    Agent,
    OutputGuardrailTripwireTriggered,
    TResponseInputItem, 
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered, 
    Runner,
    input_guardrail,
    RunContextWrapper,
    output_guardrail, 
    trace
    )

from connection import config
from pydantic import BaseModel
import rich
import asyncio

from dotenv import load_dotenv

load_dotenv()

######################## Output Guardrail ######################## 
# Output validation model for financial advice
class FinancialAdviceOutput(BaseModel):
    response: str
    isAppropriateAdvice: bool
    containsDisclaimer: bool
    reason: str

# Guardrail agent to validate financial advice output
financial_guardrail_agent = Agent(
    name='Financial Output Guardrail Agent',
    instructions=""" 
    You are an output guardrail agent for financial advice. Your task is to validate that:
    1. The response contains appropriate disclaimers about not being professional financial advice
    2. The advice is general and educational, not specific investment recommendations
    3. The response encourages consulting with licensed financial advisors
    4. No guarantees about returns or specific outcomes are made
    
    Set isAppropriateAdvice to True only if all safety criteria are met.
    Always include containsDisclaimer as True if proper disclaimers are present.
    """,
    output_type=FinancialAdviceOutput
)

@output_guardrail
async def financial_output_guardrail(ctx, agent, output) -> GuardrailFunctionOutput:
    """Output guardrail to validate financial advice responses"""
    result = await Runner.run(
        financial_guardrail_agent, 
        f"Validate this financial advice response: {output}", 
        run_config=config
    )
    
    return GuardrailFunctionOutput(
        output_info=result.final_output.reason,
        tripwire_triggered= not (
            result.final_output.isAppropriateAdvice and 
            result.final_output.containsDisclaimer
        )
    )


# Main financial advisor agent
financial_advisor_agent = Agent(
    name="Financial Advisor Agent",
    instructions=""" 
    You are a financial education agent. 
    Provide general financial information and education.
    Always include disclaimers that this is not professional financial advice.
    Encourage users to consult with licensed financial advisors for personalized advice.
    Never guarantee specific returns or outcomes.
    """,
    output_guardrails=[financial_output_guardrail]
)


# Triage agent that delegates to financial advisor
triage_agent = Agent(
    name="Financial Triage Agent",
    instructions=""" 
    You are a triage agent for financial queries. Delegate financial questions to the financial advisor agent.
    """,
    # handoffs=[financial_advisor_agent]
    handoffs=[financial_advisor_agent],
)


async def main():
    prompt1 = """ Tell me exactly which stocks to buy to guarantee 50% returns in 6 months """ # True
    prompt2 = """ Should I put all my retirement savings into Bitcoin? Give me definitive advice. """ # True
    promtp3 = """ What should I invest in to get rich quick? """ #False

    try:
        result = await Runner.run(
            triage_agent, 
            prompt1,
            run_config=config
        )
        print("Response passed guardrails:")
        print(result.final_output)
        print(result.last_agent)
        
    except OutputGuardrailTripwireTriggered as e:
        print('Output guardrail triggered - response did not meet safety standards')
        
# if __name__ == "__main__":
#     asyncio.run(main())