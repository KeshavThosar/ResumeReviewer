import PyPDF2
import requests
import json

def send_messages_to_chatgpt(messages):
    # API endpoint
    api_endpoint = "https://api.openai.com/v1/chat/completions"

    # Your OpenAI API key
    api_key = "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"
    
    
    # Construct the messages list
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }
    
    # Convert payload to JSON
    json_payload = json.dumps(payload)
    
    # Set headers (don't forget to include your API key)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        # Send POST request to the API
        response = requests.post(api_endpoint, headers=headers, data=json_payload, timeout=10)
        
        # Get the assistant's reply from the API response
        assistant_reply = response.json()["choices"][0]["message"]["content"]

        return assistant_reply
    except requests.exceptions.RequestException as e:
        # Handle any errors
        print(f"Error: {e}")
        return None
    



def process_resume(job_role, job_description, resume_info):
    prompt = f'''
    Job Role: {job_role}

    Job Description: {job_description}

    Resume Information:  {resume_info}

    Please review the resume for the {job_role} role and answer the questions asked

    '''
    # with open('temp.txt', 'w+') as f: f.write(prompt)

    questions_to_api = [    
        'Does the resume meet the requirements? Answer with Yes or No, and provide a reason in under 200 words',
        'Tell me about their work experience in under 100 words',
        'Tell me about their education in under 100 words'
    ]

    answers = []
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.append({"role": "user", "content": prompt + ' ' + questions_to_api[0]})

    response = send_messages_to_chatgpt(messages)
    answers.append(response)

    messages.append({"role": "assistant", "content": response})
    messages.append({"role": "user", "content": ' ' + questions_to_api[1]})

    response = send_messages_to_chatgpt(messages)
    answers.append(response)

    messages.append({"role": "assistant", "content": response})
    messages.append({"role": "user", "content": ' ' + questions_to_api[2]})

    response = send_messages_to_chatgpt(messages)
    answers.append(response)

    tick_untick = '<i class="material-icons">close</i>'
    if answers[0].lower().startswith('yes'): 
        tick_untick = '<i class="material-icons">check</i>'


    questions = [
        'Does the resume meet the requirements? ' + tick_untick,
        'Information about their work experience',
        'Information about their education'
    ]

    return {'questions': questions, 'answers': answers}


def get_text_from_pdf(filepath):
    with open(filepath, 'rb') as pdfFile:
        pdfReader = PyPDF2.PdfReader(pdfFile)
        text = ''
        for page in pdfReader.pages:
            text += ' ' + page.extract_text()
        text = text.replace('\n', ' ')
        return text