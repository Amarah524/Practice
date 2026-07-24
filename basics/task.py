import re
with open('log.txt', 'r') as f:
    log = f.read()
    content = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', log)
    print(set(content))
with open('output.txt', 'w') as f:
    for email in set(content):
        f.write(email + '\n')