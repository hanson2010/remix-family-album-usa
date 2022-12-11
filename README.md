# 给《走遍美国》加字幕

## 背景

走遍美国（Family Album, U.S.A.），是美国 Prentice Hall 出版社于 1991 年出版的一套英语教材，配有情景剧，共 26 集。

网上常见的视频版本或者带有大量广告字样，或者没有字幕。在此使用开源软件对字幕进行修正，供有兴趣的同学参考使用。涉及外部资料均来自公开网络，请尊重原始作者版权，勿用于商业用途。

为方便英文学习者使用，并保持画面简洁，采取只保留英文字幕的方式操作。

## 进虚拟环境

```bash
cd envs
python -m venv sandbox
cd
source envs/sandbox/bin/activate

# 验证是否已进虚拟环境
which python
```

## 准备工具

以下使用开源项目 [srt](https://github.com/cdown/srt) 和 [zhon](https://github.com/tsroten/zhon) 。

```bash
pip install srt
pip install zhon
```

## 处理 srt 文件

把下载好的 srt 文件放在 `~/remix-family-album-usa/orig` 目录。

```bash
cd remix-family-album-usa

# 改变原始文件编码
mkdir 01
for file in orig/*; do
    iconv -f gb18030 -t utf-8 $file -o 01/$(basename $file)
done

# 删除中文（删除第一个中文字到行尾），以及空白行
./remove_zh.py 01 02

# 替换或删除第 0 号字幕，修正人为错误
vi 02/01.srt
...

# 标准化
mkdir 03
srt normalise --input 02/01.srt --output 03/01.srt
srt normalise --input 02/02.srt --output 03/02.srt
srt normalise --input 02/03.srt --output 03/03.srt
...
```

运行`srt normalise`时不建议以批处理方式执行，因为需留意报错信息，并手工处理，具体包括：

1. 起止时间不合法，字幕被清理；

2. 未翻译人名等英文，从而未被删除造成字幕重复。

以下进行时移和拼接。

```bash
# 时移
mkdir 04
srt fixed-timeshift --seconds -19 --input 03/01.srt --output 04/01.srt
srt fixed-timeshift --seconds 483.5 --input 03/02.srt --output 04/02.srt
srt fixed-timeshift --seconds 855.5 --input 03/03.srt --output 04/03.srt
...

# 拼接
mkdir 05
cat author.srt 04/01.srt 04/02.srt 04/03.srt > 05/01.srt
...

# 标准化
mkdir final
srt normalise --input 05/01.srt --output final/01.srt
...
```

## 视频混合

以下使用著名的开源软件 [ffmpeg](https://ffmpeg.org/) 。

```bash
sudo apt install ffmpeg

ffmpeg -i video/FAUSA_01.mp4 -i final/01.srt -c:v libx265 -tag:v hvc1 -filter:v unsharp -c:a copy -c:s srt video/FAUSA_01.mkv
...
```

其中：

1. `-c:v libx265 -tag:v hvc1`表示视频使用 HEVC (x265) 编码；

2. `-filter:v unsharp` 可以实现视频锐化，默认参数即可满足需求；

3. `-c:a copy`表示原样拷贝音频轨道；

4. `-c:s srt`指定字幕编码方式；

5. 输出文件以`.mkv`命名，ffmpeg 就冰雪聪明的明白封装格式意图了。
