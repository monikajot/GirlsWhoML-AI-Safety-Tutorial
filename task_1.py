from inspect_ai import eval
from inspect_ai import Task, task
from inspect_ai.dataset import example_dataset
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import (
  prompt_template, generate, self_critique
)
import os

OPENAI_API_KEY="OPENAI_API_KEY" # you'll be given this by Tom or Monika
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
api_key = os.environ.get('OPENAI_API_KEY')
assert api_key is not None, "Please set your OPENAI_API_KEY"

DEFAULT_PROMPT="{prompt}"

@task
def theory_of_mind():
    return Task(
        dataset=example_dataset("theory_of_mind")[:1],
        solver=..., # Write your code here and define the solver using DEFAULT_PROMPT and self_critique()
        scorer=model_graded_fact()
    )

# Note: hint is in the imports :)

logs = eval(theory_of_mind(),model="openai/gpt-4o-mini", model_args={"api_key": OPENAI_API_KEY})
# when you run this, an .eval file should be created which you can open/view using either Inspect Extension on VSCode
# or simply running `inspect view` command
