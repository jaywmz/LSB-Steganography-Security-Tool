import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import numpy as np
import wave

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
            if (i + ((bits-1)-bit_index)) < payload_len:
                # to get the replacement bit from payload_bin at the index corresponding with the bit_index 
                bit = int(payload_bin[i + ((bits-1)-bit_index)])
                # create the mask to clear the bit at the specified bit_index, depending on how many LSBs selected
                mask = ~(1 << bit_index)
                # AND the mask, to clear the bit at the specific index
                clearedByte = byte & mask
                # move the replacement bit to specific index position
                positionedReplacementBit = bit << bit_index
                # OR the positioned replacement bit, to set the bit at the specified index of frame byte with the replacement bit
                byte = clearedByte | positionedReplacementBit
                # byte = (byte & ~(1 << bit_index)) | (bit << bit_index)
        flat_cover_array[i//bits] = byte
    
    stego_array = flat_cover_array.reshape(cover_array.shape)
    stego_image = Image.fromarray(stego_array)
    stego_image_path = "stego_image.png"
    stego_image.save(stego_image_path)
    stego_file_label.config(text=stego_image_path)
    display_image(stego_image_path, stego_canvas)
    messagebox.showinfo("Success", "Payload has been successfully encoded into the cover image.")
    
    
# Function to encode text into a .wav file
def WAV_encode():
    cover_path = cover_file_label.cget("text")
    payload_path = payload_file_label.cget("text")
    
    try:
        LSB_bits = int(bits_entry.get())
        if LSB_bits < 1 or LSB_bits > 8:
            raise ValueError("Number of LSBs must be between 1 and 8.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
    if not cover_path or not payload_path:
        messagebox.showerror("Error", "Please select both cover and payload files.")
        return
    
    # Open cover_path as audio file
    with wave.open(cover_path, 'rb') as audioCoverFile:
        # Read audio data
        frames = audioCoverFile.readframes(audioCoverFile.getnframes())
        frame_array = bytearray(frames) 
    
        # Read payload text
        with open(payload_path, 'r') as file:
            payload = file.read()
            
            # Convert payload to binary
            payload_bin = ''.join([ format(ord(char), '08b') for char in payload ])
            payload_len = len(payload_bin)
                
            # Check if payload can be hidden in cover image, every byte = 8 bits
            if payload_len > len(frame_array) * 8: 
                messagebox.showerror("Error", "Payload is too large to hide in the selected cover image.")
                return
            
            # Encode secret data into LSB of audio frames
            data_index = 0
            for i in range(len(frame_array)): # for every byte
                for j in range(LSB_bits):  # for 0 to (LSBs input)-1
                    if data_index < payload_len: # if have not reached last bit of payload
                        # Get the next bit from secret data
                        secretBit = (int(payload_bin[data_index]) >> j) & 1
                        # replaces the j-th bit of frame byte with secretBit, be it 0 or 1
                        frame_array[i] = (frame_array[i] & ~(1 << j)) | (secretBit << j)
                        data_index += 1
                    else:
                        break
                
    # Write the modified audio data to a new file
    stego_path = "output_audio_stego.wav"
    with wave.open(stego_path, 'wb') as audio_out:
        audio_out.setparams(audioCoverFile.getparams())
        audio_out.writeframes(frame_array)
        messagebox.showinfo("Encoded", "Payload written into audio cover file successfully")
        
        
def WAV_decode():
    stego_path = stego_file_label.cget("text")
    
    try:
        LSB_bits = int(bits_entry.get())
        if LSB_bits < 1 or LSB_bits > 8:
            raise ValueError("Number of LSBs must be between 1 and 8.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
    if not stego_path:
        messagebox.showerror("Error", "Please select a stego file.")
        return
    
    # Open the audio file for reading
    with wave.open(stego_path, 'rb') as audioStegoFile:
        # Read audio data
        frames = audioStegoFile.readframes(audioStegoFile.getnframes())
        frame_array = bytearray(frames)
                    
        # Extract payload from stego audio file
        payload_bin = ''
        for i in range(len(frame_array)):
            for j in range(LSB_bits):
                bit = (frame_array[i] >> j) & 1
                payload_bin += str(bit)
                
        # Convert binary payload to text
        payload = ''
        for i in range(0, len(payload_bin), 8):
            byte = payload_bin[i:i+8]
            if len(byte) == 8:
                char = chr(int(byte, 2))
                payload += char
        
        messagebox.showinfo("Decoded Payload", f"Decoded text: {payload}")
        

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
    mask = getMask(bits)
    for i in range(0, flat_stego_array.size, bits):
        byte = flat_stego_array[i//bits]
        # for bit_index in range(bits):
        #     # essentially popping bits from the right, one by one every iteration, but then the bits are appended in reversed order, so wrong payload
        #     bit = (byte >> bit_index) & 1
        #     payload_bin += str(bit)
        byte = byte & mask
        bin = format(byte, 'b').rjust(bits, '0')
        payload_bin += bin
    
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
    
    
def getMask(lsb):
        match(lsb):
            case 1:
                return 1
            case 2:
                return 3
            case 3:
                return 7
            case 4:
                return 15
            case 5:
                return 31
            case 6:
                return 63
            case 7:
                return 127
            case 8:
                return 255


# Main GUI setup
root = TkinterDnD.Tk()
root.title("LSB Steganography")

# Create a main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas inside the main frame
my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
my_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# Create another frame inside the canvas
second_frame = tk.Frame(my_canvas)

# Add that new frame to a window in the canvas
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

# Now add all your widgets to the second_frame instead of the root
# For example:
tk.Label(second_frame, text="Cover File:").grid(row=0, column=0, padx=10, pady=10)
cover_file_label = tk.Label(second_frame, text="", width=50)
cover_file_label.grid(row=0, column=1, padx=10, pady=10)
tk.Button(second_frame, text="Select Cover File", command=lambda: select_file("cover")).grid(row=0, column=2, padx=10, pady=10)
cover_file_label.drop_target_register(DND_FILES)
cover_file_label.dnd_bind('<<Drop>>', lambda event: drop(event, "cover"))

cover_canvas = tk.Canvas(second_frame, width=300, height=300, bg="white")
cover_canvas.grid(row=0, column=3, padx=10, pady=10)

tk.Label(second_frame, text="Payload File:").grid(row=1, column=0, padx=10, pady=10)
payload_file_label = tk.Label(second_frame, text="", width=50)
payload_file_label.grid(row=1, column=1, padx=10, pady=10)
tk.Button(second_frame, text="Select Payload File", command=lambda: select_file("payload")).grid(row=1, column=2, padx=10, pady=10)
payload_file_label.drop_target_register(DND_FILES)
payload_file_label.dnd_bind('<<Drop>>', lambda event: drop(event, "payload"))

tk.Label(second_frame, text="Stego File:").grid(row=2, column=0, padx=10, pady=10)
stego_file_label = tk.Label(second_frame, text="", width=50)
stego_file_label.grid(row=2, column=1, padx=10, pady=10)
tk.Button(second_frame, text="Select Stego File", command=lambda: select_file("stego")).grid(row=2, column=2, padx=10, pady=10)
stego_file_label.drop_target_register(DND_FILES)
stego_file_label.dnd_bind('<<Drop>>', lambda event: drop(event, "stego"))

stego_canvas = tk.Canvas(second_frame, width=300, height=300, bg="white")
stego_canvas.grid(row=2, column=3, padx=10, pady=10)

tk.Label(second_frame, text="Number of LSBs:").grid(row=3, column=0, padx=10, pady=10)
bits_entry = tk.Entry(second_frame)
bits_entry.grid(row=3, column=1, padx=10, pady=10)
bits_entry.insert(0, "1")

tk.Button(second_frame, text="Encode", command=encode).grid(row=3, column=2, padx=10, pady=10)
tk.Button(second_frame, text="Decode", command=decode).grid(row=3, column=3, padx=10, pady=10)
tk.Button(second_frame, text="Encode Audio File", command=WAV_encode).grid(row=3, column=4, padx=10, pady=10)
tk.Button(second_frame, text="Decode Audio File", command=WAV_decode).grid(row=3, column=5, padx=10, pady=10)

root.mainloop()