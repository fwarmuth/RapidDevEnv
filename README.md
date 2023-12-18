# RapidDevEnv
Out-of-the-Box Configuration: Instantly deploy a development environment with a pre-configured set of tools, libraries, and dependencies commonly used by me.
## Features
- `sudo` access within the container
- `zsh`, as the default shell
- `oh-my-zsh`, plugins: `git`
- `git`
- `neovim`
- `fd-find`
- `ripgrep`


# Usage
## 1. Clone the repository
```bash
git clone
```
## 2. Setup the container generation
```
# Change directory to the repository
cd RapidDevEnv
# Install python dependencies
pip3 install -r scripts/requirements.txt
# Run the setup script
./scripts/setup_dev_container.py <ProjectName>
```
This modifies the `devcontainer.json` file to use the project name as the container name and sets the user within the container to the current user 
## 3. Open the folder in VSCode
```
code .
```
Accept the prompt to open the folder in the container.