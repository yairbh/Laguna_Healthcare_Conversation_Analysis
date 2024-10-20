import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import login
import torch
import time
from src.data.fixes_filter import get_long_convs
from src.data.fixes_modify_df import fix_apostrophes, fix_strings_with_I, fix_portland
from src.utils.common import create_file_path
import os

# export_file_path = 'C:/Users/yairb/PycharmProjects/Laguna_June/tests/classified_recordings_RAG_FLAN_exp1.csv'


# Use a path valid on the remote machine
export_file_path = '/home/adir/yair/output/classified_recordings_RAG_FLAN_exp1.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(export_file_path), exist_ok=True)

# Login to Hugging Face Hub using a personal access token for authentication
login(token="huggingface_token")  # User Access Token

def create_single_recording_text(df_single_recording):
    recording_id = df_single_recording['recording_id'].iloc[0]
    recording_text = " ".join(
        "Speaker " + row['speaker'] + ': ' + row['text']
        for _, row in df_single_recording.iterrows()
    )
    return recording_id, recording_text

general_prompt_v1 = """
Choose one of the following options based on the conversation segment:
{question}

Conversation:
{context}

Your response (1, 0, or -9):
"""

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
    "Q3": "This is a placeholder for a question prompt",
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

prompts_version_control = {
    "general_prompt": {
        "v1": general_prompt_v1
    },
    "question_prompts": {
        "v1": question_prompts_v1
    }
}

current_version = "v1"
current_general_prompt = prompts_version_control["general_prompt"][current_version]
current_question_prompts = prompts_version_control["question_prompts"][current_version]

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

tokenizer.model_max_length = 2048

def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True).to(device)
    outputs = model.generate(**inputs, max_new_tokens=512)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def sliding_window_context(conversation, window_size, step_size):
    tokens = conversation.split()
    for i in range(0, len(tokens), step_size):
        yield " ".join(tokens[i:i + window_size])

window_size = 512
step_size = 256

questions_to_test = ['Q1', 'Q2', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11']

def classify_RAG_FLAN(recording_id, recording_entire_text, current_question_prompts, current_general_prompt, window_size, step_size, questions_to_test, output):
    start_time = time.time()
    if output == 'print':
        for question_id, question_prompt in current_question_prompts.items():
            if question_id in questions_to_test:
                # print(f'Processing Question: {question_id}')
                print('-' * (10 + len(question_id)))
                for context_segment in sliding_window_context(recording_entire_text, window_size, step_size):
                    prompt = current_general_prompt.format(question=question_prompt, context=context_segment)
                    answer = generate_answer(prompt)
                    print(f"Prompt:\n{prompt}\n\nAnswer: {answer}\n")
    elif output == 'dataframe':
        all_rows = []
        columns = ['recording_id', 'general_prompt', 'question_id', 'question_prompt', 'conversation_window', 'class']

        for question_id, question_prompt in current_question_prompts.items():
            if question_id in questions_to_test:
                # print(f'Processing Question: {question_id}')
                current_question_id = question_id
                current_question_prompt = question_prompt
                for context_segment in sliding_window_context(recording_entire_text, window_size, step_size):
                    current_conversation_window = context_segment
                    prompt = current_general_prompt.format(question=question_prompt, context=context_segment)
                    current_answer = generate_answer(prompt)
                    all_rows.append({
                        'recording_id': recording_id,
                        'general_prompt': current_general_prompt,
                        'question_id': current_question_id,
                        'question_prompt': current_question_prompt,
                        'conversation_window': current_conversation_window,
                        'class': current_answer
                    })
                    # print(f"Processed segment for question {question_id}")

        df = pd.DataFrame(all_rows)
        # end_time = time.time()
        # print(f"Finished processing recording {recording_id} in {end_time - start_time:.2f} seconds")
        return df

##########MAIN###########
from src.utils.common import get_project_root
import os
from src.utils.constants import raw_data_df, cities_file
from src.data.data_pipeline_functions import clean_data


print("Staring script...")

# Getting folder's path
project_root = get_project_root()

# Importing data
df = raw_data_df.copy()

# Cleaning data
print("Filtering and fixing utterances...")
df = clean_data(df, cities_file=cities_file, cities_threshold=3) # includes keeping only long convs


print(f"Number of recordings in Data: {len(df['recording_id'].unique())}")
print()
print("Starting inference...")


batch_counter = 0
batch_list = []
batch_size = 100
# df_list = []
for i, recording_id in enumerate(df['recording_id'].unique()):
    start_time = time.time()
    num_utterances = raw_data_df[raw_data_df['recording_id'] == recording_id].shape[0]
    print(f"Processing recording {i+1}/{len(df['recording_id'].unique())} ({num_utterances} utterances): {recording_id}")
    single_recording_df = df[df['recording_id'] == recording_id]
    current_recording_id, current_recording_text = create_single_recording_text(single_recording_df)
    current_df = classify_RAG_FLAN(
        recording_id=current_recording_id,
        recording_entire_text=current_recording_text,
        current_question_prompts=current_question_prompts,
        current_general_prompt=current_general_prompt,
        window_size=window_size,
        step_size=step_size,
        questions_to_test=questions_to_test,
        output='dataframe'
    )

    # df_list.append(current_df)
    batch_list.append(current_df)
    batch_counter += 1

    if batch_counter >= batch_size:
        # Concatenate and save the current batch
        batch_df = pd.concat(batch_list, ignore_index=True)
        batch_filename = f"/home/adir/yair/output/classified_recordings_RAG_FLAN_batch_{i // batch_size + 1}.csv"
        batch_df.to_csv(batch_filename, index=False)
        print(f"Saved batch {i // batch_size + 1} to {batch_filename}")

        # Reset batch list and counter
        batch_list = []
        batch_counter = 0

    end_time = time.time()
    print(f"Finished processing recording {recording_id} in {end_time - start_time:.2f} seconds")

# Save any remaining rows in the last batch
if batch_list:
    batch_df = pd.concat(batch_list, ignore_index=True)
    batch_filename = f"/home/adir/yair/output/classified_recordings_RAG_FLAN_batch_{(i // batch_size) + 1}.csv"
    batch_df.to_csv(batch_filename, index=False)
    print(f"Saved final batch to {batch_filename}")

# all_recordings_classified_df = pd.concat(df_list, ignore_index=True)

# all_recordings_classified_df.to_csv(export_file_path)
# print("Script finished. CSV file created.")
