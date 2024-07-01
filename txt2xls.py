import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    # 打开 PDF 文件
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def is_numeric_or_punctuation(line):
    # 使用正则表达式检查行是否只包含数字和标点符号
    return re.match(r'^[\d\W]+$', line) is not None

def should_delete_line(line):
    # 检查行是否包含 "Cisco Secure Firewall ASA Series Syslog Messages"
    if "Cisco Secure Firewall ASA Series Syslog Messages" in line or line.startswith("Syslog Messages"):
        return True
    # 检查行是否只包含数字和标点符号
    if is_numeric_or_punctuation(line.strip()):
        return True
    # 检查行是否为空行
    if not line.strip():
        return True
    return False

def should_merge_with_previous_line(line):
    # 检查行是否以 "Error Message", "Explanation", "Recommended Action" 开头
    return re.match(r'^(Error Message|Explanation|Recommended Action)', line) is not None

def process_text(text):
    lines = text.split('\n')
    processed_lines = []
    previous_line = None

    for line in lines:
        if should_delete_line(line):
            continue

        if previous_line is not None:
            if should_merge_with_previous_line(previous_line):
                if not should_merge_with_previous_line(line) and not line.strip() == "":
                    # 将当前行拼接到上一行行尾
                    previous_line = previous_line.rstrip() + ' ' + line.lstrip()
                    continue
            processed_lines.append(previous_line)
        previous_line = line

    # 写入最后一行
    if previous_line is not None and not should_delete_line(previous_line):
        processed_lines.append(previous_line)

    return '\n'.join(processed_lines)

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(text)

# 输入文件和输出文件路径
pdf_path = 'message_log.pdf'
output_file = 'messages.txt'

# 提取 PDF 文本
text = extract_text_from_pdf(pdf_path)

# 处理文本
processed_text = process_text(text)

# 保存处理后的文本到文件
save_text_to_file(processed_text, output_file)

print(f'Processed file saved to {output_file}')


