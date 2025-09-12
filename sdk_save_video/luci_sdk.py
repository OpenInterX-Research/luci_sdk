import subprocess
import os
import signal
import platform


class RtspRecorder:
    def __init__(self, rtsp_url, ffmpeg_path="ffmpeg", save_dir="recording", segment_time=60):
        self.rtsp_url = rtsp_url
        self.ffmpeg_path = ffmpeg_path
        self.save_dir = save_dir
        self.segment_time = segment_time
        self.proc = None

        os.makedirs(save_dir, exist_ok=True)

    def start(self):
        """启动录制"""
        if self.proc is not None:
            raise RuntimeError("Recorder already running!")

        output_pattern = os.path.join(self.save_dir, "output_%Y-%m-%d_%H-%M-%S.h264")

        command = [
            self.ffmpeg_path,
            "-i", self.rtsp_url,
            "-c", "copy",
            "-an",                       # 去掉音频
            "-f", "segment",
            "-segment_time", str(self.segment_time),
            "-reset_timestamps", "1",
            "-strftime", "1",
            output_pattern
        ]

        self.proc = subprocess.Popen(command)
        print(f"[Recorder] Started recording RTSP stream to {self.save_dir}")

    def stop(self):
        """安全停止录制，保存当前文件"""
        if self.proc is None:
            print("[Recorder] Not running.")
            return

        print("[Recorder] Stopping...")

        try:
            if platform.system() == "Windows":
                self.proc.terminate()  # Windows 下 terminate 就能触发 ffmpeg flush
            else:
                self.proc.send_signal(signal.SIGINT)  # Linux/macOS 用 SIGINT
            self.proc.wait()
        except Exception as e:
            print(f"[Recorder] Error stopping process: {e}")
        finally:
            self.proc = None
            print("[Recorder] Recording stopped and files saved.")