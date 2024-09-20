import argparse
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import os


def generate_barcode(code, image_name):
    EAN = barcode.get_barcode_class("code128")
    ean = EAN(code, writer=ImageWriter())
    ean.save(image_name)


def create_barcode_image(codes, output_image="combined_barcodes.png"):
    barcode_images = []

    # Generate and collect barcode images
    for i, code in enumerate(codes):
        image_name = f"barcode_{i}"
        generate_barcode(code, image_name)
        barcode_images.append(Image.open(f"{image_name}.png"))

    width, height = barcode_images[0].size
    total_height = height * len(barcode_images)

    # Create a new blank image to combine all barcodes
    combined_image = Image.new("RGB", (width, total_height))

    # Paste barcodes into the combined image and delete intermediate images
    y_offset = 0
    for i, barcode_img in enumerate(barcode_images):
        combined_image.paste(barcode_img, (0, y_offset))
        y_offset += height
        barcode_img.close()  # Close the image to release resources
        os.remove(f"barcode_{i}.png")  # Delete the intermediate barcode image

    combined_image.save(output_image)

    print(f"Combined barcode image saved as {output_image}")


def read_barcodes_from_file(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    parser = argparse.ArgumentParser(description="Generate barcodes and combine them into a single image.")

    parser.add_argument(
        "codes",
        metavar="CODES",
        type=str,
        nargs="*",
        help="List of barcode numbers to generate (supports alphanumeric)."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="File containing barcode numbers (one per line)."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="combined_barcodes.png",
        help="Output image file name (default: combined_barcodes.png)."
    )

    args = parser.parse_args()

    # Check if a file is provided; if so, read barcodes from the file
    if args.file:
        codes = read_barcodes_from_file(args.file)
    else:
        codes = args.codes

    # Ensure we have some codes to process
    if not codes:
        print("Error: No barcodes provided. Use either a list of codes or a file.")
        return

    # Generate and combine barcode images
    create_barcode_image(codes, args.output)


if __name__ == "__main__":
    main()
