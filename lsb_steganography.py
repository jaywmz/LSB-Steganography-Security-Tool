import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import numpy as np

# Function to select a file
def select_file(file_type):
    file_path = filedialog.askopenfilename()
    update_file_label(file_path, file_type)
    return file_path

# Function to update the label text
def update_file_label(file_path, file_type):
    if file_type == "cover":
        cover_file_label.config(text=file_path)
        display_image(file_path, cover_canvas)
    elif file_type == "payload":
        payload_file_label.config(text=file_path)
    elif file_type == "stego":
        stego_file_label.config(text=file_path)
        display_image(file_path, stego_canvas)

# Function to display an image in a canvas
def display_image(file_path, canvas):
    image = Image.open(file_path)
    image.thumbnail((300, 300))  # Resize image to fit within the canvas
    img = ImageTk.PhotoImage(image)
    canvas.image = img  # Keep a reference to avoid garbage collection
    canvas.create_image(150, 150, image=img)

# Function to encode text into an image
def encode():
    cover_path = cover_file_label.cget("text")
    payload_path = payload_file_label.cget("text")
    try:
        bits = int(bits_entry.get())
        if bits < 1 or bits > 8:
            raise ValueError("Number of LSBs must be between 1 and 8.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
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
    display_image(stego_image_path, stego_canvas)
    messagebox.showinfo("Success", "Payload has been successfully encoded into the cover image.")

# Function to decode text from an image
def decode():
    stego_path = stego_file_label.cget("text")
    try:
        bits = int(bits_entry.get())
        if bits < 1 or bits > 8:
            raise ValueError("Number of LSBs must be between 1 and 8.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
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

# Function to handle drag-and-drop events
def drop(event, file_type):
    file_path = event.data
    if file_path.startswith('{') and file_path.endswith('}'):
        file_path = file_path[1:-1]  # Remove curly braces if present
    update_file_label(file_path, file_type)

# Main GUI setup
root = TkinterDnD.Tk()
root.title("LSB Steganography")

tk.Label(root, text="Cover File:").grid(row=0, column=0, padx=10, pady=10)
cover_file_label = tk.Label(root, text="", width=50)
cover_file_label.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Select Cover File", command=lambda: select_file("cover")).grid(row=0, column=2, padx=10, pady=10)
cover_file_label.drop_target_register(DND_FILES)
cover_file_label.dnd_bind('<<Drop>>', lambda event: drop(event, "cover"))

cover_canvas = tk.Canvas(root, width=300, height=300, bg="white")
cover_canvas.grid(row=0, column=3, padx=10, pady=10)

tk.Label(root, text="Payload File:").grid(row=1, column=0, padx=10, pady=10)
payload_file_label = tk.Label(root, text="", width=50)
payload_file_label.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Select Payload File", command=lambda: select_file("payload")).grid(row=1, column=2, padx=10, pady=10)
payload_file_label.drop_target_register(DND_FILES)
payload_file_label.dnd_bind('<<Drop>>', lambda event: drop(event, "payload"))

tk.Label(root, text="Stego File:").grid(row=2, column=0, padx=10, pady=10)
stego_file_label = tk.Label(root, text="", width=50)
stego_file_label.grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Select Stego File", command=lambda: select_file("stego")).grid(row=2, column=2, padx=10, pady=10)
stego_file_label.drop_target_register(DND_FILES)
stego_file_label.dnd_bind('<<Drop>>', lambda event: drop(event, "stego"))

stego_canvas = tk.Canvas(root, width=300, height=300, bg="white")
stego_canvas.grid(row=2, column=3, padx=10, pady=10)

tk.Label(root, text="Number of LSBs:").grid(row=3, column=0, padx=10, pady=10)
bits_entry = tk.Entry(root)
bits_entry.grid(row=3, column=1, padx=10, pady=10)
bits_entry.insert(0, "1")

tk.Button(root, text="Encode", command=encode).grid(row=3, column=2, padx=10, pady=10)
tk.Button(root, text="Decode", command=decode).grid(row=3, column=3, padx=10, pady=10)

root.mainloop()
