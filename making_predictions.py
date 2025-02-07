from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from ultralytics import YOLO

model_path = 'best.pt'
image_path = 'folder_with_photos/6.jpeg'

# Загрузка модели
model = YOLO(model_path)

# Загрузка изображения
image = Image.open(image_path)
results = model(image)


# Функция для отрисовки bbox и масок
def draw_bboxes_and_masks(image, results):
    draw = ImageDraw.Draw(image)

    for result in results[0].boxes.data:
        x_min, y_min, x_max, y_max, confidence, class_id = result

        # Преобразование координат к целым числам
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

        draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=3)

        label = f"{model.model.names[int(class_id)]} {confidence:.2f}"
        draw.text((x_min, y_min - 10), label, fill="red")

    return image


result_image = draw_bboxes_and_masks(image.copy(), results)

# Отображение результата
plt.figure(figsize=(10, 10))
plt.imshow(result_image)
plt.axis('off')
plt.show()
