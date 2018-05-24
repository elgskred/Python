import pandas as pd

def dagger():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/dagger')]
    lines = list(set(lines))
    dagger = pd.DataFrame(columns=lines)
    return dagger

def claw():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/claw')]
    lines = list(set(lines))
    claw = pd.DataFrame(columns=lines)
    return claw


def wand():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/wand')]
    lines = list(set(lines))
    wand = pd.DataFrame(columns=lines)
    return wand

def one_handed_sword():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/oneSword')]
    lines = list(set(lines))
    one_handed_sword = pd.DataFrame(columns=lines)
    return one_handed_sword

def one_handed_axe():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/oneAxe')]
    lines = list(set(lines))
    one_handed_axe = pd.DataFrame(columns=lines)
    return one_handed_axe

def one_handed_mace():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/oneMace')]
    lines = list(set(lines))
    one_handed_mace = pd.DataFrame(columns=lines)
    return one_handed_mace

def scepter():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/scepter')]
    lines = list(set(lines))
    scepter = pd.DataFrame(columns=lines)
    return scepter

def bow():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/bow')]
    lines = list(set(lines))
    bow = pd.DataFrame(columns=lines)
    return bow

def staff():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/bow')]
    lines = list(set(lines))
    staff = pd.DataFrame(columns=lines)
    return staff

def two_handed_sword():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/twoSword')]
    lines = list(set(lines))
    two_handed_sword = pd.DataFrame(columns=lines)
    return two_handed_sword

def two_handed_axe():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/twoAxe')]
    lines = list(set(lines))
    two_handed_axe = pd.DataFrame(columns=lines)
    return two_handed_axe

def two_handed_mace():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/twoMace')]
    lines = list(set(lines))
    two_handed_mace = pd.DataFrame(columns=lines)
    return two_handed_mace

def gloves():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/gloves')]
    lines = list(set(lines))
    gloves = pd.DataFrame(columns=lines)
    return gloves

def boots():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/boots')]
    lines = list(set(lines))
    boots = pd.DataFrame(columns=lines)
    return boots

def chest():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/bodyArmour')]
    lines = list(set(lines))
    chest = pd.DataFrame(columns=lines)
    return chest

def helmet():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/helmet')]
    lines = list(set(lines))
    helmet = pd.DataFrame(columns=lines)
    return helmet

def shield():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/shield')]
    lines = list(set(lines))
    shield = pd.DataFrame(columns=lines)
    return shield

def amulet():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/amulet')]
    lines = list(set(lines))
    amulet = pd.DataFrame(columns=lines)
    return amulet

def ring():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/ring')]
    lines = list(set(lines))
    ring = pd.DataFrame(columns=lines)
    return ring

def belt():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/belt')]
    lines = list(set(lines))
    belt = pd.DataFrame(columns=lines)
    return belt

def quiver():
    lines = [line.rstrip('\n') for line in open('./dataframeColumns/quiver')]
    lines = list(set(lines))
    quiver = pd.DataFrame(columns=lines)
    return quiver

