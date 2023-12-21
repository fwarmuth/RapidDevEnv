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
git clone https://github.com/fwarmuth/RapidDevEnv.git <ProjectName>
```
## 2. Setup the container generation
```
# Change directory to the repository
cd <ProjectName>
# Install python dependencies for the setup script
pip3 install -r scripts/requirements.txt
# Run the setup script
./scripts/setup_dev_container.py
```
This modifies:
- `devcontainer.json` file to use the project name as the container name
- sets the user within the container to the user running the 
- and more

## 3. Open the folder in VSCode
```
code .
```
Accept the prompt to open the folder in the container.