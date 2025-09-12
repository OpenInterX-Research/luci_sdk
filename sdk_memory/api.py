from sdk_memory import RtspRecorder
import time

rec = RtspRecorder(
    rtsp_url="rtsp://192.168.137.99:50001/live/0",
    ffmpeg_path=r"C:\Users\vq24975\Downloads\ffmpeg-7.0.2-full_build\ffmpeg-7.0.2-full_build\bin\ffmpeg.exe",
    save_dir="recording",
    mode="memory",
    buffer_size=60  # 缓存最近 60 秒
)


rec.start()
time.sleep(20)

# 导出最近 10 秒视频
rec.dump("last10s.ts", start=-10, end=0)

# 导出最近 30 到最近 15 秒之间的视频
rec.dump("mid_clip.ts", start=-30, end=-15)

rec.stop()
