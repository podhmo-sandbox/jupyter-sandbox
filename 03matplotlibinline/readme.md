# matplotlib inline

jupyter notebook上のこれってどこで解釈されているんだろう？

```
%matplotlib inline
```

- %付きのコマンドの解釈はkernel?
- inlineの定義はmatplotlib側のnotebook側のどちらなんだろう？

## notebookを探してみる

notebookの中を覗いてみる。inlineでgrepしてみれば何か分かるかもしれない。

```console
$ cat `which jupyter-notebook`
#!VENV/bin/python

# -*- coding: utf-8 -*-
import re
import sys

from notebook.notebookapp import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

$ grep -r inline $(pyinspect resolve notebook) | grep -v js | grep -v test | grep -v css | grep -v static
```

jsやcssのそれは見つかるものの特にnotebookにはないみたい。

## pythonのkernelの覗いてみる

kernelの中にあるかもしれない。とはいえそもそもkernelがどのパッケージで実装されているかわからない。

```console
$ jupyter-kernelspec list 
Available kernels:
  python3    VENV/share/jupyter/kernels/python3

$ cat VENV/share/jupyter/kernels/python3/kernel.json
{
 "argv": [
  "python",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Python 3",
 "language": "python"
```

ipykernel_launcherというモジュールらしい。

```console
$ pyinspect resolve ipykernel_launcher | xargs cat
"""Entry point for launching an IPython kernel.

This is separate from the ipykernel package so we can avoid doing imports until
after removing the cwd from sys.path.
"""

import sys

if __name__ == '__main__':
    # Remove the CWD from sys.path while we load stuff.
    # This is added back by InteractiveShellApp.init_path()
    if sys.path[0] == '':
        del sys.path[0]

    from ipykernel import kernelapp as app
    app.launch_new_instance()
```

本体はipykernelか。そういえばpip freezeの時点でもipykernelがあった気がする。

```console
$ pip freeze | grep ipy
ipykernel==4.9.0
ipython==6.5.0
ipython-genutils==0.2.0
ipywidgets==7.4.1
```

ipykernelでもinlineを探してみよう。

```console
$ grep -r inline $(pyinspect resolve ipykernel) | grep -v js | grep -v test | grep -v css | grep -v static
VENV/lib/python3.7/site-packages/ipykernel/inprocess/ipkernel.py:    # IPython's GUI support (including pylab). The default is 'inline' because
VENV/lib/python3.7/site-packages/ipykernel/inprocess/ipkernel.py:    gui = Enum(('tk', 'gtk', 'wx', 'qt', 'qt4', 'inline'),
VENV/lib/python3.7/site-packages/ipykernel/inprocess/ipkernel.py:               default_value='inline')
VENV/lib/python3.7/site-packages/ipykernel/eventloops.py:    'inline': None,
VENV/lib/python3.7/site-packages/ipykernel/kernelapp.py:        # Register inline backend as default
VENV/lib/python3.7/site-packages/ipykernel/kernelapp.py:            os.environ['MPLBACKEND'] = 'module://ipykernel.pylab.backend_inline'
VENV/lib/python3.7/site-packages/ipykernel/pylab/backend_inline.py:        from IPython.core.pylabtools import configure_inline_support, activate_matplotlib
VENV/lib/python3.7/site-packages/ipykernel/pylab/backend_inline.py:            configure_inline_support(ip, backend)
VENV/lib/python3.7/site-packages/ipykernel/pylab/backend_inline.py:                configure_inline_support(ip, backend)
VENV/lib/python3.7/site-packages/ipykernel/pylab/config.py:"""Configurable for configuring the IPython inline backend
VENV/lib/python3.7/site-packages/ipykernel/pylab/config.py:# Configurable for inline backend options
VENV/lib/python3.7/site-packages/ipykernel/pylab/config.py:    """An object to store configuration of the inline backend."""
VENV/lib/python3.7/site-packages/ipykernel/pylab/config.py:    # The typical default figure size is too large for inline use,
VENV/lib/python3.7/site-packages/ipykernel/pylab/config.py:        inline backend."""
```

何やらありそう。ついでにmatplotlibも探してみる。

```console
$ grep -r matplotlib $(pyinspect resolve pyinspect) | grep -v js | grep -v test | grep -v css | grep -v static
```

何もなかった。hmm。記憶が確かならmatploblibの便利機能の昔の名前がpylabだったような。

```console
$ pyinspect list matplotlib | grep pylab
matplotlib.pylab
$ pyinspect resolve matplotlib.pylab | xargs wc
  268  1602 10489 VENV/lib/python3.7/site-packages/matplotlib/pylab.py
```

たしかそう。もう一度ipykernelのpylabを覗いてみよう。と言うかそのものズバリっぽいファイルが存在している。

```
VENV/lib/python3.7/site-packages/ipykernel/pylab/backend_inline.py
```


ipykernel/pylab/backend_inline.py

```python
def _enable_matplotlib_integration():
    """Enable extra IPython matplotlib integration when we are loaded as the matplotlib backend."""
    from matplotlib import get_backend
    ip = get_ipython()
    backend = get_backend()
    if ip and backend == 'module://%s' % __name__:
        from IPython.core.pylabtools import configure_inline_support, activate_matplotlib
        try:
            activate_matplotlib(backend)
            configure_inline_support(ip, backend)
        except (ImportError, AttributeError):
            # bugs may cause a circular import on Python 2
            def configure_once(*args):
                activate_matplotlib(backend)
                configure_inline_support(ip, backend)
                ip.events.unregister('post_run_cell', configure_once)
            ip.events.register('post_run_cell', configure_once)

_enable_matplotlib_integration()
```

なにやら中を覗いてみると、Ipython譲りの機能でありそうなコメントが書かれている？
ここでちょっと一段落。

## ちょっとしたまとめ

- `%matplotlib inline` がどこで解釈されているかわからない
- `%matplotlib inline` はipykernelパッケージ付近で何か行われていそう。

このあたりで以下２つを整理したい

- `%matplotlib inline` という字句をmagic commandとして解釈している部分はどこか
- `%matplotlib inline` という字句が解釈された結果どのように状態が変わるのか

## 字句を解釈している場所を探す

まずは、字句を解釈している場所を探してみることにする。その前にmagic commandの定義の仕方整理。

`% foo` という表記のものはmagic commandと呼ばれていたはず。テキトウに`jupyter magic command` などで検索してみる。ipythonのドキュメントが出てきた。

[Built-in magic commands — IPython 6.5.0 documentation](https://ipython.readthedocs.io/en/stable/interactive/magics.html "Built-in magic commands — IPython 6.5.0 documentation")

> To Jupyter users: Magics are specific to and provided by the IPython kernel. Whether magics are available on a kernel is a decision that is made by the kernel developer on a per-kernel basis. To work properly, Magics must use a syntax element which is not valid in the underlying language. For example, the IPython kernel uses the % syntax element for magics as % is not a valid unary operator in Python. While, the syntax element has meaning in other languages.

合っていそう。ついでにipykernelで`% matplotlib inline` の解釈が実装されている可能性が高まった。

ただ、一旦、magic commandとしての`%matplotlib` については置いておいて、magic command自体について調べることにする。

### magic commandの定義の仕方

「magic commandの定義の仕方」、これくらいに検索対象が明らかならドキュメントもすぐに探せるようになってくるし。ドキュメントにも書かれていそう。実際以下の様なページが見つかる。

- [Defining custom magics — IPython 6.5.0 documentation](https://ipython.readthedocs.io/en/stable/config/custommagics.html "Defining custom magics — IPython 6.5.0 documentation")

`IPython.core.magic`で提供されているデコレーターを使ってあげれば良いという話。実際に作ってみたい場合は[この例](https://ipython.readthedocs.io/en/stable/config/custommagics.html#complete-example)などを参考にすればどうにかなりそう。

しかし今の興味はどのように使うかではなくどのように実装されているかなので使いかたには深入りしない。内部を見ていく。

先程紹介したサンプルで紹介されていたデコレーターは以下の様な定義になっている。`_function_magic_marker()`というファクトリー的な関数で作られたもの。

IPython/core/magic.py

```python
register_line_magic = _function_magic_marker('line')
register_cell_magic = _function_magic_marker('cell')
register_line_cell_magic = _function_magic_marker('line_cell')
```

この内部の関数の分岐を減らしたバージョンは以下の様な定義。重要そうなのは `register_magic_function()`と `get_ipython()`

IPython/core/magic.py

```python
def _function_magic_marker(magic_kind):
    def magic_deco(arg):
        call = lambda f, *a, **k: f(*a, **k)

        # Find get_ipython() in the caller's namespace
        caller = sys._getframe(1)
        for ns in ['f_locals', 'f_globals', 'f_builtins']:
            get_ipython = getattr(caller, ns).get('get_ipython')
            if get_ipython is not None:
                break

        ip = get_ipython()

        func = arg
        name = func.__name__
        ip.register_magic_function(func, magic_kind, name)
        retval = decorator(call, func)
        return retval

    # Ensure the resulting decorator has a usable docstring
    ds = _docstring_template.format('function', magic_kind)
    magic_deco.__doc__ = ds
    return magic_deco
```

雰囲気的には、取り出したipythonのインスタンスでmagic functionを登録しているという感じ。

#### get_ipython()

これはipythonのinstanceを取得したいときに使うらしい。以下の様なコード。

IPython/core/getipython.py

```python
def get_ipython():
    """Get the global InteractiveShell instance.
    
    Returns None if no InteractiveShell instance is registered.
    """
    from IPython.core.interactiveshell import InteractiveShell
    if InteractiveShell.initialized():
        return InteractiveShell.instance()
```

initializedじゃないと値を返してくれないが。これはsingletonなインスタンスをクラスメソッドで呼んであげれば良い。

```python
from IPython import InteractiveShell

shell = InteractiveShell.instance()

ip = get_ipython()
ip.run_cell("%time None")
# CPU times: user 2 µs, sys: 0 ns, total: 2 µs
# Wall time: 3.58 µs
```

という感じで使える(普通にpdbっぽい感じで使いたい場合にはIPython.embedの方を使う)。

#### register_magic_function()

MagicsManagerの`register_function()`に渡している。

IPython/core/interactiveshell.py

```python
class InteractiveShell(SingletonConfigurable):
    magics_manager = Instance('IPython.core.magic.MagicsManager', allow_none=True)


    # Defined here so that it's included in the documentation
    @functools.wraps(magic.MagicsManager.register_function)
    def register_magic_function(self, func, magic_kind='line', magic_name=None):
        self.magics_manager.register_function(func, 
                                  magic_kind=magic_kind, magic_name=magic_name)
```

MagicsManagerは以下のようなもの。内部のmagicsという変数に格納しているだけ（lineかcellのどのmagic commandなのかという指定はあるけれど）。

IPython/core/magic.py
```python
class MagicsManager(Configurable):
    magics = Dict()

    def __init__(self, shell=None, config=None, user_magics=None, **traits):

        super(MagicsManager, self).__init__(shell=shell, config=config,
                                           user_magics=user_magics, **traits)
        self.magics = dict(line={}, cell={})
        # Let's add the user_magics to the registry for uniformity, so *all*
        # registered magic containers can be found there.
        self.registry[user_magics.__class__.__name__] = user_magics

    def register_function(self, func, magic_kind='line', magic_name=None):
        validate_type(magic_kind)
        magic_name = func.__name__ if magic_name is None else magic_name
        setattr(self.user_magics, magic_name, func)
        record_magic(self.magics, magic_kind, magic_name, func)


def record_magic(dct, magic_kind, magic_name, func):
    if magic_kind == 'line_cell':
        dct['line'][magic_name] = dct['cell'][magic_name] = func
    else:
        dct[magic_kind][magic_name] = func
```

というわけでMagicsManagerという所に登録される。実際これはIntractiveShellのクラスで初期化されている。

IPython/core/interactiveshell.py

```python
class InteractiveShell(SingletonConfigurable):
    """An enhanced, interactive shell for Python."""

    _instance = None

    magics_manager = Instance('IPython.core.magic.MagicsManager', allow_none=True)

    # __init__()で呼ばれる
    def init_magics(self):
        from IPython.core import magics as m
        self.magics_manager = magic.MagicsManager(shell=self,
                                   parent=self,
                                   user_magics=m.UserMagics(self))
        self.configurables.append(self.magics_manager)

        # Expose as public API from the magics manager
        self.register_magics = self.magics_manager.register

        self.register_magics(m.AutoMagics, m.BasicMagics, m.CodeMagics,
            m.ConfigMagics, m.DisplayMagics, m.ExecutionMagics,
            m.ExtensionMagics, m.HistoryMagics, m.LoggingMagics,
            m.NamespaceMagics, m.OSMagics, m.PylabMagics, m.ScriptMagics,
        )

        # Register Magic Aliases
        # ...
```

IPython.core.magicsにあるものがMagicsManagerに登録される。

### magic commandの解釈のされ方

InteractiveShellはshell(repl)なので何らかのloopの中でevalをするための入力を待っているというオブジェクト。のはず。そして今回で言えばevalというのは`run_cell()`というメソッドがそう(探し方はIpython.embed()で使われているInteractiveShellEmbedが呼ばれるとmain_loop()を呼び、それが内部で継承元のTerminalInteractiveShellのinteract()を呼び、このメソッドがrun_cell()を呼ぶという形でわかる（嘘です。雰囲気であたりをつけました）)。

IPython/core/interactiveshell.py

```python
class InteractiveShell(SingletonConfigurable):
    """An enhanced, interactive shell for Python."""

    def run_cell(self, raw_cell, store_history=False, silent=False, shell_futures=True):
        try:
            result = self._run_cell(
                raw_cell, store_history, silent, shell_futures)
        finally:
            self.events.trigger('post_execute')
            if not silent:
                self.events.trigger('post_run_cell', result)
        return result

    def _run_cell(self, raw_cell, store_history, silent, shell_futures):
        # 長いので省略
        ...
```

処理はほとんど内部の`_run_cell()` で行われているが[長すぎる](https://github.com/ipython/ipython/blob/d132824d870e07dbb04ae223ddecc0a3d5182c79/IPython/core/interactiveshell.py#L2669-L2801)ので省略(ちなみにこのあたりmasterだと実装が変わっていて[run_cell_asyncを呼ぶように変わっていたりする](https://github.com/ipython/ipython/blob/517ba8dff482073aef2abf58a89f5c5d23996573/IPython/core/interactiveshell.py#L2824-L2850))。

ちょっとさすがにこのあたりの説明の文章を逐一書くのはつらすぎるので例をあげてお茶濁すことにする。

#### %time Noneの例

例えば、作ったInteractiveShellに以下の様な入力を与えたとき、

```
%time None
```

内部的には、以下のような式に変換されて解釈されている。

```
get_ipython().run_line_magic('time', 'None')\n
```

それに対応する部分を先程の`_run_cell()`中で抜き出すと以下の様な感じ。

```python
class InteractiveShell(SingletonConfigurable):

    # This InputSplitter instance is used to transform completed cells before
    # running them. It allows cell magics to contain blank lines.
    input_transformer_manager = Instance('IPython.core.inputsplitter.IPythonInputSplitter',
                                         (), {'line_input_checker': False})


    def _run_cell(self, raw_cell, store_history, silent, shell_futures):
        # ...
        try:
            # Static input transformations
            cell = self.input_transformer_manager.transform_cell(raw_cell)
        except SyntaxError:
            preprocessing_exc_tuple = sys.exc_info()
            cell = raw_cell  # cell has to exist so it can be stored/logged
        # ...
```

このinput_transformerでraw_cellの値がcellに変換されている(`get_ipython()`を使った形式に変換されている)。
使われるのはInputSplitterというオブジェクト。このクラスの`transform_cell()`がmagic commandをpythonのコードに変換している。

IPython/core/inputsplitter.py

```python
class InputSplitter(object):

    def transform_cell(self, cell):
        """Process and translate a cell of input.
        """
        self.reset()
        try:
            self.push(cell)
            self.flush_transformers()
            return self.source
        finally:
            self.reset()
```

ただここだけみてもわからない通り、実際に変換しているのはinputtransformer.pyに定義されている変換用の関数が主。

IPython/core/inputtransformer.py

```python
ESC_MAGIC  = '%'     # Call magic function
ESC_MAGIC2 = '%%'    # Call cell-magic function

tr = { ESC_SHELL  : _tr_system,
       ESC_SH_CAP : _tr_system2,
       ESC_HELP   : _tr_help,
       ESC_HELP2  : _tr_help,
       ESC_MAGIC  : _tr_magic,
       ESC_QUOTE  : _tr_quote,
       ESC_QUOTE2 : _tr_quote2,
       ESC_PAREN  : _tr_paren }

@StatelessInputTransformer.wrap
def escaped_commands(line):
    """Transform escaped commands - %magic, !system, ?help + various autocalls.
    """
    if not line or line.isspace():
        return line
    lineinf = LineInfo(line)
    if lineinf.esc not in tr:
        return line
    
    return tr[lineinf.esc](lineinf)

def _tr_magic(line_info):
    "Translate lines escaped with: %"
    tpl = '%sget_ipython().run_line_magic(%r, %r)'
    if line_info.line.startswith(ESC_MAGIC2):
        return line_info.line
    cmd = ' '.join([line_info.ifun, line_info.the_rest]).strip()
    #Prepare arguments for get_ipython().run_line_magic(magic_name, magic_args)
    t_magic_name, _, t_magic_arg_s = cmd.partition(' ')
    t_magic_name = t_magic_name.lstrip(ESC_MAGIC)
    return tpl % (line_info.pre, t_magic_name, t_magic_arg_s)


# line-magicでもassign用のものは別途用意されている
@StatelessInputTransformer.wrap
def assign_from_magic(line):
    """Transform assignment from magic commands (e.g. a = %who_ls)"""
    ...

# cell-magic command の方は cellmagic()という関数などが定義される。
@CoroutineInputTransformer.wrap
def cellmagic(end_on_blank_line=False):
    """Captures & transforms cell magics.
    
    After a cell magic is started, this stores up any lines it gets until it is
    reset (sent None).
    """
    ...
```

これらはtransformerというオブジェクトになっている(`wrap()`は関数からオブジェクトを生成する関数を生成する関数)。

```python
class InputTransformer(metaclass=abc.ABCMeta):
    """Abstract base class for line-based input transformers."""
    
    @abc.abstractmethod
    def push(self, line):
        pass
    
    @abc.abstractmethod
    def reset(self):
        pass
    
    @classmethod
    def wrap(cls, func):
        """Can be used by subclasses as a decorator, to return a factory that
        will allow instantiation with the decorated object.
        """
        @functools.wraps(func)
        def transformer_factory(**kwargs):
            return cls(func, **kwargs)
        
        return transformer_factory
```

そしてこれらが先程のsplitterに渡される。そして先程の `transform_cell()` の中で `flush_transformers()` が呼ばれて、その中で登録されたtransformerが`push()`されまくる。

IPython/core/inputsplitter.py

```python
from IPython.core.inputtransformer import (leading_indent,
                                           classic_prompt,
                                           ipy_prompt,
                                           cellmagic,
                                           assemble_logical_lines,
                                           help_end,
                                           escaped_commands,
                                           assign_from_magic,
                                           assign_from_system,
                                           assemble_python_lines,
                                           )

class InputSplitter(object):
    def __init__(self, line_input_checker=True, physical_line_transforms=None,
                    logical_line_transforms=None, python_line_transforms=None):
        super(IPythonInputSplitter, self).__init__()
        self.physical_line_transforms = [
                                         leading_indent(),
                                         classic_prompt(),
                                         ipy_prompt(),
                                         cellmagic(end_on_blank_line=line_input_checker),  # <-
                                        ]
        self.logical_line_transforms = [
                                        help_end(),
                                        escaped_commands(), # <-
                                        assign_from_magic(),  # <-
                                        assign_from_system(),
                                       ]
```

実際以下の様なコードを書けば変換できる。

```python
from IPython.core.inputsplitter import IPythonInputSplitter

spliter = IPythonInputSplitter()

cell = "%time None"
print(spliter.transform_cell(cell))
# get_ipython().run_line_magic('time', 'None')
```

もっと言うと、内部では以下の様な感じで実行されている。

```python
from IPython.core.inputtransformer import escaped_commands

transformer = escaped_commands()

code = "%time None"
print(transformer.push(code))
# get_ipython().run_line_magic('time', 'None')
```

### magic commandの実行

あとは、変換後の`run_line_magic()`の部分で登録されたhook(magic)に渡されて実行される。これは本当に実行されているだけ。

ちなみ例にしているmagic commandのtimeの定義は[このあたり](https://github.com/ipython/ipython/blob/d132824d870e07dbb04ae223ddecc0a3d5182c79/IPython/core/magics/execution.py#L1129-L1258)。これも長いので省略。やっていることは、ASTをparseする時間、compileする時間、実行時間を調べるというようなもの。

IPython/core/magics/execution.py

```python
from IPython.utils.timing import clock, clock2

    def time(self,line='', cell=None, local_ns=None):
        expr = self.shell.input_transformer_manager.transform_cell(cell)

        ## parse ast
        tp_min = 0.1
        t0 = clock()
        expr_ast = self.shell.compile.ast_parse(expr)
        tp = clock()-t0

        ## compile
        tc_min = 0.1
        t0 = clock()
        code = self.shell.compile(expr_ast, source, mode)
        tc = clock()-t0

        ## execute
        st = clock2()
        try:
            exec(code, glob, local_ns)
        except:
            self.shell.showtraceback()
            return
        end = clock2()

        # Compute actual times and report
        cpu_user = end[0]-st[0]
        cpu_sys = end[1]-st[1]
        cpu_tot = cpu_user+cpu_sys
        print("CPU times: user %s, sys: %s, total: %s" % (_format_time(cpu_user),_format_time(cpu_sys),_format_time(cpu_tot)))
        if tc > tc_min:
            print("Compiler : %s" % _format_time(tc))
        if tp > tp_min:
            print("Parser   : %s" % _format_time(tp))
```

そんなわけで以下が動く。

```python
from IPython import get_ipython
from IPython import InteractiveShell

shell = InteractiveShell.instance()

ip = get_ipython()
# get_ipython().run_line_magic('time', 'None')\n に変換
ip.run_cell("%time None")

# CPU times: user 2 µs, sys: 0 ns, total: 2 µs
# Wall time: 3.58 µs
```

## 字句が解釈された結果どのように状態が変わるのか調べる

`%matplotlib inline` 解釈された結果についての把握に戻る。

実はmagic commandの定義の仕方などについて調べる前段階で見ていたページにもっと詳しいことが書いてあった。

- [Defining custom magics — IPython 6.5.0 documentation](https://ipython.readthedocs.io/en/stable/config/custommagics.html "Defining custom magics — IPython 6.5.0 documentation")

[%matplotlib](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-matplotlib)に関する説明。

```
 %matplotlib

    %matplotlib [-l] [gui]

  Set up matplotlib to work interactively.
```

IPython Notebook(jupyter notebook)用の説明まで書かれている。

> To enable the inline backend for usage with the IPython Notebook:
```
In [1]: %matplotlib inline
```

magic commandの解釈のされ方を覗いた結果、実装場所などが透けて見えるようになってきた。`%matplotlib` 行レベルのmagic commandなのだから、`%time` の時と同様の雰囲気で探していけば良い。つまるところIPython.core.magics付近を探していく。するとpylab.pyが見つかる。

IPython/core/magics/pylab.py

```python
@magics_class
class PylabMagics(Magics):
    """Magics related to matplotlib's pylab support"""
    
    @skip_doctest
    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-l', '--list', action='store_true',
                              help='Show available matplotlib backends')
    @magic_gui_arg
    def matplotlib(self, line=''):
        """Set up matplotlib to work interactively.
        
        This function lets you activate matplotlib interactive support
        at any point during an IPython session. It does not import anything
        into the interactive namespace.
        """
        args = magic_arguments.parse_argstring(self.matplotlib, line)
        if args.list:
            backends_list = list(backends.keys())
            print("Available matplotlib backends: %s" % backends_list)
        else:
            gui, backend = self.shell.enable_matplotlib(args.gui)
            self._show_matplotlib_backend(args.gui, backend)
```

そんなわけで `enable_matplotlib()` が呼ばれる。ここでのshellというのは、`IPython.core.interactiveshell.InteractiveShell` のこと。

IPython/core/interactiveshell.py

```python
class InteractiveShell(SingletonConfigurable):
    def enable_matplotlib(self, gui=None):
        from IPython.core import pylabtools as pt
        gui, backend = pt.find_gui_and_backend(gui, self.pylab_gui_select)
    
        if gui != 'inline':
            # If we have our first gui selection, store it
            if self.pylab_gui_select is None:
                self.pylab_gui_select = gui
            # Otherwise if they are different
            elif gui != self.pylab_gui_select:
                print('Warning: Cannot change to a different GUI toolkit: %s.'
                        ' Using %s instead.' % (gui, self.pylab_gui_select))
                gui, backend = pt.find_gui_and_backend(self.pylab_gui_select)
        
        pt.activate_matplotlib(backend)
        pt.configure_inline_support(self, backend)
        
        # Now we must activate the gui pylab wants to use, and fix %run to take
        # plot updates into account
        self.enable_gui(gui)
        self.magics_manager.registry['ExecutionMagics'].default_runner = \
            pt.mpl_runner(self.safe_execfile)
        
        return gui, backend
```

ptというのはIPython.core.pylabtoolsのことでここで定義されている関数群を呼び出して何かしら設定している模様。どこかで実行後の値にhookか何かをしているはず？

`configure_inline_support()` は以下の様な形(不要そうな条件分岐は取り除いている)。

IPython/core/pylabtools.py

```python
def configure_inline_support(shell, backend):
    from ipykernel.pylab.backend_inline import InlineBackend
    import matplotlib

    cfg = InlineBackend.instance(parent=shell)
    cfg.shell = shell
    shell.configurables.append(cfg)

    from ipykernel.pylab.backend_inline import flush_figures
    shell.events.register('post_execute', flush_figures)

    # Save rcParams that will be overwrittern
    shell._saved_rcParams = {}
    for k in cfg.rc:
        shell._saved_rcParams[k] = matplotlib.rcParams[k]

    # load inline_rc
    matplotlib.rcParams.update(cfg.rc)
    new_backend_name = "inline"

    # only enable the formats once -> don't change the enabled formats (which the user may
    # has changed) when getting another "%matplotlib inline" call.
    # See https://github.com/ipython/ipykernel/issues/29
    cur_backend = getattr(configure_inline_support, "current_backend", "unset")
    if new_backend_name != cur_backend:
        # Setup the default figure format
        select_figure_formats(shell, cfg.figure_formats, **cfg.print_figure_kwargs)
        configure_inline_support.current_backend = new_backend_name
```

結局、ipykernelのInlineBackendにたどり着く。ただし実際の定義はipykernel/pylab/config.pyの方にある。

ipykernel/pylab/config.py

```python

```


## version

見ていたパッケージのバージョンなどは以下。

```console
$ python -V
Python 3.7.0

$ pip freeze | grep -Pi 'ipykernel|matplotlib|ipython'
ipykernel==4.8.2
ipython==6.5.0
ipython-genutils==0.2.0
matplotlib==2.2.3
```

post execution
formatterという概念
- [Developer’s guide for third party tools and libraries — IPython 6.5.0 documentation](https://ipython.readthedocs.io/en/stable/development/ "Developer’s guide for third party tools and libraries — IPython 6.5.0 documentation")
- [Module: core.formatters — IPython 6.5.0 documentation](https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.formatters.html "Module: core.formatters — IPython 6.5.0 documentation")
- この辺で現状のmagic commandsの一覧も取得してみたくなったりする。

