from utils.call_llm import call_llm

# Simple test prompt
response = call_llm("Say hello!", use_cache=False)
print("API Response:", response) 