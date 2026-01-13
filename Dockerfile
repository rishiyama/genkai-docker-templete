# Base image with CUDA 11.8 and Ubuntu 20.04
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Build args
ARG UID=1000
ARG GID=1000
ARG USER_NAME=dev

# Avoid tz prompt
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential wget curl tzdata \
    ca-certificates libgl1-mesa-glx libcairo2 libcairo2-dev libffi-dev \
    git vim-tiny openssh-client \
    && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Create user/group (name is USER_NAME, id is UID/GID)
RUN groupadd -g ${GID} ${USER_NAME} 2>/dev/null || true \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER_NAME} 2>/dev/null || true

# Install uv, then place it globally
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh \
 && mv /root/.local/bin/uv /usr/local/bin/uv \
 && mv /root/.local/bin/uvx /usr/local/bin/uvx

WORKDIR /workspace

# Prepare SSH dir for the user
RUN mkdir -p /home/${USER_NAME}/.ssh \
 && chmod 700 /home/${USER_NAME}/.ssh \
 && chown -R ${USER_NAME}:${USER_NAME} /home/${USER_NAME}/.ssh

# Prefer compose-mounted ssh-agent socket if present (fix for VS Code overriding SSH_AUTH_SOCK)
RUN printf '\nif [ -S /ssh-agent ]; then\n  export SSH_AUTH_SOCK=/ssh-agent\nfi\n' >> /home/${USER_NAME}/.bashrc

# Switch to non-root user
USER ${USER_NAME}


CMD ["bash"]
