from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

# Global
class State(str, Enum):
    PLAN = "plan"
    HELP = "help"
    COMPLETED = "completed"

class Task(BaseModel):
    id: int
    description: str
    result: Optional[str] 

class Memory(BaseModel):
    objective: str
    current_state: State
    final_response: Optional[str]
    completed_tasks: Optional[List[Task]]
    current_task: Optional[Task]

    class Config:
        use_enum_values = True

# Planner 
class PlannerInput(BaseModel):
    objective: str
    task_for_review: Optional[Task] 
    completed_tasks: List[Task] 

class PlannerOutput(BaseModel):
    next_task: Optional[Task] 
    is_complete: bool
    final_response: Optional[str] 

# Helper
class HelperInput(BaseModel):
    task: Task

class HelperOutput(BaseModel):
    completed_task: Task