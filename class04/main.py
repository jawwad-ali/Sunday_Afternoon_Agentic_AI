from agents import Agent, Runner, function_tool
from connection import config
from datetime import datetime
# uv add rich
import rich

@function_tool
def get_weather(city:str)->str:
    return f'the weather of {city} is rainy'

@function_tool
def get_date():
    _now= datetime.now()
    return _now.strftime("the date is %d-%m-%Y")

@function_tool()
def multiply(num1: int, num2: int) -> int:
    return num1 * num2

agent=Agent(
    name="assistant",
    instructions="you are a helpful assistant",
    tools=[get_date,get_weather, multiply]
)
# result=Runner.run_sync(agent,
#                        """tell me the current time and date,
#                        and tell me weather of karaachi ,
#                        and what is my current location"""
#                        , run_config=config)
result = Runner.run_sync(
    agent,
    "multiply number 5 into 10",
    run_config=config
)
rich.print(result.new_items)
print(result.final_output)
