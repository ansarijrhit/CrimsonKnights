from enum import Enum
import pandas as pd
import xml.etree.ElementTree as gfg
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

class CardType(Enum):
    CREATURE = 'C'
    MATERIAL = 'M'
    SPELL = 'S'
    REACTION = 'R'
    WEAPON = 'W'
    EQUIPMENT = 'E'
    HERO = 'H'

class Card:
    name: str
    card_type: str
    attack: int
    ac: int
    description: str

def card_type_to_row(card_type: CardType):
    if card_type == CardType.CREATURE.value:
        return 1
    if card_type == CardType.EQUIPMENT.value or card_type == CardType.WEAPON.value:
        return 0
    else:
        return 3
    
def generate_hero_image(name: str, attack: int, ac: int, hp: int, description: str):
    blank = Image.open('charactercardblank.jpg')
    im = Image.new('RGB', (400, 560))
    im.paste(blank)
    portrait = Image.open('CharacterPortraits/'+name+'.jpg')
    im.paste(portrait, (36, 68))
    bigFont = ImageFont.truetype(font="C:/Users/System-Pc/Desktop/arial.ttf", size=20)
    normalFont = ImageFont.truetype(font="C:/Users/System-Pc/Desktop/arial.ttf", size=15)
    d = ImageDraw.Draw(im)
    d.text((39, 34), name, fill="black",font=bigFont)
    d.text((301, 34), 'HP: ' + str(hp), fill="black",font=bigFont)
    lines = textwrap.wrap(description, width=46)
    y_text = 354
    for line in lines:
        d.text((40, y_text), line, fill="black", font=normalFont)
        y_text += 17
    d.text((200, 520), 'Attack: '+str(int(attack)), fill="black", font=normalFont)
    d.text((300, 520), 'AC: '+str(int(ac)), fill="black", font=normalFont)
    im.save('images/'+name.replace("/", " ")+'.jpg', quality=95)

def generate_image(name: str, cardtype: str, attack: int, ac: int, description: str, character: str):
    blank = Image.open('cardblank.jpg')
    im = Image.new('RGB', (400, 560))
    im.paste(blank)
    iconIm = Image.open('./icons/'+cardtype+'.png')
    im.paste(iconIm, (100, 80), iconIm)
    bigFont = ImageFont.truetype(font="C:/Users/System-Pc/Desktop/arial.ttf", size=20)
    normalFont = ImageFont.truetype(font="C:/Users/System-Pc/Desktop/arial.ttf", size=15)
    d = ImageDraw.Draw(im)
    d.text((39, 34), name, fill="black",font=bigFont)
    d.text((280, 34), character, fill="black",font=bigFont)
    d.text((145, 318), cardtype, fill="black", font = bigFont)
    lines = textwrap.wrap(description, width=46)
    y_text = 354
    for line in lines:
        d.text((40, y_text), line, fill="black", font=normalFont)
        y_text += 15
    if cardtype == CardType.CREATURE.name:
        d.text((200, 515), 'Attack: '+str(int(attack)), fill="black", font=normalFont)
        d.text((300, 515), 'AC: '+str(int(ac)), fill="black", font=normalFont)
    im.save('images/'+name.replace("/", " ")+'.jpg', quality=95)




def main():
    image_names = os.listdir("images")
    for image in image_names:
        if ".jpg" in image:
            os.remove("images/" + image)
    data = pd.concat([pd.read_excel('card_lists/' + filename) for filename in os.listdir('card_lists')])
    xml = gfg.Element('cockatrice_carddatabase')
    xml.set("version", "4")

    sets = gfg.Element('sets')
    xml.append(sets)

    characters = data['Character'].unique()

    for character in characters:
        card_set = gfg.SubElement(sets, 'set')

        gfg.SubElement(card_set, 'name').text = "CKCG: " + character
        gfg.SubElement(card_set, 'longname').text = character
        gfg.SubElement(card_set, 'settype').text = "Custom"

        releasedate = gfg.SubElement(card_set, 'releasedate')
        releasedate.text = "XX-XX-XXXX"

    cards = gfg.Element('cards')
    xml.append(cards)



    for index, row in data.iterrows():
        card = gfg.SubElement(cards, 'card')

        name = gfg.SubElement(card, 'name')
        name.text = row['Name'].replace("/", " ")

        text = gfg.SubElement(card, 'text')
        text.text = str(row['Description'])

        prop = gfg.SubElement(card, 'prop')
        gfg.SubElement(prop, 'layout').text = "normal"
        gfg.SubElement(prop, 'side').text = "front"
        gfg.SubElement(prop, 'type').text = CardType(row['Type']).name
        gfg.SubElement(prop, 'maintype').text = CardType(row['Type']).name
        gfg.SubElement(prop, 'manacost').text = "0"
        gfg.SubElement(prop, 'cmc').text = "0"
        if row['Type'] == CardType.CREATURE.value: gfg.SubElement(prop, 'pt').text = str(int(row['Attack'])) + "/" + str(int(row['AC']))
        gfg.SubElement(prop, 'format-standard').text = "legal"
        gfg.SubElement(prop, 'format-commander').text = "legal"
        gfg.SubElement(prop, 'format-modern').text = "legal"
        gfg.SubElement(prop, 'format-pauper').text = "legal"

        rarity = gfg.SubElement(card, 'set')
        rarity.text = "CKCG: " + row["Character"]
        rarity.set('rarity', "Common")

        gfg.SubElement(card, 'tablerow').text = str(card_type_to_row(row['Type']))
    #     print(card_type_to_row(row['Type']))

        generate_image(row['Name'], CardType(row['Type']).name, row['Attack'], row['AC'], str(row['Description']), row['Character'])

    heros = pd.read_excel('characters.xlsx')

    for index, row in heros.iterrows():
        card = gfg.SubElement(cards, 'card')

        name = gfg.SubElement(card, 'name')
        name.text = row['Name'].replace("/", " ")

        text = gfg.SubElement(card, 'text')
        text.text = str(row['Description'])

        prop = gfg.SubElement(card, 'prop')
        gfg.SubElement(prop, 'layout').text = "normal"
        gfg.SubElement(prop, 'side').text = "front"
        gfg.SubElement(prop, 'type').text = CardType(row['Type']).name
        gfg.SubElement(prop, 'maintype').text = CardType(row['Type']).name
        gfg.SubElement(prop, 'manacost').text = "0"
        gfg.SubElement(prop, 'cmc').text = "0"
        gfg.SubElement(prop, 'pt').text = str(int(row['Attack'])) + "/" + str(int(row['AC']))
        gfg.SubElement(prop, 'format-standard').text = "legal"
        gfg.SubElement(prop, 'format-commander').text = "legal"
        gfg.SubElement(prop, 'format-modern').text = "legal"
        gfg.SubElement(prop, 'format-pauper').text = "legal"

        rarity = gfg.SubElement(card, 'set')
        rarity.text = "CKCG: " + row["Name"]
        rarity.set('rarity', "Common")

        gfg.SubElement(card, 'tablerow').text = "3"

        generate_hero_image(row['Name'], row['Attack'], row['AC'], row['HP'], str(row['Description']))

    tree = gfg.ElementTree(xml) 


    save_path_file = "CrimsonKnights.xml"
    header = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    with open(save_path_file, "wb") as f:
        f.write(header.encode('utf-8'))
        tree.write(f)


main()

#<?xml version="1.0" encoding="UTF-8"?>