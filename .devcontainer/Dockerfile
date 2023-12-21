# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04 as base

# Arguments for build
ARG USERNAME=$USERNAME
ARG USER_UID=$USER_UID
ARG USER_GID=$USER_GID

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

# Install oh-my-zsh
USER $USERNAME
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" --unattended
# Set the default shell to zsh
RUN sudo chsh -s $(which zsh) $USERNAME
# Activate oh-my-zsh plugins
RUN sed -i 's/plugins=(git)/plugins=(git per-directory-history z)/g' ~/.zshrc
# Link the per-directory-history plugin to /workspace/$PROJECT_NAME/.devcontainer/persistent/.directory_history
ARG PROJECT_NAME=$PROJECT_NAME
RUN ln -s /workspaces/$PROJECT_NAME/.devcontainer/persistent/.directory_history ~/.directory_history
# Change the default theme
RUN sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="bira"/g' ~/.zshrc
# Install zsh-completions
RUN sh -c "git clone --depth=1 https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions"
RUN sh -c "echo 'autoload -U compinit && compinit' >> ~/.zshrc"
# Install fzf
RUN sh -c ". /etc/environment && git clone --depth=1 https://github.com/junegunn/fzf.git ~/.fzf"
RUN sh -c ". /etc/environment && ~/.fzf/install"

# Setup additional SSH server for x11 forwarding,
# Needs to be started manually, `sudo service ssh start`
USER root
# Install sshd server
RUN apt-get update && sudo apt-get install -y openssh-server
# Set port to 10000 + UID
RUN sed -i "s/#Port 22/Port $((10000 + $USER_UID))/g" /etc/ssh/sshd_config 
# Set user password to user
RUN echo "$USERNAME:$USERNAME" | chpasswd

# Install Python and Pypoetry
USER root
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add poetry to PATH for non-root user
USER $USERNAME
RUN echo 'export PATH="/opt/pypoetry/bin:$PATH"' >> ~/.zshrc

# Remove the non-interactive mode
ARG DEBIAN_FRONTEND=

FROM base as cuda
USER root
# Install CUDA Toolkit stuff
ARG DISTRO=ubuntu2204
ARG ARCH=x86_64
RUN sudo apt-get update && \
    sudo apt-get install -y \
        gnupg \
        wget \
        && \
    sudo rm -rf /var/lib/apt/lists/*
# Install NVIDIA Repo
# https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/$DISTRO/$ARCH/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    && rm cuda-keyring_1.1-1_all.deb
# Set the CUDA version as a build argument with a default value
ARG CUDA_VERSION=12.1
# Install CUDA stuff
RUN apt-get update && \
    apt-get install -y \
    cuda-nvcc-$CUDA_VERSION \
    && rm -rf /var/lib/apt/lists/*