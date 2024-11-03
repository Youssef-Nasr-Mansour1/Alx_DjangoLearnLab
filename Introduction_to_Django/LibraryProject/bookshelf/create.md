    import os

# Define the file path and the commands to check
file_path = 'LibraryProject/bookshelf/create.md'
commands_to_check = ["Book.objects.create", "title", "author", "George Orwell"]

# Check if the file exists
if os.path.exists(file_path):
    print(f"{file_path} exists.")
    
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Check for each command in the content
    for command in commands_to_check:
        if command in content:
            print(f"'{command}' is present in {file_path}.")
        else:
            print(f"'{command}' is NOT present in {file_path}.")
else:
    print(f"{file_path} does not exist.")
