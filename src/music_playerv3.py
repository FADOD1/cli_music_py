from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image
from term_image.image import BlockImage
import io
import sys
import os

def calculate_terminal_size(image, max_width=None):
    # Obtém o tamanho do terminal
    term_width, term_height = os.get_terminal_size()
    
    # Define largura máxima (80% do terminal)
    max_width = max_width or int(term_width * 0.8)
    
    # Calcula proporção
    aspect_ratio = image.width / image.height
    
    # Ajusta para proporção de caracteres do terminal (~2:1)
    terminal_char_ratio = 2.0
    new_height = int((max_width / aspect_ratio) * terminal_char_ratio)
    
    return (max_width, new_height)



def extract_and_display_cover(mp3_file_path, scale=0.8):
    audio = MP3(mp3_file_path, ID3=ID3)
    
    # Extrair imagem
    for tag in audio.tags.values():
        if tag.FrameID == 'APIC':
            image = Image.open(io.BytesIO(tag.data))
            break
    else:
        print("Nenhuma imagem encontrada.")
        return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} [arquivo.mp3] [escala (0.1-1.0)]")
    else:
        scale = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
        extract_and_display_cover(sys.argv[1], scale)