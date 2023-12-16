from pydantic import BaseModel, parse_obj_as
from typing import List, Union
from gpt4all import GPT4All

class ToolArguments(BaseModel):
    args: List[Union[ int, float, str]]

class AgentTools:
    _instance = None  # Class variable to store the single instance of AgentTools

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AgentTools, cls).__new__(cls)
            cls._instance.model = None  # Initialize the model attribute
            cls._instance.tools = []
        return cls._instance

    def __init__(self, model=None, model_name=None, threads=1):
        if not self.model:
            try:
                if model and model_name:
                    print('Only provide either Model or Model name.')
                elif model:
                    self.use_model(model, threads)
                    print(f'Model initialized with {threads} threads!!!')
                elif model_name:
                    self.use_model_name(model_name, threads)
                    print(f'{model_name} initialized with {threads} threads!!!')
            except Exception as e:
                print(f"Error initializing model: {e}")

    @classmethod
    def use_model(cls, model, threads=1):
        cls._instance.model = model
        cls._instance.model.model.set_thread_count(threads)

    @classmethod
    def use_model_name(cls, model_name, threads=1):
        cls._instance.model = GPT4All(model_name, n_threads=threads)
            
    def add_tool(self, name, function, description, usage):
        """
        Add a tool to the AgentTools.

        Parameters:
        - name (str): The name of the tool.
        - function (callable): The actual function associated with the tool.
        - description (str): A brief description of the tool.
        """
        tool = {'name': name, 'function': function, 'description': description, "Usage": usage}
        self.tools.append(tool)
    def remove_tool(self, tool_name):
        """
        Remove a tool from the AgentTools based on its name.

        Parameters:
        - tool_name (str): The name of the tool to remove.

        Returns:
        - True if the tool was removed successfully, False otherwise.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                self.tools.remove(tool)
                print(f"'{tool_name}' tool removed")
                return True
        return False
    def list_tools(self):
        """
        List all available tools with their descriptions.
        """
        string = ""
        for tool in self.tools:
            string+= f"{tool['name']}: {tool['description']} "
        return string
    def retrieve_description(self, tool_name):
        """
        Retrieves the Description of a Tool Added to this class using the tool name
        
        Parameters:
        - tool_name (str): The name of the tool whose description to retrieve..
        
        Returns:
        - The Description of the Tool Name
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                try:
                    return tool['description']
                except Exception as e:
                    # Handle validation or execution errors
                    print(f"Error executing {tool_name}: {e}")
                    return None
    
    def retrieve_usage(self, tool_name):
        """
        Retrieves the Description of a Tool Added to this class using the tool name
        
        Parameters:
        - tool_name (str): The name of the tool whose description to retrieve..
        
        Returns:
        - The Description of the Tool Name
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                try:
                    return tool['Usage']
                except Exception as e:
                    # Handle validation or execution errors
                    print(f"Error executing {tool_name}: {e}")
                    return None
    def exec_func_by_name(self, tool_name, args_string):
        """
        Execute the function associated with the given tool name and return its output.

        Parameters:
        - tool_name (str): The name of the tool whose function to execute.

        Returns:
        - The output of the executed function.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                try:
                    # Split the string into a list of arguments
                    args_list = args_string.split(', ')

                    # Use Pydantic to validate the arguments
                    tool_args = parse_obj_as(ToolArguments, {'args': args_list})

                    # Call the function with the validated arguments
                    return tool['function'](*tool_args.args)

                except Exception as e:
                    # Handle validation or execution errors
                    print(f"Error executing {tool_name}: {e}")
                    return None
    def agent_execute(self, query):
        """
        Execute an Agentic Workflow and run it step-by-step.

        Parameters:
        - query (str): Query by the user.

        Returns:
        - The output of the Agent Workflow.
        """
        try:
            model = self._instance.model
        except:
            return "Model Not Intialised, Initialise a model by using a GPT4all instance. or use the use_model() Class method."
        func_choice = model.generate(f"""You are an AI assistant that is really good with choosing tools to execute. Help as much as you can. The tools are as follows: {self.list_tools()}
Only return the tool/tools name out the list of tools provided for the given task in the format given below. Return multiple if needed
QUERY: (Query by user)
TOOL: (Tool/Tools to be used seperated by comma)
##Examples
QUERY: What is 89 times 44?
TOOL: mul

QUERY: What is 89 times 44, divided by 3?
TOOL: mul,div

##Real Execution
QUERY: "{query}"?
TOOL: """, max_tokens=200)
        func_choice = func_choice.replace(" ", "")
        func_list = [func for func in func_choice.split(',')]
        print(f"Chosen function {func_choice}")
        step = 1
        for func in func_list:
            if step==1:
                func_args = model.generate(f"""You are an AI assistant that is an expert with arguments for python functions. Help as much as you can.
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

QUERY: {query}
CHOSEN FUNCTION: {self.retrieve_usage(func)} 
ARGUMENTS: """, max_tokens=200)
                print(f'Retrieved Arguments: {func_args}')
                print(f'Chosen function on step {step} "{func}" with args: {func_args}')
                result = self.exec_func_by_name(func, func_args)
                step+=1
            
            else:
                func_args = model.generate(f"""You are AI Assistant which is a part of a Query Chain where Questions are Answered Step-by-Step. Currently you are on step {str(step+1)}.
If the step is bigger than 1, that means some result has already been obtained because only one step is done at a time. 
Your Task is to just return Arguments for a Task which can passed Directly into a Chosen Python Function, Arguments could be one or multiple, based on the User Query in the format given below
###Format:
QUERY: (Query by User)
CHOSEN FUNCTION: (Function Chosen for the Task)
RESULT TILL CURRENT STEP: (Result Obtained by Operations till the Current Step)
ARGUMENTS: (Argument/ List of Arguments)

###Examples:

QUERY: What is 89 times 44, divided by 3?
CHOSEN FUNCTION: division(a, b)
RESULT TILL CURRENT STEP: 3916
ARGUMENTS: 3916, 3

###Real Execution (ONLY complete the Argument)

QUERY: {query}
CHOSEN FUNCTION: {self.retrieve_usage(func)} 
RESULT TILL CURRENT STEP: {result}
ARGUMENTS: """)
                print(f'Retrieved Arguments: {func_args}')
                print(f'Chosen function on step {step} "{func}" with args: {func_args}')
                result = self.exec_func_by_name(func, func_args)
        print(f'Got Output: {result}')
        return result
    
        
    def chat(self, query):
        """Minimal Chatbot Functionality for the AgentTools Class. This is a very basic chatbot functionality and is not recommended to be used for production.
        
        Parameters- 
        query (str): Query by the user.
        
        Returns-
        The output of the Agent Workflow, If tools are not initialized, it will return the output of the General Chatbot."""
        try:
            if len(self.tools)==0:
                print('No tools added, Switching to General Chat')
                output = self.model.generate(f"""You are an AI Assistant, expert at answering General Questions. Help the user with their query. 

    USER: {query}

    ASSISTANT: """, max_tokens=200)
                return output
            elif len(self.tools)!=0:
                output = self.agent_execute(query)
        except:
            return "Model Not Intialised, Initialise a model by using a GPT4all instance. or use the use_model() Class method."
            