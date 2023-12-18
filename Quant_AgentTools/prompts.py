from string import Template

GENERAL_CHAT = Template("""You are an AI Assistant, expert at answering General Questions. Help the user with their query. 

USER: $query

ASSISTANT: """)

TOOL_CHOICE = Template("""You are an AI assistant that is really good with choosing tools to execute. Help as much as you can. The tools are as follows: $tools
Only return the tool/tools name out the list of tools provided for the given task in the format given below. Return multiple if needed
QUERY: (Query by user)
TOOL: (Tool/Tools to be used seperated by comma)
##Examples
QUERY: What is 89 times 44?
TOOLS: mul

QUERY: What is 89 times 44, divided by 3?
TOOLS: mul,div

##Real Execution
QUERY: "$query"?
TOOLS: """)

AGENT_INITIAL_STEP = Template("""You are an AI assistant that is an expert with arguments for python functions. Help as much as you can.
Only Return the arguments to be passed to the chosen python function, Arguments could be one or multiple, based on the User Query in the format given below. 
###STRICT INSTRUCTION:
If the function uses query as argument, pass the query in the arguments.
###Format:

QUERY: (Query by User)
CHOSEN FUNCTION: (Function Chosen for the Task)
ARGUMENTS: (Argument/ List of Arguments)

###Example:

QUERY: What is 23 times 87?
CHOSEN FUNCTION: multiply(a, b)
ARGUMENTS: 23, 87

QUERY: What is the theory of relativity?
CHOSEN FUNCTION: RAG_query(query)
ARGUMENTS: "What is the Theory of Relativity?"

QUERY: What is 89 times 44, divided by 3?
CHOSEN FUNCTION: multiply(a, b)
ARGUMENTS: 89, 44

QUERY: What is a neural network?
CHOSEN FUNCTION: search(query)
ARGUMENTS: "What is a neural network?"

### Real Execution (Only complete the Argument):

QUERY: $query
CHOSEN FUNCTION: $function 
ARGUMENTS: """)

AGENT_DEFAULT_STEP = Template("""You are AI Assistant which is a part of a Query Chain where Questions are Answered Step-by-Step. Currently you are on step $step_count.
If the step is bigger than 1, that means some result has already been obtained because only one step is done at a time. 
Your Task is to just return Arguments for a Task which can passed Directly into a Chosen Python Function, Arguments could be one or multiple, based on the User Query in the format given below
###Format:
QUERY: (Query by User)
CHOSEN FUNCTION: (Function Chosen for the Task)
RESULT TILL CURRENT STEP: (Result Obtained by Operations till the Current Step)
ARGUMENTS: (Argument/ List of Arguments)

###Examples:

QUERY: What is 89 times 44, divided by 3?
CHOSEN FUNCTION: div(a, b)
RESULT TILL CURRENT STEP: 3916
ARGUMENTS: 3916, 3

###Real Execution (ONLY complete the Arguments)

QUERY: $query
CHOSEN FUNCTION FOR CURRENT STEP: $function 
RESULT TILL CURRENT STEP: $result
ARGUMENTS: """)

