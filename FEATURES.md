# Features List By Version

## 0.1.0

### Functions

#### Transfer

- `upload_file_to_blt` (does what it says on the tin)
- `download_file_from_blt`

Plus two backends for those functions:

- `ftp_{upload|download}_file_{to|from}_blt` FTP backend (for people with VPN connections)

- `croc_{upload|download}_file_{to|from}_blt` Croc backend (for people with no VPN connections)

#### Execution

- `run_function_wait_result` Run a python function on BLT, wait for the result

- `run_function_async` Asynchronously run a python function on BLT, return an object you can ask for the result

- `run_console_cmd` Run a console command on BLT

- `install_python_package` Install a python package on BLT. Should be used only by powerusers

- `fxsh` - driver function for `fxsh` script

### Scripts

- `blt_transfer` script for uploading and downloading files

- `fxsh` virtual terminal using FuncX as a backend.

### Other

- Dev docs in docstrings for functions
- Examples in `scripts` directory

## 0.12.0

### Functions

#### Transfer

#### Execution

### Scripts

### Other

- Logging system
- User docs