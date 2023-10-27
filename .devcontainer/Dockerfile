FROM mcr.microsoft.com/devcontainers/python:1-3.10-bullseye

# Here I use the USER from the FROM image
ARG USERNAME=vscode
ARG GROUPNAME=vscode

# Here I use the UID/GID from _my_ computer
ARG USER_UID=501
ARG USER_GID=20

RUN groupmod --gid $USER_GID -o $GROUPNAME \
    && usermod --uid $USER_UID --gid $USER_GID $USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME