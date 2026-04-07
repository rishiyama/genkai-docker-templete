FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ARG UID=1000
ARG GID=1000
ARG USER_NAME=dev

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential wget curl tzdata \
    ca-certificates libgl1 libglib2.0-0 libcairo2 libcairo2-dev libffi-dev \
    git vim-tiny openssh-client \
    && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} ${USER_NAME} 2>/dev/null || true \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER_NAME} 2>/dev/null || true

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN curl -LsSf https://astral.sh/uv/0.11.2/install.sh | sh \
 && mv /root/.local/bin/uv /usr/local/bin/uv \
 && mv /root/.local/bin/uvx /usr/local/bin/uvx

WORKDIR /workspace

RUN mkdir -p /home/${USER_NAME}/.ssh \
 && chmod 700 /home/${USER_NAME}/.ssh \
 && chown -R ${USER_NAME}:${USER_NAME} /home/${USER_NAME}

RUN printf '\nif [ -S /ssh-agent ]; then\n  export SSH_AUTH_SOCK=/ssh-agent\nfi\n' \
  >> /home/${USER_NAME}/.bashrc

USER ${USER_NAME}

CMD ["bash"]