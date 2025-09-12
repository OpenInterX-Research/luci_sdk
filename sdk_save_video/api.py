from luci_sdk import RtspRecorder
import time

rec = RtspRecorder(
    rtsp_url="rtsp://192.168.137.54:50001/live/0",
    ffmpeg_path=r"C:\Users\vq24975\Downloads\ffmpeg-7.0.2-full_build\ffmpeg-7.0.2-full_build\bin\ffmpeg.exe",
    save_dir="recording",
    segment_time=60
)

rec.start()
time.sleep(120)   # 录制 2 分钟
rec.stop()