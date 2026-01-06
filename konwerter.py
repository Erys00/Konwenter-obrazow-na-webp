#!/usr/bin/env python3
"""
Konwerter obrazów do formatu WebP
Konwertuje zdjęcia z folderu 'do przerobienia' na format WebP
i zapisuje je w folderze 'przerobione'.
"""

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Biblioteka Pillow nie jest zainstalowana.")
    print("Zainstaluj ją komendą: pip install Pillow")
    exit(1)

# Obsługa formatu HEIC
HEIC_SUPPORTED = False
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    pass

# Ścieżki do folderów
SCRIPT_DIR = Path(__file__).parent
INPUT_FOLDER = SCRIPT_DIR / "do przerobienia"
OUTPUT_FOLDER = SCRIPT_DIR / "przerobione"

# Obsługiwane formaty obrazów
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif'}
HEIC_FORMATS = {'.heic', '.heif'}


def create_folders():
    """Tworzy foldery wejściowy i wyjściowy jeśli nie istnieją."""
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    print(f"📁 Folder wejściowy: {INPUT_FOLDER}")
    print(f"📁 Folder wyjściowy: {OUTPUT_FOLDER}")


def convert_to_webp(input_path: Path, output_path: Path, quality: int = 85):
    """
    Konwertuje obraz do formatu WebP.
    
    Args:
        input_path: Ścieżka do pliku wejściowego
        output_path: Ścieżka do pliku wyjściowego
        quality: Jakość kompresji (0-100), domyślnie 85
    """
    try:
        with Image.open(input_path) as img:
            # Konwertuj do RGB jeśli obraz ma kanał alfa i jest w trybie RGBA
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Zachowaj przezroczystość dla formatów które ją obsługują
                img.save(output_path, 'WEBP', quality=quality, lossless=False)
            else:
                # Konwertuj do RGB dla innych trybów
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, 'WEBP', quality=quality)
        return True
    except Exception as e:
        print(f"  ❌ Błąd podczas konwersji {input_path.name}: {e}")
        return False


def get_file_size_mb(path: Path) -> float:
    """Zwraca rozmiar pliku w MB."""
    return path.stat().st_size / (1024 * 1024)


def main():
    """Główna funkcja programu."""
    print("=" * 50)
    print("🖼️  Konwerter obrazów do WebP")
    print("=" * 50)
    
    # Tworzenie folderów
    create_folders()
    
    # Znajdowanie plików do konwersji
    all_formats = SUPPORTED_FORMATS.copy()
    if HEIC_SUPPORTED:
        all_formats.update(HEIC_FORMATS)
    
    image_files = [
        f for f in INPUT_FOLDER.iterdir()
        if f.is_file() and f.suffix.lower() in all_formats
    ]
    
    # Sprawdź czy są pliki HEIC bez wsparcia
    heic_files = [
        f for f in INPUT_FOLDER.iterdir()
        if f.is_file() and f.suffix.lower() in HEIC_FORMATS
    ]
    if heic_files and not HEIC_SUPPORTED:
        print(f"\n⚠️  Znaleziono {len(heic_files)} plików HEIC, ale brak biblioteki pillow-heif.")
        print("   Zainstaluj ją komendą: pip install pillow-heif")
    
    if not image_files:
        print(f"\n⚠️  Brak obrazów do konwersji w folderze '{INPUT_FOLDER}'")
        print(f"   Obsługiwane formaty: {', '.join(sorted(all_formats))}")
        return
    
    print(f"\n📷 Znaleziono {len(image_files)} obrazów do konwersji\n")
    
    # Konwersja obrazów
    success_count = 0
    total_input_size = 0
    total_output_size = 0
    
    for i, input_file in enumerate(image_files, 1):
        output_file = OUTPUT_FOLDER / f"{input_file.stem}.webp"
        
        print(f"[{i}/{len(image_files)}] Konwertuję: {input_file.name}", end="")
        
        input_size = get_file_size_mb(input_file)
        total_input_size += input_size
        
        if convert_to_webp(input_file, output_file):
            output_size = get_file_size_mb(output_file)
            total_output_size += output_size
            reduction = ((input_size - output_size) / input_size) * 100 if input_size > 0 else 0
            print(f" ✅ ({input_size:.2f} MB → {output_size:.2f} MB, -{reduction:.1f}%)")
            success_count += 1
        else:
            print()
    
    # Podsumowanie
    print("\n" + "=" * 50)
    print("📊 PODSUMOWANIE")
    print("=" * 50)
    print(f"✅ Skonwertowano: {success_count}/{len(image_files)} plików")
    print(f"📥 Rozmiar wejściowy: {total_input_size:.2f} MB")
    print(f"📤 Rozmiar wyjściowy: {total_output_size:.2f} MB")
    
    if total_input_size > 0:
        total_reduction = ((total_input_size - total_output_size) / total_input_size) * 100
        print(f"💾 Oszczędność miejsca: {total_input_size - total_output_size:.2f} MB ({total_reduction:.1f}%)")
    
    print(f"\n📁 Pliki zapisano w: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
