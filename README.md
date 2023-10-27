# DevContainer and Mac OSX mount permissions

I have the need to develop using a particular version of CPython and ABI/platform for architecture `x86_64` but I'm on Apple Silicon M2 (`arm64`) (SEO: aarch64 ARM).
I found [DevContainer](https://containers.dev/) could be helpful but I experienced some issues as detailed in [this article](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#:~:text=Inside%20the%20container%2C%20any%20mounted%20files/folders%20will%20have%20the%20exact%20same%20permissions%20as%20outside%20the%20container%20%2D%20including%20the%20owner%20user%20ID%20(UID)%20and%20group%20ID%20(GID).).
I am NOT using _Docker for Mac_, I'm specifically using `colima version 0.5.6` as it was the first suggesion on [this page](https://code.visualstudio.com/remote/advancedcontainers/docker-options), but the concepts can be helpful in general for [mount permission issues](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_change-the-uidgid-of-an-existing-container-user).

i.e.:
Take the DevContainter `image`, use it as the `FROM` in a Dockerfile, and apply snippet at the end similar to:
```docker
# Here I use the USER from the FROM image
ARG USERNAME=vscode
ARG GROUPNAME=vscode

# Here I use the UID/GID from _my_ computer
ARG USER_UID=nnn
ARG USER_GID=nn

RUN groupmod --gid $USER_GID -o $GROUPNAME \
    && usermod --uid $USER_UID --gid $USER_GID $USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME
``` 

I am wondering if this is the _expected_ way to use DevContainer on a Mac when not using Docker for Mac, or I hope these notes could be helpful if someone lands here :)

In the end it seems to me any DevContainer mount permission issues I encounterd, boils down to the `mountType` (virtiofs, 9p, sshfs) used by Colima depending if using qemu or vz Rosetta.

You can follow along notes of the tests also in the git history of this repo.

## mountType: sshfs - works out of the box

Used: `colima start`.

Because by default is `mountType: sshfs`, writing file seems to be working just fine.

## mountType: 9p - does NOT work ootb

Used: `colima start --mount-type 9p`.
Because is `mountType: 9p`, writing file does not work and seems to be affected by what described [here](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#:~:text=on%20Linux%3A%20Inside%20the%20container).

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

```docker
ARG USERNAME=vscode
ARG GROUPNAME=vscode

# Here I use the UID/GID from _my_ computer
ARG USER_UID=nnn
ARG USER_GID=nn

RUN groupmod --gid $USER_GID -o $GROUPNAME \
    && usermod --uid $USER_UID --gid $USER_GID $USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME
```

I have added `-o` to `groupmod` as the gid might be already present from the inherited Docker images.

## mountType: virtiofs - does NOT work ootb

Used: `colima start --vz-rosetta --vm-type vz --arch x86_64 --cpu 4 --memory 8`.
Because is `mountType: virtiofs`, writing file (againg) does not work and seems to be affected by what described [here](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#:~:text=on%20Linux%3A%20Inside%20the%20container).

```
vscode ➜ /workspaces/demo20231027-dcmac (main) $ python demo.py 
Traceback (most recent call last):
  File "/workspaces/demo20231027-dcmac/demo.py", line 23, in <module>
    write_datetime_to_file(unique_filename)
  File "/workspaces/demo20231027-dcmac/demo.py", line 16, in write_datetime_to_file
    with open(filename, 'w') as file:
PermissionError: [Errno 13] Permission denied: 'tmp20231027-194539-0.log'
vscode ➜ /workspaces/demo20231027-dcmac (main) $ touch asdf
touch: cannot touch 'asdf': Permission denied
```

So again to fix the permission issue,
applying the variation of the Dockerfile snippet.

```
vscode ➜ /workspaces/demo20231027-dcmac (main) $ python demo.py 
File 'tmp20231027-195156-0.log' has been created.
```

This is what I need.
The DevContainer is connecting into a `x86_64`.
I can use the CPython and the ABI/Platform I need.
I can write to file in the workspace/repository.

## What did _not_ work

Tried with using in `devcontainer.json`:
```json
"runArgs": ["--user=uid:gid"]
```

but did not help.

## Other resources I found helpful

- https://github.com/microsoft/vscode-remote-release/issues/7284#issuecomment-1738617318
- https://stackoverflow.com/a/77105985/893991
