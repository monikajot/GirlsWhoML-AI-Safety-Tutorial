# GirlsWhoML-AI-Safety-Tutorial


For those who want to use Colab
[The Colab notebook](https://colab.research.google.com/drive/1Cpf_3NYOC99AFFM1SuWWAJddYakVMEUT?usp=sharing)


Those who'll use local IDE, start by setting up the following

```
pip install inspect-ai

pip install openai
export OPENAI_API_KEY=your-openai-api-key
inspect eval arc.py --model openai/gpt-4o
```


# Introduction

Inspect is built around three main components:

### **Datasets**
- Definition: a set of labelled samples. 
- Datasets are typically just a table with input and target columns, where input is a prompt and target is either literal value(s) or grading guidance.
- Line 13 (see task_1.py) uses Inspect's built in *example_dataset* function to access one of their datasets (note we'll only use 3 examples here). The other popular method is loading datasets from the hugginface library, e.g.

```
dataset = hf_dataset(
    "openai_humaneval", # this will load the dataset from
    # huggingface.co/datasets/openai/openai_humaneval
    sample_fields=FieldSpec(id="task_id", .. # specify other field names))
```

### **Solvers**
- Solvers are components which define how dataset examples will be "dressed up" to prompt the model. 
- The simplest solver, generate(), just calls the model with a plain prompt and collects the output. Other solvers might do prompt engineering, multi-turn dialog, critique, or provide an agent scaffold.

In lines 14-18 (see task_1.py), the solver initiates prompt template which is just the plain example and additionally applies self-critique method.

Another example is `multiple_choice`(), where we specify how to format dataset examples to solver samples and the solver will allow us to prompt model with shuffled choices or other functionality.


```
@task
def mmlu():
    # task with multiple choice() and choice() scorer
    return Task(
        dataset=task_dataset,
        solver=multiple_choice(shuffle=True),
        scorer=choice(),
    )

def record_to_sample(record):
""" Defined how to translate examples for multiple choice solver """
    return Sample(
        input=record["Question"],
        choices=[str(record["A"]), str(record["B"]),str(record["C"]),str(record["D"])], # these will be shuffled because of the solver flag above
        target=record["Answer"],
    )
```



### **Scorers**
- Score the final output of solvers against the target output. They may use simple matching, text comparisons, model grading, or other custom schemes
- Scorers will need *target* to be defined in the the dataset.

Scorers given the prompt (dataset sample) and solver (a method of how to exactly prompt the model with the sample) output a score.

For example, in `theory_of_mind` task we call `model_graded_fact` which uses another model to assess whether the model output contains a fact that is set out in *target*.

### Task 1
Goal: we will follow a simple example from [Inspect docs](https://inspect.ai-safety-institute.org.uk/) and explain how everything comes together. Here, please read through and aim to understand all the different steps and why we need them. If you get stuck, refer to the docs or ask for help.

1. Go to task_1.py, fill in the missing code and run the evaluation.
2. Then run `Inspect view` on your terminal and explore the logs.

### Task 2

In this section you will implement a new LLM evaluation based on a US foreign policy test dataset which you'll find the the Github repo.

1. Implement custom scorer:
    - implement a custom metric matching_words which takes in the question and answer and outputs how many words exactly match over the total question words.
    - implement accuracy score for the multiple choice questions.

Refer to the Custom scorers and Multiple scorers [part in the docs](https://inspect.ai-safety-institute.org.uk/scorers.html#sec-multiple-scorers)

2. Add a custom solver

For this simple eval, using the `generate` solver would be sufficient.
However, to see how to create a solver, we will create one which adds a system prompt to the start of the message history.

3. Now define the task Task() and run you evaluation

Note: you'll need to read the dataset from the `us_foreign_policy_test.csv` file

<details>
<summary>Hints</summary>


<details>
<summary>Use multiple scorer</summary>

```
@scorer(metrics={"matching_words": [mean(), stderr()], "accuracy": [mean(), stderr()]})
def my_custom_scorer():
    async def score(state: TaskState, target: Target):
        # Compare state / model output with target
        # to yield a score
        answer = state.output.completion
        question = state.input

        # TODO: calculate metric values

        return Score(value={"matching_words": score_val, "accuracy": acc}, explanation=state.output.completion)

    return score
```
</details>

</details>

Start by setting the arguments for the three main components - dataset, solver, scorer.

1. How do you read a custom dataset? Can you find examples in the docs?
3. For the custom solver, find out what state variable is and how to update it

Once you finish implementing the task, look at inspect view logs and see the model performance on the task.

4. Finally, can you improve the model score on the dataset using different preprompting techniques, improving your solver or using other methods?

### Task 3 - Design your own evaluation! 🧠

What makes LLM evaluation good?
- Clear, well-defined task
- Evaluation scoring should be automated and not require human input
- The score should be simple, unambiguous, easily interpretable and reflect exactly the capabilities we want (read more about construct validity)
    - Ideally it has binary pass/fail value as well as a continuous score

UK AISI already has a suite of evalutions implemented called [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals). Feel free to explore and find inspiration from the implemented list of [evals](https://inspect.ai-safety-institute.org.uk/evals/).

Your steps:
1. What capability would you like to evaluate?
2. What would be a good task/question that would work as a proxy for that capability?
3. How would your dataset look like? What is your target value?
4. How could you assign automatic score?

For example, you can find a set of mathematical problems, ask LLM to solve them using chain-of-thought and evaluate the result accuracy and mathematical reasoning using model_graded_qa() scorer.

Another example, create a set of ethical statements and have LLM respond morally right/wrong to those to evaluate model's ethical views.

Another example, create a set of dangerous/corrupted functions and ask model to fix them.

### Optional extension:

Want to dive even deeper?

Go through the [Agent Basics docs ](https://inspect.ai-safety-institute.org.uk/agents.html)and run the following agentic evaluation and observe the logs to understand how it works.

Questions:
1. Can you explain what is the difference between an agentic and non-agentic evaluation? What makes an evaluation *agentic*?
2. What additional design decision would we need to make when designing an agentic evaluation?
3. What tools/affordances are supported in Inspect? refer [here](https://inspect.ai-safety-institute.org.uk/tools.html)

