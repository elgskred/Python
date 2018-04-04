import pandas as pd
import re



regex = "Gain ..% of Physical Damage as Extra Fire Damage"
l = ['Socketed Gems are Supported by Level 22 Added Fire Damage','Socketed Gems are Supported by Level 16 Added Fire Damage','235 to Accuracy Rating']
l2 = ["+28 to Strength", "Gain 33% of Physical Damage as Extra Fire Damage", "Gain 18% of Physical Damage as Extra Cold Damage","+275 to Accuracy Rating",'Socketed Gems are Supported by Level 16 Added Fire Damage',"5% chance to gain Onslaught for 4 seconds on Kill",'Socketed Gems are Supported by Level 18 Faster Attacks']
matches = [string for string in l2 if re.match(regex, string)]
col = dagger.columns
for c in range(0, len(col)):
    for i in range(0, len(l2)):
        matches = [string for string in l2 if re.match(col[c], string)]
        itemString = l2[i]
        columnString = col[c]
        if itemString.split(columnString, 1)[-1] != itemString:
            print(itemString.split(columnString, 1)[-1])
            print(columnString)

def dagger():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/dagger')]
    dagger = pd.DataFrame(columns=lines)
    return dagger

def claw():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/claw')]
    claw = pd.DataFrame(columns=lines)
    return claw

def ring():
    ring = pd.DataFrame(columns=['maximum Life', 'maximum Mana', 'maximum Energy Shield',
                               'Physical Damage to Attacks', 'Fire Damage to Attacks',
                               'Cold Damage to Attacks', 'Lightning Damage to Attacks',
                               'Physical Attack Damage Leeched as Life', 'Evasion Rating',
                               'increased Elemental Damage with Attack Skills', 'Physical Attack Damage Leeched as Mana',
                               'increased Rarity of Items found', 'increased Evasion Rating',
                               'increased Armour', 'Chaos Damage to Attacks', 'Energy Shield Recharge',
                               'Strength', 'Dexterity', 'Intelligence', 'all Attributes',
                               'increased Cast Speed', 'increased Attack Speed', 'Accuracy Rating',
                               'Life Regenerated per second', 'increased Mana Regeneration Rate',
                               'Fire Resistance', 'Cold Resistance', 'Lightning Resistance',
                               'Chaos Resistance', 'Elemental Resistances', 'Life gained for each Enemy hit by your Attacks',
                               'increased Fire Damage', 'increased Cold Damage', 'increased Lightning Damage',
                               'increased Global Critical Strike Chance', 'crafted',
                               'reduced Reflected Elemental Damage taken', 'Cold Damage to Spells and Attacks',
                               'Lightning Damage to Spells and Attacks', 'increased Experience gain', 'Life gained for each Enemy hit by your Spells',
                               'Mana gained for each Enemy Hit by your Spells', 'Cold Damage against Chilled or Frozen Enemies',
                               'Lightning Damage against Shocked Enemies', 'reduced Effect of Curses on You', 'increased Spell Damage',
                               "Assassin's Mark on Hit", 'Herald of Ice Skill', 'Herald of Thunder Skill',
                               'Reflected Physical Damage taken', 'Fire Damage to Spells and Attacks',
                               'Mana gained for each Enemy hit by your Attacks', 'Fire Damage against Ignited Enemies', 'increased Melee Damage	',
                               'increased Projectile Attack Damage', 'Global Critical Strike Multiplier', 'increased Accuracy Rating',
                               "Poacher's Mark on Hit", "Warlord's Mark on Hit", 'Herald of Ash Skill', 'chance to Evade Attacks',
                               'elder', 'shaper', 'ilvl','stashID','itemID','price'])
    return ringDF

def wand():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/wand')]
    wand = pd.DataFrame(columns=lines)
    return wand

def one_handed_sword():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/oneSword')]
    one_handed_sword = pd.DataFrame(columns=lines)
    return one_handed_sword

def one_handed_axe():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/oneAxe')]
    one_handed_axe = pd.DataFrame(columns=lines)
    return one_handed_axe

def one_handed_mace():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/oneMace')]
    one_handed_mace = pd.DataFrame(columns=lines)
    return one_handed_mace

def scepter():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/scepter')]
    scepter = pd.DataFrame(columns=lines)
    return scepter

def bow():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/bow')]
    bow = pd.DataFrame(columns=lines)
    return bow

def staff():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/bow')]
    staff = pd.DataFrame(columns=lines)
    return staff

def two_handed_sword():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/twoSword')]
    two_handed_sword = pd.DataFrame(columns=lines)
    return two_handed_sword

def two_handed_axe():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/twoAxe')]
    two_handed_axe = pd.DataFrame(columns=lines)
    return two_handed_axe

