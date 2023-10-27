NOT WORKING OOTB.

Used: `colima start --vz-rosetta --vm-type vz --arch x86_64 --cpu 4 --memory 8`.
Because is `mountType: virtiofs`, writing file (againg) does not work and seems to be affected by what described here: https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#:~:text=on%20Linux%3A%20Inside%20the%20container .

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