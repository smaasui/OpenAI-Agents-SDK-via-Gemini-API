import asyncio
from pydantic import BaseModel
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from connection import config # Import our Gemini config

# Schema for Guardrail Output
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# 1. Guardrail Agent
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework. Set is_homework to True if it is.",
    output_type=HomeworkOutput,
)

# 2. Specialist Agents
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="Explain math problems step-by-step with examples.",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="Provide historical context and explain important events.",
)

# 3. Guardrail Logic
async def homework_guardrail(ctx, agent, input_data):
    # Running guardrail check using Gemini config
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context, run_config=config)
    final_output = result.final_output_as(HomeworkOutput)
    
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

# 4. Triage Agent (The Boss)
triage_agent = Agent(
    name="Triage Agent",
    instructions="Direct the user to the Math or History tutor based on their homework question.",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    # Test 1: History (Should work)
    print("\n--- Testing History Query ---")
    try:
        result = await Runner.run(triage_agent, "Who was the first president of the US?", run_config=config)
        print("Response:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail: This doesn't look like homework!")

    # Test 2: Random (Should be blocked)
    print("\n--- Testing Random Query ---")
    try:
        result = await Runner.run(triage_agent, "What is the best pizza topping?", run_config=config)
        print("Response:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail blocked this input: User is not asking about homework.")

if __name__ == "__main__":
    asyncio.run(main())  