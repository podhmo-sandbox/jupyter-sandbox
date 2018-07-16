```
$ pyinspect inspect nbconvert.exporters.html:HTMLExporter

nbconvert.exporters.html.HTMLExporter <- nbconvert.exporters.templateexporter.TemplateExporter <- nbconvert.exporters.exporter.Exporter <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [property, OVERRIDE] default_config
    [method, OVERRIDE] default_filters(self)
        [method] markdown2html(self, source)
    [method, OVERRIDE] from_notebook_node(self, nb, resources=None, **kw)

nbconvert.exporters.templateexporter.TemplateExporter <- nbconvert.exporters.exporter.Exporter <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] __init__(self, config=None, **kw)
        [method] _invalidate_environment_cache(self, change=None)
            [method] _invalidate_template_cache(self, change=None)
        [method] _invalidate_template_cache(self, change=None)
    [method] _create_environment(self)
        [method] default_filters(self)
        [method] _register_filter(self, environ, name, jinja_filter)
    [method] _load_template(self)
        [property] environment
    [property, OVERRIDE] default_config
    [method, OVERRIDE] from_notebook_node(self, nb, resources=None, **kw)
        [property] template
    [method] register_filter(self, name, jinja_filter)
        [method] _register_filter(self, environ, name, jinja_filter)
        [property] environment

nbconvert.exporters.exporter.Exporter <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] __init__(self, config=None, **kw)
        [property] default_config
        [method] _init_preprocessors(self)
            [method] register_preprocessor(self, preprocessor, enabled=False)
    [method] from_filename(self, filename, resources=None, **kw)
        [method] from_file(self, file_stream, resources=None, **kw)
            [method] from_notebook_node(self, nb, resources=None, **kw)
                [method] _init_resources(self, resources)
                [method] _preprocess(self, nb, resources)

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
