import os
import telebot
import torch
from PIL import Image, ImageDraw
from ultralytics import YOLO

# Загрузка модели
MODEL_PATH = "best.pt"
model = YOLO(MODEL_PATH)

TOKEN = "your token"
bot = telebot.TeleBot(TOKEN)


def draw_bboxes(image, results):
    draw = ImageDraw.Draw(image)
    for result in results[0].boxes.data:
        x_min, y_min, x_max, y_max, confidence, class_id = result.tolist()
        x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
        draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=3)
        label = f"{model.model.names[int(class_id)]} {confidence:.2f}"
        draw.text((x_min, y_min - 10), label, fill="red")
    return image


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Отправьте мне фото, и я обработаю его.")


@bot.message_handler(content_types=["photo"])
def process_image(message):
    processing_msg = bot.reply_to(message, "Фото обрабатывается ...")

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_path = "input.jpg"
    output_path = "output.jpg"

    with open(image_path, "wb") as file:
        file.write(downloaded_file)

    image = Image.open(image_path)
    results = model(image)
    processed_image = draw_bboxes(image.copy(), results)
    processed_image.save(output_path)

    with open(output_path, "rb") as file:
        bot.send_photo(message.chat.id, file)

    bot.delete_message(message.chat.id, processing_msg.message_id)

    os.remove(image_path)
    os.remove(output_path)


bot.polling(none_stop=True)
