import pandas as pd
import re



regex = "Gain ..% of Physical Damage as Extra Fire Damage"
l = ['Socketed Gems are Supported by Level 22 Added Fire Damage','Socketed Gems are Supported by Level 16 Added Fire Damage','235 to Accuracy Rating']
l2 = ["+28 to Strength", "Gain 33% of Physical Damage as Extra Fire Damage", "Gain 18% of Physical Damage as Extra Cold Damage","+275 to Accuracy Rating","5% chance to gain Onslaught for 4 seconds on Kill"]
matches = [string for string in l2 if re.match(regex, string)]

def daggerDF():
    daggerDF = pd.DataFrame(columns=[
            'to maximum Mana',
            'increased Physical Damage',
            'to Accuracy Rating',
            'increased Physical Damage',
            'to Physical Damage',
            'to Fire Damage',
            'to Cold Damage',
            'to Lightning Damage',
            'increased Spell Damage',
            'increased Elemental Damage with Attack Skills',
            'to Level of Socketed Gems',
            'to Level of Socketed Fire Gems',
            'to Level of Socketed Cold Gems',
            'to Level of Socketed Lightning Gems',
            'to Level of Socketed Chaos Gems',
            'to Level of Socketed Melee Gems',
            'of Physical Attack Damage Leeched as Life',
            'of Physical Attack Damage Leeched as Mana',
            'to Fire Damage to Spells',
            'to Cold Damage to Spells',
            'to Lightning Damage to Spells',
            'to Chaos Damage',
            'of Fire Damage Leeched as Life',
            'of Cold Damage Leeched as Life',
            'of Lightning Damage Leeched as Life',
            'increased Curse Duration',
            'chance to Shock',
            'chance to Ignite',
            'chance to Freeze',
            'additional Block Chance while Dual Wielding',
            'chance to cause Bleeding on Hit',
            'reduced Enemy Block Chance',
            'increased Damage over Time',
            'to Dexterity',
            'to Intelligence',
            'increased Attack Speed',
            'increased Mana Regeneration Rate',
            'to Fire Resistance',
            'to Cold Resistance',
            'to Lightning Resistance',
            'to Chaos Resistance',
            'increased Stun Duration on Enemies',
            'increased Critical Strike Chance for Spells',
            'Life gained for each Enemy hit by Attacks',
            'Life gained on Kill',
            'Mana gained on Kill',
            'increased Critical Strike Chance',
            'to Global Critical Strike Multiplier',
            'reduced Attribute Requirements',
            'increased Light Radius',
            'increased Poison Duration',
            'chance to Poison on Hit',
            'increased Damage with Poison',
            'Life gained for each Enemy hit by your Attacks',
            'reduced Enemy Stun Threshold with this Weapon',
            'to Weapon range',
            'Socketed Gems are Supported by Level .. Added Fire Damage',
            'Socketed Gems are supported by Level .. Elemental Damage with Attacks',
            'of Physical Damage as Extra Cold Damage',
            'of Physical Damage as Extra Lightning Damage',
            'Cold Damage to Attacks with this Weapon per 10 Dexterity',
            'Lightning Damage to Attacks with this Weapon per 10 Intelligence',
            'Socketed Gems are Supported by Level .. Controlled Destruction',
            'increased Cold Damage',
            'Socketed Gems are Supported by Level .. Cold Penetration',
            'increased Lightning Damage',
            'Socketed Gems are Supported by Level .. Lightning Penetration',
            'of Elemental Damage as Extra Chaos Damage',
            'Socketed Gems are supported by Level .. Melee Splash',
            'increased Area Damage',
            'Socketed Gems are Supported by Level .. Faster Attacks',
            'Socketed Gems are Supported by Level .. Increased Critical Strikes',
            'chance to Maim on Hit',
            'Socketed Gems are Supported by Level .. Maim',
            'Damage Penetrates',
            'increased Cast Speed',
            'Socketed Gems are Supported by Level .. Faster Casting',
            'Socketed Gems are Supported by Level .. Increased Critical Strikes',
            'Socketed Gems are Supported by Level .. Lesser Poison',
            'increased Area of Effect',
            'Socketed Gems are Supported by Level .. Spell Cascade',
            'to Critical Strike Multiplier against Enemies that are on Full Life',
            'Socketed Gems are Supported by Level .. Melee Physical Damage',
            'Socketed Gems are Supported by Level .. Brutality',
            'Socketed Gems are Supported by Level .. Ruthless',
            'Socketed Gems are Supported by Level .. Efficacy',
            'Physical Damage to Spells',
            'Chaos Damage to Spells',
            'increased Spell Damage per 16 Dexterity',
            'increased Spell Damage per 16 Intelligence',
            'Socketed Gems are Supported by Level .. Ancestral Call',
            'Socketed Gems are supported by Level .. Multistrike',
            'Socketed Gems are supported by Level .. Increased Critical Damage',
            'Socketed Gems are Supported by Level .. Chance To Bleed',
            'of Physical Damage Converted to Chaos Damage',
            'Socketed Gems are Supported by Level .. Spell Echo',
            'Socketed Gems are Supported by Level .. Poison',
            'Socketed Gems are Supported by Level .. Increased Area of Effect',
            'increased Critical Strike Chance against Poisoned Enemies'
            ])
    return daggerDF

def clawDF():
    clawDF = pd.DataFrame(columns=['to maximum Mana','increased Physical Damage','to Accuracy Rating',
                            'Physical Damage','Fire Damage','Cold Damage','Lightning Damage',
                            'increased Elemental Damage with Attack Skills','to Level of Socketed Gems',
                            'to Level of Socketed Melee Gems','of Physical Attack Damage Leeched as Life',
                            'of Physical Attack Damage Leeched as Mana','Chaos Damage','of Fire Damage Leeched as Life',
                            'of Cold Damage Leeched as Life','of Lightning Damage Leeched as Life',
                            'increased Curse Duration','chance to Shock','chance to Ignite','chance to Freeze',
                            'chance to cause Bleeding on Hit','reduced Enemy Block Chance','increased Damage over Time',
                            'to Dexterity','increased Attack Speed','increased Mana Regeneration Rate',
                            'to Fire Resistance','to Cold Resistance','to Lightning Resistance',
                            'to Chaos Resistance','increased Stun Duration on Enemies','Life gained for each Enemy hit by Attacks',
                            'Life gained on Kill','Mana gained on Kill','increased Critical Strike Chance',
                            'to Global Critical Strike Multiplier','reduced Attribute Requirements',
                            'increased Light Radius','increased Poison Duration','chance to Poison on Hit',
                            'increased Damage with Poison','Life gained for each Enemy hit by your Attacks',
                            'reduced Enemy Stun Threshold with this Weapon','to Weapon range',
                            'Socketed Gems are Supported by Level .. Added Fire Damage','Socketed Gems are supported by Level .. Elemental Damage with Attacks',
                            'of Physical Damage as Extra Cold Damag','of Physical Damage as Extra Lightning Damage',
                            'Cold Damage to Attacks with this Weapon per 10 Dexterity','Lightning Damage to Attacks with this Weapon per 10 Intelligence',
                            'Socketed Gems are supported by Level .. Melee Splash','increased Area Damage',
                            'Socketed Gems are Supported by Level .. Faster Attacks','Socketed Gems are Supported by Level .. Increased Critical Strikes',
                            'chance to Maim on Hit','Socketed Gems are Supported by Level .. Maim',
                            'chance to gain Onslaught for 4 seconds on Kill','additional Block Chance while Dual Wielding',
                            'Damage Penetrates .% Elemental Resistances','Enemies have 20% reduced Evasion if you have Hit them Recently',
                            'increased Critical Strike Chance against Blinded Enemies','Socketed Gems are Supported by Level .. Melee Physical Damage',
                            'Socketed Gems are Supported by Level .. Brutality','Socketed Gems are Supported by Level .. Ruthless',
                            'Socketed Gems are Supported by Level .. Ancestral Call','Socketed Gems are supported by Level .. Multistrike	Claws',
                            'Socketed Gems are supported by Level .. Increased Critical Damage','Socketed Gems are Supported by Level .. Poison',
                            'Socketed Gems are Supported by Level .. Chance To Bleed','chance to gain Unholy Might for 3 seconds on Kill','chance to Blind Enemies on Hit with Attacks',
                            'increased Physical Weapon Damage while Dual Wielding','of Physical Damage Converted to Chaos Damage',
                            'chance to gain one of its mods for 10 seconds','Life gained for each Blinded Enemy Hit by this Weapon'])

    return clawDF

def ringDF():
    ringDF = pd.DataFrame(columns=['maximum Life', 'maximum Mana', 'maximum Energy Shield',
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

def wandDF():
    wandDF = pd.DataFrame(columns=[
            'to maximum Mana',
            'increased Physical Damage',
            'to Accuracy Rating',
            'to Physical Damage',
            'to Fire Damage',
            'to Cold Damage',
            'to Lightning Damage',
            'increased Spell Damage',
            'increased Fire Damage',
            'increased Cold Damage',
            'increased Lightning Damage',
            'increased Elemental Damage with Attack Skills',
            'to Level of Socketed Gems',
            'to Level of Socketed Fire Gems',
            'to Level of Socketed Cold Gems',
            'to Level of Socketed Lightning Gems',
            'to Level of Socketed Chaos Gems',
            'of Physical Attack Damage Leeched as Life',
            'of Physical Attack Damage Leeched as Mana',
            'to Fire Damage to Spells',
            'to Cold Damage to Spells',
            'to Lightning Damage to Spells',
            'to Chaos Damage',
            'of Fire Damage Leeched as Life',
            'of Cold Damage Leeched as Life',
            'of Lightning Damage Leeched as Life',
            'increased Curse Duration',
            'chance to Shock',
            'chance to Ignite',
            'chance to Freeze',
            'Attack Projectiles Return to You after hitting targets',
            'reduced Enemy Block Chance',
            'increased Damage over Time',
            'to Intelligence',
            'increased Cast Speed',
            'increased Attack Speed',
            'increased Mana Regeneration Rate',
            'to Fire Resistance',
            'to Cold Resistance',
            'to Lightning Resistance',
            'to Chaos Resistance',
            'increased Stun Duration on Enemies',
            'increased Critical Strike Chance for Spells',
            'increased Projectile Speed',
            'Life gained for each Enemy hit by Attacks',
            'Life gained on Kill',
            'Mana gained on Kill',
            'increased Critical Strike Chance',
            'to Global Critical Strike Multiplier',
            'reduced Attribute Requirements',
            'increased Light Radius',
            'chance to Ignite',
            'chance to Freeze',
            'chance to Shock',
            'increased Burning Damage',
            'Socketed Gems are Supported by Level .. Added Fire Damage',
            'Socketed Gems are supported by Level .. Elemental Damage with Attacks',
            'of Physical Damage as Extra Lightning Damage',
            'Lightning Damage to Attacks with this Weapon per 10 Intelligence',
            'Socketed Gems are Supported by Level .. Controlled Destruction',
            'Socketed Gems are Supported by Level .. Cold Penetration',
            'Socketed Gems are Supported by Level .. Lightning Penetration',
            'Elemental Damage as Extra Chaos Damage',
            'Socketed Gems are Supported by Level .. Faster Attacks',
            'Socketed Gems are Supported by Level .. Increased Critical Strikes',
            'Damage Penetrates',
            'Projectiles Pierce',
            'Socketed Gems are Supported by Level .. Faster Casting',
            'Socketed Gems are Supported by Level .. Increased Critical Strikes',
            'Socketed Gems are Supported by Level .. Spell Cascade',
            'Socketed Gems are Supported by Level .. Volley',
            'Gain a Power Charge after you Spend a total of 200 Mana',
            'Socketed Gems are Supported by Level .. Efficacy',
            'Socketed Gems are Supported by Level .. Fire Penetration',
            'Physical Damage to Spells',
            'Chaos Damage to Spells',
            'increased Spell Damage per 16 Intelligence',
            'Socketed Gems are Supported by Level .. Onslaught',
            'Socketed Gems are supported by Level .. Increased Critical Damage',
            'Physical Damage Converted to Chaos Damage',
            'Socketed Gems are Supported by Level .. Spell Echo',
            'increased Area Damage',
            'Socketed Gems are Supported by Level .. Increased Area of Effect',
            'increased Projectile Damage',
            'Socketed Gems are Supported by Level .. Lesser Multiple Projectiles',
            'increased Damage per Power Charge'
            ])
    return wandDF

def oneSword():
    oneSwordDF = pd.DataFrame(columns=[
            'increased Physical Damage',
            'to Accuracy Rating',
            'to Physical Damage',
            'to Fire Damage',
            'to Cold Damage',
            'to Lightning Damage',
            'increased Elemental Damage with Attack Skills',
            'to Level of Socketed Gems',
            'to Level of Socketed Melee Gems',
            'of Physical Attack Damage Leeched as Life',
            'of Physical Attack Damage Leeched as Mana',
            'to Chaos Damage',
            'additional Block Chance while Dual Wielding',
            'chance to cause Bleeding on Hit',
            'reduced Enemy Block Chance',
            'increased Damage over Time',
            'to Dexterity',
            'increased Attack Speed',
            'reduced Enemy Stun Threshold',
            'to Fire Resistance',
            'to Cold Resistance',
            'to Lightning Resistance',
            'to Chaos Resistance',
            'increased Stun Duration on Enemies',
            'Life gained for each Enemy hit by Attacks',
            'Life gained on Kill',
            'Mana gained on Kill',
            'increased Critical Strike Chance',
            'to Global Critical Strike Multiplier',
            'to Accuracy Rating',
            'reduced Attribute Requirements',
            'increased Light Radius',
            'increased Poison Duration',
            'increased Bleeding Duration',
            'chance to cause Bleeding on Hit',
            'chance to Poison on Hit',
            'increased Damage with Poison',
            'increased Damage with Bleeding',
            'Life gained for each Enemy hit by your Attacks',
            'reduced Enemy Stun Threshold with this Weapon',
            'to Weapon range',
            'Socketed Gems are Supported by Level .. Added Fire Damage',
            'Socketed Gems are supported by Level .. Elemental Damage with Attacks',
            'of Physical Damage as Extra Fire Damage',
            'of Physical Damage as Extra Cold Damage',
            'Fire Damage to Attacks with this Weapon per 10 Strength',
            'Cold Damage to Attacks with this Weapon per 10 Dexterity',
            'Socketed Gems are supported by Level .. Melee Splash',
            'increased Area Damage',
            'Socketed Gems are Supported by Level .. Faster Attacks',
            'Socketed Gems are Supported by Level .. Increased Critical Strikes',
            '20% chance to Maim on Hit',
            'Socketed Gems are Supported by Level 20 Maim',
            'chance to gain Onslaught for 4 seconds on Kill',
            'additional Block Chance while Dual Wielding',
            'Damage Penetrates',
            'increased Accuracy Rating per Frenzy Charge',
            'chance to gain a Frenzy Charge when you Block',
            'Socketed Movement Skills have no Mana Cost',
            'Socketed Gems are Supported by Level .. Melee Physical Damage',
            'Socketed Gems are Supported by Level .. Brutality',
            'Socketed Gems are Supported by Level .. Ruthless',
            'Socketed Gems are Supported by Level .. Ancestral Call',
            'increased Area of Effect',
            'Socketed Gems are supported by Level .. Multistrike',
            'Socketed Gems are supported by Level .. Increased Critical Damage',
            'Socketed Gems are Supported by Level .. Poison',
            'Socketed Gems are Supported by Level .. Chance To Bleed',
            'chance to Blind Enemies on Hit with Attacks',
            'increased Physical Weapon Damage while Dual Wielding',
            'Physical Damage Converted to Chaos Damage',
            'additional Block Chance per Endurance Charge',
            'chance to gain an Endurance Charge when you Block',
            'Gain an Endurance Charge every 4 seconds while Stationary'
            ])
    return oneSwordDF