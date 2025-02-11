import string
import sys
from PIL import Image, ExifTags # type: ignore
from stegano import lsb, lsbset # type: ignore
from stegano.lsbset import generators # type: ignore
from tkinter import OptionMenu, Tk, filedialog, Button, Label, StringVar
import cv2 # type: ignore
import os
import numpy as np # type: ignore
import face_recognition # type: ignore



def extract_gps(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return "No EXIF data found."

            gps_data = {}
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    for key in value:
                        sub_tag_name = ExifTags.GPSTAGS.get(key, key)
                        gps_data[sub_tag_name] = value[key]


            if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                lat = gps_data["GPSLatitude"]
                lon = gps_data["GPSLongitude"]
                lat_ref = gps_data.get("GPSLatitudeRef", "N")
                lon_ref = gps_data.get("GPSLongitudeRef", "E")

                latitude = convert_to_decimal(lat, lat_ref)
                longitude = convert_to_decimal(lon, lon_ref)
                lati= decimal_to_dms(latitude, is_latitude=True)
                longi= decimal_to_dms(longitude, is_latitude=False)
                print("To be precise Lat/Lon: (",lati,")/(",longi,")")
                return f"In decimal Latitude: {latitude}, Longitude: {longitude}"
                
            else:
                return "No GPS data found."
    except Exception as e:
        return f"Error: {e}"



def convert_to_decimal(coords, ref):
    degrees, minutes, seconds = coords
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ["S", "W"]:
        decimal = -decimal
    return decimal

def decimal_to_dms(decimal_value, is_latitude=True):
    """Convert a decimal GPS coordinate to degrees, minutes, and seconds."""
    direction = "N" if is_latitude else "E"
    if decimal_value < 0:
        direction = "S" if is_latitude else "W"
    decimal_value = abs(decimal_value)
    
    degrees = int(decimal_value)
    minutes_float = (decimal_value - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60

    return f"{degrees} deg {minutes}' {seconds:.2f}\" {direction}"

    
def extract_stegano(image_path):
    try:
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()

        printable_chars = ''.join(
            chr(byte) for byte in image_data if chr(byte) in string.printable
        )

        if not printable_chars:
            return "Aucune chaîne de caractères interprétable trouvée."


        # Extraction de blocs PGP s'ils sont présents
        start = printable_chars.find("-----BEGIN PGP PUBLIC KEY BLOCK-----")
        end = printable_chars.find("-----END PGP PUBLIC KEY BLOCK-----") + len("-----END PGP PUBLIC KEY BLOCK-----")

        if start != -1 and end != -1:
            pgp_block = printable_chars[start:end]
            print("[PGP Public Key Block détecté] :")
            # print(pgp_block)
            return pgp_block

        return printable_chars

    except Exception as e:
        return f"Erreur lors de l'extraction : {e}"




def embed_stegano(image_path, message, output_path):
    try:
        secret_image = lsbset.hide(image_path, message, generators.eratosthenes())
        secret_image.save(output_path)
        return f"Message successfully embedded in {output_path}."
    except Exception as e:
        return f"Error: {e}"


def extract_stegano_alternate(image_path):
    try:
        hidden_data = lsbset.reveal(image_path, generators.eratosthenes())
        return hidden_data if hidden_data else "No hidden data found."
    except Exception as e:
        return f"Error: {e}"


def compare_faces(image1_path, image2_path, tolerance=0.5):
    try:
        # Charger les images
        image1 = face_recognition.load_image_file(image1_path)
        image2 = face_recognition.load_image_file(image2_path)

        # Encodages des visages
        encodings1 = face_recognition.face_encodings(image1)
        encodings2 = face_recognition.face_encodings(image2)

        if not encodings1 or not encodings2:
            return "No faces detected in one or both images."

        # Comparer avec tolérance stricte
        result = face_recognition.compare_faces([encodings1[0]], encodings2[0], tolerance=tolerance)

        return "Faces match!" if result[0] else "Faces do not match."
    except Exception as e:
        return f"Error: {e}"

# Main function for CLI
def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "-help":
        print("Usage:")
        print("  image -map 'or -m' <image_path>             # Extract GPS data")
        print("  image -steg 'or -s' <image_path>            # Reveal hidden data (LSB)")
        print("  image -steg-alt <image_path>        # Reveal hidden data (Alternate)")
        print("  image -embed <image_path> <message> <output_path>  # Embed hidden data")
        print("  image -compare 'or -c'<image1> <image2>    # Compare faces in two images")
        return

    command = sys.argv[1]

    if (command == "-map" or command == "-m") and len(sys.argv)>2 :
        image_path = sys.argv[2]
        print(extract_gps(image_path))
    elif (command == "-steg" or command == "-s") and len(sys.argv)>2:
        image_path = sys.argv[2]
        print(extract_stegano(image_path))
    elif (command == "-steg-alt" or command == "-sta") and len(sys.argv)>2 :
        image_path = sys.argv[2]
        print(extract_stegano_alternate(image_path))
    elif (command == "-embed" or command == "-e") and len(sys.argv)>4 :
        image_path, message, output_path = sys.argv[2], sys.argv[3], sys.argv[4]
        print(embed_stegano(image_path, message, output_path))
    elif command == "-compare" and len(sys.argv)>2 :
        image1, image2 = sys.argv[2], sys.argv[3]
        print(compare_faces(image1, image2))

    else:
        print("Invalid command. Try the command '-h' or '-help' for usage.")


if __name__ == "__main__":
    main()
