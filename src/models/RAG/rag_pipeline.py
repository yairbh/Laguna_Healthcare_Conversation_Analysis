import pickle
import  re
import numpy as np
import requests
from langchain.chains.llm import LLMChain
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

import get_model
from preprocessing_for_RAG import preprocess_for_RAG  # Performs preprocessing the prepares segments (chunks) for RAG model
from prompts import topic_prompts, prompt_template
from src.utils.constants import raw_data_df

# Choosing and loading model
llm = get_model.mistral()



# ---------------------- Assigning context text ----------------------
# Load raw dataframe
df = raw_data_df.copy()
df_single_conv = df[df['recording_id'] == 'd5c13967-e360-4be9-b8d4-1485a1830c89']  # Replace as needed

# Preprocess data
# processed_dict is a dictionary with recording_id (keys) and list of concatenated utterance texts (values).
single_conv_dict = preprocess_for_RAG(df_single_conv)  # key: recording id; value: full text
entire_convs_dict = preprocess_for_RAG(df, enumerate_file_names=True)  # key: recording#; value: full text

# context_text = import_pini_the_who()  # assigning pinni the wooh data for validation and debugging
context_text = single_conv_dict['d5c13967-e360-4be9-b8d4-1485a1830c89']


# ------------------------------ Version Control ------------------------------
# Versions of the different questions
prompt_versions = {1: 'y5', 2: 'y2',3: 'y2',4: 'y2',5: 'y2',6: 'y2',7: 'y2',8: 'y2',9: 'y2',10: 'y2',11: 'y2',}
test_set = topic_prompts(prompt_versions=prompt_versions)
template_version = prompt_template['y5'] # version of the general prompt


# ------------------------------ Evaluation Functions ------------------------------
# Creating a similarity model:

sentence_transformer_name = 'sentence-transformers/all-mpnet-base-v2'
sentence_transformer = SentenceTransformer(sentence_transformer_name)


def answer_question(question, model, llm_chain, retriever=None, window: str = None, use_retriever=False):
    if use_retriever:
        # Use the retriever to find relevant context for the question
        context = retriever.get_relevant_documents(question)
    else:
        context = window

    # Use the language model to generate an answer based on the context
    input_data = {"question": question, "context": context}

    answer = llm_chain.invoke(input_data)
    return answer


def evaluate_model(questions_list,  # Question
                   model,
                   full_text: str,  # Context
                   window_size: int, step_size: int,
                   llm_chain=None,  # Prompt template
                   use_retriever=False, retriever=None,
                   to_print=False):
    """

    :param questions_list:
    :param model:
    :param full_text:
    :param window_size:
    :param step_size:
    :param use_retriever:
    :param retriever:
    :param llm_chain:
    :param to_print:
    :return:
    """
    # total_questions = len(questions_list)
    # correct_answers = 0
    print('#'*10, 'Inference loop', '#'*10)
    i = 0
    evaluation_results = {}
    window_number = int(np.ceil((len(full_text.split()) - window_size) / step_size) + 1)
    for window in sliding_window_context(full_text, window_size, step_size):
        i += 1
        if to_print:
            print(f'window {i}/{window_number}:')
            print(window, '\n')

        evaluation_results[f'window {i}/{window_number}'] = {'text': window,
                                             'questions': []}
        # Itterate over all questions
        for item in questions_list:
            question = item["question"]
            if question == '':
                continue

            # Get the model's answer
            if use_retriever and retriever and llm_chain:
                prompt_data = {"question": question, "context": window}
                model_answer = answer_question(question,    # Question
                                               model,
                                               retriever,   # Context
                                               llm_chain    # Prompt template
                                               )
            else:
                prompt_data = {"question": question, "context": window}
                model_answer = answer_question(question=question,    # Question
                                               model=model,
                                               window=window,        # Context
                                               llm_chain=llm_chain,  # Prompt template
                                               use_retriever=False
                                               )
            # Print the question, correct answer, and model's answer for verification

            if to_print:
                # print(f"Question: {question}")
                # print(f"Correct Answer: {correct_answer}")
                print("Complete prompt being fed into the model:")
                print("-----------------------------------------")
                print(llm_chain.prompt.format(**prompt_data))
                print(f"Model Answer: {model_answer}")

            evaluation_results[f'window {i}/{window_number}']['questions'].append(f"Question: {question}")
            evaluation_results[f'window {i}/{window_number}']['questions'].append(f"Model Answer: {model_answer}")

            if to_print:
                print("-" * 30)

    if to_print:
        print("-" * 99)

    return evaluation_results



# -------------------------- Creating prompt template --------------------------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template_version,
)

# --------------------------- Creating Language Model Chain ---------------------------
llm_chain = LLMChain(llm=llm, prompt=prompt)


# --------------------------- Inference ---------------------------
def sliding_window_context(full_text: str, window_size: int, step_size: int) -> str:
    """
    Generate sliding windows of text from the full text.

    :param full_text: The complete text to split into windows.
    :param window_size: The number of words in each window.
    :param step_size: The number of words to move the window by.
    :return: The next window of text.
    """
    words = full_text.split()
    for start in range(0, len(words), step_size):
        end = min(start + window_size, len(words))
        yield " ".join(words[start:end])
        if end == len(words):
            break


def answer_questions_with_sliding_window(full_text: str, questions: list, llm_chain, window_size=512, step_size=256) -> list:
    """
    Answer questions using a sliding window approach on the full text.

    :param full_text: The full text of the conversation.
    :param questions: The list of questions to answer.
    :param llm_chain: The language model chain to use for generating answers.
    :param window_size: The size of each window in words. Defaults to 512.
    :param step_size: The step size to move the window by. Defaults to 256.
    :return: The answers generated by the model.
    """
    all_answers = []
    for window in sliding_window_context(full_text, window_size, step_size):
        input_data = {"context": window, "questions": "\n".join([q[list(q.keys())[0]] for q in questions])}
        window_answers = llm_chain.invoked(input_data)
        all_answers.append(window_answers)
    return all_answers


use_retriever = False
if use_retriever:
    # --------------------------- Preprocess Book Text for Retrieval ---------------------------
    # Replace multiple newlines with a single newline to standardize spacing
    context_text = context_text.replace('\r\n', '\n').replace('\r', '\n').strip()

    # Split the text into sentences and remove empty lines
    sentences = context_text.split('. ')
    sentences = [line.strip() for line in sentences if line.strip()]

    # Group lines into sections of 10 lines each
    sections = ['\n'.join(sentences[i:i + 10]) for i in range(0, len(sentences), 10)]

    # Print the first few sections to verify
    # for i, section in enumerate(sections[:5]):
    #     print(f"Section {i+1}:\n{section}\n{'-'*40}")

    # --------------------------- Create Embeddings and FAISS Index ---------------------------
    # Index the processed documents with FAISS for efficient retrieval
    db = FAISS.from_texts(
        sections,
        HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L12-v2')
    )

    n = 10
    # Convert the FAISS index into a retriever
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": n},
        )

    # --------------------------- Save and Load Retriever ---------------------------
    def save_object(obj, filename):
        with open(filename, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


    def load_object(filename):
        with open(filename, 'rb') as inp:  # Open the file in binary read mode
            obj = pickle.load(inp)
        return obj


    # Save the retriever
    # retriever_name = 'pooh_retriever'
    retriever_name = 'laguna_retriever'
    save_object(retriever, '%s.pkl' % retriever_name)
    # Load the retriever
    loaded_retriever = load_object('%s.pkl' % retriever_name)

    results_retriever = evaluate_model(questions_list=test_set,  # Questions
                                       model=llm,
                                       full_text=context_text,  # Context
                                       window_size=1024, step_size=512,
                                       llm_chain=llm_chain,  # llm + prompt
                                       use_retriever=use_retriever,
                                       retriever=loaded_retriever,  # The retriever comes with the context (recording)
                                       to_print=True
                                       )


# --------------------------- Evaluate the Model ---------------------------
# Evaluate the model using the retriever
# accuracy, results = evaluate_model(test_set, llm, use_retriever=True, retriever=loaded_retriever, llm_chain=llm_chain, to_print=False)
results = evaluate_model(questions_list=test_set,           # Questions
                         model=llm,
                         full_text=context_text,            # Context
                         window_size=512, step_size=256,
                         llm_chain=llm_chain,               # llm + prompt
                         use_retriever=use_retriever,
                         to_print=True
                         )

# --------------------------- Printing results ---------------------------
for result in results:
    print(result)

pass
# print('\n'*5, '~'*100, '\n\nhello there')
