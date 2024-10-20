"""
Defining and importing the LLM for answering the questions.
Each model's definition should be written as a functions that returns the model.
"""

import locale
import os

import torch
import transformers
from huggingface_hub import login
from langchain_huggingface import HuggingFacePipeline
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from src.utils.common import load_secrets

# Logging to huggingface - insert personal token from:
# https://huggingface.co/docs/hub/en/security-tokens
# secrets = load_secrets()
# huggingface_token = secrets['huggingface_token']  # User_Access_Token
from huggingface_hub import login
login(token="huggingface_token") # User_Access_Token

# ----------------- Mistral -----------------
def mistral(model_name='mistralai/Mistral-7B-Instruct-v0.1'):
    """
    Initialize Mistral Model and Tokenizer with BitsAndBytes Configuration.
    By default, sets up Mistral-7B-Instruct-v0.1.
    :param model_name: The name of the model from HuggingFace
    :return: An LLM
    """
    saved_model_name = 'mistral'
    local_model_dir = f'./saved_models/{saved_model_name}'
    if not os.path.exists(local_model_dir):
        def getpreferredencoding(do_setlocale=True):
            return 'UTF-8'

        locale.getpreferredencoding = getpreferredencoding
        login(token=huggingface_token)

        # Configure BitsAndBytes for efficient model loading
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_compute_dtype='float16',
            bnb_4bit_use_double_quant=False,
        )

        # Check if GPU is available
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load the model with the above configuration
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            do_sample=True,
        )

        # Initialize tokenizer and set padding
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = 'right'

        # Save the model and tokenizer locally
        model.save_pretrained(local_model_dir)
        tokenizer.save_pretrained(local_model_dir)
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = AutoModelForCausalLM.from_pretrained(local_model_dir)#.to(device)
        tokenizer = AutoTokenizer.from_pretrained(local_model_dir)

    # ---------------- Set up Text Generation Pipeline -------------------
    # Set up the text generation pipeline with specific parameters
    text_generation_pipeline = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        repetition_penalty=1.1,
        return_full_text=False,
        max_new_tokens=256,
        do_sample=True,
    )

    # Create a HuggingFacePipeline instance for text generation
    mistral_llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

    return mistral_llm


if __name__ == '__main__':

    model = mistral()

    pass
