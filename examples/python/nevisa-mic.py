from nevisa_file_api import *
import socketio
import pyaudio
import threading
import requests
import subprocess
import ffmpeg
import io

# تنظیمات استریم صوتی
CHUNK = 1024  # تعداد فریم‌ها در هر بافر
FORMAT = pyaudio.paInt16  # فرمت صوتی
CHANNELS = 1  # تعداد کانال‌ها
RATE = 16000  # نرخ نمونه‌برداری (در هرتز)

#sio = socketio.Client(logger=True, engineio_logger=True) # For Debugging
http_session = requests.Session()
http_session.verify = False
sio = socketio.Client(http_session=http_session)
recording = False
stream = None
audio_interface = None

# Event handlers
@sio.event
def connect():
    print("connected")

@sio.event
def disconnect():
    print("disconnected")

@sio.on('result')
def on_result(data):
    if "result" in data:
        print("Received result:", data["text"])

@sio.on('start-microphone')
def on_start_microphone(data):
    print("on_start_microphone:")
    if data.get("lockChecked", False):
        print("lockChecked")
        stream_audio()
# تابعی برای استریم و ارسال صدا
def stream_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # تنظیمات ffmpeg برای تبدیل صوت به فرمت webm
    process = (
        ffmpeg
        .input('pipe:0', format='s16le', ac=CHANNELS, ar=RATE)
        .output('pipe:1', format='webm', codec='libopus')
        .run_async(pipe_stdin=True, pipe_stdout=True)
    )

    def send_audio():
        while True:
            data = process.stdout.read(CHUNK)
            if not data:
                break
            sio.emit('microphone-blob', data)  # ارسال داده‌های صوتی به سرور

    threading.Thread(target=send_audio, daemon=True).start()

    while True:
        data = stream.read(CHUNK)
        process.stdin.write(data)


def stop_recording():
    print("stop_recording:")
    sio.emit('stop-microphone')

if __name__ == '__main__':
    try:
        # Login --------------------------------------
        token, code = login("username", "password")

        sio.connect(SERVER_ADDRESS, headers={'token': token, 'platform': 'browser'})

        sio.emit('start-microphone')

        sio.wait()
    except KeyboardInterrupt: # stop on ctrl + c
        pass
    finally:
        stop_recording()
