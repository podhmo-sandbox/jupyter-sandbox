## zmqを使っている部分を調べてみる

```
$ TARGETDIR=~/venvs/viz
$ mkdir -p data
$ (cd $TARGETDIR && find . -name "*.py" | grep -v lib/ | xargs grep zmq -l 2>/dev/null) | sort > data/zmq.files
```

[./data/zmq.files](./data/zmq.files)

jupyter-consoleのあたりを見ると良いかもしれない。jupyter_consoleのrepository。

:warning: その前にjupyter系のアプリのmainの書き方を把握しないとダメそう。

特に重要なものはなさそう？

```console
grep "^class ZMQ"  -r ../../jupyter_console/
../../jupyter_console/jupyter_console/tests/test_image_handler.py:class ZMQTerminalInteractiveShellTestCase(unittest.TestCase):
../../jupyter_console/jupyter_console/zmqhistory.py:class ZMQHistoryManager(HistoryAccessorBase):
../../jupyter_console/jupyter_console/ptshell.py:class ZMQTerminalInteractiveShell(SingletonConfigurable):
../../jupyter_console/jupyter_console/app.py:class ZMQTerminalIPythonApp(JupyterApp, JupyterConsoleApp):
../../jupyter_console/jupyter_console/completer.py:class ZMQCompleter(Configurable):
```

どうも色々adapterを書かないといけない模様？色々なクラスの構造は[structure.md](./structure.md)に。

## jupyter appのmainの書き方

[memo](../docs/jupyter-app.md)

main部分は以下 `main = ZMQTerminalIPythonApp.launch_instance`

- 生成 -> instance()
- 初期化 -> initialize()
- 開始 -> start()

initializeとstartがオーバーライドされている。startだけ見れば良さそう。

```python
    def start(self):
        # JupyterApp.start dispatches on NoStart
        super(ZMQTerminalIPythonApp, self).start()
        self.log.debug("Starting the jupyter console mainloop...")
        self.shell.mainloop()
```

shellのmainloop()を見て行けば良い感じっぽい。shellって何？mainloopなのでeventloop的なもの？（それともrunloop)

```python
    def init_shell(self):
        JupyterConsoleApp.initialize(self)
        # relay sigint to kernel
        signal.signal(signal.SIGINT, self.handle_sigint)
        self.shell = ZMQTerminalInteractiveShell.instance(parent=self,
                        manager=self.kernel_manager,
                        client=self.kernel_client,
        )
        self.shell.own_kernel = not self.existing
```

特にasyncioやtornadoのeventloopというわけではなさそう。

```
jupyter_console.ptshell.ZMQTerminalInteractiveShell <- traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
```

直接自分自身で定義しているメソッドのよう。repl的なもの。

```python
class ZMQTerminalInteractiveShell(SingletonConfigurable):

    def mainloop(self):
        self.keepkernel = not self.own_kernel
        # An extra layer of protection in case someone mashing Ctrl-C breaks
        # out of our internal code.
        while True:
            try:
                self.interact()
                break
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt escaped interact()\n")
```

まだzeromqが出てこない。

```console
$ jupyter-console --debug
[ZMQTerminalIPythonApp] Searching ['VENV/jupyter-sandbox/00zmq', '$HOME/.jupyter', 'VENV/etc/jupyter', '/usr/local/etc/jupyter', '/etc/jupyter'] for config files
[ZMQTerminalIPythonApp] Looking for jupyter_config in /etc/jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_config in /usr/local/etc/jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_config in VENV/etc/jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_config in $HOME/.jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_config in VENV/jupyter-sandbox/00zmq
[ZMQTerminalIPythonApp] Looking for jupyter_console_config in /etc/jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_console_config in /usr/local/etc/jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_console_config in VENV/etc/jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_console_config in $HOME/.jupyter
[ZMQTerminalIPythonApp] Looking for jupyter_console_config in VENV/jupyter-sandbox/00zmq
[ZMQTerminalIPythonApp] Connection File not found: /run/user/1000/jupyter/kernel-17249.json
[ZMQTerminalIPythonApp] Starting kernel: ['VENV/bin/python', '-m', 'ipykernel_launcher', '-f', '/run/user/1000/jupyter/kernel-17249.json']
[ZMQTerminalIPythonApp] Connecting to: tcp://127.0.0.1:38591
[ZMQTerminalIPythonApp] connecting shell channel to tcp://127.0.0.1:47871
[ZMQTerminalIPythonApp] Connecting to: tcp://127.0.0.1:47871
[ZMQTerminalIPythonApp] connecting iopub channel to tcp://127.0.0.1:39353
[ZMQTerminalIPythonApp] Connecting to: tcp://127.0.0.1:39353
[ZMQTerminalIPythonApp] connecting stdin channel to tcp://127.0.0.1:41619
[ZMQTerminalIPythonApp] Connecting to: tcp://127.0.0.1:41619
[ZMQTerminalIPythonApp] connecting heartbeat channel to tcp://127.0.0.1:56095
Jupyter console 5.2.0

Python 3.6.4 (default, Jan  5 2018, 02:35:40) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.4.0 -- An enhanced Interactive Python. Type '?' for help.

[ZMQTerminalIPythonApp] Starting the jupyter console mainloop...
```

普通にstarting kernelの部分でipykernel_launcherを呼んでるな。そしてConnecting toで何らかのnetworkに接続していそう。

```
[ZMQTerminalIPythonApp] Connection File not found: /run/user/1000/jupyter/kernel-17249.json
[ZMQTerminalIPythonApp] Starting kernel: ['VENV/bin/python', '-m', 'ipykernel_launcher', '-f', '/run/user/1000/jupyter/kernel-17249.json']
[ZMQTerminalIPythonApp] Connecting to: tcp://127.0.0.1:38591
```

- connection fileが/runに作られるみたい

  - reuseの仕方はどうすれば良いんだろ？


```console
$ pyinspect list | grep jupyter | pyinspect resolve | grep -v "\.py" | xargs grep -r 'Starting kernel:'
VENV/lib/python3.6/site-packages/jupyter_client/manager.py:        self.log.debug("Starting kernel: %s", kernel_cmd)
```

jupyter_clientでkernelは立ち上がる。

ptshell.py

```python
class ZMQTerminalInteractiveShell(SingletonConfigurable):
# ...
    manager = Instance('jupyter_client.KernelManager', allow_none=True)
    client = Instance('jupyter_client.KernelClient', allow_none=True)
```

このmanagerやclientがどう使われるかということを把握しないとダメそう。Instanceというのはただの型の指定でしかなさそう。なるほど。traitletsの使いかたを把握しておくと良い([雑なgist](https://gist.github.com/podhmo/6c1c37b0b13fa8a2750aa6d399c3088d))

app.py

```python
class ZMQTerminalIPythonApp(JupyterApp, JupyterConsoleApp):
# ...
    def init_shell(self):
        JupyterConsoleApp.initialize(self)
        # relay sigint to kernel
        signal.signal(signal.SIGINT, self.handle_sigint)
        self.shell = ZMQTerminalInteractiveShell.instance(parent=self,
                        manager=self.kernel_manager,
                        client=self.kernel_client,
        )
        self.shell.own_kernel = not self.existing
```

kernel_managerはjupyter_clientの方で設定される模様？ (下記の `init_kernel_manager`)

```
jupyter_client.consoleapp.JupyterConsoleApp <- jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _connection_file_default(self)
    [method] _new_connection_file(self)
    [method] build_kernel_argv(self, argv=None)
    [method] initialize(self, argv=None)
        [method] init_connection_file(self)
        [method] init_ssh(self)
        [method] init_kernel_manager(self)
        [method] init_kernel_client(self)
```

`kernel_manager_class`が色々やっている。普通に初期値が使われているっぽい。

```
class JupyterConsoleApp(ConnectionFileMixin):
#...
    kernel_manager_class = KernelManager
    kernel_client_class = BlockingKernelClient
```

実際のところ、KernelManagerクラスのstart_kernelで件のメッセージが出力されている模様。

```python
class KernelManager(ConnectionFileMixin):
#...
    def start_kernel(self, **kw):
#...

        # launch the kernel subprocess
        self.log.debug("Starting kernel: %s", kernel_cmd)
        self.kernel = self._launch_kernel(kernel_cmd, env=env,
                                    **kw)
        self.start_restarter()
        self._connect_control_socket()
```

start_kernelは。。 ConsoleAppの `init_kernel_manager()` あたりで呼ばれていそう（ちなみに、kernelappのstart()で呼ばれる）。

```python

#...

    def init_kernel_manager(self):
#...
        kwargs = {}
        if self.kernel_manager.ipykernel:
            kwargs['extra_arguments'] = self.kernel_argv
        self.kernel_manager.start_kernel(**kwargs)
        atexit.register(self.kernel_manager.cleanup_ipc_files)
```

KernelAppとConsoleAppの使い分けがよくわからない感じかも。

ちなみに、init_kernel_manager自体は、 ZMQTerminalIPythonAppが継承しているJupyterConsoleAppのinitializeで呼ばれているみたい。

```

jupyter_client.consoleapp.JupyterConsoleApp <- jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _connection_file_default(self)
    [method] _new_connection_file(self)
    [method] build_kernel_argv(self, argv=None)
    [method] initialize(self, argv=None)
        [method] init_connection_file(self)
        [method] init_ssh(self)
        [method] init_kernel_manager(self)
        [method] init_kernel_client(self)
```

