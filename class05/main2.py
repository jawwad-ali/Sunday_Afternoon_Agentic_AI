from agents import Agent, Runner
from connection import config
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

welcome_agent = Agent(
    name = 'Welcome Agent',
    instructions =f"""You are a helpful assistant"""
)

# Streaming run_streamed
async def main():
    result = Runner.run_streamed(welcome_agent, "hello", run_config=config)
    print(result.final_output)
    
    async for event in result.stream_events():
        if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


# Just for clear understanding I have made a separate function
async def main():
    result = await Runner.run(welcome_agent, "hello", run_config=config)
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())