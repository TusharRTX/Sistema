from PIL import Image
import os

input_folder = "input"
output_folder = "output"
canvas_size = (1024, 1024)
scale_factor = 0.7

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path).convert("RGBA")

        original_width, original_height = image.size
        max_width = int(canvas_size[0] * scale_factor)
        max_height = int(canvas_size[1] * scale_factor)

        ratio = min(max_width / original_width, max_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

        paste_position = (
            (canvas_size[0] - new_size[0]) // 2,
            (canvas_size[1] - new_size[1]) // 2,
        )

        canvas.paste(resized_image, paste_position, resized_image)
        canvas.save(os.path.join(output_folder, filename))
