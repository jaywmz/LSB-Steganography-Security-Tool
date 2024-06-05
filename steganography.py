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
import platform
import time

# Define a class for steganography operations
class Steganography:

    # Method to encode a message into an image, audio, gif or video file
    @staticmethod
    def encode(input_path, msg, stop_code, lsb, output_dir):
        """
        Use the LSB of the pixels to encode the message into something
        """
        # Print the input parameters
        print(f"Input path: {input_path}")
        print(f"Message: {msg}")
        print(f"LSB: {lsb}")
        print(f"Output directory: {output_dir}")

        # Check the file type and call the appropriate encoding method
        if input_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print("Encoding message into image...")
            return Steganography.encode_image(input_path, msg, lsb, output_dir)

        elif input_path.endswith(('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac')):
            print("Encoding message into audio...")
            return Steganography.encode_audio(input_path, msg, lsb, output_dir)

        elif input_path.endswith(('.gif')):
            print("Encoding message into GIF...")
            return Steganography.encode_gif(input_path, msg, lsb, output_dir)

        elif input_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            print("Encoding message into video...")
            return Steganography.encode_steganography_video(input_path, msg, stop_code, lsb, output_dir)

    # Method to decode a message from an image, audio, gif or video file
    @staticmethod
    def decode(input_path, stop_code, lsb):
        """
        Use the LSB of the pixels to encode the message into something
        """
        # Print the input parameters
        print(f"Input path: {input_path}")
        print(f"LSB: {lsb}")

        # Check the file type and call the appropriate decoding method
        if input_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print("Decoding message from image...")
            return Steganography.decode_image(input_path, lsb)

        elif input_path.endswith(('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac')):
            print("Decoding message from audio...")
            return Steganography.decode_audio(input_path, lsb)

        elif input_path.endswith(('.gif')):
            print("Decoding message from GIF...")
            return Steganography.decode_gif(input_path, lsb)

        elif input_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            print("Decoding message from video...")
            return Steganography.decode_steganography_video(input_path, stop_code, lsb)

    # Method to encode a message into an image
    @staticmethod
    def encode_image(img_path, msg, lsb, output_dir):
        """
        Use the LSBs of the pixels to encode the message into the image
        """
        stop_code = "\x00"
        # Open the image and convert it to RGB
        img = Image.open(img_path).convert("RGB")
        width, height = img.size
        # Calculate the maximum payload characters for the current image
        max_payload_char = math.floor((width * height * 3 * lsb) / 8) - len(stop_code)
        print("Maximum number of payload characters for the current image: " + str(max_payload_char))
        # Add a stopping null character to the message
        msg += stop_code
        length = len(msg)
        print(msg)
        # Check if the message is too long for the image
        if length > max_payload_char:
            print(f"text too long! (don't exceed {max_payload_char} characters)")
            return {"status": False, "message": "text too long! (don't exceed " + str(max_payload_char) + " characters)"}

        # Calculate and print some statistics about the image and the message
        total_image_bits = width * height * 3 * 8
        print(f"Total amount of characters used up: {length}/{max_payload_char} ({length / max_payload_char * 100}%)")
        print("Total amount of bits available in image: " + str(total_image_bits))
        print("Total amount of bits to replace for payload: " + str(length * 8))
        print(f"Estimated image distortion: {length * 8 / total_image_bits * 100}%")

        # Copy the image for encoding
        encoded = img.copy()
        index = 0

        # Create a mask to clear the least significant bits
        mask = 0xFF << lsb

        # Convert the message to binary
        binary_msg = ''.join([format(ord(i), '08b') for i in msg])
        len_binary_msg = len(binary_msg)

        end = False

        # Iterate over the pixels of the image
        for row in range(height):
            for col in range(width):
                pixel = img.getpixel((col, row))
                pixel = list(pixel)
                for i in range(len(pixel)):
                    # If there are still bits of the message left, encode them into the pixel
                    if index < len_binary_msg:
                        secretBits = binary_msg[index:index + lsb]
                        if len(secretBits) < lsb:
                            secretBits = secretBits.ljust(lsb, '0')
                        secretBitsInt = int(secretBits, 2)
                        pixel[i] &= mask
                        pixel[i] |= secretBitsInt
                        index += lsb
                    else:
                        end = True
                        break
                encoded.putpixel((col, row), tuple(pixel))
                if end is True:
                    break
            if end is True:
                break

        # Save the encoded image
        if isinstance(encoded, Image.Image):
            img_ext = img_path.split('.')
            output_path = os.path.join(output_dir, 'stego_image.' + img_ext[-1])
            encoded.save(output_path)
            # Open the encoded image
            if os.name == 'nt':
                os.startfile(output_path)
            elif os.name == 'posix':
                subprocess.run(['open', output_path])

            return {"status": True, "message": "Message encoded successfully into image", "output_file_path": output_path}
        else:
            return {"status": False, "message": "Error encoding message into image"}

    @staticmethod
    def decode_image(img_path, lsb):
        """
        Use the LSB of the pixels to decode the message from the image
        """
        try:
            # Open the image and convert it to RGB
            img = Image.open(img_path).convert("RGB")
            width, height = img.size
            msg_bin = ""

            # Create a mask to clear the least significant bits
            mask = Steganography.getMask(lsb)
            end = False

            # Iterate over the pixels of the image
            for row in range(height):
                for col in range(width):
                    pixel = tuple()
                    pixel = list(img.getpixel((col, row)))
                    for color in pixel:
                        # Extract the least significant bits of the color
                        color &= mask
                        bin = format(color, 'b').rjust(lsb, '0')
                        msg_bin += bin
                        # If the end of the message is reached, stop decoding
                        if msg_bin.endswith("00000000"):
                            end = True
                            break
                    if end is True:
                        break
                if end is True:
                    break

            # Convert the binary message to text
            decoded_msg = ''
            for i in range(0, len(msg_bin), 8):
                byte = msg_bin[i:i + 8]
                if (len(byte) == 8) and (int(byte, 2) != 0):
                    char = chr(int(byte, 2))
                    decoded_msg += char
                else:
                    break
            
            with open("decoded_message.txt", "w") as file:
                file.write(decoded_msg)
            return {"status": True, "message": "Check decoded_message.txt for the decoded message."}
            # return {"status": True, "message": decoded_msg}
        except Exception as e:
            return {"status": False, "message": str(e)}

    @staticmethod
    def encode_audio(audio_path, msg, lsb, output_dir):
        """
        Use the LSB of the audio samples to encode the message into the audio file
        """
        fileExt = audio_path.split('.')[-1]

        # Open the audio file
        song = wave.open(audio_path, mode='rb')

        # Add a stop character to the message
        stop_char = '='
        msg += stop_char

        # Check if the message is too long for the audio file
        if (len(msg) * 8) > song.getnframes():
            return {"status": False, "message": "The message is too long for the audio file"}

        # Read the audio samples
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))

        # Convert the message to binary
        secretBits = ''.join([bin(ord(eachChar)).lstrip('0b').rjust(8, '0') for eachChar in msg])
        lenOfSecretBits = len(secretBits)

        # Create a mask to clear the least significant bits
        mask = 0xFF << lsb

        # Encode the message into the audio samples
        index = 0
        for i in range(len(frame_bytes)):
            if index < lenOfSecretBits:
                secretlsbs = secretBits[index:index + lsb]
                if len(secretlsbs) < lsb:
                    secretlsbs = secretlsbs.ljust(lsb, '0')
                secretlsbsInt = int(secretlsbs, 2)
                frame_bytes[i] &= mask
                frame_bytes[i] |= secretlsbsInt
                index += lsb
            else:
                break

        # Save the encoded audio
        frame_modified = bytes(frame_bytes)
        output_path = os.path.join(output_dir, 'encoded_audio.' + fileExt)
        with wave.open(output_path, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        song.close()

        try:
            # Open the encoded audio
            with wave.open(output_path, 'rb') as fd:
                if os.name == 'nt':
                    os.startfile(output_path)
                elif os.name == 'posix':
                    subprocess.run(['open', output_path])
                return {"status": True, "message": "Audio encoded successfully", "output_file_path": output_path}
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
            # Open the audio file
            song = wave.open(audio_path, mode='rb')
            # Read the audio samples
            frame_bytes = bytearray(list(song.readframes(song.getnframes())))

            # Extract the least significant bits of the samples
            payload_bin = ''
            mask = Steganography.getMask(lsb)
            for i in range(0, len(frame_bytes), lsb):
                byte = frame_bytes[i // lsb]
                byte = byte & mask
                bin = format(byte, 'b').rjust(lsb, '0')
                payload_bin += bin
                # If the end of the message is reached, stop decoding
                if payload_bin.__contains__("00111101"):
                    break

            decoded_msg = ''
            for i in range(0, len(payload_bin), 8):
                byte = payload_bin[i:i + 8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    if char == "=":
                        break
                    else:
                        decoded_msg += char

            song.close()
            
            with open("decoded_message.txt", "w") as file:
                file.write(decoded_msg)
                
            return {"status": True, "message": "Check decoded_message.txt for the decoded message."}
            # return {"status": True, "message": payload}
        except Exception as e:
            return {"status": False, "message": str(e)}

    @staticmethod
    def encode_gif(gif_path, msg, lsb, output_dir):
        """
        Use the LSB of the pixels to encode the message into the GIF
        """
        # Open the GIF
        gif = Image.open(gif_path)

        # Convert each frame to RGB or RGBA
        frames = []
        for frame in ImageSequence.Iterator(gif):
            if frame.mode == 'P':
                frames.append(frame.convert('RGB'))
            else:
                frames.append(frame.convert('RGBA'))

        # Calculate the total number of bits available for encoding
        total_bits = sum(frame.width * frame.height * 3 for frame in frames)

        # Add a stop character to the message and convert it to binary
        stop_code = '\x00'
        msg += stop_code
        binary_msg = ''.join(format(ord(i), '08b') for i in msg)

        # Check if the message is too long for the GIF
        if len(binary_msg) > total_bits * lsb:
            return {"status": False, "message": "Message too long to fit in GIF"}

        # Create a mask to clear the least significant bits
        index = 0
        mask = (1 << lsb) - 1
        clear_mask = ~mask & 0xFF

        # Encode the message into the pixels of the frames
        for frame in frames:
            for row in range(frame.height):
                for col in range(frame.width):
                    pixel = list(frame.getpixel((col, row)))

                    for i in range(3):
                        if index < len(binary_msg):
                            pixel[i] &= clear_mask
                            pixel[i] |= int(binary_msg[index:index + lsb].ljust(lsb, '0'), 2)
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

        return {"status": True, "message": "Message encoded successfully", "output_file_path": output_path}

    @staticmethod
    def decode_gif(gif_path, lsb):
        """
        Decode the hidden message from a GIF
        """
        try:
            # Open the GIF
            gif = Image.open(gif_path)
            msg_bin = ""

            # Create a mask to extract the least significant bits
            mask = (1 << lsb) - 1

            # Extract the least significant bits of the pixels to decode the message
            for frame in ImageSequence.Iterator(gif):
                width, height = frame.size

                for row in range(height):
                    for col in range(width):
                        pixel = frame.getpixel((col, row))

                        if frame.mode == 'P':
                            palette = frame.getpalette()
                            r, g, b = palette[pixel * 3:pixel * 3 + 3]
                        elif isinstance(pixel, int):
                            r = g = b = pixel
                            a = 255
                        else:
                            if frame.mode == 'RGBA':
                                r, g, b, a = pixel
                            else:
                                r, g, b = pixel

                        msg_bin += format(r & mask, f'0{lsb}b')
                        msg_bin += format(g & mask, f'0{lsb}b')
                        msg_bin += format(b & mask, f'0{lsb}b')

                        # If the end of the message is reached, stop decoding
                        if len(msg_bin) >= 8 and msg_bin[-8:] == format(ord('\x00'), '08b'):
                            break
                    if len(msg_bin) >= 8 and msg_bin[-8:] == format(ord('\x00'), '08b'):
                        break
                if len(msg_bin) >= 8 and msg_bin[-8:] == format(ord('\x00'), '08b'):
                    break

            # Convert the binary message to text
            decoded_msg = ''
            for i in range(0, len(msg_bin), 8):
                byte = msg_bin[i:i + 8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    if char == '\x00':
                        break
                    decoded_msg += char
                    
            with open("decoded_message.txt", "w") as file:
                file.write(decoded_msg)
            return {"status": True, "message": "Check decoded_message.txt for the decoded message."}
            # return {"status": True, "message": decoded_msg}
        except Exception as e:
            return {"status": False, "message": str(e)}

    @staticmethod
    def getMask(lsb):
        """
        Create a mask to extract the least significant bits
        """
        return (1 << lsb) - 1

    def encode_steganography_video(self, path_to_cover_video, payload_text, stop_code, num_lsb, output_directory):
        try:
            # Start the video encoding process
            print("Initiating video encoding...")
            
            # Convert the number of least significant bits (LSB) to an integer
            try:
                number_of_lsb = int(num_lsb)
            except ValueError:
                raise ValueError(f"num_lsb should be an integer, got: {num_lsb}")
            print(f"Encoding with {number_of_lsb} LSBs")

            # Extract frames from the video
            self.extract_frames_from_video_improve(path_to_cover_video)

            # Define the temporary folder and get the list of frame files
            temporary_folder = "./temporary/"
            frame_files = sorted([file for file in os.listdir(temporary_folder) if file.endswith('.png')],
                                 key=lambda file: int(file.split('.')[0]))

            # Convert the payload text to binary and append the stop code
            payload_bits = ''.join([format(ord(char), '08b') for char in payload_text])
            payload_bits += stop_code
            bit_counter = 0

            # Process each frame and encode the payload into the pixels
            total_frames = len(frame_files)
            for frame_index, frame_file in enumerate(frame_files):
                frame = cv2.imread(os.path.join(temporary_folder, frame_file))
                if bit_counter >= len(payload_bits):
                    break
                for row in range(frame.shape[0]):
                    for col in range(frame.shape[1]):
                        for channel in range(3):
                            if bit_counter < len(payload_bits):
                                frame[row, col, channel] = (frame[row, col, channel] & ~((1 << num_lsb) - 1)) | int(
                                    payload_bits[bit_counter:bit_counter + num_lsb], 2)
                                bit_counter += num_lsb

                # Save the modified frame
                cv2.imwrite(os.path.join(temporary_folder, frame_file), frame)
                print(f"\rProcessed frame {total_frames} of {total_frames}", end="")

            # Get the frames per second of the original video
            frames_per_second = VideoFileClip(path_to_cover_video).fps

            # Extract the audio from the original video
            print("\nExtracting audio...")
            audio_extraction_command = f'ffmpeg -i "{path_to_cover_video}" -q:a 0 -map a temporary/audio.mp3 -y -loglevel error'
            audio_extraction_result = os.system(audio_extraction_command)
            if audio_extraction_result != 0:
                print(f"Error extracting audio with command: {audio_extraction_command}")
                return {"status": False, "message": "Error extracting audio from the video"}

            # Define the path for the steganography video
            steganography_video_path = os.path.join(output_directory,
                                                    os.path.basename(path_to_cover_video).split('.')[0] + '_stego.mp4')
            print(f"Stego video path: {steganography_video_path}")

            # Combine the new video frames and the original audio
            print("Combining new video and audio...")
            combine_video_command = f'ffmpeg -framerate {frames_per_second} -i temporary/%d.png -codec copy -y temporary/video-only.mp4 -loglevel error'
            combine_video_result = os.system(combine_video_command)
            if combine_video_result != 0 or not os.path.exists('temporary/video-only.mp4'):
                print(f"Error combining video with command: {combine_video_command}")
                return {"status": False, "message": "Error combining video frames"}

            combine_audio_command = f'ffmpeg -i temporary/video-only.mp4 -i temporary/audio.mp3 -codec copy -y "{steganography_video_path}" -loglevel error'
            combine_audio_result = os.system(combine_audio_command)
            if combine_audio_result != 0 or not os.path.exists(steganography_video_path):
                print(f"Error combining audio with command: {combine_audio_command}")
                return {"status": False, "message": "Error combining audio with video"}

            # Delete the temporary folder
            print("Deleting temporary folder...")
            if os.path.exists("./temporary"):
                try:
                    shutil.rmtree("./temporary", onerror=self.change_file_permissions)
                    print("Temporary folder deleted successfully.")
                except OSError as e:
                    print(f"Error: {e.strerror} : {e.filename}")

            print("Encoding completed!")
            return {"status": True, "message": f"Stego video created successfully at {steganography_video_path}",
                    "output_file_path": steganography_video_path}

        except Exception as error:
            return {"status": False, "message": f"Error encoding video: {str(error)}"}

    def change_file_permissions(self, operation, file_path, _):
        # Change the file permissions to writeable
        os.chmod(file_path, stat.S_IWRITE)
        operation(file_path)

    @staticmethod
    def extract_frames_with_ffmpeg(path_to_video):
        # Create a temporary folder if it doesn't exist
        if not os.path.exists("./temporary"):
            os.makedirs("./temporary")
        temporary_folder = "./temporary/"
        # Use FFmpeg to extract frames from the video
        command = f'ffmpeg -i "{path_to_video}" "{temporary_folder}%d.png" -hide_banner'
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            raise Exception("Error extracting frames using FFmpeg")

    def extract_frames_from_video(self, path_to_video):
        # Extract frames from the video using the old method
        start_time = time.time()

        if not os.path.exists("./temporary"):
            os.makedirs("./temporary")
        temporary_folder = "./temporary/"
        video_clip = VideoFileClip(path_to_video)
        for frame_number, frame in enumerate(video_clip.iter_frames()):
            print(f"Processing frames... (Frame {frame_number})")
            image = Image.fromarray(frame, 'RGB')
            image.save(f'{temporary_folder}{frame_number}.png')

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Processing time using old method: {elapsed_time} seconds")

    def extract_frames_from_video_improve(self, path_to_video):
        # Extract frames from the video using the improved method
        start_time = time.time()

        if not os.path.exists("./temporary"):
            os.makedirs("./temporary")
        temporary_folder = "./temporary/"

        video_capture = cv2.VideoCapture(path_to_video)
        frame_count = 0
        while True:
            success, image = video_capture.read()
            if not success:
                break
            print(f"Processing frames... (Frame {frame_count})")
            cv2.imwrite(os.path.join(temporary_folder, f"{frame_count}.png"), image)  # save frame as PNG file
            frame_count += 1

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Processing time using new method: {elapsed_time} seconds")

    @staticmethod
    def decode_steganography_video(path_to_steganography_video, stop_code, num_lsb):
        try:
            # Start the video decoding process
            print("Initiating video decoding...")
            
            # Convert the number of least significant bits (LSB) to an integer
            number_of_lsb = int(num_lsb)
            print(f"Decoding with {number_of_lsb} LSBs")

            # Extract frames from the video
            Steganography.extract_frames_with_ffmpeg(path_to_steganography_video)

            # Define the temporary folder and get the list of frame files
            temporary_folder = "./temporary/"
            frame_files = sorted([file for file in os.listdir(temporary_folder) if file.endswith('.png')],
                                 key=lambda file: int(file.split('.')[0]))

            # Initialize the payload bits
            payload_bits = ''

            # Process each frame and decode the payload from the pixels
            total_frames = len(frame_files)
            for frame_file in frame_files:
                frame = cv2.imread(os.path.join(temporary_folder, frame_file))
                for row in range(frame.shape[0]):
                    for col in range(frame.shape[1]):
                        for channel in range(3):  # Iterate over the BGR channels
                            # Extract the LSBs from the pixel
                            bits = format(frame[row, col, channel] & ((1 << num_lsb) - 1), f'0{num_lsb}b')
                            payload_bits += bits
                            # If the stop code is found, decode the message and write it to a file
                            if payload_bits.endswith(stop_code):
                                decoded_message = ''.join(
                                    [chr(int(payload_bits[i:i + 8], 2)) for i in range(0, len(payload_bits) - 64, 8)])
                                # Delete the temporary folder
                                if os.path.exists("./temporary"):
                                    try:
                                        shutil.rmtree("./temporary", onerror=Steganography.change_file_permissions)
                                        print("Temporary folder deleted successfully.")
                                    except OSError as error:
                                        print(f"Error: {error.strerror} : {error.filename}")
                                # Write the decoded message to a file
                                with open("decoded_message.txt", "w") as file:
                                    file.write(decoded_message)
                                print("Decoding completed!")
                                return {"status": True, "message": "Check decoded_message.txt for the decoded message."}

            print(f"\rProcessed frame {total_frames} / {total_frames}")

            # Delete the temporary folder
            if os.path.exists("./temporary"):
                try:
                    shutil.rmtree("./temporary", onerror=Steganography.change_file_permissions)
                    print("\nTemporary folder deleted successfully.")
                except OSError as error:
                    print(f"Error: {error.strerror} : {error.filename}")

            return ''

        except Exception as error:
            # Return an error message if an exception is raised
            return {"status": False, "message": f"Error decoding video: {str(error)}"}