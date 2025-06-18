import os
import uuid
from fastapi import UploadFile
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MEDIA_DIR = BASE_DIR / 'media'
MEDIA_URL = '/media'

MEDIA_DIR.mkdir(parents=True, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
    """
    Сохраняет UploadFile на диск в папку media/ и возвращает публичный URL
    """
    # Генерируем уникальное имя с сохранением расширения
    ext = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = MEDIA_DIR / unique_name

    # Записываем файл
    with file_path.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Формируем публичный URL
    return f"{MEDIA_URL}/{unique_name}"

async def delete_media_file(public_url: str):
    """Удаляет файл с диска по его публичному URL"""
    filename = public_url.rsplit('/', 1)[-1]
    file_path = MEDIA_DIR / filename
    if file_path.exists():
        file_path.unlink()


