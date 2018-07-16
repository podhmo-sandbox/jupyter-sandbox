## nbconvert

jupyter-nbconvertの実態は、`nbconvert` のnbconvertapp

```console
$ cat $(which jupyter-nbconvert)
#!VENV/bin/python

# -*- coding: utf-8 -*-
import re
import sys

from nbconvert.nbconvertapp import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

構造

```
$ pyinspect list nbconvert
nbconvert
nbconvert.exporters
nbconvert.exporters.asciidoc
nbconvert.exporters.base
nbconvert.exporters.export
nbconvert.exporters.exporter
nbconvert.exporters.exporter_locator
nbconvert.exporters.html
nbconvert.exporters.latex
nbconvert.exporters.markdown
nbconvert.exporters.notebook
nbconvert.exporters.pdf
nbconvert.exporters.python
nbconvert.exporters.rst
nbconvert.exporters.script
nbconvert.exporters.slides
nbconvert.exporters.templateexporter
nbconvert.filters
nbconvert.filters.ansi
nbconvert.filters.citation
nbconvert.filters.datatypefilter
nbconvert.filters.filter_links
nbconvert.filters.highlight
nbconvert.filters.latex
nbconvert.filters.markdown
nbconvert.filters.markdown_mistune
nbconvert.filters.metadata
nbconvert.filters.pandoc
nbconvert.filters.strings
nbconvert.nbconvertapp
nbconvert.postprocessors
nbconvert.postprocessors.base
nbconvert.postprocessors.serve
nbconvert.preprocessors
nbconvert.preprocessors.base
nbconvert.preprocessors.clearoutput
nbconvert.preprocessors.coalescestreams
nbconvert.preprocessors.convertfigures
nbconvert.preprocessors.csshtmlheader
nbconvert.preprocessors.execute
nbconvert.preprocessors.extractoutput
nbconvert.preprocessors.highlightmagics
nbconvert.preprocessors.latex
nbconvert.preprocessors.regexremove
nbconvert.preprocessors.sanitize
nbconvert.preprocessors.svg2pdf
nbconvert.preprocessors.tagremove
nbconvert.resources
nbconvert.utils
nbconvert.utils.base
nbconvert.utils.exceptions
nbconvert.utils.io
nbconvert.utils.lexers
nbconvert.utils.pandoc
nbconvert.utils.version
nbconvert.writers
nbconvert.writers.base
nbconvert.writers.debug
nbconvert.writers.files
nbconvert.writers.stdout
```

あとで調べるとわかるけれど。けっこうきれいに分かれている?

- exporters -- output format?
- filters -- ???
- preprocessors
- postprocessors
- writers

todo: あとで調べる。

### main

nbconvert.nbconvertapp をもう少し詳しく。内部的な関係は以下のようなもの。まぁNbConvertAppだけを見ていけば良さそう。JupyterAppがkernel_managerやkernel_clientを作ってくれているはずなのでただただ通信部分を見れば良い。はず？

```
$ pyinspect inspect nbconvert.nbconvertapp
nbconvert.nbconvertapp.DottedOrNone <- traitlets.traitlets.DottedObjectName <- traitlets.traitlets.ObjectName <- traitlets.traitlets.TraitType <- traitlets.traitlets.BaseDescriptor <- builtins.object
    [method, OVERRIDE] validate(self, obj, value)

----------------------------------------
nbconvert.nbconvertapp.NbConvertApp <- jupyter_core.application.JupyterApp <- traitlets.config.application.Application <- traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] initialize(self, argv=None)
        [method] init_syspath(self)
        [method] init_notebooks(self)
        [method] init_writer(self)
        [method] init_postprocessor(self)
    [method, OVERRIDE] start(self)
        [method] convert_notebooks(self)
            [method] convert_single_notebook(self, notebook_filename, input_buffer=None)
                [method] init_single_notebook_resources(self, notebook_filename)
                [method] export_single_notebook(self, notebook_filename, resources, input_buffer=None)
                [method] write_single_notebook(self, output, resources)
                [method] postprocess_single_notebook(self, write_results)

jupyter_core.application.JupyterApp <- traitlets.config.application.Application <- traitlets.config.configurable.SingletonConfigurable <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method] _config_dir_default(self)
    [method] _config_file_name_default(self)
    [method] _data_dir_default(self)
    [method] _jupyter_path_default(self)
    [method] _log_level_default(self)
    [method] _runtime_dir_changed(self, new)
    [method] _runtime_dir_default(self)
    [method, OVERRIDE] initialize(self, argv=None)
        [property] _dispatching
        [method] migrate_config(self)
        [method, OVERRIDE] load_config_file(self, suppress_errors=True)
            [property] config_file_paths
        [method] _find_subcommand(self, name)
    [class method, OVERRIDE] launch_instance(argv=None, **kwargs)
    [method, OVERRIDE] start(self)
        [method] write_default_config(self)

# ... traitlets関係は省略
```

基本的には以下の２つのメソッド

- initialize()
- start()

convert_notebooks() が処理の本体。


```python
class NbConvertApp(JupyterApp):
#...
    def start(self):
        """Run start after initialization process has completed"""
        super(NbConvertApp, self).start()
        self.convert_notebooks()

```

traitlets.Instanceをgrepしてみても良い。トップレベルではこの2つだけがdefaultとして読み込まれるらしい。

```console
$ grep 'Instance(' nbconvertapp.py
    writer = Instance('nbconvert.writers.base.WriterBase',
    postprocessor = Instance('nbconvert.postprocessors.base.PostProcessorBase',
```

### 処理の本体

実質的にはexporterを取り出して設定しているだけ。（このコード微妙じゃない？）

```python
    def convert_notebooks(self):
        # initialize the exporter
        cls = get_exporter(self.export_format)
        self.exporter = cls(config=self.config)

        # convert each notebook
        if not self.from_stdin:
            for notebook_filename in self.notebooks:
                self.convert_single_notebook(notebook_filename)
        else:
            input_buffer = unicode_stdin_stream()
            # default name when conversion from stdin
            self.convert_single_notebook("notebook.ipynb", input_buffer=input_buffer)
```

続いてconvert_single_notebook

1. Initialize notebook resources
2. Export the notebook to a particular format
3. Write the exported notebook to file
4. (Maybe) postprocess the written file

後々分かることだけれど。重要なのはexporterだった。

```python
    def convert_single_notebook(self, notebook_filename, input_buffer=None):
        self.log.info("Converting notebook into %s", self.export_format)

        resources = self.init_single_notebook_resources(notebook_filename)
        output, resources = self.export_single_notebook(notebook_filename, resources, input_buffer=input_buffer)
        write_results = self.write_single_notebook(output, resources)
        self.postprocess_single_notebook(write_results)
```

それぞれ見ていく。

init_single_notebook_resources()のresourcesというのは利用するファイルや設定などを保持したdictのこと。

```python
    def init_single_notebook_resources(self, notebook_filename):
#..
        # first initialize the resources we want to use
        resources = {}
        resources['config_dir'] = self.config_dir
        resources['unique_key'] = notebook_name

        output_files_dir = (self.output_files_dir
                            .format(notebook_name=notebook_name))

        resources['output_files_dir'] = output_files_dir

        return resources

```


export_single_notebook()はexporterのfrom_filename()やfrom_file()を呼ぶだけ。

```python
    def export_single_notebook(self, notebook_filename, resources, input_buffer=None):
#..
        output, resources = self.exporter.from_file(input_buffer, resources=resources)
#..
        return output, resources
```

writeとpostはまぁ流れで(コードは一部省略している）。writeとpostprocessorってなんなんだろうな。

```python
    def write_single_notebook(self, output, resources):
        notebook_name = resources['unique_key']
        write_results = self.writer.write(
            output, resources, notebook_name=notebook_name)
        return write_results

    def postprocess_single_notebook(self, write_results):
        # Post-process if post processor has been defined.
        if hasattr(self, 'postprocessor') and self.postprocessor:
            self.postprocessor(write_results)
```

あんまりまじめに読む必要はなさそうだ。Writerは例えばファイルに書き込むということだし。PostProcessorは出力されたファイル名などをどうこうするだけ(reveal.jsでslide化されたものをserveみたいな場合がある)。

```
class Writer:
    def write(self, output, resources, notebook_names=None, **kw):
    	# ...
        with open(dest) as wf:
            wf.write(output)
        return dest

class PostProcessor:
    def __call__(self, input):
        raise NotImplementedError('postprocess')
```

通信するやつはだれだろ？

### 実際の処理の本体はexporter


例えば、HTMLなら以下の様な形。

`nbconvert.exporters.html.HTMLExporter <- nbconvert.exporters.templateexporter.TemplateExporter <- nbconvert.exporters.exporter.Exporter`

基本的にはExporterのfrom_notebook_node()を見る感じ。

そういえば、そもそも `--execute` みたいなオプションを付けないと実行はされなかった記憶。
本体は `nbconvert.preprocessors.execute.ExecutePreprocessor <- nbconvert.preprocessors.base.Preprocessor <- nbconvert.utils.base.NbConvertBase`。

```
nbconvert.preprocessors.execute.ExecutePreprocessor <- nbconvert.preprocessors.base.Preprocessor <- nbconvert.utils.base.NbConvertBase <- traitlets.config.configurable.LoggingConfigurable <- traitlets.config.configurable.Configurable <- traitlets.traitlets.HasTraits <- traitlets.traitlets.HasDescriptors <- builtins.object
    [method, OVERRIDE] preprocess(self, nb, resources)
    [method, OVERRIDE] preprocess_cell(self, cell, resources, cell_index)
        [method] run_cell(self, cell, cell_index=0)
            [method] _wait_for_reply(self, msg_id, cell)
            [method] _update_display_id(self, display_id, msg)
```


実際の所ExecutePreprocessorは、mainがpreprocess()

- jupyter_clientのstart_new_kernel()に似た関数でkernel_clientを作る
- kernel_clientを使ったpreprocess_cell()をcell毎に呼ぶ

memo:

- kernel_clientのwait_for_ready()を確認
- 後処理系の作業を整理
- このあたりの毎回kernel clientを立ち上げては終了させている部分をどうにかしたい

```python
    def preprocess(self, nb, resources):
#..
        self.km, self.kc = start_new_kernel(
            startup_timeout=self.startup_timeout,
            kernel_name=kernel_name,
            extra_arguments=self.extra_arguments,
            cwd=path)
        self.kc.allow_stdin = False

        try:
            nb, resources = super(ExecutePreprocessor, self).preprocess(nb, resources)
        finally:
            self.kc.stop_channels()
            self.km.shutdown_kernel(now=self.shutdown_kernel == 'immediate')

        return nb, resources
```

シンプルに使うには `nbconvert.preprocessors.execute:executenb` が便利。

