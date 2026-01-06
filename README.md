# Konwerter obrazów na WebP

Prosty skrypt do konwersji zdjęć na format WebP. Wrzuć pliki do folderu `do przerobienia`, uruchom skrypt i gotowe - skonwertowane obrazy znajdziesz w `przerobione`.

## Jak używać

1. Zainstaluj wymagane biblioteki:
   ```bash
   pip install Pillow
   ```

2. Wrzuć zdjęcia do folderu `do przerobienia`

3. Uruchom skrypt:
   ```bash
   python konwerter.py
   ```

4. Skonwertowane pliki znajdziesz w folderze `przerobione`

## Obsługiwane formaty

JPG, PNG, BMP, GIF, TIFF

Opcjonalnie HEIC (wymaga `pip install pillow-heif`)

## Co robi

- Konwertuje obrazy do WebP z jakością 85%
- Pokazuje postęp i statystyki oszczędności miejsca
- Zachowuje przezroczystość dla formatów które ją obsługują

