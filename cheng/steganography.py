from PIL import Image, ImageSequence
from moviepy.editor import VideoFileClip, VideoClip
import numpy as np
import wave
import os 
import subprocess
import math
import cv2
import shutil
import stat

class Steganography:
    
    @staticmethod
    def encode(input_path, msg, lsb, output_dir):
        """
        Use the LSB of the pixels to encode the message into something
        """
        print(f"Input path: {input_path}")
        print(f"Message: {msg}")
        print(f"LSB: {lsb}")
        print(f"Output directory: {output_dir}")
        
        if(input_path.endswith(('.png', '.jpg', '.jpeg', '.bmp'))):
            print("Encoding message into image...")
            return Steganography.encode_image(input_path, msg, lsb, output_dir)
                        
        elif(input_path.endswith(('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'))):
            print("Encoding message into audio...")
            return Steganography.encode_audio(input_path, msg, lsb, output_dir)
        
        elif(input_path.endswith(('.gif'))):
            print("Encoding message into GIF...")
            return Steganography.encode_gif(input_path, msg, lsb, output_dir)
        
        elif input_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            print("Encoding message into video...")
            return Steganography.encode_steganography_video(input_path, msg, lsb, output_dir)
    
    
    @staticmethod
    def decode(input_path, lsb):
        """
        Use the LSB of the pixels to encode the message into something
        """
        print(f"Input path: {input_path}")
        print(f"LSB: {lsb}")
        
        if(input_path.endswith(('.png', '.jpg', '.jpeg', '.bmp'))):
            print("Decoding message from image...")
            return Steganography.decode_image(input_path, lsb)
                        
        elif(input_path.endswith(('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'))):
            print("Decoding message from audio...")
            return Steganography.decode_audio(input_path, lsb)
        
        elif(input_path.endswith(('.gif'))):
            print("Decoding message from GIF...")
            return Steganography.decode_gif(input_path, lsb)
        
        elif input_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            print("Decoding message from video...")
            return Steganography.decode_steganography_video(input_path, lsb)
    
    
    @staticmethod
    def encode_image(img_path, msg, lsb, output_dir):
        """
        Use the LSBs of the pixels to encode the message into the image
        """
        fileExt = img_path.split('.')[-1]     
           
        if fileExt.lower() == 'gif':
            img = Image.open(img_path).convert("RGB")
        else:   
            img = Image.open(img_path)

        width, height = img.size
        stop_code = '\x00'
        max_payload_char = math.floor((width * height * 3 * lsb) / 8) - len(stop_code)
        print("Maximum number of payload characters for the current image: " + str(max_payload_char))
        msg += stop_code # add a stopping null character, one char space should be reserved for stopping code
        length = len(msg)
        print(msg)
        if length > max_payload_char:
            print(f"text too long! (don't exceed {max_payload_char} characters)")
            return {"status": False, "message": "text too long! (don't exceed " + str(max_payload_char) + " characters)"}
        
        total_image_bits = width * height * 3 * 8
        print(f"Total amount of characters used up: {length}/{max_payload_char} ({length / max_payload_char * 100}%)")
        print("Total amount of bits available in image: " + str(total_image_bits))
        print("Total amount of bits to replace for payload: " + str(length * 8))
        print(f"Estimated image distortion: {length * 8 / total_image_bits * 100}%")
        
        encoded = img.copy()
        index = 0

        mask = 0xFF << lsb  # Create a mask to clear the least significant bits

        binary_msg = ''.join([format(ord(i), '08b') for i in msg])  # Convert the message to binary
        len_binary_msg = len(binary_msg)

        for row in range(height):
            for col in range(width):
                r, g, b, a = img.getpixel((col, row))
                
                # clear LSBs 
                r &= mask
                g &= mask
                b &= mask

                # Add the bits of the message
                if index < len_binary_msg:
                    secretBits = binary_msg[index:index+lsb]
                    # if message not divisible by lsb, last character bits misalign, need to pad 0s on the right to width of lsb
                    if len(secretBits) < lsb:
                        secretBits = secretBits.ljust(lsb, '0')
                    secretBitsInt = int(secretBits, 2)
                    r = r | secretBitsInt
                    index += lsb
                if index < len_binary_msg:
                    secretBits = binary_msg[index:index+lsb]
                    if len(secretBits) < lsb:
                        secretBits = secretBits.ljust(lsb, '0')
                    secretBitsInt = int(secretBits, 2)
                    g = g | secretBitsInt
                    index += lsb
                if index < len_binary_msg:
                    secretBits = binary_msg[index:index+lsb]
                    if len(secretBits) < lsb:
                        secretBits = secretBits.ljust(lsb, '0')
                    secretBitsInt = int(secretBits, 2)
                    b = b | secretBitsInt
                    index += lsb
                if index >= len_binary_msg:
                    break
                
                encoded.putpixel((col, row), (r, g, b, a))
                
        if isinstance(encoded, Image.Image):
            img_ext = img_path.split('.')
            output_path = os.path.join(output_dir, 'stego_image.' + img_ext[-1])
            encoded.save(output_path)
            if os.name == 'nt':
                os.startfile(output_path)
            elif os.name == 'posix':
                subprocess.run(['open', output_path])
            return {"status": True, "message": "Message encoded successfully"}
        else:
            return {"status": False, "message": "Error encoding message into image"}
    
    
    @staticmethod
    def decode_image(img_path, lsb):
        """
        Use the LSB of the pixels to decode the message from the image
        """
        try:
            fileExt = img_path.split('.')[-1]
            if fileExt.lower() == 'gif':
                img = Image.open(img_path).convert("RGB")
            else:
                img = Image.open(img_path)
            width, height = img.size
            msg_bin = ""
            
            mask = Steganography.getMask(lsb)
            
            for row in range(height):
                for col in range(width):
                    r, g, b, a  = img.getpixel((col, row))
                    
                    # Extract the bits of the message
                    r &= mask
                    bin = format(r, 'b').rjust(lsb, '0')
                    msg_bin += bin
                    
                    g &= mask
                    bin = format(g, 'b').rjust(lsb,'0')
                    msg_bin += bin
                    
                    b &= mask
                    bin = format(b, 'b').rjust(lsb,'0')
                    msg_bin += bin

            # Convert the binary message to a string
            decoded_msg = ''
            for i in range(0, len(msg_bin), 8):
                byte = msg_bin[i:i+8]
                if len(byte) == 8:
                    if int(byte, 2) == 0: # break if we hit a null character (stop code)
                        break
                    char = chr(int(byte, 2))
                    decoded_msg += char

            return {"status": True, "message": decoded_msg}
        except Exception as e:
            return {"status": False, "message": str(e)}
    
    @staticmethod
    def encode_audio(audio_path, msg, lsb, output_dir):
        """
        Use the LSB of the audio samples to encode the message into the audio file
        """
        # Get the file extension
        fileExt = audio_path.split('.')[-1]
        
        # read wave audio file
        song = wave.open(audio_path, mode='rb')
        
        # add stop code char to signify end of secret msg
        stop_char = '='
        msg += stop_char
        
        # check if cover audio file is large enough for payload msg
        if (len(msg) * 8) > song.getnframes():
            return {"status": False, "message": "The message is too long for the audio file"}
        
        # Read frames and convert to byte array
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        
        # convert secret msg into binary string
        secretBits = ''.join([bin(ord(eachChar)).lstrip('0b').rjust(8,'0') for eachChar in msg])
        lenOfSecretBits = len(secretBits)
        
        # Encode payload into cover frame
        for i in range(0, lenOfSecretBits, lsb):
            byte = frame_bytes[i//lsb]
            for bit_index in range(lsb):
                if (i + ((lsb-1)-bit_index)) < lenOfSecretBits:
                    # to get the replacement bit from secret bits at the index corresponding with the bit_index 
                    bit = int(secretBits[i + ((lsb-1)-bit_index)])
                    # create the mask to clear the bit at the specified bit_index, depending on how many LSBs selected
                    mask = ~(1 << bit_index)
                    # AND the mask, to clear the bit at the specific index
                    clearedByte = byte & mask
                    # move the replacement bit to specific index position
                    positionedReplacementBit = bit << bit_index
                    # OR the positioned replacement bit, to set the bit at the specified index of frame byte with the replacement bit
                    byte = clearedByte | positionedReplacementBit
            frame_bytes[i//lsb] = byte
        
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)
        output_path = os.path.join(output_dir, 'encoded_audio.' + fileExt)
        # Write bytes to a new wave audio file
        with wave.open(output_path, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        song.close()
        
        # Handle the case where the output file is not created
        try:
            with wave.open(output_path, 'rb') as fd:
                os.startfile(output_path)
                return {"status": True, "message": "Audio encoded successfully"}
        except FileNotFoundError:
            return {"status": False, "message": "Error creating encoded audio file"}
        except wave.Error:
            return {"status": False, "message": "Error creating encoded audio file"}
        
        
    @staticmethod
    def decode_audio(audio_path, lsb):
        """
        Decode the hidden message from an audio file
        """
        try:
            song = wave.open(audio_path, mode='rb')
            # Convert audio to byte array
            frame_bytes = bytearray(list(song.readframes(song.getnframes())))
            
            # Extract payload from stego audio
            payload_bin = ''
            mask = Steganography.getMask(lsb)
            for i in range(0, len(frame_bytes), lsb):
                byte = frame_bytes[i//lsb]
                byte = byte & mask
                bin = format(byte, 'b').rjust(lsb, '0')
                payload_bin += bin
            
            # Convert binary payload to text
            payload = ''
            for i in range(0, len(payload_bin), 8):
                byte = payload_bin[i:i+8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    if char.__eq__("="): # stop code reached
                        break
                    else:
                        payload += char
            
            song.close()
            return {"status": True, "message": payload}
        except Exception as e:
            return {"status": False, "message": str(e)}
        

    @staticmethod
    def encode_gif(gif_path, msg, lsb, output_dir):
        # Open the GIF and convert each frame to RGB
        gif = Image.open(gif_path)

        frames = []
        for frame in ImageSequence.Iterator(gif):
            if frame.mode == 'P':
                frames.append(frame.convert('RGB'))
            else:
                frames.append(frame.convert('RGBA'))

        # Calculate the total number of bits available in the GIF
        total_bits = sum(frame.width * frame.height * 3 for frame in frames)

        # Add a stop code to the message and convert it to binary
        stop_code = '\x00'
        msg += stop_code
        binary_msg = ''.join(format(ord(i), '08b') for i in msg)

        # Check if the message is too long to fit in the GIF
        if len(binary_msg) > total_bits * lsb:
            return {"status": False, "message": "Message too long to fit in GIF"}

        # Encode the message into each frame
        index = 0
        mask = (1 << lsb) - 1
        clear_mask = ~mask & 0xFF

        for frame in frames:
            for row in range(frame.height):
                for col in range(frame.width):
                    pixel = list(frame.getpixel((col, row)))

                    for i in range(3):  # RGB channels
                        if index < len(binary_msg):
                            pixel[i] &= clear_mask  # Clear the LSBs
                            pixel[i] |= int(binary_msg[index:index+lsb].ljust(lsb, '0'), 2)
                            index += lsb

                    if frame.mode == 'RGBA':
                        frame.putpixel((col, row), tuple(pixel))
                    else:
                        frame.putpixel((col, row), (pixel[0], pixel[1], pixel[2]))

        # Save the encoded GIF
        output_path = os.path.join(output_dir, 'stego_gif.gif')
        frames[0].save(output_path, save_all=True, append_images=frames[1:])

        # Open the encoded GIF
        if os.name == 'nt':
            os.startfile(output_path)
        elif os.name == 'posix':
            subprocess.run(['open', output_path])

        return {"status": True, "message": "Message encoded successfully"}

    @staticmethod
    def decode_gif(gif_path, lsb):
        try:
            gif = Image.open(gif_path)
            msg_bin = ""
            
            mask = (1 << lsb) - 1

            # Iterate over each frame in the GIF
            for frame in ImageSequence.Iterator(gif):
                width, height = frame.size
                
                for row in range(height):
                    for col in range(width):
                        pixel = frame.getpixel((col, row))

                        if frame.mode == 'P':
                            palette = frame.getpalette()
                            r, g, b = palette[pixel*3:pixel*3+3]
                        elif isinstance(pixel, int):
                            r = g = b = pixel
                            a = 255
                        else:
                            if frame.mode == 'RGBA':
                                r, g, b, a = pixel
                            else:
                                r, g, b = pixel
                        
                        # Extract the bits of the message
                        msg_bin += format(r & mask, f'0{lsb}b')
                        msg_bin += format(g & mask, f'0{lsb}b')
                        msg_bin += format(b & mask, f'0{lsb}b')

                        # Check if we've found the stop code
                        if len(msg_bin) >= 8 and msg_bin[-8:] == format(ord('\x00'), '08b'):
                            break
                    if len(msg_bin) >= 8 and msg_bin[-8:] == format(ord('\x00'), '08b'):
                        break
                if len(msg_bin) >= 8 and msg_bin[-8:] == format(ord('\x00'), '08b'):
                    break

            # Convert the binary message to a string
            decoded_msg = ''
            for i in range(0, len(msg_bin), 8):
                byte = msg_bin[i:i+8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    if char == '\x00':
                        break
                    decoded_msg += char

            return {"status": True, "message": decoded_msg}
        except Exception as e:
            return {"status": False, "message": str(e)}

        
    @staticmethod
    def getMask(lsb):
        return (1 << lsb) - 1
    
    @staticmethod
    def encode_steganography_video(path_to_cover_video, payload_text, num_lsb, output_directory):
        try:
            print("Initiating video encoding...")
            try:
                number_of_lsb = int(num_lsb)
            except ValueError:
                raise ValueError(f"num_lsb should be an integer, got: {num_lsb}")
            print(f"Encoding with {number_of_lsb} LSBs")
    
            Steganography.extract_frames_from_video(path_to_cover_video)
    
            temporary_folder = "./temporary/"
            frame_files = sorted([file for file in os.listdir(temporary_folder) if file.endswith('.png')], key=lambda file: int(file.split('.')[0]))
    
            payload_bits = ''.join([format(ord(char), '08b') for char in payload_text])
            payload_bits += '00000000' * 8  # Adding 8 null bytes to signify the end of the message
            bit_counter = 0
    
            total_frames = len(frame_files)
            for frame_index, frame_file in enumerate(frame_files):
                frame = cv2.imread(os.path.join(temporary_folder, frame_file))
                if bit_counter >= len(payload_bits):
                    break  # Stop encoding if all payload bits are encoded
                for row in range(frame.shape[0]):
                    for col in range(frame.shape[1]):
                        for channel in range(3):  # Iterate over the BGR channels
                            if bit_counter < len(payload_bits):
                                frame[row, col, channel] = (frame[row, col, channel] & ~((1 << num_lsb) - 1)) | int(payload_bits[bit_counter:bit_counter + num_lsb], 2)
                                bit_counter += num_lsb
    
                cv2.imwrite(os.path.join(temporary_folder, frame_file), frame)
                print(f"\rProcessed frame {total_frames} of {total_frames}", end="")
    
            frames_per_second = VideoFileClip(path_to_cover_video).fps
    
            print("\nExtracting audio...")
            audio_extraction_command = f'ffmpeg\\bin\\ffmpeg -i "{path_to_cover_video}" -q:a 0 -map a temporary/audio.mp3 -y -loglevel error'
            audio_extraction_result = os.system(audio_extraction_command)
            if audio_extraction_result != 0:
                print(f"Error extracting audio with command: {audio_extraction_command}")
                return {"status": False, "message": "Error extracting audio from the video"}
    
            steganography_video_path = os.path.join(output_directory, os.path.basename(path_to_cover_video).split('.')[0] + '_stego.mp4')
            print(f"Stego video path: {steganography_video_path}")
    
            print("Combining new video and audio...")
            combine_video_command = f'ffmpeg\\bin\\ffmpeg -framerate {frames_per_second} -i temporary/%d.png -codec copy -y temporary/video-only.mp4 -loglevel error'
            combine_video_result = os.system(combine_video_command)
            if combine_video_result != 0 or not os.path.exists('temporary/video-only.mp4'):
                print(f"Error combining video with command: {combine_video_command}")
                return {"status": False, "message": "Error combining video frames"}
    
            combine_audio_command = f'ffmpeg\\bin\\ffmpeg -i temporary/video-only.mp4 -i temporary/audio.mp3 -codec copy -y "{steganography_video_path}" -loglevel error'
            combine_audio_result = os.system(combine_audio_command)
            if combine_audio_result != 0 or not os.path.exists(steganography_video_path):
                print(f"Error combining audio with command: {combine_audio_command}")
                return {"status": False, "message": "Error combining audio with video"}
    
            print("Deleting temporary folder...")
            if os.path.exists("./temporary"):
                try:
                    shutil.rmtree("./temporary", onerror=Steganography.change_file_permissions)
                    print("Temporary folder deleted successfully.")
                except OSError as e:
                    print(f"Error: {e.strerror} : {e.filename}")
    
            print("Encoding completed!")
            return {"status": True, "message": f"Stego video created successfully at {steganography_video_path}"}
    
        except Exception as error:
            return {"status": False, "message": f"Error encoding video: {str(error)}"}

    @staticmethod
    def change_file_permissions(operation, file_path, _):
        os.chmod(file_path, stat.S_IWRITE)
        operation(file_path)

    @staticmethod
    def extract_frames_from_video(path_to_video):
        if not os.path.exists("./temporary"):
            os.makedirs("./temporary")
        temporary_folder = "./temporary/"
        video_clip = VideoFileClip(path_to_video)
        for frame_number, frame in enumerate(video_clip.iter_frames()):
            print(f"Processing frames... (Frame {frame_number})")
            image = Image.fromarray(frame, 'RGB')
            image.save(f'{temporary_folder}{frame_number}.png')

    @staticmethod
    def decode_steganography_video(path_to_steganography_video, num_lsb):
        try:
            print("Initiating video decoding...")
            number_of_lsb = int(num_lsb)
            print(f"Decoding with {number_of_lsb} LSBs")
    
            Steganography.extract_frames_from_video(path_to_steganography_video)
    
            temporary_folder = "./temporary/"
            frame_files = sorted([file for file in os.listdir(temporary_folder) if file.endswith('.png')], key=lambda file: int(file.split('.')[0]))
    
            payload_bits = ''
    
            total_frames = len(frame_files)
            for frame_file in frame_files:
                frame = cv2.imread(os.path.join(temporary_folder, frame_file))
                for row in range(frame.shape[0]):
                    for col in range(frame.shape[1]):
                        for channel in range(3):  # Iterate over the BGR channels
                            bits = format(frame[row, col, channel] & ((1 << num_lsb) - 1), f'0{num_lsb}b')
                            payload_bits += bits
                            if payload_bits.endswith('00000000' * 8):
                                decoded_message = ''.join([chr(int(payload_bits[i:i + 8], 2)) for i in range(0, len(payload_bits) - 64, 8)])
                                if os.path.exists("./temporary"):
                                    try:
                                        shutil.rmtree("./temporary", onerror=Steganography.change_file_permissions)
                                        print("Temporary folder deleted successfully.")
                                    except OSError as error:
                                        print(f"Error: {error.strerror} : {error.filename}")
                                with open("decoded_message.txt", "w") as file:
                                    file.write(decoded_message)
                                print("Decoding completed!")
                                return {"status": True, "message": "Check decoded_message.txt for the decoded message."}
    
            print(f"\rProcessed frame {total_frames} / {total_frames}")
    
            if os.path.exists("./temporary"):
                try:
                    shutil.rmtree("./temporary", onerror=Steganography.change_file_permissions)
                    print("\nTemporary folder deleted successfully.")
                except OSError as error:
                    print(f"Error: {error.strerror} : {error.filename}")
    
            return ''
    
        except Exception as error:
            return {"status": False, "message": f"Error decoding video: {str(error)}"}