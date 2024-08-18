from orchestrator.orchestrator import Orchestrator
from models.models import Memory, State, PlannerInput, PlannerOutput, HelperInput, HelperOutput
from agent.agent import Agent
from prompts.prompts import planner_system_prompt, helper_system_prompt

if __name__ == "__main__":
    initial_memory = Memory(
        objective="Create a report on climate change in 2022",
        current_state=State.PLAN,
        completed_tasks=[],
        current_task=None,
        final_response=None
    )

    state_to_agent_map = {
        State.PLAN: Agent(
            name = "planner",
            system_prompt = planner_system_prompt,
            input_format = PlannerInput,
            output_format = PlannerOutput, 
            keep_message_history = False
        ),
        State.HELP: Agent(
            name = "helper",
            system_prompt = helper_system_prompt,
            input_format = HelperInput,
            output_format = HelperOutput,
            keep_message_history = False
        )
    }

    orchestrator = Orchestrator(initial_memory, state_to_agent_map = state_to_agent_map)
    
    final_memory = orchestrator.run()

    print(f"Final Response: {final_memory}")