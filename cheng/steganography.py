from PIL import Image
import wave
import os 
import subprocess

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
            print("Decoding message into image...")
            return Steganography.decode_image(input_path, lsb)
                        
        elif(input_path.endswith(('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'))):
            print("Encoding message into audio...")
            return Steganography.decode_audio(input_path, lsb)
        
        elif(input_path.endswith(('.mp4', '.avi', '.mov', '.mkv'))):
            print("Encoding message into video file...")
            return {"status": False, "message": "Video file encoding not supported yet"}
    
    
    @staticmethod
    def encode_image(img_path, msg, lsb, output_dir):
        """
        Use the LSB of the pixels to encode the message into the image
        """
        fileExt = img_path.split('.')[-1]     
           
        if fileExt == '.gif' or fileExt == '.GIF':
            img = Image.open(img_path).convert("RGB")
        else:
            img = Image.open(img_path)
        length = len(msg)
        if length > 255:
            print("text too long! (don't exceed 255 characters)")
            return {"status": False, "message": "text too long! (don't exceed 255 characters)"}
        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return {"status": False, "message": "image mode needs to be RGB"}
        encoded = img.copy()
        width, height = img.size
        index = 0

        mask = 0xFF << lsb  # Create a mask to clear the least significant bits

        binary_msg = ''.join([format(ord(i), '08b') for i in msg])  # Convert the message to binary

        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))

                # Clear the least significant bits
                r &= mask
                g &= mask
                b &= mask

                # Add the bits of the message
                if index < len(binary_msg):
                    r |= int(binary_msg[index:index+lsb], 2)  # Red channel
                    index += lsb
                if index < len(binary_msg):
                    g |= int(binary_msg[index:index+lsb], 2)  # Green channel
                    index += lsb
                if index < len(binary_msg):
                    b |= int(binary_msg[index:index+lsb], 2)  # Blue channel
                    index += lsb

                encoded.putpixel((col, row), (r, g, b))
                
        if isinstance(encoded, Image.Image):
            # encoded.save(output_path)
            # get img path extension to save the image in the same format
            img_ext = img_path.split('.')
            output_path = os.path.join(output_dir + '/encoded.' + img_ext[-1])
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
            msg = ""
            index = 0
            
            for row in range(height):
                for col in range(width):
                    r, g, b = img.getpixel((col, row))

                    # Extract the bits of the message
                    if index < len(msg):
                        msg += bin(r)[-lsb:]  # Red channel
                        index += lsb
                    if index < len(msg):
                        msg += bin(g)[-lsb:]  # Green channel
                        index += lsb
                    if index < len(msg):
                        msg += bin(b)[-lsb:]  # Blue channel
                        index += lsb

            # Convert the binary message to a string
            decoded_msg = ''.join(chr(int(msg[i:i+8].replace('b', ''), 2)) for i in range(0, len(msg), 8))

            print(decoded_msg)

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
        # Read frames and convert to byte array
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))

        # Check if message is too long for audio
        if len(msg) > 255:
            return {"status": False, "message": "The message is too long for the audio file"}

        # The "secret" text message
        string = msg
        # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
        string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
        # Convert text to bit array
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & (255 - 2**lsb)) | bit
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)

        output_path = os.path.join(output_dir + '/encoded.' + fileExt)
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

            # Extract the LSB of each byte
            extracted = [frame_bytes[i] & (1 << lsb) for i in range(len(frame_bytes))]
            # Convert byte array back to string
            string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
            # Cut off at the filler characters
            decoded = string.split("###")[0]
            song.close()
            return {"status": True, "message": decoded}
        except Exception as e:
            return {"status": False, "message": str(e)}