"""
This file defines the prompts for the RAG model.
"""

list_of_topics = ['1. Member Identification',
                  '2. Call Recording',
                  '3. Participant Verification',
                  '4. CM Introduction',
                  '5. Handling PHI',
                  '6. TCPA Compliance',
                  '7. Sensitive Information Protocol',
                  '8. Medical consultation / advice',
                  '9. Care Coordination',
                  '10. Log protocol',
                  '11. Treatment compliance / medical state']
topic_range = range(1, len(list_of_topics) + 1)
topic_dict = {x: list_of_topics[x - 1] for x in topic_range}
topic = topic_dict
default_prompt_versions={x: 'v1' for x in list_of_topics}


def topic_prompts(prompt_versions:dict=None) -> list:
    """
    This function creates the prompts for each topic.
    Each topic-prompt can have multiple versions in order to experiment and find the optimal one.
    v0 is an empty version, designed to exclude a certain topic from a specific experiment.
    v1 is a naive approach, in which the model also gets the original topic list from Laguna, and simply asks whether the topic appeares
        in the conversation.
    Further versions should be added as items to the prompt_version_updates dictionary./n
    This function should get a list with strings of version names with small letter 'v' and a number, without white space.

    :param prompt_versions: Dict of version names with small letter 'v'. Should contain a version for each topic. To exclude a topic, provide v0.
    :return: A list of with a question dictionary for each topic.
    """

    # Defaults all versions to v1 if not specified otherwise
    if prompt_versions is None:
        prompt_versions = default_prompt_versions
    version = prompt_versions

    # ------------------ creating topic-prompts template ------------------
    # Creating a dictionary of default prompts per topic:
    #   - v0: An empty prompt, to exclude a topic from general prompt
    #   - v1: A naive template in the format: 'Does the topic "<topic>" appear in this convesation?'
    # Example for prompts_dictionary[1]:
    #                                 key:    '1. Member Identification'
    #                                 values: {'v0': '',
    #                                          'v1': 'Does the topic "Member Identification" appear in this convesation?'}
    prompts_dictionary = {topic[x]: {'v0': '',
                                     'v1': f'Does the topic "{topic[x].split(". ")[1]}" appear in this conversation?'}
                          for x in topic_range}

    ############## y1 ##############

    ############## y2 ##############
    y2_question_1 = """
- "1" if the speaker asks for the listener's name, date of birth, and address.
- "0" if the speaker does not ask for the listener's name, date of birth, and address.
- "-9" if you are not sure whether the speaker asks for the listener's name, date of birth, and address.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "Thank you for calling DataPeak Co Medical Center. We are pleased to announce that HorizonEdge Corp has changed its name to DataPeak Co. Over the coming months, you'll notice the new name, a new logo, and a new look. As we transition from FutureMind Solutions to DataPeak Co across our health system, our name and look will be different, but our purpose remains the same and you can expect the same great care and service from your physicians, nurses, and hospitals. Eight of our attendants will be with you shortly."
   Analysis: 0 

2. Conversation Segment: "Good, good. Um, and then just Sofia, before we move further, if you can just give me, just for DataPeak Corp again, for protection of your medical and your personal information, just your full name and date of birth and 9942 Church Road."
   Analysis: 1 
    """

    y2_question_2 = """
- "1" if the speaker informs the listener that the conversation is being recorded.
- "0" if the speaker does not inform the listener that the conversation is being recorded.
- "-9" if you are not sure whether the speaker informs the listener that the conversation is being recorded.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "Hi Olivia. My name is Gilli. I'm a nurse with TechFuse LLC calling from a recorded line. We are partnering with your Anthem, Blue Cross and StormFront Inc benefits to support you with your care needs and recovery."
   Analysis: 1 

2. Conversation Segment: "Thank you for calling DataPeak Co Medical Center. We are pleased to announce that HorizonEdge Corp has changed its name to DataPeak Co. Over the coming months, you'll notice the new name, a new logo, and a new look. As we transition from FutureMind Solutions to DataPeak Co across our health system, our name and look will be different, but our purpose remains the same and you can expect the same great care and service from your physicians, nurses, and hospitals."
   Analysis: 0 
    """

    y2_question_3 = """
- "1" if the speaker is speaking directly with a healthcare member.
- "2" if the speaker is speaking with a caregiver/authorized representative and proper authorization is provided.
- "0" if the speaker is speaking with a caregiver/authorized representative but proper authorization is not provided.
- "-9" if you are not sure about the relationship or the authorization status.

Only provide the number ("2", "1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "Hi, Olivia. This is Gilli from TechFuse LLC. Can I confirm that I am speaking with Olivia Carrasco?"
   Analysis: 1 

2. Conversation Segment: "Hello, this is Gilli from TechFuse LLC. Am I speaking with Olivia's authorized representative? Can you confirm your authorization to discuss Olivia's health information?"
   Analysis: 2 

3. Conversation Segment: "Hi, I'm Gilli from TechFuse LLC. Are you authorized to speak on behalf of Olivia? We need to confirm authorization before we proceed."
   Analysis: 0 
    """

    y2_question_4 = """
- "1" if the speaker introduces themselves to the listener, including their name and organization.
- "0" if the speaker does not introduce themselves to the listener, including their name and organization.
- "-9" if you are not sure whether the speaker introduces themselves to the listener, including their name and organization.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "Hi, this is Gilli from TechFuse LLC. I'm calling to discuss your recent visit to our clinic."
   Analysis: 1 

2. Conversation Segment: "Hello, I'm a representative from TechFuse LLC. How can I assist you today?"
   Analysis: 1 

3. Conversation Segment: "Good morning, I'm calling regarding your appointment next week."
   Analysis: 0 
    """

    y2_question_5 = """
- "1" if the speaker mentions PHI (Protected Health Information) or relates to handling PHI.
- "0" if the speaker does not mention PHI (Protected Health Information) or relate to handling PHI.
- "-9" if you are not sure whether the speaker mentions PHI (Protected Health Information) or relates to handling PHI.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "We need to discuss your protected health information related to your recent treatment."
   Analysis: 1 

2. Conversation Segment: "We will review your recent lab results and discuss the next steps in your treatment."
   Analysis: 1 

3. Conversation Segment: "Can you confirm your next appointment date with us?"
   Analysis: 0 
    """

    y2_question_6 = """
- "1" if one of the speakers requests to opt-out of future communication.
- "0" if none of the speakers requests to opt-out of future communication.
- "-9" if you are not sure whether one of the speakers requests to opt-out of future communication.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: 
   Speaker 1: "I would like to opt-out of future communications, please."
   Analysis: 1 

2. Conversation Segment:
   Speaker 1: "Please remove me from your contact list. I don't want to receive any more calls."
   Analysis: 1 

3. Conversation Segment:
   Speaker 1: "Can I stop receiving these calls?"
   Analysis: 1 

4. Conversation Segment:
   Speaker 1: "I don't have any more questions. Thank you for the information."
   Analysis: 0 
    """

    y2_question_7 = """
- "1" if the speaker mentions sensitive medical information, including substance abuse, mental health, and sexually transmitted diseases.
- "0" if the speaker does not mention sensitive medical information, including substance abuse, mental health, and sexually transmitted diseases.
- "-9" if you are not sure whether the speaker mentions sensitive medical information, including substance abuse, mental health, and sexually transmitted diseases.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "We need to discuss your recent diagnosis of depression and the treatment options available."
   Analysis: 1 

2. Conversation Segment: "Your lab results indicate that you have an STI. We need to talk about the next steps."
   Analysis: 1 

3. Conversation Segment: "It's important that we address your substance abuse issues to ensure your recovery."
   Analysis: 1 

4. Conversation Segment: "Let's review your medication list and see if there are any changes needed."
   Analysis: 0 
    """

    y2_question_8 = """
- "1" if the speaker provides any medical consultation or advice during the call.
- "0" if the speaker does not provide any medical consultation or advice during the call.
- "-9" if you are not sure whether the speaker provides any medical consultation or advice during the call.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "You should take your medication twice daily and monitor your blood pressure regularly."
   Analysis: 1 

2. Conversation Segment: "It's important to follow a balanced diet and exercise regularly to manage your condition."
   Analysis: 1 

3. Conversation Segment: "Please make sure to attend your follow-up appointment next week."
   Analysis: 0 

4. Conversation Segment: "Can you confirm your next appointment date with us?"
   Analysis: 0 
    """

    y2_question_9 = """
- "1" if the speakers discuss care coordination efforts, such as referrals to other health services or coordination with other providers, and follow-up actions.
- "0" if the speakers do not discuss care coordination efforts, such as referrals to other health services or coordination with other providers, and follow-up actions.
- "-9" if you are not sure whether the speakers discuss care coordination efforts, such as referrals to other health services or coordination with other providers, and follow-up actions.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "We will refer you to a specialist for further evaluation and coordinate with your primary care provider for follow-up."
   Analysis: 1 

2. Conversation Segment: "Our team will make sure that all your test results are sent to your cardiologist and schedule a follow-up appointment."
   Analysis: 1 

3. Conversation Segment: "Make sure to attend your physical therapy sessions and let us know if you need any assistance."
   Analysis: 1 

4. Conversation Segment: "Please take your medication as prescribed and contact us if you have any questions."
   Analysis: 0 
    """

    y2_question_10 = """
- "1" if the speaker asks for the listener's levels of pain, mood, energy, sleep, mobility, or appetite during the call.
- "0" if the speaker does not ask for the listener's levels of pain, mood, energy, sleep, mobility, or appetite during the call.
- "-9" if you are not sure whether the speaker asks for the listener's levels of pain, mood, energy, sleep, mobility, or appetite during the call.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "Can you tell me how your pain levels have been over the past week?"
   Analysis: 1 

2. Conversation Segment: "How have you been feeling emotionally? Any changes in your mood?"
   Analysis: 1 

3. Conversation Segment: "Have you been sleeping well lately? Any issues with your sleep?"
   Analysis: 1 

4. Conversation Segment: "I need to verify your appointment details for next week."
   Analysis: 0 
    """

    y2_question_11 = """
- "1" if the speaker discusses the listener's treatment compliance and medical state, including medications, treatments, and overall medical state.
- "0" if the speaker does not discuss the listener's treatment compliance and medical state, including medications, treatments, and overall medical state.
- "-9" if you are not sure whether the speaker discusses the listener's treatment compliance and medical state, including medications, treatments, and overall medical state.

Only provide the number ("1", "0", or "-9") as your response.

Here are some examples of how to analyze:
1. Conversation Segment: "Are you taking your medications as prescribed?"
   Analysis: 1 

2. Conversation Segment: "Have you been following the treatment plan we discussed? Any issues with the medications?"
   Analysis: 1 

3. Conversation Segment: "Can you update me on your current medical condition and any treatments you're undergoing?"
   Analysis: 1 

4. Conversation Segment: "Please remember to bring your insurance card to the next appointment."
   Analysis: 0 
    """

    ############## y3 ##############

    ############## y4 ##############
    y4_question_1 = """
        - "1" if the speaker asks for the listener's name, date of birth, and address.
        - "0" if the speaker does not ask for the listener's name, date of birth, and address.
        - "-9" if you are not sure whether the speaker asks for the listener's name, date of birth, and address.

        Here are some examples of how to analyze:
        1. Conversation Segment: "Thank you for calling DataPeak Co Medical Center. We are pleased to announce that HorizonEdge Corp has changed its name to DataPeak Co. Over the coming months, you'll notice the new name, a new logo, and a new look. As we transition from FutureMind Solutions to DataPeak Co across our health system, our name and look will be different, but our purpose remains the same and you can expect the same great care and service from your physicians, nurses, and hospitals. Eight of our attendants will be with you shortly."
           Analysis: 0 

        2. Conversation Segment: "Good, good. Um, and then just Sofia, before we move further, if you can just give me, just for DataPeak Corp again, for protection of your medical and your personal information, just your full name and date of birth and address."
           Analysis: 1 
            """

    ############## y5 ##############
    y5_question_1 = """
           - "1" if the speaker asks for the listener's name, date of birth, and address.
           - "0" if the speaker does not ask for the listener's name, date of birth, and address.
           - "-9" if you are not sure whether the speaker asks for the listener's name, date of birth, and address.
               """



    prompt_version_updates = {1: {'y2': y2_question_1,
                                  'y4': y4_question_1,
                                  'y5': y5_question_1
                                  },
                              2: {'y2': y2_question_2,
                                  },
                              3: {'y2': y2_question_3,
                                  },
                              4: {'y2': y2_question_4,
                                  },
                              5: {'y2': y2_question_5,
                                  },
                              6: {'y2': y2_question_6,
                                  },
                              7: {'y2': y2_question_7,
                                  },
                              8: {'y2': y2_question_8,
                                  },
                              9: {'y2': y2_question_9,
                                  },
                              10: {'y2': y2_question_10,
                                   },
                              11: {'y2': y2_question_11,
                                   }
                              }

    # Update prompts_dictionary with new versions:
    for i in topic_range:
        prompts_dictionary[topic[i]].update(prompt_version_updates[i])
    prompt = prompts_dictionary

    # Create the question list based on provided list of versions
    test_set = [{'question': prompt[topic[x]][version[x]]} for x in topic_range]

    return test_set


prompt_template = {
'y1': """
Please analyze the following conversation segment and categorize it into one of the following three options:
{question}

Now analyze the following conversation segment:
{context}
""",

'y2': """
Analyze the following conversation segment and provide your response as a single number: "1", "0", or "-9".
{question}

Now analyze the following conversation segment:
{context}
""",

'y3': """
Here is a part of a conversation: 
{context}

Analyze this conversation segment and provide your response as a single number ("1", "0", or "-9") according to the following alternatives: 
{question}

Provide your answer here (remember: respond only with a number: "1", "0", or "-9").   
""",

'y4': """
Here is a part of a conversation (it ends with "END OF CONVERSATION"): 
{context}
END OF CONVERSATION
From the following options, choose the one that best describes this conversation segment. Provide only the best option's number ("1", "0", or "-9"):  
{question}
""",

'y5': """
Analyze the following conversation segment and respond with a single number:
{question}

Conversation:
{context}

Your response (1, 0, or -9):
""",
}



