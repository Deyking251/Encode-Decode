from flask import Flask, render_template, request
import urllib.parse
import codecs
import base64

app = Flask(__name__)

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': '/'
}
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

# Braille Dictionary
BRAILLE_DICT = {
    'A': '100000', 'B': '101000', 'C': '110000', 'D': '110100', 'E': '100100',
    'F': '111000', 'G': '111100', 'H': '101100', 'I': '011000', 'J': '011100',
    'K': '100010', 'L': '101010', 'M': '110010', 'N': '110110', 'O': '100110',
    'P': '111010', 'Q': '111110', 'R': '101110', 'S': '011010', 'T': '011110',
    'U': '100011', 'V': '101011', 'W': '011101', 'X': '110011', 'Y': '110111', 'Z': '100111',
    '1': '100000', '2': '101000', '3': '110000', '4': '110100', '5': '100100',
    '6': '111000', '7': '111100', '8': '101100', '9': '011000', '0': '011100',
    ' ': '000000'
}
REVERSE_BRAILLE_DICT = {v: k for k, v in BRAILLE_DICT.items()}

# Encoding Functions
def utf8_encoding(text):
    return text.encode("utf-8").hex()  

def url_encoding(text):
    return urllib.parse.quote(text)

def hex_encoding(text):
    return text.encode().hex()

def rot13_encoding(text):
    return codecs.encode(text, 'rot_13')

def binary_encoding(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def octal_encoding(text):
    return ' '.join(format(ord(char), 'o') for char in text)

def punycode_encoding(text):
    return text.encode('punycode').decode()

def morse_encoding(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '?') for char in text)

def braille_encoding(text):
    return ' '.join(BRAILLE_DICT.get(char.upper(), '?') for char in text)

def base64_encoding(text):
    return base64.b64encode(text.encode()).decode()

# Decoding Functions
def decode_utf8(text):
    try:
        return bytes.fromhex(text).decode("utf-8")
    except ValueError:
        return "Invalid UTF-8 Hex Input"

def decode_url(text):
    return urllib.parse.unquote(text)

def decode_hex(text):
    try:
        return bytes.fromhex(text).decode()
    except ValueError:
        return "Invalid Hex Input"

def decode_rot13(text):
    return codecs.decode(text, 'rot_13')

def decode_binary(text):
    try:
        return ''.join(chr(int(b, 2)) for b in text.split())
    except ValueError:
        return "Invalid Binary Input"

def decode_octal(text):
    try:
        return ''.join(chr(int(o, 8)) for o in text.split())
    except ValueError:
        return "Invalid Octal Input"

def decode_punycode(text):
    try:
        return text.encode().decode('punycode')
    except UnicodeError:
        return "Invalid Punycode Input"

def decode_morse(text):
    return ''.join(REVERSE_MORSE_CODE_DICT.get(code, '?') for code in text.split())

def decode_braille(text):
    return ''.join(REVERSE_BRAILLE_DICT.get(code, '?') for code in text.split())

def decode_base64(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return "Invalid Base64 Input"

# Encoding & Decoding Dictionary
ENCODINGS = {
    "utf8": utf8_encoding,
    "url": url_encoding,
    "hex": hex_encoding,
    "rot13": rot13_encoding,
    "binary": binary_encoding,
    "octal": octal_encoding,
    "punycode": punycode_encoding,
    "morse": morse_encoding,
    "braille": braille_encoding,
    "base64": base64_encoding
}

DECODINGS = {
    "utf8": decode_utf8,
    "url": decode_url,
    "hex": decode_hex,
    "rot13": decode_rot13,
    "binary": decode_binary,
    "octal": decode_octal,
    "punycode": decode_punycode,
    "morse": decode_morse,
    "braille": decode_braille,
    "base64": decode_base64
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form.get("text")
        action = request.form.get("action")
        encoding_type = request.form.get("encoding")

        if action == "encode" and encoding_type in ENCODINGS:
            result = ENCODINGS[encoding_type](text)
        elif action == "decode" and encoding_type in DECODINGS:
            result = DECODINGS[encoding_type](text)
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
