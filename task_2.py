from inspect_ai import Task, task
from inspect_ai.scorer import scorer, Score
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.model import ChatMessageSystem

def matching_words_metric(model_output, correct_answer):
    # YOUR CODE GOES HERE
    score = ...
    return score

def accuracy_metric(model_output, correct_answer):
    # YOUR CODE GOES HERE
    score = ...
    return score

@scorer
def my_custom_scorer():
    # YOUR CODE GOES HERE
    # TODO: Compare state / model output with target to yield a score

    # TODO: calculate metric values


    return Score(value=...)

    return score


@solver
def include_system_prompt(system_prompt: str) -> Solver:
    """Prepend a system prompt to the start of the messages.

    Parameters
    ----------
    system_prompt : str
        The system prompt to prepend to the start of the messages.
    """
    return


# We use a silly system prompt as a way of testing that the solver works.
system_prompt = "Answer questions using as many words beginning with the letter 'Z' as possible."

def foreign_policy_eval_task():
    # YOUR CODE GOES HERE
    return Task()