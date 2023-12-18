# Quant_AgentTools
🚀 Revolutionize your workflow with AgentTools! 🤖💼

AgentTools introduces the power of quantized models, enabling seamless local CPU execution for lightning-fast processing. 🌐⚡

💡 Key Advantages:

- Utilize quantized models for efficient local execution.
- Experience accelerated performance on CPU setups.
- Craft a responsive and dynamic workflow with ease.
- Combine the flexibility of custom functions with the speed of quantized models.
- Unlock unparalleled efficiency in your AI-driven tasks! 🚀🔍


## Motivation
My motivation to create this library was to have access to Agentic Workflow which has been well developed for OpenAI Models, but not for Open Source Quantized models that work on cpu and can leverage multi-threading. A big thanks to [GPT4All](https://github.com/nomic-ai/gpt4all) for making this possible.  

## Install the Library

```bash
pip install Quant-AgentTools 
```

# Using the AgentTools Class

To use the `AgentTools` class from the `Quant_AgentTools` library, follow the steps below:

## Importing the Class

First, import the `AgentTools` class from the `Quant_AgentTools.agent_tools` module:

```python
from Quant_AgentTools.agent_tools import AgentTools
```
# Creating an Instance

Next, create an instance of the AgentTools class. You can optionally pass a model or model name to the constructor:

```python
agent = AgentTools(model=my_model)
#or
agent = AgentTools(model_name = "mistral-7b-instruct-v0.1.Q4_0.gguf")
```

## Chat

Chat with your newly created Agent, make sure to at least initialize the model, by passing a model or model_name in `AgentTools` class. You can access the list of models here. [Models](https://raw.githubusercontent.com/nomic-ai/gpt4all/main/gpt4all-chat/metadata/models2.json).

```python
agent.chat(query='What is the theory of relativity?')
```

## Add Tools

Add Tools that the Model can access, the tools can be user-defined python functions, also do add their description and usage so that the models can understand them better. 

```python
def mul(a,b):
    try:
        return a*b
    except:
        return None
def div(a,b):
    try:
        return a/b
    except:
        return None

agent.add_tool('multiply', mul, "Multiplies two numbers", "mul(a,b)")
agent.add_tool('division', div, "Divides two numbers", "div(a,b)")

result = agent.chat('What is 89 times 44?')
print(result)
```
```bash
3916
```

# Contributing
Feel free to Contribute further by forking the repository and submitting pull requests or submitting issues. [Github](https://github.com/abhiram1809/Quant_AgentTools)