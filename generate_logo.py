# generate_logo.py
from PIL import Image, ImageDraw, ImageFont

# Taille du logo
size = (200, 200)
bg_color = (31, 59, 90)        # bleu foncé
text_color = (255, 255, 255)   # blanc

# Créer l'image
img = Image.new("RGB", size, color=bg_color)
draw = ImageDraw.Draw(img)

# Ajouter un cercle (style graphique)
draw.ellipse((50, 50, 150, 150), outline=text_color, width=5)

# Ajouter le texte "ML"
try:
    font = ImageFont.truetype("arial.ttf", 60)
except:
    font = ImageFont.load_default()
draw.text((60, 70), "ML", fill=text_color, font=font)

# Sauvegarder
img.save("assets/logo.png")
print("✅ Logo généré dans assets/logo.png")