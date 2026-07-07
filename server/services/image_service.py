from PIL import Image
import io
import uuid

from settings.config import *

class ImageService():
    #метод который создает изображения типа pillow из байтов
    def image_from_bytes(self, image_bytes:bytes):
        return Image.open(io.BytesIO(image_bytes))
    
    #Обрезка изображения
    def cut_image(self, image:Image):
        width, height = image.size

        #если размеры изображения больше стандартного, тогда обрезаем изображение
        height_cut = HEIGHT_CUT if height > IMAGE_STANDART else 0
        sides_cut = SIDES_CUT if width > IMAGE_STANDART else 0

        #обрезаем изображение и возвращаем
        return image.crop((sides_cut, height_cut, width-sides_cut, height-height_cut))
    
    #возвращает байты сжатого изображения. Изображение сжимается в зависимости от настроек конфига
    def compress_image(self, image:Image):
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=IMAGE_QUALITY, speed=CUT_SPEED)

        return buffer.getvalue()

    #конвертация изображения pillow в байты
    def get_bytes_image(self, image:Image):
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        
        return buffer.getvalue()