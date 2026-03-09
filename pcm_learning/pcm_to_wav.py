import wave
import os

def pcm_to_wav(pcm_filename, wav_filename, channels=1, sample_width=2, frame_rate=44100):
    """
    将裸 PCM 文件封装为 WAV 格式。
    
    参数:
    - pcm_filename: 输入 PCM 文件路径
    - wav_filename: 输出 WAV 文件路径
    - channels: 声道数 (1=单声道, 2=立体声)
    - sample_width: 每个样本的字节数 (1=8bit, 2=16bit, 4=32bit)
    - frame_rate: 采样率 (Hz)
    """
    
    if not os.path.exists(pcm_filename):
        print(f"错误: 找不到 PCM 文件: {pcm_filename}")
        return

    print(f"正在将 PCM 转换为 WAV: {wav_filename}")
    print(f"参数: 声道={channels}, 位深={sample_width*8}bit, 采样率={frame_rate}Hz")

    try:
        # 打开 PCM 文件读取所有字节
        with open(pcm_filename, 'rb') as pcm_file:
            pcm_data = pcm_file.read()
            
        # 打开 WAV 文件进行写入
        with wave.open(wav_filename, 'wb') as wav_file:
            # 设置参数
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(frame_rate)
            
            # 写入音频数据
            wav_file.writeframes(pcm_data)
            
        print("转换成功！可以使用任意播放器播放该 WAV 文件。")
        
    except Exception as e:
        print(f"转换失败: {e}")

if __name__ == "__main__":
    # 假设之前的生成脚本生成了 sine_wave_440hz.pcm
    # 参数必须匹配生成脚本中的设定 (44100Hz, 16-bit Mono -> sample_width=2, channels=1)
    pcm_file = "sine_wave_440hz.pcm"
    wav_file = "sine_wave_440hz.wav"
    
    pcm_to_wav(pcm_file, wav_file)
