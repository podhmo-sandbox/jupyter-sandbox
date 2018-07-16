```console
$ pyinspect inspect nbconvert.preprocessors.execute:ExecutePreprocessor
nbconvert.preprocessors.execute.ExecutePreprocessor <- nbconvert.preprocessors.base.Preprocessor <- nbconvert.utils.base.NbConvertBase <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] preprocess(self, nb, resources)
    [method, OVERRIDE] preprocess_cell(self, cell, resources, cell_index)
        [method] run_cell(self, cell, cell_index=0)
            [method] _wait_for_reply(self, msg_id, cell)
            [method] _update_display_id(self, display_id, msg)

nbconvert.preprocessors.base.Preprocessor <- nbconvert.utils.base.NbConvertBase <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] __call__(self, nb, resources)
        [method] preprocess(self, nb, resources)
            [method] preprocess_cell(self, cell, resources, index)
    [method, OVERRIDE] __init__(self, **kw)

nbconvert.utils.base.NbConvertBase <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] __init__(self, **kw)

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

