"""
This file defines the prompts and questions for the RAG model.
"""

def topic_prompts(version='v1'):
    questions_dict = {
        'v1': [
            {'1': "Does the care manager asks for the member's name, date of birth, and address?"}#,
            # {'2': "Does the care manager inform the call participant that the conversation is being recorded?"},
            # {'3': "Is the care manager speaking directly with the member or with a caregiver/authorized representative? If the latter, is proper authorization provided?"},
            # {'4': "Does the care manager introduce themselves at the start of the call, including their name and organization?"},
            # {'5': "Does the care manager mention PHI (Protected Health Information) or relate to handling PHI?"},
            # {'6': "Does the member requests to opt-out of future communication? If so, does the care manager confirms the memebers' request?"},
            # {'7': "Does the care manager mention sensitive medical information, including substance abuse, mental health, and sexually transmitted diseases?"},
            # {'8': "Does the care manager provide any medical consultation or advice during the call?"},
            # {'9': "Does the care manager discuss care coordination efforts, such as referrals to other health services or coordination with other providers, and follow-up actions?"},
            # {'10': "Does the care manager ask for the member's levels of pain, mood, energy, sleep, mobility, and appetite during the call?"},
            # {'11': "Does the care manager discuss the member's treatment compliance and medical state, including medications, treatments, and overall medical state?"}
        ],
        'v2': [
            {'1': ""},
            {'2': ""},
            {'3': ""},
            {'4': ""},
            {'5': ""},
            {'6': ""},
            {'7': ""},
            {'8': ""},
            {'9': ""},
            {'10': ""},
            {'11': ""}
        ]
    }
    return questions_dict[version]

def prompt_templates(version='v1'):
    templates_dict = {
        'v1': """The provided context contains a segment of a conversation between a care manager from a medical 
        insurance company in the USA and a member of that company. The member was recently released from 
        hospitalization and received medical instructions to follow to prevent re-hospitalization. Read this context 
        carefully and answer the following questions about the conversation:

{context}

If you can't find the answer in the context, respond with: "The answer isn't in the data supplied."

Questions:
{questions}

Answer:
""",

        'v2': """

"""
    }
    return templates_dict[version]
