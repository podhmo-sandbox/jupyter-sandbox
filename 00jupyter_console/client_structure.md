```console
$ pyinspect inspect jupyter_client.manager:KernelManager
jupyter_client.manager.KernelManager <- jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] __del__(self)
        [method] _close_control_socket(self)
    [method] _client_class_changed(self, name, old, new)
    [method] _client_factory_default(self)
    [method] _context_default(self)
    [method] _kernel_cmd_changed(self, name, old, new)
    [method] _kernel_name_changed(self, name, old, new)
    [method] _kernel_spec_manager_changed(self)
    [method] _kernel_spec_manager_default(self)
    [method] add_restart_callback(self, callback, event='restart')
    [method] client(self, **kwargs)
    [method] interrupt_kernel(self)
        [property] has_kernel
        [property] kernel_spec
        [method] signal_kernel(self, signum)
            [property] has_kernel
        [method] _connect_control_socket(self)
    [property] ipykernel
    [method] remove_restart_callback(self, callback, event='restart')
    [method] restart_kernel(self, now=False, newports=False, **kw)
        [method] shutdown_kernel(self, now=False, restart=False)
            [method] stop_restarter(self)
            [method] cleanup(self, connection_file=True)
                [method] _close_control_socket(self)
            [method] _kill_kernel(self)
                [property] has_kernel
                [method] signal_kernel(self, signum)
                    [property] has_kernel
            [method] request_shutdown(self, restart=False)
                [method] _connect_control_socket(self)
            [method] finish_shutdown(self, waittime=None, pollinterval=0.1)
                [property] has_kernel
                [method] is_alive(self)
                    [property] has_kernel
                [method] _kill_kernel(self)
                    [property] has_kernel
                    [method] signal_kernel(self, signum)
                        [property] has_kernel
        [method] start_kernel(self, **kw)
            [method] format_kernel_cmd(self, extra_arguments=None)
                [property] kernel_spec
            [method] _launch_kernel(self, kernel_cmd, **kw)
            [method] start_restarter(self)
            [method] _connect_control_socket(self)
            [property] kernel_spec

jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _data_dir_default(self)
    [method] _ip_changed(self, name, old, new)
    [method] _session_default(self)
    [method] blocking_client(self)
        [method] get_connection_info(self, session=False)
    [method] cleanup_ipc_files(self)
        [property] ports
    [method] cleanup_random_ports(self)
        [method] cleanup_connection_file(self)
    [method] connect_control(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_hb(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_iopub(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_shell(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_stdin(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] load_connection_file(self, connection_file=None)
        [method] load_connection_info(self, info)
            [method] _record_random_port_names(self)
            [method] _ip_default(self)
    [method] write_connection_file(self)
        [method] _record_random_port_names(self)

traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object

traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] __init__(self, **kwargs)
        [method] _load_config(self, cfg, section_names=None, traits=None)
            [method] _find_my_config(self, cfg)
                [class method] section_names()
            [class method] section_names()
    [class method] class_config_rst_doc()
    [class method] class_config_section()
    [class method] class_print_help(inst=None)
        [class method] class_get_help(inst=None)
            [class method] class_get_trait_help(trait, inst=None)
    [method] update_config(self, config)
        [method] _load_config(self, cfg, section_names=None, traits=None)
            [method] _find_my_config(self, cfg)
                [class method] section_names()
            [class method] section_names()

traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] __getstate__(self)
    [method, OVERRIDE] __init__(self, *args, **kwargs)
        [method] hold_trait_notifications(self)
            [method] notify_change(self, change)
            [method] set_trait(self, name, value)
                [method] has_trait(self, name)
        [method] has_trait(self, name)
    [method] __setstate__(self, state)
    [method] _notify_trait(self, name, old_value, new_value)
        [method] notify_change(self, change)
    [method] _register_validator(self, handler, names)
    [method] add_traits(self, **traits)
    [class method] class_own_trait_events(name)
    [class method] class_own_traits(**metadata)
        [class method] class_traits(**metadata)
    [class method] class_trait_names(**metadata)
        [class method] class_traits(**metadata)
    [property] cross_validation_lock
    [method] on_trait_change(self, handler=None, name=None, remove=False)
        [method] unobserve(self, handler, names=traitlets.All, type='change')
            [method] _remove_notifiers(self, handler, name, type)
        [method] observe(self, handler, names=traitlets.All, type='change')
            [method] _add_notifiers(self, handler, name, type)
    [method, OVERRIDE] setup_instance(self, *args, **kwargs)
    [class method] trait_events(name=None)
        [method] trait_names(self, **metadata)
            [method] traits(self, **metadata)
    [method] trait_metadata(self, traitname, key, default=None)
    [method] unobserve_all(self, name=traitlets.All)

traitlets.traitlets.HasDescriptors <- builtins.object
    [static method, OVERRIDE] __new__(cls, *args, **kwargs)
    [method] setup_instance(self, *args, **kwargs)


```

```console
$ pyinspect inspect jupyter_client.client:KernelClient
jupyter_client.client.KernelClient <- jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _context_default(self)
    [method] _handle_kernel_info_reply(self, msg)
    [property] channels_running
    [method] comm_info(self, target_name=None)
        [property] shell_channel
    [method] complete(self, code, cursor_pos=None)
        [property] shell_channel
    [method] execute(self, code, silent=False, store_history=True, user_expressions=None, allow_stdin=None, stop_on_error=True)
        [property] shell_channel
    [method] get_iopub_msg(self, *args, **kwargs)
        [property] iopub_channel
    [method] get_shell_msg(self, *args, **kwargs)
        [property] shell_channel
    [method] get_stdin_msg(self, *args, **kwargs)
        [property] stdin_channel
    [method] history(self, raw=True, output=False, hist_access_type='range', **kwargs)
        [property] shell_channel
    [method] input(self, string)
        [property] stdin_channel
    [method] inspect(self, code, cursor_pos=None, detail_level=0)
        [property] shell_channel
    [method] is_alive(self)
    [method] is_complete(self, code)
        [property] shell_channel
    [method] shutdown(self, restart=False)
        [property] shell_channel
    [method] start_channels(self, shell=True, iopub=True, stdin=True, hb=True)
        [method] kernel_info(self)
            [property] shell_channel
        [property] shell_channel
        [property] iopub_channel
        [property] stdin_channel
        [property] hb_channel
    [method] stop_channels(self)
        [property] shell_channel
        [property] iopub_channel
        [property] stdin_channel
        [property] hb_channel

jupyter_client.connect.ConnectionFileMixin <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _data_dir_default(self)
    [method] _ip_changed(self, name, old, new)
    [method] _session_default(self)
    [method] blocking_client(self)
        [method] get_connection_info(self, session=False)
    [method] cleanup_ipc_files(self)
        [property] ports
    [method] cleanup_random_ports(self)
        [method] cleanup_connection_file(self)
    [method] connect_control(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_hb(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_iopub(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_shell(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] connect_stdin(self, identity=None)
        [method] _create_connected_socket(self, channel, identity=None)
            [method] _make_url(self, channel)
    [method] load_connection_file(self, connection_file=None)
        [method] load_connection_info(self, info)
            [method] _record_random_port_names(self)
            [method] _ip_default(self)
    [method] write_connection_file(self)
        [method] _record_random_port_names(self)

traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object

traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] __init__(self, **kwargs)
        [method] _load_config(self, cfg, section_names=None, traits=None)
            [method] _find_my_config(self, cfg)
                [class method] section_names()
            [class method] section_names()
    [class method] class_config_rst_doc()
    [class method] class_config_section()
    [class method] class_print_help(inst=None)
        [class method] class_get_help(inst=None)
            [class method] class_get_trait_help(trait, inst=None)
    [method] update_config(self, config)
        [method] _load_config(self, cfg, section_names=None, traits=None)
            [method] _find_my_config(self, cfg)
                [class method] section_names()
            [class method] section_names()

traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] __getstate__(self)
    [method, OVERRIDE] __init__(self, *args, **kwargs)
        [method] hold_trait_notifications(self)
            [method] notify_change(self, change)
            [method] set_trait(self, name, value)
                [method] has_trait(self, name)
        [method] has_trait(self, name)
    [method] __setstate__(self, state)
    [method] _notify_trait(self, name, old_value, new_value)
        [method] notify_change(self, change)
    [method] _register_validator(self, handler, names)
    [method] add_traits(self, **traits)
    [class method] class_own_trait_events(name)
    [class method] class_own_traits(**metadata)
        [class method] class_traits(**metadata)
    [class method] class_trait_names(**metadata)
        [class method] class_traits(**metadata)
    [property] cross_validation_lock
    [method] on_trait_change(self, handler=None, name=None, remove=False)
        [method] unobserve(self, handler, names=traitlets.All, type='change')
            [method] _remove_notifiers(self, handler, name, type)
        [method] observe(self, handler, names=traitlets.All, type='change')
            [method] _add_notifiers(self, handler, name, type)
    [method, OVERRIDE] setup_instance(self, *args, **kwargs)
    [class method] trait_events(name=None)
        [method] trait_names(self, **metadata)
            [method] traits(self, **metadata)
    [method] trait_metadata(self, traitname, key, default=None)
    [method] unobserve_all(self, name=traitlets.All)

traitlets.traitlets.HasDescriptors <- builtins.object
    [static method, OVERRIDE] __new__(cls, *args, **kwargs)
    [method] setup_instance(self, *args, **kwargs)
```
