from Quant_AgentTools.agent_tools import AgentTools

agent = AgentTools(model_name = "mistral-7b-instruct-v0.1.Q4_0.gguf", threads=4)

print(agent.chat("What is the theory of relativity?"))