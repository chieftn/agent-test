import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "prompts",  "testPrompt.md")
with open(file_path, "r") as file:
    TEST_PROMPT = file.read()
