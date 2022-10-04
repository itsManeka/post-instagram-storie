from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from io import BytesIO
import textwrap
import requests
import sys
import os

from instagrapi import Client
from instagrapi.types import StoryLink

# IG_USERNAME = "gibipromo"
# IG_PASSWORD = "Setembro@27"
# IMAGE_LINK = "https://m.media-amazon.com/images/I/61auvO7PuuL._SL500_.jpg"
# PRECO = "R$ XXX,XX"
# DESCONTO = "(XXX% off)"
# PRECO_CAPA = "R$ XXX,XX"
# TITULO = "Desconsiderar"
# DESCRICAO = "Favor desconsiderar esse story, ele é um teste. Com uma descrição muito muito grande para ver como fica na imagem e letras pequenas para não quebrar."
# LINK = 'https://google.com.br'

IG_USERNAME = sys.argv[1]
IG_PASSWORD = sys.argv[2]
IMAGE_LINK = sys.argv[3]
PRECO = sys.argv[4]
DESCONTO = sys.argv[5]
PRECO_CAPA = sys.argv[6]
TITULO = sys.argv[7]
DESCRICAO = sys.argv[8]
LINK = sys.argv[9]
IG_CREDENTIAL_PATH = './src/python/credential.json'

cl = Client()

def login():
    global cl
    
    try:
        if os.path.exists(IG_CREDENTIAL_PATH):
            cl.load_settings(IG_CREDENTIAL_PATH)
            cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(IG_CREDENTIAL_PATH)
        return True
    except:
        print("Erro: Erro ao logar")
        return False

def save_image():
    
    try:
        try:
            response = requests.get(IMAGE_LINK)
        except:
            print('Erro: Erro ao requerir imagem')

        bg = Image.open('./src/python/res/story.jpg')
        image = Image.open(BytesIO(response.content))
        image = image.resize((322, 430))
        link = Image.open('./src/python/res/link.png')

        imgcp = bg.copy()
        imgcp.paste(image, ((199), (311)))
        imgcp.paste(link, ((100), (1050)), link)

        draw = ImageDraw.Draw(imgcp)
        pos_y = 110
        pos_x = 60
        position = (pos_x, pos_y)

        # Titulo
        font = ImageFont.truetype('./src/python/res/SEGUISB.TTF', 30)
        width, height = font.getsize(TITULO)
        lines = textwrap.wrap(TITULO, width=20)
        for line in lines:
            draw.text(position, line, font=font, fill="#662F8E", stroke_width=1, stroke_fill="#662F8E")
            pos_y += height
            position = (pos_x, pos_y)

        # Preço
        position = (460, 105)
        font = ImageFont.truetype('./src/python/res/SEGUISB.TTF', 40)
        draw.text(position, PRECO, font=font, fill="#662F8E", stroke_width=1, stroke_fill="#662F8E")
        
        #Preço capa
        pos_y = 150
        pos_x = 460
        position = (pos_x, pos_y)
        font = ImageFont.truetype('./src/python/res/SEGUISB.TTF', 30)
        width, height = font.getsize(PRECO_CAPA)
        draw.text(position, PRECO_CAPA, font=font, fill="#662F8E")

        pos_y += (height / 1.5)
        pos_xf = pos_x + width
        draw.line([(pos_x, pos_y), (pos_xf, pos_y)], fill="#662F8E", width=3)

        # Desconto
        position = (460, 185)
        font = ImageFont.truetype('./src/python/res/SEGUISB.TTF', 25)
        draw.text(position, DESCONTO, font=font, fill="#662F8E")

        # Descrição
        pos_y = 770
        pos_x = 60
        position = (pos_x, pos_y)

        font = ImageFont.truetype('./src/python/res/SEGUISB.TTF', 30)
        width, height = font.getsize(DESCRICAO)
        lines = textwrap.wrap(DESCRICAO, width=40)
        for line in lines:
            draw.text(position, line, font=font, fill="#662F8E", align='center')
            pos_y += height
            position = (pos_x, pos_y)

        imgcp.save('./src/python/res/img_final.jpg')

        return True
    except:
        print('Erro: Erro ao montar a imagem')
        return False

def post_story():
    global cl
    print('storie')
    #cl.photo_upload_to_story("./src/python/res/img_final.jpg", "", links=[StoryLink(webUri=LINK, x=0.29, y=0.84, width=0.3, height=0.05)])

def main():
    result = login()
    if result:
        result = save_image()

    if result: 
        post_story()

    print('finalizou')

if __name__ == "__main__":
    main()