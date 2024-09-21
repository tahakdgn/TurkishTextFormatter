# -*- coding: utf-8 -*-
import json

def get_language_choice():
    while True:
        choice = input("Turkish or English? / Türkçe mi İngilizce mi?\nTürkçe için 1, For English press 2: ")
        if choice in ['1', '2']:
            return choice
        print("Invalid choice. Please try again. / Geçersiz seçim. Lütfen tekrar deneyin.")

def get_messages(lang):
    if lang == '1':  # Turkish
        return {
            "file_path_prompt": r"Lütfen JSON dosyasının tam yolunu girin (örneğin, C:\tr.json): ",
            "file_not_found": "Dosya bulunamadı. Lütfen dosya yolunu kontrol edin.",
            "invalid_json": "Geçersiz JSON dosyası. Lütfen dosyanın içeriğini kontrol edin.",
            "file_saved": "Güncellenmiş dosya şu adla kaydedildi: {}",
            "file_write_error": "Dosya yazma hatası oluştu: {}"
        }
    else:  # English
        return {
            "file_path_prompt": r"Please enter the full path of the JSON file (e.g., C:\tr.json): ",
            "file_not_found": "File not found. Please check the file path.",
            "invalid_json": "Invalid JSON file. Please check the file contents.",
            "file_saved": "Updated file saved as: {}",
            "file_write_error": "File writing error occurred: {}"
        }

lang_choice = get_language_choice()
messages = get_messages(lang_choice)

# Get the file path for the JSON file from the user
file_path = input(messages["file_path_prompt"])

# Load the JSON file from the specified path
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print(messages["file_not_found"])
    exit(1)
except json.JSONDecodeError:
    print(messages["invalid_json"])
    exit(1)

# Function for Turkish-specific case conversion
def capitalize_turkish_v2(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "text" and isinstance(value, str):
                # Replace İ with i, I with ı and capitalize only the first letter
                value = value.replace("\u0130", "i").replace("I", "\u0131").capitalize()
                obj[key] = value
            else:
                capitalize_turkish_v2(value)
    elif isinstance(obj, list):
        for item in obj:
            capitalize_turkish_v2(item)
    return obj

# Apply the updated function to the data
updated_turkish_data_v2 = capitalize_turkish_v2(data)

# Save the new updated JSON to a file
output_turkish_file_v2 = 'updated_tr_turkish_v2.json'
try:
    with open(output_turkish_file_v2, 'w', encoding='utf-8') as file:
        json.dump(updated_turkish_data_v2, file, ensure_ascii=False, indent=2)
    print(messages["file_saved"].format(output_turkish_file_v2))
except IOError:
    print(messages["file_write_error"].format(output_turkish_file_v2))
    exit(1)