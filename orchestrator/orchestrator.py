from models.models import Memory, State, Task, PlannerInput, PlannerOutput, HelperInput, HelperOutput
from agent.base import Agent
from colorama import Fore, init
import textwrap

init(autoreset=True)

class Orchestrator:
    def __init__(self, objective:str, initial_state: State, state_machine: dict[State, list[State]],state_to_agent_map: dict[State, Agent]):
        self.state_to_agent_map = state_to_agent_map
        self.state_machine = state_machine
        self.current_state = initial_state
        self.memory = Memory(
        objective=objective,
        completed_tasks=[],
        current_task=None,
        final_response=None
    )

    def run(self) -> str:
        while self.current_state != State.COMPLETED:
            self._handle_state()

        self._print_final_response()
        return self.memory.final_response

    def _handle_state(self):
        current_state = self.current_state
        if current_state not in self.state_to_agent_map: 
            raise ValueError(f"Unhandled state! No agent for {current_state}")
    
        if current_state == State.PLAN:
            self._handle_plan_state()
        elif current_state == State.HELP:
            self._handle_help_state()
        else:
            raise ValueError(f"Unhandled state: {current_state}")
        
    def _handle_plan_state(self):
        agent = self.state_to_agent_map[State.PLAN]
        self._print_memory_and_agent(agent.name)
    
        input_data = PlannerInput(
            objective=self.memory.objective,
            task_for_review=self.memory.current_task,
            completed_tasks=self.memory.completed_tasks
            )
        
        output = agent.run(input_data)
        
        # Update memory
        self._update_memory_from_planner(output)
        
        print(f"{Fore.MAGENTA}Planner has updated the memory.")

    
    def _handle_help_state(self):
        agent = self.state_to_agent_map[State.HELP]
        self._print_memory_and_agent(agent.name)
    
        input_data = HelperInput(task=self.memory.current_task)
        
        output: HelperOutput = agent.run(input_data)

        self._print_task_result(output.completed_task)
        
        self._update_memory_from_helper(output)
        
        print(f"{Fore.MAGENTA}Helper has completed a task.")
        

    
    def _update_memory_from_planner(self, planner_output: PlannerOutput):
        if planner_output.is_complete:
            self.current_state = State.COMPLETED
            self.memory.final_response = planner_output.final_response
        elif planner_output.next_task:
            self.current_state = State.HELP
            next_task_id = len(self.memory.completed_tasks) + 1
            self.memory.current_task = Task(id=next_task_id, description = planner_output.next_task.description, result=None)
        else:
            raise ValueError("Planner did not provide next task or completion status")

    
    def _update_memory_from_helper(self, helper_output: HelperOutput):
        self.memory.completed_tasks.append(helper_output.completed_task)
        self.memory.current_task = None
        self.current_state = State.PLAN
        print("naman")
        print(self.memory.completed_tasks)

    def _print_memory_and_agent(self, agent_type: str):
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}Current State: {Fore.GREEN}{self.memory.current_state}")
        print(f"{Fore.YELLOW}Agent: {Fore.GREEN}{agent_type}")
        if self.memory.current_task:
            print(
                f"{Fore.YELLOW}Current Task: {Fore.GREEN}{self.memory.current_task.description}"
            )
        if len(self.memory.completed_tasks) == 0: 
            print(f"{Fore.YELLOW}Completed Tasks:{Fore.GREEN} none")
        else:
            print(f"{Fore.YELLOW}Completed Tasks:")
            for task in self.memory.completed_tasks:
                status = "✓" if task.result else " "
                print(f"{Fore.GREEN}  [{status}] {task.description}")
        print(f"{Fore.CYAN}{'='*50}")

    def _print_task_result(self, task: Task):
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}Completed Task: {Fore.GREEN}{task.description}")
        print(f"{Fore.YELLOW}Result:")
        wrapped_result = textwrap.wrap(task.result, width=80)
        for line in wrapped_result:
            print(f"{Fore.WHITE}{line}")
        print(f"{Fore.CYAN}{'='*50}")

    def _print_final_response(self):
        print(f"\n{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}Objective Completed!")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.YELLOW}Final Response:")
        wrapped_response = textwrap.wrap(self.memory.final_response, width=80)
        for line in wrapped_response:
            print(f"{Fore.WHITE}{line}")
        print(f"{Fore.GREEN}{'='*50}")
