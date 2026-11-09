"""Genere 2 images de test dans le dossier samples/ (recu + lettre).
Lancer : python make_samples.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

os.makedirs("samples", exist_ok=True)


def font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def make(path, lines, size=(800, 600), fsize=30):
    img = Image.new("RGB", size, "white")
    d = ImageDraw.Draw(img)
    f = font(fsize)
    y = 30
    for line in lines:
        d.text((40, y), line, fill="black", font=f)
        y += fsize + 16
    img.save(path)
    print("cree :", path)


make(
    "samples/recu.png",
    [
        "SUPERMARCHE EL AMEL",
        "Date: 03/11/2026",
        "",
        "Lait 1L            2.100 TND",
        "Pain               0.250 TND",
        "Fromage            6.800 TND",
        "Eau 1.5L           1.200 TND",
        "",
        "TOTAL             10.350 TND",
        "Merci de votre visite",
    ],
)

make(
    "samples/lettre.png",
    [
        "Sesame University - La Marsa",
        "",
        "Dear students,",
        "The final project presentations will take",
        "place on December 15, 2026 in room B12.",
        "Please submit your report by December 10.",
        "",
        "Best regards,",
        "The Academic Office",
    ],
)
