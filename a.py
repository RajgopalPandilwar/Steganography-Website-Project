"""
Steganography Tool — Hide and extract secret messages within images.
Uses LSB (Least Significant Bit) steganography to embed text into image pixels.

Author: Rajgopal Pandilwar
"""

from PIL import Image
import numpy as np


def text_to_binary(text):
    """Convert a string to its binary representation (8 bits per character)."""
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    """Convert a binary string back to readable text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)


def embed_message(image_path, message, output_path):
    """
    Hide a secret message inside an image using LSB steganography.

    Args:
        image_path: Path to the cover image (PNG recommended).
        message: The secret text message to hide.
        output_path: Path where the steganographic image will be saved.
    """
    # Load the image and convert to RGB mode
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    # Append a delimiter to mark the end of the message
    message += "###END###"
    binary_msg = text_to_binary(message)

    # Check if the image can hold the message
    max_bits = pixels.shape[0] * pixels.shape[1] * 3  # 3 color channels
    if len(binary_msg) > max_bits:
        raise ValueError(f"Message too large! Max {max_bits // 8} chars, got {len(message)} chars.")

    # Embed each bit into the LSB of color channel values
    bit_idx = 0
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for channel in range(3):  # R, G, B
                if bit_idx < len(binary_msg):
                    # Clear the LSB and set it to the message bit
                    pixels[row, col, channel] = (pixels[row, col, channel] & 0xFE) | int(binary_msg[bit_idx])
                    bit_idx += 1

    # Save the steganographic image
    result = Image.fromarray(pixels)
    result.save(output_path)
    print(f"Message embedded successfully! Saved to {output_path}")


def extract_message(image_path):
    """
    Extract a hidden message from a steganographic image.

    Args:
        image_path: Path to the image containing a hidden message.

    Returns:
        The extracted secret message as a string.
    """
    # Load the image
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    # Extract LSB from each color channel
    binary_msg = ""
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for channel in range(3):
                binary_msg += str(pixels[row, col, channel] & 1)

    # Convert binary to text and find the delimiter
    extracted_text = ""
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        char = chr(int(byte, 2))
        if extracted_text.endswith("###END###"):
            break
        extracted_text += char

    # Remove the delimiter and return
    return extracted_text.replace("###END###", "")


# === Example Usage ===
if __name__ == "__main__":
    # To hide a message:
    # embed_message("cover_image.png", "This is a secret message!", "output_image.png")

    # To extract a message:
    # msg = extract_message("output_image.png")
    # print(f"Extracted message: {msg}")

    print("Steganography tool ready. Uncomment the example usage to test.")
