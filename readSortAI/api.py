import requests
import json
import base64

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        raise

def read_title_page(image_path, api_key):
    # Encode the image
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"} # Headers for API request
    
    increment = 0
    correct_syntax = False
    while not correct_syntax:
        payload = { # API payload
        "model": "gpt-4o-mini-2024-07-18",
        "messages": [
            {
            "role": "system",
            "content": "You are an impersonal machine that takes an image as input, reads it and creates several outputs. Extrapolate from the plain text, what data belongs to what category. If a category can't be filled out, leave it blank, but please make a qualified guess. You know all European languages."
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Extract the text from the image."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
            "name": "math_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "all text in image 1": {"type": "string"},
                        "author": {"type": "string"},
                        "title": {"type": "string"},
                        "subtitle": {"type": "string"},
                        "editor": {"type": "string"},
                        "additional author": {"type": "string"},
                        "honoree": {"type": "string"},
                        "translator": {"type": "string"},
                        "illustrator": {"type": "string"},
                        "version": {"type": "string"},
                        "year": {"type": "string"},
                        "city": {"type": "string"},
                        "publisher": {"type": "string"},
                        "language": {"type": "string"}
                    },
                    "required": ["all text in image 1", "author", "title", 'subtitle', "editor", "additional author", "honoree", "translator", "illustrator", "version", "year", "city", "publisher", "language"],
                    "additionalProperties": False
                    }
                },
                },
                "required": ["steps"],
                "additionalProperties": False
            }
            }
        }
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) # Send request and print response

        try:
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                parsed_result = json.loads(result)
                result = parsed_result["steps"]

                correct_syntax = True
            else:
                print(f"Error: {response.status_code}, {response.text}")
                
                increment += 1
                if increment > 3:
                    correct_syntax = True
                    result = "NoError"
                else:
                    correct_syntax = False
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            continue

    return result

def read_multiple_inputs(image_path, colophone_path, api_key):
    # Encode the image
    base64_image = encode_image(image_path)
    base64_colophone = encode_image(colophone_path)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"} # Headers for API request

    payload = { # API payload
        "model": "gpt-4o-mini-2024-07-18",
        "messages": [
            {
            "role": "system",
            "content": "You are an impersonal machine that takes two images as input, reads them and creates several outputs. Extrapolate from the plain text, what data belongs to what category. If a category be filled out, leave it blank, but please make a qualified guess. You know all European languages."
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Extract the text from the images."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_colophone}"
                }
                }
            ]
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
            "name": "math_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "all text in image 1": {"type": "string"},
                        "all text in image 2": {"type": "string"},
                        "author": {"type": "string"},
                        "additional author": {"type": "string"},
                        "title": {"type": "string"},
                        "subtitle": {"type": "string"},
                        "original title (if translation)": {"type": "string"},
                        "honoree": {"type": "string"},
                        "translator": {"type": "string"},
                        "illustrator": {"type": "string"},
                        "editor": {"type": "string"},
                        "version": {"type": "string"},
                        "year": {"type": "string"},
                        "city": {"type": "string"},
                        "publisher": {"type": "string"},
                        "language": {"type": "string"},
                        "isbn": {"type": "string"},
                    },
                    "required": ["all text in image 1", "all text in image 2", "author", "additional author", "title", "subtitle", "original title (if translation)", "honoree", "translator", "illustrator", "editor", "version", "year", "city", "publisher", "language", "isbn"],
                    "additionalProperties": False
                    }
                },
                },
                "required": ["steps"],
                "additionalProperties": False
            }
            }
        }
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) # Send request and print response
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return
    
    if response.status_code == 200:
        try:
            result = response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error parsing response: The result wasn't where expected: {e}")
            return
        parsed_result = json.loads(result)
        result = parsed_result["steps"]
    
    return result