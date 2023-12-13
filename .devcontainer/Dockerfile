# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Arguments for build
ARG USERNAME=$USERNAME
ARG USER_UID=$USER_UID
ARG USER_GID=$USER_GID

# Print build arguments
RUN echo "USERNAME: $USERNAME"
RUN echo "USER_UID: $USER_UID"
RUN echo "USER_GID: $USER_GID"

# Set non-interactive mode during build
ARG DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
        sudo \
        curl \
        git \
        zsh \
        fd-find \
        ripgrep \
        neovim \
        && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set the non-root user as the default user
USER $USERNAME

# Install oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" --unattended
# Set the default shell to zsh
RUN sudo chsh -s $(which zsh) $USERNAME
# Activate oh-my-zsh plugins
RUN sed -i 's/plugins=(git)/plugins=(git per-directory-history z)/g' ~/.zshrc
# Link the per-directory-history plugin to /workspace/RapidDevEnv/.devcontainer/persistent/.directiory_history
RUN ln -s /workspaces/RapidDevEnv/.devcontainer/persistent/.directory_history ~/.directory_history
# Change the default theme
RUN sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="bira"/g' ~/.zshrc
# Install zsh-completions
RUN sh -c "git clone --depth=1 https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions"
RUN sh -c "echo 'autoload -U compinit && compinit' >> ~/.zshrc"
# Install fzf
RUN sh -c ". /etc/environment && git clone --depth=1 https://github.com/junegunn/fzf.git ~/.fzf"
RUN sh -c ". /etc/environment && ~/.fzf/install"

