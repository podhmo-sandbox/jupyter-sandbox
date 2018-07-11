## zmqを使っている部分を調べてみる

```
$ TARGETDIR=~/venvs/viz
$ mkdir -p data
$ (cd $TARGETDIR && find . -name "*.py" | grep -v lib/ | xargs grep zmq -l 2>/dev/null) | sort > data/zmq.files
```

[./data/zmq.files](./data/zmq.files)

jupyter-consoleのあたりを見ると良いかもしれない。jupyter_consoleのrepository。

特に重要なものはなさそう？

```console
grep "^class ZMQ"  -r ../../jupyter_console/
../../jupyter_console/jupyter_console/tests/test_image_handler.py:class ZMQTerminalInteractiveShellTestCase(unittest.TestCase):
../../jupyter_console/jupyter_console/zmqhistory.py:class ZMQHistoryManager(HistoryAccessorBase):
../../jupyter_console/jupyter_console/ptshell.py:class ZMQTerminalInteractiveShell(SingletonConfigurable):
../../jupyter_console/jupyter_console/app.py:class ZMQTerminalIPythonApp(JupyterApp, JupyterConsoleApp):
../../jupyter_console/jupyter_console/completer.py:class ZMQCompleter(Configurable):
```

どうも色々adapterを書かないといけない模様？

```console
$ pyinspect jupyter_console.zmqhistory:ZMQHistoryManager
jupyter_console.zmqhistory.ZMQHistoryManager <- IPython.core.history.HistoryAccessorBase <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, client)
    _load_history(self, raw=True, output=False, hist_access_type='range', **kwargs)
    end_session(self)
    @OVERRIDE: get_range(self, session, start=1, stop=None, raw=True, output=False)
    @OVERRIDE: get_range_by_str(self, rangestr, raw=True, output=False)
    @OVERRIDE: get_tail(self, n=10, raw=True, output=False, include_latest=False)
    reset(self, new_session=True)
    @OVERRIDE: search(self, pattern='*', raw=True, search_raw=True, output=False, n=None, unique=False)

IPython.core.history.HistoryAccessorBase <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    get_range(self, session, start=1, stop=None, raw=True, output=False)
    get_range_by_str(self, rangestr, raw=True, output=False)
    get_tail(self, n=10, raw=True, output=False, include_latest=False)
    search(self, pattern='*', raw=True, search_raw=True, output=False, n=None, unique=False)

traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    <traitlets.traitlets.DefaultHandler object>
traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, **kwargs)
    <traitlets.traitlets.ObserveHandler object>_find_my_config(self, cfg)
    _load_config(self, cfg, section_names=None, traits=None)
    update_config(self, config)

traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    __getstate__(self)
    @OVERRIDE: __init__(self, *args, **kwargs)
    __setstate__(self, state)
    _add_notifiers(self, handler, name, type)
    _notify_trait(self, name, old_value, new_value)
    _register_validator(self, handler, names)
    _remove_notifiers(self, handler, name, type)
    add_traits(self, **traits)
    has_trait(self, name)
    hold_trait_notifications(self)
    notify_change(self, change)
    observe(self, handler, names=traitlets.All, type='change')
    on_trait_change(self, handler=None, name=None, remove=False)
    set_trait(self, name, value)
    @OVERRIDE: setup_instance(self, *args, **kwargs)
    trait_metadata(self, traitname, key, default=None)
    trait_names(self, **metadata)
    traits(self, **metadata)
    unobserve(self, handler, names=traitlets.All, type='change')
    unobserve_all(self, name=traitlets.All)

traitlets.traitlets.HasDescriptors <- builtins.object
    setup_instance(self, *args, **kwargs)
```

```console
$ pyinspect jupyter_console.ptshell:ZMQTerminalInteractiveShell
jupyter_console.ptshell.ZMQTerminalInteractiveShell <- traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, **kwargs)
    _banner1_default(self)
    _client_changed(self, name, old, new)
    ask_exit(self)
    check_complete(self, code)
    from_here(self, msg)
    get_continuation_tokens(self, cli, width)
    get_out_prompt_tokens(self)
    get_prompt_tokens(self, cli)
    handle_execute_reply(self, msg_id, timeout=None)
    handle_image(self, data, mime)
    handle_image_PIL(self, data, mime)
    handle_image_callable(self, data, mime)
    handle_image_stream(self, data, mime)
    handle_image_tempfile(self, data, mime)
    handle_input_request(self, msg_id, timeout=0.1)
    handle_iopub(self, msg_id='')
    handle_is_complete_reply(self, msg_id, timeout=None)
    handle_rich_data(self, data)
    include_output(self, msg)
    init_completer(self)
    init_history(self)
    init_io(self)
    init_kernel_info(self)
    init_prompt_toolkit_cli(self)
    interact(self, display_banner=None)
    mainloop(self)
    pre_prompt(self)
    print_out_prompt(self)
    prompt_for_code(self)
    run_cell(self, cell, store_history=True)
    show_banner(self)

traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object

traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    <traitlets.traitlets.DefaultHandler object>
traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, **kwargs)
    <traitlets.traitlets.ObserveHandler object>_find_my_config(self, cfg)
    _load_config(self, cfg, section_names=None, traits=None)
    update_config(self, config)

traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    __getstate__(self)
    @OVERRIDE: __init__(self, *args, **kwargs)
    __setstate__(self, state)
    _add_notifiers(self, handler, name, type)
    _notify_trait(self, name, old_value, new_value)
    _register_validator(self, handler, names)
    _remove_notifiers(self, handler, name, type)
    add_traits(self, **traits)
    has_trait(self, name)
    hold_trait_notifications(self)
    notify_change(self, change)
    observe(self, handler, names=traitlets.All, type='change')
    on_trait_change(self, handler=None, name=None, remove=False)
    set_trait(self, name, value)
    @OVERRIDE: setup_instance(self, *args, **kwargs)
    trait_metadata(self, traitname, key, default=None)
    trait_names(self, **metadata)
    traits(self, **metadata)
    unobserve(self, handler, names=traitlets.All, type='change')
    unobserve_all(self, name=traitlets.All)

traitlets.traitlets.HasDescriptors <- builtins.object
    setup_instance(self, *args, **kwargs)
```

```console
$ pyinspect jupyter_console.app:ZMQTerminalIPythonApp
jupyter_console.app.ZMQTerminalIPythonApp <- jupyter_core.application.JupyterApp <- traitlets.config.application.Application <- traitlets.config.configurable.SingletonConfigurable <- jupyter_client.consoleapp.JupyterConsoleApp <- jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    handle_sigint(self, *args)
    init_banner(self)
    init_gui_pylab(self)
    init_shell(self)
    @OVERRIDE: initialize(self, argv=None)
    @OVERRIDE: parse_command_line(self, argv=None)
    @OVERRIDE: start(self)

jupyter_core.application.JupyterApp <- traitlets.config.application.Application <- traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    _config_dir_default(self)
    _config_file_name_default(self)
    _data_dir_default(self)
    _find_subcommand(self, name)
    _jupyter_path_default(self)
    _log_level_default(self)
    _runtime_dir_changed(self, new)
    _runtime_dir_default(self)
    @OVERRIDE: initialize(self, argv=None)
    @OVERRIDE: load_config_file(self, suppress_errors=True)
    migrate_config(self)
    @OVERRIDE: start(self)
    write_default_config(self)

traitlets.config.application.Application <- traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, **kwargs)
    _classes_in_config_sample(self)
    _classes_inc_parents(self)
    @OVERRIDE: <traitlets.traitlets.ObserveHandler object><traitlets.traitlets.ObserveHandler object>@OVERRIDE: <traitlets.traitlets.DefaultHandler object><traitlets.traitlets.ObserveHandler object><traitlets.traitlets.ObserveHandler object>document_config_options(self)
    exit(self, exit_status=0)
    flatten_flags(self)
    generate_config_file(self)
    initialize(self, argv=None)
    initialize_subcommand(self, subc, argv=None)
    load_config_file(self, filename, path=None)
    parse_command_line(self, argv=None)
    print_alias_help(self)
    print_description(self)
    print_examples(self)
    print_flag_help(self)
    print_help(self, classes=False)
    print_options(self)
    print_subcommands(self)
    print_version(self)
    start(self)

traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object

jupyter_client.consoleapp.JupyterConsoleApp <- jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    _connection_file_default(self)
    _new_connection_file(self)
    build_kernel_argv(self, argv=None)
    init_connection_file(self)
    init_kernel_client(self)
    init_kernel_manager(self)
    init_ssh(self)
    initialize(self, argv=None)

jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    _create_connected_socket(self, channel, identity=None)
    _data_dir_default(self)
    _ip_changed(self, name, old, new)
    _ip_default(self)
    _make_url(self, channel)
    _record_random_port_names(self)
    _session_default(self)
    blocking_client(self)
    cleanup_connection_file(self)
    cleanup_ipc_files(self)
    cleanup_random_ports(self)
    connect_control(self, identity=None)
    connect_hb(self, identity=None)
    connect_iopub(self, identity=None)
    connect_shell(self, identity=None)
    connect_stdin(self, identity=None)
    get_connection_info(self, session=False)
    load_connection_file(self, connection_file=None)
    load_connection_info(self, info)
    write_connection_file(self)

traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    <traitlets.traitlets.DefaultHandler object>
traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, **kwargs)
    <traitlets.traitlets.ObserveHandler object>_find_my_config(self, cfg)
    _load_config(self, cfg, section_names=None, traits=None)
    update_config(self, config)

traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    __getstate__(self)
    @OVERRIDE: __init__(self, *args, **kwargs)
    __setstate__(self, state)
    _add_notifiers(self, handler, name, type)
    _notify_trait(self, name, old_value, new_value)
    _register_validator(self, handler, names)
    _remove_notifiers(self, handler, name, type)
    add_traits(self, **traits)
    has_trait(self, name)
    hold_trait_notifications(self)
    notify_change(self, change)
    observe(self, handler, names=traitlets.All, type='change')
    on_trait_change(self, handler=None, name=None, remove=False)
    set_trait(self, name, value)
    @OVERRIDE: setup_instance(self, *args, **kwargs)
    trait_metadata(self, traitname, key, default=None)
    trait_names(self, **metadata)
    traits(self, **metadata)
    unobserve(self, handler, names=traitlets.All, type='change')
    unobserve_all(self, name=traitlets.All)

traitlets.traitlets.HasDescriptors <- builtins.object
    setup_instance(self, *args, **kwargs)
```

```console
$ pyinspect jupyter_console.completer:ZMQCompleter
jupyter_console.completer.ZMQCompleter <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, shell, client, config=None)
    complete_request(self, code, cursor_pos)

traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    @OVERRIDE: __init__(self, **kwargs)
    <traitlets.traitlets.ObserveHandler object>_find_my_config(self, cfg)
    _load_config(self, cfg, section_names=None, traits=None)
    update_config(self, config)

traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    __getstate__(self)
    @OVERRIDE: __init__(self, *args, **kwargs)
    __setstate__(self, state)
    _add_notifiers(self, handler, name, type)
    _notify_trait(self, name, old_value, new_value)
    _register_validator(self, handler, names)
    _remove_notifiers(self, handler, name, type)
    add_traits(self, **traits)
    has_trait(self, name)
    hold_trait_notifications(self)
    notify_change(self, change)
    observe(self, handler, names=traitlets.All, type='change')
    on_trait_change(self, handler=None, name=None, remove=False)
    set_trait(self, name, value)
    @OVERRIDE: setup_instance(self, *args, **kwargs)
    trait_metadata(self, traitname, key, default=None)
    trait_names(self, **metadata)
    traits(self, **metadata)
    unobserve(self, handler, names=traitlets.All, type='change')
    unobserve_all(self, name=traitlets.All)

traitlets.traitlets.HasDescriptors <- builtins.object
    setup_instance(self, *args, **kwargs)
```
