import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

# Function to select a file
def select_file(file_type):
    file_path = filedialog.askopenfilename()
    if file_type == "cover":
        cover_file_label.config(text=file_path)
    elif file_type == "payload":
        payload_file_label.config(text=file_path)
    elif file_type == "stego":
        stego_file_label.config(text=file_path)
    return file_path

# Function to encode text into an image
def encode():
    cover_path = cover_file_label.cget("text")
    payload_path = payload_file_label.cget("text")
    bits = int(bits_entry.get())
    
    if not cover_path or not payload_path:
        messagebox.showerror("Error", "Please select both cover and payload files.")
        return
    
    # Load cover image
    cover_image = Image.open(cover_path)
    cover_array = np.array(cover_image)

    # Read payload text
    with open(payload_path, 'r') as file:
        payload = file.read()
    
    # Convert payload to binary
    payload_bin = ''.join(format(ord(char), '08b') for char in payload)
    payload_len = len(payload_bin)

    # Check if payload can be hidden in cover image
    if payload_len > cover_array.size * bits:
        messagebox.showerror("Error", "Payload is too large to hide in the selected cover image.")
        return
    
    # Encode payload into cover image
    flat_cover_array = cover_array.flatten()
    for i in range(0, payload_len, bits):
        byte = flat_cover_array[i//bits]
        for bit_index in range(bits):
            if i + bit_index < payload_len:
                bit = int(payload_bin[i + bit_index])
                byte = (byte & ~(1 << bit_index)) | (bit << bit_index)
        flat_cover_array[i//bits] = byte
    
    stego_array = flat_cover_array.reshape(cover_array.shape)
    stego_image = Image.fromarray(stego_array)
    stego_image_path = "stego_image.png"
    stego_image.save(stego_image_path)
    stego_file_label.config(text=stego_image_path)
    messagebox.showinfo("Success", "Payload has been successfully encoded into the cover image.")

# Function to decode text from an image
def decode():
    stego_path = stego_file_label.cget("text")
    bits = int(bits_entry.get())
    
    if not stego_path:
        messagebox.showerror("Error", "Please select a stego file.")
        return
    
    # Load stego image
    stego_image = Image.open(stego_path)
    stego_array = np.array(stego_image)
    
    # Extract payload from stego image
    flat_stego_array = stego_array.flatten()
    payload_bin = ''
    for i in range(0, flat_stego_array.size, bits):
        byte = flat_stego_array[i//bits]
        for bit_index in range(bits):
            bit = (byte >> bit_index) & 1
            payload_bin += str(bit)
    
    # Convert binary payload to text
    payload = ''
    for i in range(0, len(payload_bin), 8):
        byte = payload_bin[i:i+8]
        if len(byte) == 8:
            char = chr(int(byte, 2))
            payload += char
    
    messagebox.showinfo("Decoded Payload", f"Decoded text: {payload}")

# Main GUI setup
root = tk.Tk()
root.title("LSB Steganography")

tk.Label(root, text="Cover File:").grid(row=0, column=0, padx=10, pady=10)
cover_file_label = tk.Label(root, text="")
cover_file_label.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Select Cover File", command=lambda: select_file("cover")).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Payload File:").grid(row=1, column=0, padx=10, pady=10)
payload_file_label = tk.Label(root, text="")
payload_file_label.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Select Payload File", command=lambda: select_file("payload")).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Stego File:").grid(row=2, column=0, padx=10, pady=10)
stego_file_label = tk.Label(root, text="")
stego_file_label.grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Select Stego File", command=lambda: select_file("stego")).grid(row=2, column=2, padx=10, pady=10)

tk.Label(root, text="Number of LSBs:").grid(row=3, column=0, padx=10, pady=10)
bits_entry = tk.Entry(root)
bits_entry.grid(row=3, column=1, padx=10, pady=10)
bits_entry.insert(0, "1")

tk.Button(root, text="Encode", command=encode).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Decode", command=decode).grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
