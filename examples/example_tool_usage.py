from Quant_AgentTools.agent_tools import AgentTools

agent = AgentTools(model_name="mistral-7b-instruct-v0.1.Q4_0.gguf", threads=4)


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def div(a, b):
    return a / b


agent.add_tool("mul", multiply, "Multiplies two numbers", "mul(a, b)")
agent.add_tool("div", div, "Divides two numbers", "div(a, b)")

print(agent.chat("What is 7200 divided by 36, then times 5?"))
