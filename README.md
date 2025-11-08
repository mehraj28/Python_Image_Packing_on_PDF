Learn Basics Take-Home Task: Image Packing on PDF

Task Overview
Your goal is to implement a Python program that arranges a set of images of random sizes and shapes into a PDF in a way that minimizes the total space used, while preserving each image's original aspect ratio.

# Image Packing & PDF Generator

This project reads a set of images (optionally with transparent backgrounds), optimizes their placement using a smart packing algorithm, and exports them into a compact multi-page PDF.

---

## Features

- ✅ Automatically removes transparent backgrounds (optional step).
- ✅ Crops images to visible bounding boxes while preserving aspect ratio.
- ✅ Efficiently packs multiple images on each PDF page to minimize white space.
- ✅ Supports multiple image formats (`.png`, `.jpg`, `.jpeg`).
- ✅ Outputs a clean, high-quality `output.pdf`.

---

## Project Structure

python_hiring_task_1/
│
├── input_images/ # Folder containing all input images
├── output.pdf # Generated after running the script
├── sample_data_generation.py # Utility script to generate sample images
├── task_1_starter_code.py # Main image packing and PDF generation logic
├── requirements.txt # Dependencies list
└── README.md # Instructions file



## Setup Instructions

### Clone the Repository

git clone https://github.com/code-learnbasics/python_hiring_task_1.git
cd python_hiring_task_1

Create a Virtual Environment
python -m venv venv

Activate it:

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Option A-Generate Sample Images
If you don’t have images yet, generate some test data:
python sample_data_generation.py
This will create a set of images inside the input_images/ folder.

Option B — Use Your Own Images
Place your .png, .jpg, or .jpeg files inside the input_images/ folder.

Run the Main Script
python task_1_starter_code.py

This will:

Preprocess images (remove transparency and crop).

Pack them efficiently on each PDF page.

Save the final result as output.pdf.

Output

The final PDF (output.pdf) will be created in the project root.

Transparent areas are preserved in final rendering.

All provided images are packed efficiently with minimal empty space.

