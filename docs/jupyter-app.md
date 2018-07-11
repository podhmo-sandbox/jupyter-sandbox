## jupyter関係のコマンドの実装の仕方

概ね以下のような感じ

- mainはJupyterAppかJupyterConsoleAppのlaunch_instance
  - 実際にはtraitlets.config.application.Applicationの意味を知らないとだめ
  - [Configurable objects with traitlets.config — traitlets 4.3.2 documentation](https://traitlets.readthedocs.io/en/stable/config.html "Configurable objects with traitlets.config — traitlets 4.3.2 documentation")
  - App系のものはたいていSingletonConfigurableが付いている
- オプションなどの設定はtraitlets経由でやる

```python
from traitlets import (
    Dict, Any
)
from jupyter_core.application import JupyterApp
from jupyter_client.consoleapp import JupyterConsoleApp

class MyTerminalIPythonApp(JupyterApp, JupyterConsoleApp):
    name = "jupyter-console"
    version = __version__
    """Start a terminal frontend to the IPython my kernel."""
    description = "...."

    examples = _examples

    classes = [MyTerminalInteractiveShell] + JupyterConsoleApp.classes
    flags = Dict(flags)
    aliases = Dict(aliases)
    frontend_aliases = Any(frontend_aliases)
    frontend_flags = Any(frontend_flags)

    subcommands = Dict()

    force_interact = True

main = launch_new_instance = MyTerminalIPythonApp.launch_instance


if __name__ == '__main__':
    main()
```

謎

- JupyterConsoleAppとは？
- classesというのは？
- launch_instanceの処理は？

### JupyterConsoleApp

```
jupyter_client.consoleapp.JupyterConsoleApp <- jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _connection_file_default(self)
    [method] _new_connection_file(self)
    [method] build_kernel_argv(self, argv=None)
    [method] init_connection_file(self)
    [method] init_kernel_client(self)
    [method] init_kernel_manager(self)
    [method] init_ssh(self)
    [method] initialize(self, argv=None)
```

特にoverrideしているものはないらしい

JupyterAppの方はほとんどinterfaceのようなもの

```
jupyter_core.application.JupyterApp <- traitlets.config.application.Application <- traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _config_dir_default(self)
    [method] _config_file_name_default(self)
    [method] _data_dir_default(self)
    [method] _find_subcommand(self, name)
    [method] _jupyter_path_default(self)
    [method] _log_level_default(self)
    [method] _runtime_dir_changed(self, new)
    [method] _runtime_dir_default(self)
    [method, OVERRIDE] initialize(self, argv=None)
    [class method, OVERRIDE] launch_instance(argv=None, **kwargs) method of traitlets.traitlets.MetaHasTraits instance
    [method, OVERRIDE] load_config_file(self, suppress_errors=True)
    [method] migrate_config(self)
    [method, OVERRIDE] start(self)
    [method] write_default_config(self)
```

http://traitlets.readthedocs.io/en/stable/index.html

### classes

### launch_instance


