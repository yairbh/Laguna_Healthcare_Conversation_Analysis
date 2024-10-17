"""
11 lists of generated utterances (one list for each topic).
All lists are merged into a dictionary.
"""

# Topic 1: Member Identification
member_identification = [
    "Hi Olivia, for our records, can you confirm your name, date of birth, and address?",
    "James, could you please verify your full name and the address listed on your account?",
    "To update our files, James, could you confirm your birth date and full address?",
    "For verification purposes, Elijah, please provide your full name and date of birth.",
    "Hi, this is Elijah speaking, right? Could you verify your address and date of birth for me?",
    "Hello, Amelia, I need to confirm your details starting with your name and address.",
    "Olivia, can you help me update your profile by confirming your birth date and full name?",
    "I have your address as 8103 Cedar Avenue, Sophia; is that correct? And your date of birth?",
    "Before we proceed, Mia, please confirm your name, birth date, and address for verification.",
    "Olivia, just as we start, I need you to confirm your full name and address on file.",
    "Can you please provide your date of birth and address for our records, Sophia?",
    "For our security check, Sophia, please verify your name and the address where you currently live.",
    "Hello Elijah, to continue, confirm your name, date of birth, and address, please.",
    "Ava, for our accuracy in records, can you verify your address and birth date?",
    "Could you confirm your personal details starting with your name and address, James?",
    "Amelia, to ensure we have the right details, could you state your full name and date of birth?",
    "Emma, please verify your address and date of birth as part of our routine check.",
    "Can I have your full name and the address you are currently residing at, Lucas?",
    "As a part of our verification process, Olivia, please confirm your birth date and address.",
    "For our database update, Emma, could you confirm your name, address, and the date you were born?"
]

# Topic 2: Call Recording Disclosure
call_recording_disclosure = [
    "I must inform you that this call is being recorded for training and quality purposes, James.",
    "Just so you're aware, Sophia, our conversation today will be recorded for compliance and quality monitoring.",
    "Please note, Ava, this call may be monitored or recorded for quality assurance purposes.",
    "Hello Mia, for your information, this call is being recorded as per our standard policy.",
    "As part of our practice, Sophia, I need to let you know that this call is recorded.",
    "To ensure the highest service quality, Amelia, this call will be recorded.",
    "Just a reminder, Olivia, we record all our calls for quality and training.",
    "Mia, please be aware that for quality and training reasons, this call is being recorded.",
    "I need to inform you, Lucas, that this call is being recorded for our mutual protection.",
    "Mia, this call may be recorded for quality review and training purposes.",
    "For record-keeping, James, this conversation is being recorded.",
    "This call is recorded for quality assurance, James, just to let you know.",
    "Lucas, just to ensure everything is clear, this call is being recorded.",
    "Please be advised, James, that for quality control, this call will be monitored.",
    "Hello James, just a heads-up that we're recording this call for training purposes.",
    "As I assist you today, Lucas, our call might be recorded for quality checks.",
    "To maintain service quality, James, this call is being recorded.",
    "Amelia, our policy requires us to record this conversation for training needs.",
    "Just for your information, Olivia, we record calls to improve service quality.",
    "Mia, for transparency, this call is recorded. We appreciate your understanding."
]

# Topic 3: Participant Verification
participant_verification = [
    "Mia, am I speaking directly with you or someone on your behalf today?",
    "Can you confirm, Olivia, are you the account holder or is someone else on the line?",
    "Hello James, for verification, are you the member or a representative?",
    "Mia, to proceed, please let me know if you are the member or if there’s someone else I should be aware of.",
    "For our records, Liam, could you clarify if you’re the main member or a caregiver?",
    "James, could you tell me if I’m speaking with you directly or with an authorized representative?",
    "Just for security, Lucas, are you the patient or is this a third-party call?",
    "Emma, are you the primary contact on this account or should I speak to someone else?",
    "Can you please confirm if you’re the registered member or someone assisting?",
    "Amelia, for compliance, are you personally the subscriber or an agent?",
    "Am I speaking to Olivia directly, or is this a representative on his behalf?",
    "Hello Sophia, quick check: is this conversation with you or another person?",
    "Lucas, just making sure, are you handling this call yourself or should we expect someone else?",
    "For accuracy, Emma, is this call being conducted by the patient or a delegate?",
    "James, to continue our discussion, are you the original member, or is someone representing you?",
    "Can you verify whether you or a representative is on the call, Emma?",
    "Hello Emma, are you the direct beneficiary of our services or should I speak with your caregiver?",
    "For our conversation today, Liam, are you the one I’m advising or is there a proxy?",
    "Emma, to manage this properly, could you state if you are the patient or a caregiver?",
    "I need to know, Emma, for this interaction, are you the member or is someone else authorized to speak?"
]

# Topic 4: CM Introduction
cm_introduction = [
    "Hi Lucas, I'm Christopher, your care manager from Arlington, calling you on a recorded line.",
    "Hello, this is Matthew from Arlington Health. How can I assist you today, Amelia?",
    "Good day, Lucas, my name is Matthew and I'll be helping you today from Arlington.",
    "Hello Elijah, I'm Joshua and I'm calling from Arlington on a recorded line for your service.",
    "Hi, this is Andrew from Arlington. I’m your designated care manager, Ava.",
    "Emma, I'm Christopher calling from Arlington. I'm here to assist you today.",
    "Good morning, Mia. Joshua here from Arlington, your care manager on the line.",
    "Hello Mia, this is Daniel from Arlington, calling to discuss your care management.",
    "Hi Lucas, Joshua from Arlington at your service today.",
    "James, I'm Andrew and I'll be your point of contact at Arlington Health.",
    "Hello, Ava, Andrew here from Arlington—how can I help you today?",
    "Good afternoon, Liam, it's John from Arlington, ready to assist you.",
    "Hi James, I'm Joshua, calling from Arlington on a secure line for our discussion.",
    "Hello Lucas, this is Matthew from Arlington, your care manager for today’s call.",
    "Mia, I'm Andrew and I'm looking forward to assisting you today from Arlington.",
    "Hi, James, you're speaking with Jacob from Arlington. How can I make your day better?",
    "Good evening, James, Joshua here from Arlington, how can I support you today?",
    "Hello, Amelia, it's Joseph from Arlington. Let’s get started with your consultation.",
    "Emma, I’m Matthew, your Arlington care manager, here to guide you through the process.",
    "Hi Ava, Joshua here from Arlington on a recorded line—what can I do for you today?"
]

# Topic 5: Handling PHI (Personal Health Information)
handling_phi = [
    "Elijah, before we proceed, I must ensure any personal health information shared is necessary and secure.",
    "As we discuss your health information, Mia, please be assured that your privacy is fully protected.",
    "I need to remind you, Elijah, that our conversation about your health information is confidential and secure.",
    "Olivia, it's important that we handle your health information with care; I'll only ask for what's absolutely necessary.",
    "For compliance, Sophia, I'm required to ensure that all personal health information discussed is strictly necessary.",
    "Just to confirm, Liam, any personal health details we discuss are protected under privacy laws.",
    "Elijah, as we talk about your medical information, please be aware that your privacy is our priority.",
    "Before we go into details, Mia, it's crucial that we handle your health information with the utmost care.",
    "While we discuss, Liam, I'll make sure to protect and handle your personal health information appropriately.",
    "Elijah, I'll need to verify some health details with you, ensuring our discussion remains confidential and compliant.",
    "It's important, Elijah, that we keep your health information secure as we discuss your treatment options.",
    "As we proceed, Olivia, I'll handle all your health information securely, adhering to the strictest privacy standards.",
    "Liam, let's ensure that any discussion of your health information today is done with full confidentiality.",
    "I want to assure you, Liam, that your personal health information is treated with the highest standard of privacy.",
    "As your care manager, Amelia, it's my duty to protect any health information you share with me today.",
    "Elijah, we'll discuss sensitive health information, which I assure you will be handled with the highest confidentiality.",
    "For your security, Lucas, I am trained to handle all health information under strict compliance guidelines.",
    "Please be assured, Ava, that our conversation regarding your health will be treated with complete privacy.",
    "Olivia, your health information is secure with us, and I'll only access what is necessary for your care.",
    "As we review your medical information, Sophia, I guarantee full compliance with privacy and health information laws."
]

# Topic 6: TCPA Compliance
tcpa_compliance = [
    "Lucas, just so you know, you have the option to opt-out of future communications at any time.",
    "I'm required to inform you, Liam, that you can request to not receive further calls as per TCPA guidelines.",
    "As part of our compliance with TCPA, James, you can let me know if you prefer not to be contacted again.",
    "Mia, you have the right to stop any future communications, just let me know if that's your choice.",
    "If at any point you wish to cease communications, Emma, you're free to do so under the TCPA regulations.",
    "Under the Telephone Consumer Protection Act, Ava, you can opt out of our calls at your discretion.",
    "Liam, if you decide you no longer wish to receive calls, just inform me, and I'll respect your decision as per TCPA.",
    "For your information, Liam, you can opt out from future communications at any time, complying with the TCPA.",
    "Please let me know, Emma, if you want to stop receiving calls, in line with TCPA requirements.",
    "As per the TCPA, Sophia, it's your right to discontinue communication with us at any point.",
    "Elijah, should you choose to no longer receive our calls, you can opt-out according to TCPA guidelines.",
    "You have control over your communications, Sophia. Let me know if you prefer to opt-out, following TCPA laws.",
    "I'm here to inform you, Olivia, that your preferences for communication can be adjusted under TCPA rules.",
    "Elijah, if at any time you wish to discontinue these conversations, just let me know as allowed by the TCPA.",
    "Under the law, Sophia, you have the option to stop any further communication. Just tell me if you prefer that.",
    "James, you are entitled to decide if you want to continue receiving our calls, adhering to TCPA standards.",
    "If you choose to opt-out of our communications, Elijah, that's completely within your rights under the TCPA.",
    "Just a reminder, Sophia, that you can opt-out of future calls at any stage, as per TCPA regulations.",
    "Sophia, let me know if you want to change your communication preferences in compliance with the TCPA.",
    "As we respect the TCPA, Ava, feel free to inform me if you wish to opt-out of these calls."
]

# Topic 7: Sensitive Information Protocol
sensitive_information_protocol = [
    "Liam, please be aware that any mention of sensitive information like HIV status will be handled with extra confidentiality.",
    "If we discuss sensitive topics such as mental health, Sophia, I assure you it's within a secure environment.",
    "Emma, remember that discussions around sensitive health information are protected under strict privacy laws.",
    "As we proceed, Sophia, please know that any sensitive health data shared will be treated with the utmost discretion.",
    "Amelia, it's important to handle topics like HIV status with extra care, ensuring full compliance with privacy regulations.",
    "During our conversation, Liam, should any sensitive health issues be mentioned, they are fully protected by law.",
    "If sensitive information comes up, Liam, I'm trained to handle it according to the highest standards of privacy.",
    "Elijah, be assured that our discussion of any sensitive health details will remain confidential and secure.",
    "Please feel comfortable, Elijah, discussing any sensitive issues, knowing they are handled with strict confidentiality.",
    "Any mention of sensitive topics, Mia, will be managed with your privacy and security as our top priority.",
    "Sensitive health topics like mental health, Liam, are treated with the highest level of privacy and care.",
    "When discussing sensitive information, Amelia, such as your medical history, we adhere to stringent privacy policies.",
    "Ava, I'm here to ensure that any sensitive health information discussed is protected under our confidentiality protocols.",
    "Should we need to discuss anything sensitive, Amelia, please know it's within a tightly secured and private framework.",
    "Liam, our handling of sensitive topics like HIV status meets all legal protections for your privacy and security.",
    "I want to reassure you, Ava, that any sensitive information shared during this call is safeguarded with great care.",
    "Handling sensitive health data, James, requires utmost discretion, and that's a standard we're committed to.",
    "If our conversation touches on sensitive areas, Olivia, they will be treated with the highest confidentiality standards.",
    "Elijah, we are fully equipped to handle sensitive topics like mental health with the necessary legal and ethical care.",
    "As we address any sensitive information, James, be assured that your privacy is protected by strict regulations."
]

# Topic 8: Medical Consultation/Advice
medical_consultation_advice = [
    "Lucas, I can provide some general medical advice today based on the information you give me.",
    "During our call, Liam, I'll offer consultation on the medical issues you've mentioned.",
    "If you have any health concerns, Ava, feel free to ask, and I can provide appropriate medical advice.",
    "As your care manager, Olivia, part of my role is to give you advice on medical inquiries you may have.",
    "Should you need any guidance, Ava, I'm here to provide medical consultation based on our protocols.",
    "Lucas, let's discuss your current health situation, and I can offer some medical advice accordingly.",
    "If there are medical issues you're concerned about, Lucas, I can consult and provide recommendations.",
    "During this call, Sophia, feel free to discuss any health concerns for which you might need medical advice.",
    "As we talk about your health, Sophia, I'm prepared to give you professional medical consultation.",
    "If you're looking for medical advice, Lucas, I can provide that based on the details you share with me today.",
    "Mia, I can help answer any medical questions you have, offering professional advice as needed.",
    "Let's address any of your medical concerns, Sophia, and I'll provide advice as your care manager.",
    "Mia, based on your symptoms, I can offer some medical advice that might help.",
    "Feel free to ask any medical-related questions, Sophia, and I'll provide the best advice I can.",
    "Olivia, I'm here to consult on any medical issues you mention during our conversation.",
    "If there are specific health topics you need advice on, Emma, I'm here to help with professional guidance.",
    "Throughout our call, Liam, please know that I'm available to provide medical advice as you need it.",
    "Amelia, let's review your health concerns, and I'll provide some advice on managing your condition.",
    "As we discuss, Olivia, I'm ready to offer any medical advice that could assist with your health questions.",
    "Emma, should you need consultation on health matters, I'm equipped to provide that based on our standards."
]

# Topic 9: Care Coordination
care_coordination = [
    "Amelia, let's discuss how we can coordinate your care with other healthcare services to ensure comprehensive management.",
    "I'm here to help organize referrals to other health services as part of our care coordination efforts, Olivia.",
    "Today, we'll review the coordination of your care, including any necessary referrals to specialists, Ava.",
    "As part of coordinating your care, Ava, we'll make sure all your providers are on the same page.",
    "Let's plan your follow-up actions and coordinate with other health providers to optimize your care, Lucas.",
    "Mia, part of our discussion today includes coordinating your ongoing treatment with other healthcare providers.",
    "I will help manage the coordination between different services you're receiving, Lucas, to ensure seamless care.",
    "Let's discuss the effectiveness of our current care coordination and see where improvements can be made, Liam.",
    "Ava, I'll be arranging some referrals and coordinating with other health services to manage your care better.",
    "Today, we need to set up follow-up actions and coordinate them with other health providers you see, Liam.",
    "Olivia, let's review your current care coordination plan and make adjustments as necessary.",
    "We'll need to coordinate with your physical therapist and nutritionist to align on your care, Emma.",
    "I'll follow up on the referrals I made for you and ensure that your care is coordinated effectively, Elijah.",
    "Our focus today is on strengthening the coordination of your various healthcare services, Sophia.",
    "Mia, let's ensure all follow-up actions from today are well-coordinated with your entire health team.",
    "I'm here to oversee the coordination of your care across all services, ensuring you receive integrated support, Olivia.",
    "We'll be discussing how well your care has been coordinated so far and what steps to take next, Sophia.",
    "Olivia, part of our agenda today is to review and enhance the coordination of your healthcare services.",
    "I'll be coordinating with your cardiologist and endocrinologist to streamline your treatment plan, Lucas.",
    "Let's assess the current coordination of your care and determine if additional referrals are needed, Emma."
]

# Topic 10: Log Protocol
log_protocol = [
    "Ava, how would you rate your pain today on a scale from 1 to 10?",
    "Can you describe any changes in your mood since our last discussion, Amelia?",
    "Let's talk about your energy levels, Lucas. Have you felt more tired than usual?",
    "Elijah, how has your sleep been lately? Are you having trouble sleeping?",
    "I'd like to check on your mobility, Liam. Any difficulties moving around or completing daily tasks?",
    "How has your appetite been, Elijah? Any changes or difficulties in eating?",
    "Emma, can we go over how you've been managing your pain?",
    "Let's review your mood variations over the past week, Emma.",
    "Liam, do you feel like your energy levels have been consistent, or are there fluctuations?",
    "Can you update me on the quality of your sleep recently, Lucas?",
    "Elijah, let's discuss any recent issues you've had with mobility or accessing different areas of your home.",
    "Tell me about your eating habits this week, Lucas. Any concerns?",
    "Ava, have you noticed any new or worsening pain since our last call?",
    "Let's talk about any mood changes you've experienced, Mia. Anything significant?",
    "How have your energy levels been impacting your daily activities, Ava?",
    "Elijah, let's review your sleep patterns and discuss any disturbances.",
    "Can you tell me if you've had any mobility challenges lately, Mia?",
    "James, have there been any changes in your appetite or types of food you're eating?",
    "Please share how you've been feeling physically, any pain or discomfort, Elijah?",
    "Olivia, let's update your log to reflect any mood changes since our last meeting."
]

# Topic 11: Treatment Compliance / Medical State
treatment_compliance_medical_state = [
    "Olivia, let's review the medications you're currently taking and discuss any issues with compliance.",
    "Can we go over your treatment plan to ensure you understand all aspects, Sophia?",
    "Sophia, how have you been managing your medical state? Any concerns with your treatments?",
    "Let's ensure you're comfortable with your medication regimen, Mia. Any side effects or difficulties?",
    "Amelia, are you following the treatment plan as prescribed, or are there obstacles we need to address?",
    "We need to check on your overall medical state today, Amelia. How have you felt overall?",
    "Liam, it's important we discuss any compliance issues with your medications. Are you taking them as directed?",
    "Can you update me on how you're feeling with the current treatments, Olivia?",
    "Let's review your treatment schedule, Olivia, and make any necessary adjustments.",
    "Amelia, are there any aspects of your medication that you find difficult to manage?",
    "How are you coping with your medical regimen, Sophia? Let's make sure it's still suitable for you.",
    "Amelia, let's assess the effectiveness of your current treatment and discuss any needed changes.",
    "Are you experiencing any challenges with your medication or treatment plan, Mia?",
    "Let's ensure your treatment is progressing as expected, Emma. Any concerns?",
    "Emma, how consistent have you been with your prescribed treatments and medications?",
    "We need to review how your treatment is impacting your overall health, Amelia.",
    "Emma, let's discuss how well you are managing your health and any issues with your medications.",
    "It's time to check in on your treatment compliance, Ava. Are you finding the regimen manageable?",
    "Lucas, any problems or side effects from your current medications that we need to talk about?",
    "Let's review your medical state and treatment effectiveness today, Emma. I want to ensure you're getting the best care."
]

generated_utterances_by_topic = {
    'member_identification': member_identification,
    'call_recording_disclosure': call_recording_disclosure,
    'participant_verification': participant_verification,
    'cm_introduction': cm_introduction,
    'handling_phi': handling_phi,
    'tcpa_compliance': tcpa_compliance,
    'sensitive_information_protocol': sensitive_information_protocol,
    'medical_consultation_advice': medical_consultation_advice,
    'care_coordination': care_coordination,
    'log_protocol': log_protocol,
    'treatment_compliance_medical_state': treatment_compliance_medical_state
}