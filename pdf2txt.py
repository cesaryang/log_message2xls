import re
import pandas as pd

def parse_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    messages = []
    current_message = {}
    message_number_pattern = re.compile(r'%ASA-\d+-(\d{6,7})')

    for line in lines:
        line = line.strip()
        if line.startswith("Error Message"):
            if current_message:
                messages.append(current_message)
                current_message = {}
            message_number_match = message_number_pattern.search(line)
            if message_number_match:
                current_message["Message Number"] = message_number_match.group(1)
            current_message["Error Message"] = line
        elif line.startswith("Explanation"):
            current_message["Explanation"] = line
        elif line.startswith("Recommended Action"):
            current_message["Recommended Action"] = line
        elif current_message and not line.startswith("Error Message") and not line.startswith("Explanation") and not line.startswith("Recommended Action"):
            if "Explanation" in current_message and not current_message["Explanation"].endswith('.'):
                current_message["Explanation"] += ' ' + line
            elif "Recommended Action" in current_message and not current_message["Recommended Action"].endswith('.'):
                current_message["Recommended Action"] += ' ' + line

    if current_message:
        messages.append(current_message)

    return messages

def clean_illegal_characters(text):
    # Replace any illegal characters with an empty string
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

def save_to_excel(messages_list, output_file):
    # Clean illegal characters in each dictionary value
    for message in messages_list:
        for key in message:
            message[key] = clean_illegal_characters(message[key])

    df = pd.DataFrame(messages_list)
    # Ensure the correct order of columns
    df = df[['Message Number', 'Error Message', 'Explanation', 'Recommended Action']]
    df.to_excel(output_file, index=False)

# Input file path
file_path = 'messages.txt'
output_file = 'messages.xlsx'

# Parse file and generate list
messages_list = parse_messages(file_path)

# Save list to Excel file
save_to_excel(messages_list, output_file)

print(f'Processed file saved to {output_file}')
