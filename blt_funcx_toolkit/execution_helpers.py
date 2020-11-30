from config import blt_endpoints


def run_function_wait_result(py_fn, py_fn_args, py_fn_kwargs={}, endpoint_name="blt_small"):
    func_uuid = fxc.register_function(py_fn)
    res = fxc.run(*py_fn_args,
                  **py_fn_kwargs,
                  endpoint_id=blt_endpoints[endpoint_name].uuid,
                  function_id=func_uuid)
    while True:
        try:
            print("Waiting for results...")
            time.sleep(5)
            return fxc.get_result(res)
            break
        except Exception as e:
            if "waiting-for-ep" in str(e):
                continue
            elif "waiting-for-nodes" in str(e):
                continue
            else:
                raise e


def run_function_async(py_fn, py_fn_args, endpoint_name="blt_small"):
    # Use return value for Funcx polling
    func_uuid = fxc.register_function(py_fn)
    res = fxc.run(*py_fn_args,
                  endpoint_id=blt_endpoints[endpoint_name].uuid,
                  function_id=func_uuid)
    return res


def run_console_cmd(command, endpoint_name="blt_small", wait=True):
    def funcx_command_fn(cmd):
        import subprocess
        return subprocess.check_output(cmd, shell=True)

    if wait:
        return run_function_wait_result(funcx_command_fn, [cmd],
                                        endpoint_name=endpoint_name)
    else:
        return run_function_async(funcx_command_fn, [cmd],
                                  endpoint_name=endpoint_name)
