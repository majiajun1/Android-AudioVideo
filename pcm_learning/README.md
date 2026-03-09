# PCM (Pulse Code Modulation) 脉冲编码调制

## 什么是 PCM？

PCM（Pulse Code Modulation，脉冲编码调制）是一种将模拟信号（如声音）转换为数字信号的方法。它是计算机音频中最基础、最原始的数据格式。

简单来说，PCM 就是对模拟波形进行**采样（Sampling）**、**量化（Quantization）**和**编码（Encoding）**的过程。

## 核心概念

### 1. 采样率 (Sample Rate)
- **定义**: 每秒钟采集声音样本的次数。
- **单位**: Hz (赫兹)。
- **常见值**:
    - 44100 Hz (44.1 kHz): CD 音质。
    - 48000 Hz (48 kHz): DVD、视频标准。
    - 8000 Hz: 电话音质。
- **原理**: 根据奈奎斯特采样定理，采样率必须大于信号最高频率的2倍，才能无失真地还原信号。人耳听力范围约 20Hz-20kHz，所以 44.1kHz 足够覆盖。

### 2. 位深 (Bit Depth / Sample Size)
- **定义**: 每个样本用来存储振幅信息的比特数。
- **常见值**:
    - 8-bit: 256 个级别 (0-255)，动态范围较小，有底噪。
    - 16-bit: 65536 个级别 (-32768 到 32767)，CD 标准，动态范围大。
    - 24-bit / 32-bit:用于专业音频录制。
- **原理**: 位深越大，记录的振幅越精确，信噪比（SNR）越高。

### 3. 声道数 (Channels)
- **单声道 (Mono)**: 1 个声道。
- **立体声 (Stereo)**: 2 个声道（左、右）。
- **多声道**: 5.1, 7.1 等。
- **数据排列**: 在 PCM 数据中，立体声样本通常是交错排列的：`左声道样本1, 右声道样本1, 左声道样本2, 右声道样本2...`

## PCM 数据量计算

未经压缩的 PCM 音频数据量非常大。计算公式：

```
数据量 (字节) = (采样率 × 位深 × 声道数 × 时间秒数) / 8
```

例如：录制 1 分钟 CD 音质 (44.1kHz, 16-bit, Stereo)
`44100 * 16 * 2 * 60 / 8 = 10,584,000 bytes ≈ 10.1 MB`

## PCM vs WAV

- **PCM**: 裸数据 (Raw Data)，没有任何头信息。播放器不知道采样率和位深，无法正确播放，除非手动指定参数。
- **WAV**: 微软的一种容器格式。通常就是 `WAV Header + PCM Data`。WAV 头部包含了采样率、位深、声道数等信息，所以播放器可以直接播放。

## 常见存储格式

- **Little Endian (小端序)**: 多数 PCM 文件（如 WAV 中的 PCM）使用小端序存储（低位字节在前）。
- **Big Endian (大端序)**: 某些特定平台或格式使用。
- **Signed vs Unsigned**:
    - 8-bit 通常是 Unsigned (0 ~ 255, 静音是 128)。
    - 16-bit 通常是 Signed (-32768 ~ 32767, 静音是 0)。

## 如何播放 Raw PCM？

由于 PCM 文件没有头信息，播放器不知道如何解析它。

### 方法 1: 转换为 WAV (推荐)
使用我们提供的 `pcm_to_wav.py` 脚本，将其包装成 WAV 格式即可直接播放。

### 方法 2: 使用 Audacity
1. 打开 Audacity。
2. 选择 `文件 -> 导入 -> 原始数据 (Raw Data)`。
3. 设置参数:
   - Encoding: Signed 16-bit PCM
   - Byte order: Little-endian
   - Channels: 1 (Mono)
   - Sample rate: 44100 Hz

### 方法 3: 使用 FFmpeg (ffplay)
如果你安装了 FFmpeg，可以使用命令行播放：

```bash
ffplay -f s16le -ar 44100 -ac 1 sine_wave_440hz.pcm
```

- `-f s16le`: 格式为 Signed 16-bit Little Endian
- `-ar 44100`: 采样率 44100 Hz
- `-ac 1`: 单声道
