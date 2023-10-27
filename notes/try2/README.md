NOT WORKING OOTB.

Used: `colima start --mount-type 9p`.
Because is `mountType: 9p`, writing file does not work and seems to be affected by what described here: https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#:~:text=on%20Linux%3A%20Inside%20the%20container .

```
vscode ➜ /workspaces/demo20231027-dcmac (main) $ python demo.py 
Traceback (most recent call last):
  File "/workspaces/demo20231027-dcmac/demo.py", line 23, in <module>
    write_datetime_to_file(unique_filename)
  File "/workspaces/demo20231027-dcmac/demo.py", line 16, in write_datetime_to_file
    with open(filename, 'w') as file:
PermissionError: [Errno 13] Permission denied: 'tmp20231027-190139-0.log'
vscode ➜ /workspaces/demo20231027-dcmac (main) $ touch asdf
touch: cannot touch 'asdf': Permission denied
```

To fix the permission issue, 
using a _variation_ from this: https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_change-the-uidgid-of-an-existing-container-user

That is using image as FROM in a Dockerfile and a snippet as:

```
ARG USERNAME=vscode
ARG GROUPNAME=vscode

# Here I use the UID/GID from _my_ computer
ARG USER_UID=501
ARG USER_GID=20

RUN groupmod --gid $USER_GID -o $GROUPNAME \
    && usermod --uid $USER_UID --gid $USER_GID $USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME
```