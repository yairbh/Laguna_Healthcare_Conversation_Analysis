"""
This script processes a conversation dataset to generate answers to specific questions using a pre-trained language model.
1. Logs in to the Hugging Face Hub using a user access token.
2. Loads conversation data from a CSV file into a Pandas DataFrame.
3. Constructs a single conversation string from the DataFrame.
4. Defines a general prompt template and various question prompts for model input.
5. Stores and retrieves the current version of prompts for processing.
6. Loads a pre-trained language model and tokenizer (FLAN-T5-LARGE).
7. Sets the maximum token length for the tokenizer to handle longer contexts.
8. Defines a function to generate answers using the language model.
9. Implements a sliding window approach to handle large conversation contexts by breaking them into manageable segments.
10. Iterates over the defined questions and generates answers for each conversation segment using the sliding window approach.
"""

# Import necessary libraries for data processing and model interaction
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import login

# Login to Hugging Face Hub using a personal access token for authentication
login(token="huggingface_token")  # User Access Token

# Load the raw conversation data from a specified CSV file into a Pandas DataFrame
csv_file_path = 'C:/Users/yairb/PycharmProjects/Laguna_June/data/processed/RAG_FLAN_temp_raw_data_df.csv'
raw_data_df = pd.read_csv(csv_file_path)

# Create a dictionary with a single conversation string constructed by concatenating speaker and text
single_conv_dict = {
    "conversation": " ".join(
        "Speaker " + row['speaker'] + ': ' + row['text']
        for _, row in raw_data_df.iterrows()
    )
}

# Define the simplified general prompt template and various question prompts
general_prompt_v1 = """
Choose one of the following options based on the conversation segment:
{question}

Conversation:
{context}

Your response (1, 0, or -9):
"""

# Dictionary containing different question prompts
question_prompts_v1 = {
    "Q1": """
    - "1" if the speaker asks for the listener's name, date of birth, and address.
    - "0" if the speaker does not ask for the listener's name, date of birth, and address.
    - "-9" if you are not sure.
    """,
    "Q2": """
    - "1" if the speaker informs the listener that the conversation is being recorded.
    - "0" if the speaker does not inform the listener that the conversation is being recorded.
    - "-9" if you are not sure.
    """,
    "Q3": "This is a placeholder for a question prompt",  # Placeholder for future question prompts
    "Q4": """
    - "1" if the speaker introduces themselves to the listener, including their name and organization.
    - "0" if the speaker does not introduce themselves to the listener, including their name and organization.
    - "-9" if you are not sure.
    """,
    "Q5": """
    - "1" if the speaker mentions PHI (Protected Health Information) or relates to handling PHI.
    - "0" if the speaker does not mention PHI (Protected Health Information) or relate to handling PHI.
    - "-9" if you are not sure.
    """,
    "Q6": """
    - "1" if one of the speakers requests to opt-out of future communication.
    - "0" if none of the speakers requests to opt-out of future communication.
    - "-9" if you are not sure.
    """,
    "Q7": """
    - "1" if the speaker mentions sensitive medical information, including substance abuse, mental health, and sexually transmitted diseases.
    - "0" if the speaker does not mention sensitive medical information, including substance abuse, mental health, and sexually transmitted diseases.
    - "-9" if you are not sure.
    """,
    "Q8": """
    - "1" if the speaker provides any medical consultation or advice during the call.
    - "0" if the speaker does not provide any medical consultation or advice during the call.
    - "-9" if you are not sure.
    """,
    "Q9": """
    - "1" if the speakers discuss care coordination efforts, such as referrals to other health services or coordination with other providers, and follow-up actions.
    - "0" if the speakers do not discuss care coordination efforts, such as referrals to other health services or coordination with other providers, and follow-up actions.
    - "-9" if you are not sure.
    """,
    "Q10": """
    - "1" if the speaker asks for the listener's levels of pain, mood, energy, sleep, mobility, or appetite during the call.
    - "0" if the speaker does not ask for the listener's levels of pain, mood, energy, sleep, mobility, or appetite during the call.
    - "-9" if you are not sure. 
    """,
    "Q11": """
    - "1" if the speaker discusses the listener's treatment compliance and medical state, including medications, treatments, and overall medical state.
    - "0" if the speaker does not discuss the listener's treatment compliance and medical state, including medications, treatments, and overall medical state.
    - "-9" if you are not sure.
    """
}

# Version control dictionary for managing different versions of prompts
prompts_version_control = {
    "general_prompt": {
        "v1": general_prompt_v1
    },
    "question_prompts": {
        "v1": question_prompts_v1
    }
}

# Specify the current version of prompts to use
current_version = "v1"
current_general_prompt = prompts_version_control["general_prompt"][current_version]
current_question_prompts = prompts_version_control["question_prompts"][current_version]

# Load the pre-trained language model and tokenizer
model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Override the default token limit for the tokenizer to handle longer contexts
tokenizer.model_max_length = 2048

# Function to generate answers using the language model
def generate_answer(prompt):
    # Tokenize the input prompt, ensuring truncation for long inputs
    inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True) # Default max_length=512 (including both input + output)
    # Generate the model output with a specified maximum number of new tokens
    outputs = model.generate(**inputs, max_new_tokens=512) # Default: without "max_new_tokens"
    # Decode the generated output to a string, skipping special tokens
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# Implement the sliding window approach to break the conversation into manageable segments
def sliding_window_context(conversation, window_size, step_size):
    tokens = conversation.split()
    # Generate conversation segments using a sliding window mechanism
    for i in range(0, len(tokens), step_size):
        yield " ".join(tokens[i:i + window_size])

# Define window size and step size for the sliding window approach
window_size = 512 #TODO can try increasing to 1024
step_size = 256 #TODO can try increasing to 512

# List of questions to test
questions_to_test = ['Q1', 'Q2', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11']

# Iterate over the defined questions and generate answers for each conversation segment
for question_id, question_prompt in current_question_prompts.items():
    if question_id in questions_to_test:
        print(f'Question: {question_id}')
        print('-' * (10 + len(question_id)))
        # Apply the sliding window to the conversation string
        for context_segment in sliding_window_context(single_conv_dict['conversation'], window_size, step_size):
            # Format the prompt with the current question and conversation segment
            prompt = current_general_prompt.format(question=question_prompt, context=context_segment)
            # Generate and print the answer from the model
            answer = generate_answer(prompt)
            print(f"Prompt:\n{prompt}\n\nAnswer: {answer}\n")
