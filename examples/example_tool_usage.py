from Quant_AgentTools.agent_tools import AgentTools

agent = AgentTools(model_name="mistral-7b-openorca.Q4_0.gguf", threads=4)


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def div(a, b):
    return a / b


agent.add_tool("multiply", mul, "Multiplies two numbers", "mul(a, b)")
agent.add_tool("division", div, "Divides two numbers", "div(a, b)")

print(agent.chat("What is 7200 divided by 36, then times 5?"))
