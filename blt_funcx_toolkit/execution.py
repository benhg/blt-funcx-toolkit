from funcx.sdk.client import FuncXClient
import os
import subprocess
import time

from config import blt_endpoints, SLEEP_TIME


def run_function_wait_result(py_fn,
                             py_fn_args,
                             py_fn_kwargs={},
                             endpoint_name="blt_small",
                             print_status=True):
    """
    Run a function with funcx, wait for execution,
        and return results when they are available
    """
    fxc = FuncXClient()
    func_uuid = fxc.register_function(py_fn)
    res = fxc.run(*py_fn_args,
                  **py_fn_kwargs,
                  endpoint_id=blt_endpoints[endpoint_name].uuid,
                  function_id=func_uuid)
    while True:
        try:
            if print_status:
                print("Waiting for results...")
            time.sleep(SLEEP_TIME)
            return str(fxc.get_result(res), encoding="utf-8")
            break
        except Exception as e:
            if "waiting-for-" in str(e):
                continue
            else:
                raise e


def run_function_async(py_fn, py_fn_args, endpoint_name="blt_small"):
    # Use return value for Funcx polling
    fxc = FuncXClient()
    func_uuid = fxc.register_function(py_fn)
    res = fxc.run(*py_fn_args,
                  endpoint_id=blt_endpoints[endpoint_name].uuid,
                  function_id=func_uuid)
    return res


def funcx_command_fn(cmd):
    import subprocess
    return subprocess.check_output(cmd, shell=True)


def run_console_cmd(command, endpoint_name="blt_small", wait=True):
    if wait:
        return run_function_wait_result(funcx_command_fn, [command],
                                        endpoint_name=endpoint_name)
    else:
        return run_function_async(funcx_command_fn, [command],
                                  endpoint_name=endpoint_name)


def install_python_package(package_name):
    return run_console_cmd(
        f"sudo /local/cluster/bin/pip3 install {package_name}")


def fxsh(endpoint_name="blt_small"):
    ps1 = f"fxsh[{endpoint_name}]$ "
    cwd = "~"
    try:
        cmd = input(ps1)
        while cmd.lower() != "exit":
            
                if cmd.startswith("cd "):
                    cwd = cmd.split("cd ")[1].strip()
                    cmd = input(ps1)
                    continue

                print(run_console_cmd(f"cd {cwd} ; {cmd}", endpoint_name=endpoint_name))
                cmd = input(ps1)
    except KeyboardInterrupt:
        # Make ctrl-c look like an `exit`
        print(ps1 + "exit")
        break

if __name__ == '__main__':
    fxsh()
