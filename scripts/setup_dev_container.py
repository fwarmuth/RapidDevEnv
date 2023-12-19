#!/bin/env python3
import os
import json
import click
import re

@click.command()
@click.argument('name', required=True)
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
                # Remove newlines
                f = re.sub(r'\n', '', f)
                # Remove trailing commas
                f = re.sub(r',\s*}', '}', f)
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
    update_json_values(devcon_file, 'build.args.USER_UID', new_user_uid)
    update_json_values(devcon_file, 'build.args.USER_GID', new_user_gid)

    # Change the project name
    container_name = read_json_value(devcon_file, 'name')
    project_name = f"{container_name}"
    update_json_values(devcon_file, 'build.args.PROJECT_NAME', project_name)

    # Change the hostname of the container
    run_args = read_json_value(devcon_file, 'runArgs')
    # Find the hostname argument and change it
    for arg in run_args:
        if arg.startswith('--hostname'):
            run_args.remove(arg)
            run_args.append(f"--hostname={project_name}@{os.uname().nodename}")
            break
    # Update the runArgs
    devcontainer_data['runArgs'] = run_args

    # Write back to devcontainer.json
    with open(devcon_file, 'w') as f:
        json.dump(devcontainer_data, f, indent=2)

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

    # Rename root folder to the name of the project, needed so that the history path within the dockerfile is correct
    root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    os.rename(root_folder, os.path.join(os.path.dirname(root_folder), name))


def update_json_values(file_path, key, value):
    with open(file_path, 'r') as f:
        devcontainer_data = json.load(f)
    # If key has a dot, split it and update the value
    keys = key.split('.')
    nested_dict = devcontainer_data

    for k in keys[:-1]:
        nested_dict = nested_dict.setdefault(k, {})

    nested_dict[keys[-1]] = value

    with open(file_path, 'w') as f:
        json.dump(devcontainer_data, f, indent=2)

def read_json_value(file_path, key):
    with open(file_path, 'r') as f:
        devcontainer_data = json.load(f)
    return devcontainer_data[key]

if __name__ == "__main__":
    main()
