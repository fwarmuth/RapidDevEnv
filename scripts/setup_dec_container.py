#!/bin/env python3
import os
import json
import click
import re

@click.command()
@click.option('--name', '-n', help='Specify the name of the container')
def main(name):
    # Get the path of the script
    script_path = os.path.realpath(__file__)

    # Get the path of the devcontainer.json
    devcon_file = os.path.join(os.path.dirname(os.path.dirname(script_path)), '.devcontainer', 'devcontainer.json')

    if name:
        try:
            # Read devcontainer.json
            with open(devcon_file, 'r') as f:
                # Remove Comments
                f = re.sub(r'//.*', '', f.read())
                devcontainer_data = json.loads(f) 
            # Change container name
            devcontainer_data['name'] = name
            # Write back to devcontainer.json
            with open(devcon_file, 'w') as f:
                json.dump(devcontainer_data, f, indent=2)
            click.echo(f"Changed container name to {name}")
        except FileNotFoundError:
            click.echo("devcontainer.json not found, not changing container name.")
            exit(1)
    else:
        click.echo("No container name passed, not changing container name.")

    # Set the values for USER_UID and USER_GID
    new_user_uid = str(os.getuid())
    new_user_gid = str(os.getgid())
    update_json_values(devcon_file, 'USER_UID', new_user_uid)
    update_json_values(devcon_file, 'USER_GID', new_user_gid)

    # Change --hostname to the hostname of the machine
    container_name = read_json_value(devcon_file, 'name')
    project_name = f"{container_name}@{os.uname().nodename}"
    update_json_values(devcon_file, 'PROJECT_NAME', project_name)

    # Ask the user if .git folder should be deleted
    reply = click.prompt("Do you want to delete the .git folder? (y/n)", default='n')
    if reply.lower() == 'y':
        git_folder_path = os.path.join(os.path.dirname(script_path), '..', '.git')
        if os.path.exists(git_folder_path):
            # You can uncomment the following line to delete the .git folder
            # shutil.rmtree(git_folder_path)
            click.echo("Deleted .git folder")
        else:
            click.echo("No .git folder found")

def update_json_values(file_path, key, value):
    with open(file_path, 'r') as f:
        devcontainer_data = json.load(f)
    devcontainer_data[key] = value
    with open(file_path, 'w') as f:
        json.dump(devcontainer_data, f, indent=2)

def read_json_value(file_path, key):
    with open(file_path, 'r') as f:
        devcontainer_data = json.load(f)
    return devcontainer_data[key]

if __name__ == "__main__":
    main()
