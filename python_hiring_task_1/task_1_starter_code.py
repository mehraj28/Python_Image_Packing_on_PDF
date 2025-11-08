import os
from io import BytesIO
from PIL import Image, ImageChops
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


INPUT_DIR = "input_images"
OUTPUT_PDF = "output.pdf"
PAGE_SIZE = A4  # width, height in points (1 pt = 1/72 inch) 

# 1. PREPROCESS IMAGES

def preprocess_image(image_path: str):
    """
    Remove transparent background and crop to visible area.
    Preserves aspect ratio and returns preprocessed Pillow Image.
    """
    img = Image.open(image_path).convert("RGBA")

    # Remove fully transparent areas
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Remove alpha if present — convert transparent pixels to white background
    background = Image.new("RGBA", img.size, (255, 255, 255, 0))
    background.paste(img, mask=img)
    return background

# 2. PACK IMAGES INTO PAGES — ROW-WISE LAYOUT

def pack_images(images, page_width, page_height, padding=10):
    """
    Packs images row-wise on a page while preserving aspect ratio.
    Returns (placements, remaining_images)
    """
    placements = []
    remaining = []

    x_cursor, y_cursor = padding, padding
    max_row_height = 0

    for img in images:
        w, h = img.size

        # Scale down if image is too wide
        if w > page_width - 2 * padding:
            scale = (page_width - 2 * padding) / w
            w, h = int(w * scale), int(h * scale)
            img = img.resize((w, h), Image.LANCZOS)

        # Move to next row if not enough horizontal space
        if x_cursor + w + padding > page_width:
            x_cursor = padding
            y_cursor += max_row_height + padding
            max_row_height = 0

        # If not enough vertical space → move to next page
        if y_cursor + h + padding > page_height:
            remaining.append(img)
            continue

        placements.append((img, x_cursor, page_height - y_cursor - h))
        x_cursor += w + padding
        max_row_height = max(max_row_height, h)

    return placements, remaining

# 3. COMPRESS IMAGES

def compress_images(input_image_path: str, output_image_path: str, compression_level: int = 5):
    """Compress image using Pillow"""
    img = Image.open(input_image_path).convert("RGB")
    img.save(output_image_path, format="JPEG", optimize=True, quality=max(10, 100 - compression_level * 10))
    return output_image_path

# 4. GENERATE PDF

def generate_pdf(input_dir: str, output_pdf_path: str, page_size):
    """
    Reads all images, preprocesses them, packs optimally, and generates a PDF.
    """
    page_width, page_height = page_size
    image_paths = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not image_paths:
        print("⚠️ No images found in input_images/. Run sample_data_generation.py first.")
        return

    # Preprocess and sort (largest first)
    images = [preprocess_image(p) for p in image_paths]
    images.sort(key=lambda im: im.size[0] * im.size[1], reverse=True)

    c = canvas.Canvas(output_pdf_path, pagesize=page_size)
    remaining = images
    page_num = 1

    while remaining:
        placements, remaining = pack_images(remaining, page_width, page_height)

        if not placements:
            print("⚠️ No more images fit on this page, ending.")
            break

        print(f"🧩 Adding page {page_num} with {len(placements)} images...")

        for img, x, y in placements:
            if img.mode == "RGBA":
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg

            # Convert to bytes and draw directly (no temp file)
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG", optimize=True)
            img_bytes.seek(0)
            c.drawImage(ImageReader(img_bytes), x, y, width=img.width, height=img.height, mask='auto')

        c.showPage()
        page_num += 1

    c.save()
    print(f"✅ PDF generated successfully: {output_pdf_path}")


# 5. ENTRY POINT

if __name__ == "__main__":
    
    generate_pdf(INPUT_DIR, OUTPUT_PDF, PAGE_SIZE)