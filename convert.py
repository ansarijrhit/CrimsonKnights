from enum import Enum
import pandas as pd
import xml.etree.ElementTree as gfg
from PIL import Image, ImageDraw, ImageFont
class CardType(Enum):
    CREATURE = 'C'
    SPELL = 'S'
    REACTION = 'R'
    WEAPON = 'W'
    EQUIPMENT = 'E'

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

def generate_image(name: str, cardtype: str, attack: str, ac: str, description: str, character: str):
    blank = Image.open('cardblank.jpg')
    im = Image.new('RGB', (400, 560))
    im.paste(blank)
    font = ImageFont.truetype(font="C:/Users/System-Pc/Desktop/arial.ttf", size=30)
    d = ImageDraw.Draw(im)
    d.multiline_text((39, 37), name, fill=(0, 0, 0), )
    im.save('images/'+name+'.jpg', quality=95)




def main():
    print("loading card data")
    data = pd.read_excel('cards.xlsx')
    print(data)

  
    xml = gfg.Element('cockatrice_carddatabase')
    xml.set("version", "4")

    sets = gfg.Element('sets')
    xml.append(sets)

    characters = data['Character'].unique()

    for character in characters:
        card_set = gfg.SubElement(sets, 'set')

        gfg.SubElement(card_set, 'name').text = character
        gfg.SubElement(card_set, 'longname').text = character
        gfg.SubElement(card_set, 'settype').text = "Custom"

        releasedate = gfg.SubElement(card_set, 'releasedate')
        releasedate.text = "XX-XX-XXXX"

    cards = gfg.Element('cards')
    xml.append(cards)
    
    for index, row in data.iterrows():
        card = gfg.SubElement(cards, 'card')

        name = gfg.SubElement(card, 'name')
        name.text = row['Name']

        text = gfg.SubElement(card, 'text')
        text.text = row['Description']

        prop = gfg.SubElement(card, 'prop')
        gfg.SubElement(prop, 'layout').text = "normal"
        gfg.SubElement(prop, 'side').text = "front"
        gfg.SubElement(prop, 'type').text = CardType(row['Type']).name
        gfg.SubElement(prop, 'maintype').text = CardType(row['Type']).name
        gfg.SubElement(prop, 'manacost').text = "0"
        gfg.SubElement(prop, 'cmc').text = "0"
        if row['Type'] == CardType.CREATURE: gfg.SubElement(prop, 'pt').text = str(row['Attack']) + "/" + str(row['AC'])
        gfg.SubElement(prop, 'format-standard').text = "legal"
        gfg.SubElement(prop, 'format-commander').text = "legal"
        gfg.SubElement(prop, 'format-modern').text = "legal"
        gfg.SubElement(prop, 'format-pauper').text = "legal"

        rarity = gfg.SubElement(card, 'set')
        rarity.text = row["Character"]
        rarity.set('rarity', "Common")

        gfg.SubElement(card, 'tablerow').text = str(card_type_to_row(row['Type']))
        print(card_type_to_row(row['Type']))

        generate_image(row['Name'], CardType(row['Type']).name, str(row['Attack']), str(row['AC']), row['Description'], row['Character'])

    tree = gfg.ElementTree(xml) 

    
    save_path_file = "CrimsonKnights.xml"
    header = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    with open(save_path_file, "wb") as f:
        f.write(header.encode('utf-8'))
        tree.write(f)

main()

#<?xml version="1.0" encoding="UTF-8"?>