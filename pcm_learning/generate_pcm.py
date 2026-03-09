import math
import struct

def generate_pcm(filename, duration_seconds=5, sample_rate=44100, frequency=440, volume=0.5):
    """
    生成一个包含正弦波的原始 PCM 文件。
    
    参数:
    - filename: 输出文件名
    - duration_seconds: 音频时长（秒）
    - sample_rate: 采样率（Hz），默认 44100
    - frequency: 正弦波频率（Hz），默认 440 (A4音)
    - volume: 音量 (0.0 到 1.0)
    """
    
    print(f"正在生成 PCM 文件: {filename}")
    print(f"参数: 时长={duration_seconds}s, 采样率={sample_rate}Hz, 频率={frequency}Hz, 音量={volume}")

    # 计算总样本数
    total_samples = int(sample_rate * duration_seconds)
    
    # 16-bit 音频的最大振幅 (32767)
    max_amplitude = 32767 * volume

    with open(filename, 'wb') as f:
        for i in range(total_samples):
            # 计算当前样本的时间点 (t = i / sample_rate)
            t = i / sample_rate
            
            # 计算正弦波的值: sin(2 * pi * f * t)
            # 结果在 -1.0 到 1.0 之间
            sample_value = math.sin(2 * math.pi * frequency * t)
            
            # 缩放到 16-bit 整数范围
            pcm_value = int(sample_value * max_amplitude)
            
            # 写入二进制数据 (使用 struct.pack)
            # '<h' 表示: 小端序 (Little Endian), 有符号短整数 (signed short, 2 bytes)
            data = struct.pack('<h', pcm_value)
            f.write(data)
            
    print(f"生成完成！文件大小: {total_samples * 2} 字节")
    print("注意: 这是一个裸数据(Raw PCM)文件，普通播放器无法直接播放，")
    print("      或者需要手动指定参数 (44100Hz, 16-bit, Mono, Little Endian) 才能播放。")

if __name__ == "__main__":
    generate_pcm("sine_wave_440hz.pcm")
