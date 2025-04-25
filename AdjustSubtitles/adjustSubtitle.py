import sys
import re
from datetime import datetime, timedelta
import os

def adjust_time(timestamp, adjsec):
    current_time = datetime.strptime(timestamp, "%H:%M:%S,%f")
    new_time = current_time + timedelta(seconds=adjsec)
    if new_time < datetime.strptime("00:00:00,000", "%H:%M:%S,%f"):
        new_time = datetime.strptime("00:00:00,000", "%H:%M:%S,%f")
    return new_time.strftime("%H:%M:%S,%f")[:-3]

def adj_file(file_path, adjsec):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"File read succesfully (UTF-8)")
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='iso-8859-1') as f:
            lines = f.readlines()
        print(f"File read succesfully (ISO-8859-1)")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    print(f"Total lines in .srt file: {len(lines)}")

    regex_time = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s-->\s(\d{2}:\d{2}:\d{2},\d{3})")
    adj_lines = []

    for line in lines:
        match = regex_time.match(line)
        if match:
            adj_start = adjust_time(match.group(1), adjsec)
            adj_end = adjust_time(match.group(2), adjsec)
            new_line = f"{adj_start} --> {adj_end}\n"
            adj_lines.append(new_line)
        else:
            adj_lines.append(line)

    file_name, extension = os.path.splitext(file_path)
    new_path = f"{file_name}_adj{extension}"

    print(f"Adjusted .srt file saved in: {new_path}")

    try:
        with open(new_path, 'w', encoding='utf-8') as f:
            f.writelines(adj_lines)
        print("File created successfully!")
    except Exception as e:
        print(f"Error to create file: {e}")

adj_file('FileName.srt', 12) #filename, seconds (-/+)

