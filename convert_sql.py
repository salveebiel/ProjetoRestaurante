with open('mysql_dump.sql', 'r') as f:
    content = f.read()

# Replace double quotes with backticks
content = content.replace('"', '`')

# Replace AUTOINCREMENT with AUTO_INCREMENT
content = content.replace('AUTOINCREMENT', 'AUTO_INCREMENT')

# Remove lines containing sqlite_sequence
lines = content.split('\n')
lines = [line for line in lines if 'sqlite_sequence' not in line]

# Remove COMMIT; if present
lines = [line for line in lines if line.strip() != 'COMMIT;']

content = '\n'.join(lines)

with open('mysql_dump.sql', 'w') as f:
    f.write(content)
