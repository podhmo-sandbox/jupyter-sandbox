channelが必要とするinterface

```console
$ pyinspect inspect jupyter_client.channelsabc:HBChannelABC
jupyter_client.channelsabc.HBChannelABC <- jupyter_client.channelsabc.ChannelABC <- abc._NewBase <- builtins.object
    [method] is_beating(self)
    [method] pause(self)
    [property] time_to_dead
    [method] unpause(self)

jupyter_client.channelsabc.ChannelABC <- abc._NewBase <- builtins.object
    [method] is_alive(self)
    [method] start(self)
    [method] stop(self)

abc._NewBase <- builtins.object
```

実装(is_alive,start,stopがあれば良い。いや、それだと通信できなくない？)

```console
$ pyinspect inspect jupyter_client.blocking.channels:ZMQSocketChannel
jupyter_client.blocking.channels.ZMQSocketChannel <- builtins.object
    [method, OVERRIDE] __init__(self, socket, session, loop=None)
    [method] close(self)
    [method] get_msgs(self)
        [method] get_msg(self, block=True, timeout=None)
            [method] _recv(self, **kwargs)
    [method] is_alive(self)
    [method] msg_ready(self)
    [method] send(self, msg)
    [method] start(self)
    [method] stop(self)
```
