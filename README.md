## reality-of-Dream-of-Red-Mansions
Comparision analysis of words use between 1~80 chapters and 80~120 chapters of **A Dream of Red Mansions**. And then construct Support Vectors to determine who write the test chapters.

## 原理 

在学界一般认为，《红楼梦》后四十回并非曹雪芹所著。这里尝试应用机器学习的方法来分析文本中的词频的差异。主要使用下列文言虚词在章节中出现的频率构建特征向量。

```
之 其 或 亦 方 于 即 皆 因 仍 
故 尚 呢 了 的 着 一 不 乃 呀 
吗 咧 啊 罢 把 让 向 往 是 在 
越 再 更 比 很 偏 别 好 可 便 
就 但 儿
```

具体做法为：

1~20 回和 106~120 回分别作为正例(20回)和负例(15回)来训练模型。再对 21～105 回进行测试。

相关的著作见

> 施建军. (2011). 基于支持向量机技术的《 红楼梦》 作者研究. 红楼梦学刊, (5), 35-52.
