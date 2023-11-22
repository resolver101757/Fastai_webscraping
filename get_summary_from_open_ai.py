import os
import requests
import json

# Your OpenAI API key
api_key = 'your_api_key_here'

# The folder containing the files
folder_path = 'path_to_your_folder'

# Function to read files in a folder
def read_files_in_folder(folder_path):
    file_contents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # assuming text files
            with open(os.path.join(folder_path, filename), 'r') as file:
                file_contents.append(file.read())
    return file_contents

# Function to make an API call to OpenAI
def call_openai_api(data):
    url = 'https://api.openai.com/v1/engines/gpt-4/completions'  # adjust URL if needed
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Reading files
file_data = read_files_in_folder(folder_path)

# Prepare data for API call (example: sending one file's contents at a time)
for content in file_data:
    data = {
        'prompt': content,  # or format as per your requirement
        'max_tokens': 100  # adjust as needed
    }
    response = call_openai_api(data)
    print(response)  # handle the response as needed