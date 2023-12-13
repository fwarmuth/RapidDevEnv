#!/bin/sh
# This scripts sets up the devcontainer.json
# Get the path of the script
SCRIPT_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Delete the .git folder if it exists
if [ -d "$SCRIPT_PATH/../.git" ]; then
    #    rm -rf "$SCRIPT_PATH/../.git"
    echo "Deleted .git folder"
else
    echo "No .git folder found"
fi

# Get the path of the devcontainer.json
DEVCON_FILE="$SCRIPT_PATH/../.devcontainer/devcontainer.json"

# If argument is passed, then use it as the name of the container
if [ $# -eq 1 ]; then
    # Use sed to replace the values
    sed -i "s/\"name\": \".*\"/\"name\": \"$1\"/" "$DEVCON_FILE"
    echo "Changed container name to $1"
else
    echo "No container name passed, not changing container name."
fi

# Set the values for USER_UID and USER_GID
# New values for USER_UID and USER_GID
new_user_uid="$(id -u)"
new_user_gid="$(id -g)"
# Use sed to replace the values
sed -i "s/\"USER_UID\": \".*\"/\"USER_UID\": \"$new_user_uid\"/" "$DEVCON_FILE"
sed -i "s/\"USER_GID\": \".*\"/\"USER_GID\": \"$new_user_gid\"/" "$DEVCON_FILE"

# Change --hostname to the hostname of the machine
# Read the container name from the devcontainer.json
container_name="$(cat $DEVCON_FILE | sed 's/^ *\/\/.*//' | jq -r '.name')"
# Get the hostname
hostname="$container_name@$(hostname)"
# Use sed to replace the values
sed -i "s/\"--hostname=.*\"/\"--hostname=$hostname\"/" "$DEVCON_FILE"
