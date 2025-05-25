# run command:- pip install openai-agents
# run command:- pip install python-dotenv

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

from dotenv import dotenv_values

config = dotenv_values(".env")

# Client Connectivity (Gemini)
external_client = AsyncOpenAI(
    api_key= config['GEMINI_API_KEY'],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Choosing the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configrations
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


# maths_agent = Agent(
#     name = 'Maths Agent',
#     instructions = 'You are a Maths Agent. Help the user in his maths queries',
#     model = model
# )

# response = Runner.run_sync(maths_agent, input = 'What is 2 + 20 - (10 * 2) / 8?', run_config = config)

# print(response)

writer_agent = Agent(
    name = 'Writer Agent',
    instructions = 'You are a write. Help the user to write essay/ poem etc.',
    model = model
)

response = Runner.run_sync(writer_agent, input = 'Write 2 sentences on Python Programming language.', run_config = config)

print(response.final_output)