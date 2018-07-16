## jupyter client

### kernel client

基本的に生成にはKernelManagerが要るけれど、以降はKernelClientだけで大丈夫な感じ。

`BlockingKernelClient` 見れば良い感じ。channelの話は[この辺](https://jupyter-client.readthedocs.io/en/stable/messaging.html?highlight=idle#introduction)。


これらは全部 `ZMQSocketChannel`

- shell
- iopub
- stdin

これだけ `HBChannel`

- heart beat

何か実行させたい場合にはshellのchannel、stdout,stderrなどを受け取りたいときにはstdin

待つときにはzmq.Pollerが使われているっぽい。

### ioloop

ioloopはどこで使われているんだろ？

### kernel app

appはどこで使われるんだろ？


