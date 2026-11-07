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
pip install -r requirements.txt
```

## 处理 srt 文件

把下载好的 srt 文件放在 `~/remix-family-album-usa/01-original` 目录。

```bash
cd remix-family-album-usa

# 转为 UTF-8 编码，删除行尾空白和回车符，删除第 0 号字幕（前 9 行），输出到 02-utf8/
bash 02-convert-utf8.sh

# 删除中文（删除第一个中文字到行尾），以及空白行
./03-remove-chinese.py 02-utf8 03-english

# 修正人为错误
# 后续不要再覆盖此目录
vi 03-english/01.srt
...

# 标准化
mkdir 04-normalised
srt normalise --input 03-english/01.srt --output 04-normalised/01.srt
srt normalise --input 03-english/02.srt --output 04-normalised/02.srt
srt normalise --input 03-english/03.srt --output 04-normalised/03.srt
...
```

运行`srt normalise`时不建议以批处理方式执行，因为需留意报错信息，并手工处理，具体包括：

1. 起止时间不合法，字幕被清理；

2. 未翻译人名等英文，从而未被删除造成字幕重复。

以下进行时移和拼接。

```bash
# 时移
mkdir 05-timeshifted
srt fixed-timeshift --seconds -19 --input 04-normalised/01.srt --output 05-timeshifted/01.srt
srt fixed-timeshift --seconds 483 --input 04-normalised/02.srt --output 05-timeshifted/02.srt
srt fixed-timeshift --seconds 855 --input 04-normalised/03.srt --output 05-timeshifted/03.srt
...

# 拼接
mkdir 07-concatenated
cat 06-titles/author.srt 06-titles/01.srt 05-timeshifted/01.srt 05-timeshifted/02.srt 05-timeshifted/03.srt > 07-concatenated/01.srt
...

# 标准化
mkdir 08-prefinal
srt normalise --input 07-concatenated/01.srt --output 08-prefinal/01.srt
...

# 使用专业工具继续修正，例如Aegisub
mkdir 09-final
cp 08-prefinal/* 09-final
...
```

## 视频转码与字幕混合

以下使用著名的开源软件 [ffmpeg](https://ffmpeg.org/) ，在仓库根目录运行。原始 H.264 视频放在 `video/h264/` 目录。

```bash
sudo apt install ffmpeg

# 1. 转码为 H.265/HEVC，输出到 video/h265/（耗时长，只需做一次）
bash 10-encode-h265.sh

# 2. 混入软字幕，输出到 video/softsubs/（不重新编码，字幕修改后重跑即可）
bash 11-mux-softsubs.sh

# 或者：烧录硬字幕，输出到 video/hardsubs/（烧录需要重新编码 H.265 视频）
bash 11-burn-hardsubs.sh
```

其中：

1. `-c:v libx265 -tag:v hvc1`表示视频使用 H.265/HEVC 编码；若要 AV1 编码，改为`-c:v libsvtav1 -crf 1`；

2. `-filter:v deblock=filter=weak:block=8,hqdn3d=2:1.5:3:3,deband,scale=480:360:flags=lanczos,setsar=1,unsharp=5:5:1.2:5:5:0,format=yuv420p10le`依次去块、轻度降噪、去色带、把画面还原为原片的 4:3 比例（原始视频为 540×360，被横向拉伸成 3:2；输出为 480×360 方形像素）、锐化亮度，并输出 10 位色深；`-crf 20 -preset slow`提高编码质量；`-color_primaries smpte170m -color_trc smpte170m -colorspace smpte170m -color_range tv`标明标清视频的 BT.601 色彩信息（原始视频未标明，Aegisub 等软件会提示缺少色彩矩阵）；

3. `-c:a copy`表示原样拷贝音频轨道；

4. `-c copy`表示原样拷贝视频和音频，只加入字幕轨道；`-metadata:s:s:0 language=eng`把字幕语言标为英语，`-disposition:s:0 default`把它设为默认字幕轨，播放时自动显示；

5. `subtitles=09-final/NN.srt`把字幕烧录进画面。第 18 集剧中电视播报员的 4 句台词以`{\an8}`开头，显示在画面顶部，与底部的人物对白同时出现；ffmpeg 与多数播放器支持这一标记，不支持的播放器会把它们显示在底部或显示出标记文字；

6. 输出文件以`.mkv`命名，ffmpeg 就冰雪聪明的明白封装格式意图了；文件名采用`Family Album U.S.A (1991) - S01E01 - 46 Linden Street.mkv`格式，VidHub 等媒体软件可据此从 TMDB 识别为同一部剧集。
