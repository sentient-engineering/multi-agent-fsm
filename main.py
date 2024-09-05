from orchestrator.orchestrator import Orchestrator
from models.models import State, PlannerInput, PlannerOutput, HelperInput, HelperOutput
from agent.base import BaseAgent
from prompts.prompts import planner_system_prompt, helper_system_prompt

if __name__ == "__main__":
    # Define your agents using the base agent. 
    planner_agent = BaseAgent(
        name = "planner",
        system_prompt = planner_system_prompt,
        input_format = PlannerInput,
        output_format = PlannerOutput, 
        keep_message_history = False
    )

    helper_agent = BaseAgent(
        name = "helper",
        system_prompt = helper_system_prompt,
        input_format = HelperInput,
        output_format = HelperOutput,
        keep_message_history = False
        )
    
    # Define your state machine
    #TODO: Combine state_machine and state_agent_map and maybe also combine the upsta func in the same object. so state_machine is self contained
    state_machine = {
        State.PLAN: [State.HELP, State.COMPLETED], 
        State.HELP: [State.PLAN], 
        State.COMPLETED: [] 
    }

    # Define your state machine using states and respective agents to be called for the state
    state_to_agent_map = {
        State.PLAN: planner_agent,
        State.HELP: helper_agent 
    }

    # Call orchestrator with objective, initial state & state machine.
    orchestrator = Orchestrator(
        objective="Write a blog post on AI advancements in 2024",
        initial_state=State.PLAN, 
        state_machine=state_machine,
        state_to_agent_map = state_to_agent_map
        )
    
    final_response = orchestrator.run()

    print(f"Final Response: {final_response}")