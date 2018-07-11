## zmqを使っている部分を調べてみる

```
$ TARGETDIR=~/venvs/viz
$ mkdir -p data
$ (cd $TARGETDIR && find . -name "*.py" | grep -v lib/ | xargs grep zmq -l 2>/dev/null) | sort > data/zmq.files
```
