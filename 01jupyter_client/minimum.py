import logging
from jupyter_client.manager import run_kernel

logging.basicConfig(level=logging.DEBUG)

codes = [
    "x = 1 + 1",
    "print('hello', x)",
]

with run_kernel(kernel_name="python") as c:
    for code in codes:
        # https://jupyter-client.readthedocs.io/en/stable/messaging.html?highlight=idle#kernel-status
        # state = busy, idle, starting
        state = "busy"

        msg_id = c.execute(code)
        while state != "idle" and c.is_alive():
            msg = c.get_iopub_msg(timeout=1)
            content = msg.get('content')
            if content is None:
                continue

            if 'execution_state' in content:
                state = content['execution_state']
            print(f"{state}> content: {content}")
