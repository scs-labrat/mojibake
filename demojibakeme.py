from datetime import datetime
import pytz

def get_unicode_and_hex(mojibake_string):
    unicode_values = []
    hex_representation = []
    for c in mojibake_string:
        unicode_values.append(f"U+{ord(c):04X}")
        hex_representation.append(f'{ord(c):02x}')
    return unicode_values, ''.join(hex_representation)

def create_bytecode(hex_string):
    try:
        return bytes.fromhex(hex_string)
    except ValueError:
        print("Error converting hex to bytes. Ensure the hex string is valid.")
        return None

def try_decodings(bytecode, encodings):
    for encoding in encodings:
        try:
            decoded_text = bytecode.decode(encoding)
            print(f"Decoded text with {encoding}: {decoded_text}")
            return True  # Successful decoding
        except UnicodeDecodeError:
            print(f"Encoding {encoding} failed to decode the text.")
    return False  # No successful decoding

def main():
    
    
    # Set the timezone to PST for the given time
    pst = pytz.timezone('US/Pacific')
    current_time = datetime(2025, 2, 10, 4, 49, tzinfo=pst)
    print(f"Current time: {current_time.strftime('%I:%M %p on %B %d, %Y %Z')}")
    
    mojibake_string = input("Please enter your Mojibake string: ")
    
    unicode_values, hex_representation = get_unicode_and_hex(mojibake_string)
    print(f"\nUnicode values: {', '.join(unicode_values)}")
    print(f"Hexadecimal representation: {hex_representation}")
    
    bytecode = create_bytecode(hex_representation)
    if bytecode:
        print(f"Bytecode: {bytecode}")
        
        encodings = [
            "UTF-8", "UTF-16", "ISO-8859-1", "Windows-1252",
            "Shift_JIS", "EUC-JP", "ISO-2022-JP", "GBK", "Big5",
            "ISO-8859-2", "ISO-8859-5", "ISO-8859-7", "ISO-8859-8",
            "ISO-8859-9", "KOI8-R", "EUC-KR", "Windows-1251"
        ]
        
        while True:
            print("\nChoose an encoding from the following list, or choose 0 for all:")
            for i, encoding in enumerate(encodings, 1):
                print(f"{i}. {encoding}")
            print("0. Try all encodings")
            
            choice = input("Enter the number corresponding to your choice, or 'q' to quit: ")
            if choice.lower() == 'q':
                break
            
            if choice == '0':
                if not try_decodings(bytecode, encodings):
                    print("None of the encodings successfully decoded the text.")
                break
            else:
                try:
                    choice = int(choice) - 1
                    if 0 <= choice < len(encodings):
                        selected_encoding = [encodings[choice]]  # Wrap in list to match try_decodings signature
                        if not try_decodings(bytecode, selected_encoding):
                            retry = input("Decoding failed. Would you like to try another encoding? (y/n): ")
                            if retry.lower() != 'y':
                                break
                    else:
                        print("Invalid choice. Please select a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    main()