import os
import requests
import json
from openai import OpenAI

# Your OpenAI API key
api_key = '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'
# This code is for v1 of the openai package: pypi.org/project/openai
client = OpenAI(api_key=api_key)

# The folder containing the files
folder_path = 'output'

# Function to read files in a folder
def read_files_in_folder(folder_path):
    file_contents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # assuming text files
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                file_contents.append(file.read())
    return file_contents

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def summerise(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": message}
        ],
        temperature=0,
        max_tokens=100000 
    )
    return response

prompt_text = read_text_file('summary_prompt.txt')

# Reading files
file_data = read_files_in_folder(folder_path)

# Prepare data for API call (example: sending one file's contents at a time)
for content in file_data:
    data = content
    response = summerise(data)
    details = response.choices[0].message.content
    print(details)  # handle the details as needed