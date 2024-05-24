from PIL import Image
import wave
import os 
import subprocess
import math

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
        
        if(input_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))):
            print("Encoding message into image...")
            return Steganography.encode_image(input_path, msg, lsb, output_dir)
                        
        elif(input_path.endswith(('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'))):
            print("Encoding message into audio...")
            return Steganography.encode_audio(input_path, msg, lsb, output_dir)
        
        elif(input_path.endswith(('.mp4', '.avi', '.mov', '.mkv'))):
            print("Encoding message into video file...")
            return {"status": False, "message": "Video file encoding not supported yet"}
    
    
    @staticmethod
    def decode(input_path, lsb):
        """
        Use the LSB of the pixels to encode the message into something
        """
        print(f"Input path: {input_path}")
        print(f"LSB: {lsb}")
        
        if(input_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))):
            print("Decoding message from image...")
            return Steganography.decode_image(input_path, lsb)
                        
        elif(input_path.endswith(('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'))):
            print("Decoding message from audio...")
            return Steganography.decode_audio(input_path, lsb)
        
        elif(input_path.endswith(('.mp4', '.avi', '.mov', '.mkv'))):
            print("Decoding message from video file...")
            return {"status": False, "message": "Video file encoding not supported yet"}
    
    
    @staticmethod
    def encode_image(img_path, msg, lsb, output_dir):
        """
        Use the LSBs of the pixels to encode the message into the image
        """
        fileExt = img_path.split('.')[-1]     
           
        if fileExt == '.gif' or fileExt == '.GIF':
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
        # if img.mode != 'RGB':
        #     print("image mode needs to be RGB")
        #     return {"status": False, "message": "image mode needs to be RGB"}
        
        total_image_bits = width * height * 3 * 8
        print("Total amount of characters used up: " + str(length) + "/" + str(max_payload_char) + " (" + str(length / max_payload_char * 100) + "%)")
        print("Total amount of bits available in image: " + str(total_image_bits))
        print("Total amount of bits to replace for payload: " + str(length * 8))
        print("Estimated image distortion: " + str(length * 8 / total_image_bits * 100) + "%")
        
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
                    # r |= int(binary_msg[index:index+lsb], 2)  # Red channel
                    index += lsb
                if index < len_binary_msg:
                    secretBits = binary_msg[index:index+lsb]
                    if len(secretBits) < lsb:
                        secretBits = secretBits.ljust(lsb, '0')
                    secretBitsInt = int(secretBits, 2)
                    g = g | secretBitsInt
                    # g |= int(binary_msg[index:index+lsb], 2)  # Green channel
                    index += lsb
                if index < len_binary_msg:
                    secretBits = binary_msg[index:index+lsb]
                    if len(secretBits) < lsb:
                        secretBits = secretBits.ljust(lsb, '0')
                    secretBitsInt = int(secretBits, 2)
                    b = b | secretBitsInt
                    # b |= int(binary_msg[index:index+lsb], 2)  # Blue channel
                    index += lsb
                if index >= len_binary_msg:
                    break
                
                encoded.putpixel((col, row), (r, g, b, a))
                
        if isinstance(encoded, Image.Image):
            # encoded.save(output_path)
            # get img path extension to save the image in the same format
            img_ext = img_path.split('.')
            output_path = os.path.join(output_dir + '/stego_image.' + img_ext[-1])
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
            if fileExt == '.gif' or fileExt == '.GIF':
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

            #print("decoded_msg with stopping code: " + decoded_msg)
            #print("decoded_msg without stopping code: " + decoded_msg[:stopping_code_position])

            return {"status": True, "message": decoded_msg}
        except Exception as e:
            return {"status": False, "message": str(e)}
    
    
    # Reference :https://sumit-arora.medium.com/audio-steganography-the-art-of-hiding-secrets-within-earshot-part-2-of-2-c76b1be719b3
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
        
        # Check if message is too long for audio
        # if len(secretBits) > (len(frame_bytes) * 8):
        #     return {"status": False, "message": "The message is too long for the audio file"}
        
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
                    # byte = (byte & ~(1 << bit_index)) | (bit << bit_index)
            frame_bytes[i//lsb] = byte
        
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)
        output_path = os.path.join(output_dir + '/encoded_audio.' + fileExt)
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
            # Use wave package (native to Python) for reading the received audio file
            import wave
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
                # if payload_bin[-8:] == "00111101": # stop_char '=' = 00111101
                #     payload_bin = payload_bin[:-8]
                #     break
            
            # Convert binary payload to text
            payload = ''
            for i in range(0, len(payload_bin), 8):
                byte = payload_bin[i:i+8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    if char is "=": # stop code reached
                        break
                    else:
                        payload += char
            
            song.close()
            return {"status": True, "message": payload}
        except Exception as e:
            return {"status": False, "message": str(e)}
        
        
    @staticmethod
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