import sys

class Multiset:
    def __init__(self, elements):
        self.elements = elements

    def addElement(self, x):
        self.elements.append(x)
        return self.elements

    def deleteElement(self, x):
        if self.member(x) == True:
            self.elements.remove(x)
            return self.elements
        else:
            return "Element is not in the set"

    def member(self, x):
        if x in self.elements:
            return True
        else:
            return False

    def intersection(self, anotherSet):
        list1 = self.elements
        list2 = anotherSet.elements
        
        common = []
        
        #a quantity dic
        set = {}
        set2 = {}
        
        #set em to zero
        for key in list1:
            set[key] = 0
        for key in list2:
            set2[key] = 0
        
        #count em
        for key in list1:
            set[key] = set[key] + 1
        for key in list2:
            set2[key] = set2[key] + 1
        
        #look for similar keys and create an array of commons
        for key in set:
            value = set[key]
            if key in set2:
                value2 = set2[key]
                if value < value2:
                    for i in range(value):
                        common.append(key)
                else:
                    for i in range(value2):
                        common.append(key)

        return common

    def union(self, anotherSet):
        list1 = self.elements
        list2 = anotherSet.elements
        united = list1 + list2
        return united
    
    def subtract(self, anotherSet):
        list1 = self.elements[:]
        list2 = anotherSet.elements[:]
        intersect = self.intersection(anotherSet)
        for i in range(len(intersect)):
            list1.remove(intersect[i])
        return list1

def main():
    #Set1=Multiset([u'BannerRome: Total War Trading Card',     u'FleetNapoleon: Total War Trading Card',     u'Combine TechnologyHalf-Life 2 Profile Background',     u':CrossedBlades:Total War: SHOGUN 2 Emoticon',     u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background',     u':alyx:Half-Life 2 Emoticon',     u':witch:Left 4 Dead 2 Uncommon Emoticon',     u':p2orange:Portal 2 Emoticon',     u'The HandLeft 4 Dead 2 Uncommon Profile Background',     u'StealthRome: Total War Trading Card',     u'TurretsPortal 2 Profile Background',     u'Medic (Profile Background)Team Fortress 2 Profile Background',     u'Zero (Profile Background)Borderlands 2 Profile Background',     u'Fortress AttackMedieval II: Total War Trading Card',     u'Attack the LineMedieval II: Total War Trading Card',     u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background',     u':postcardf:Steam Summer Getaway Emoticon',     u'Professor GenkiSaints Row: The Third Uncommon Profile Background',     u'Vault HuntersBorderlands 2 Profile Background',     u"PyramidsSid Meier's Civilization V Uncommon Profile Background",     u"Washington (Trading Card)Sid Meier's Civilization V Trading Card",     u'Banner (Foil)Rome: Total War Foil Trading Card',     u":SocialPolicy:Sid Meier's Civilization V Emoticon",     u':borderlands2:Borderlands 2 Emoticon',     u':postcardb:Steam Summer Getaway Emoticon',     u'Portal 2 LogoPortal 2 Profile Background',     u'BotsPortal 2 Profile Background',     u"CatapultSid Meier's Civilization V Profile Background",     u':pandastunned:Saints Row: The Third Emoticon',     u"CivilizationSid Meier's Civilization V Profile Background",     u":CapitalDome:Sid Meier's Civilization V Emoticon",     u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background',     u'Infantry MenEmpire: Total War Profile Background',     u':diaxe:Dead Island Emoticon',     u'Purna (Profile Background)Dead Island Uncommon Profile Background',     u':Perseverance:Empire: Total War Uncommon Emoticon',     u":Uranium:Sid Meier's Civilization V Emoticon",     u'UndergroundPortal 2 Trading Card',     u"SpaceSid Meier's Civilization V Profile Background",     u'GeneralNapoleon: Total War Trading Card',     u'Pyro (Profile Background)Team Fortress 2 Profile Background',     u'HunterLeft 4 Dead 2 Trading Card',     u'The Boss of the SaintsSaints Row: The Third Trading Card',     u'The Boss of the SaintsSaints Row: The Third Trading Card',     u'The Herald of the Walking ApocalypseSaints Row: The Third Trading Card',     u'Nyte BlaydeSaints Row: The Third Trading Card',     u'Pierce WashingtonSaints Row: The Third Trading Card',     u'Johnny GatSaints Row: The Third Trading Card',     u'Zimos (Trading Card)Saints Row: The Third Trading Card',     u'Pierce WashingtonSaints Row: The Third Trading Card',     u'Oleg Kirrlov the BruteSaints Row: The Third Trading Card',     u'Pierce WashingtonSaints Row: The Third Trading Card'])
    #Set2=Multiset([u'BannerRome: Total War Trading Card',     u'Pierce WashingtonSaints Row: The Third Trading Card',     u'FleetNapoleon: Total War Trading Card',     u'HunterLeft 4 Dead 2 Trading Card',     u':CrossedBlades:Total War: SHOGUN 2 Emoticon',     u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background',     u':witch:Left 4 Dead 2 Uncommon Emoticon',     u':p2orange:Portal 2 Emoticon',     u'The HandLeft 4 Dead 2 Uncommon Profile Background',     u'The Boss of the SaintsSaints Row: The Third Trading Card',     u'StealthRome: Total War Trading Card',     u'TurretsPortal 2 Profile Background',     u"PyramidsSid Meier's Civilization V Uncommon Profile Background",     u':pandastunned:Saints Row: The Third Emoticon',     u'Zimos (Profile Background)Saints Row: The Third Uncommon Profile Background',     u'Pierce WashingtonSaints Row: The Third Trading Card',     u'Medic (Profile Background)Team Fortress 2 Profile Background',     u'Combine TechnologyHalf-Life 2 Profile Background',     u'Zero (Profile Background)Borderlands 2 Profile Background',     u'Fortress AttackMedieval II: Total War Trading Card',     u'Attack the LineMedieval II: Total War Trading Card',     u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background',     u':postcardf:Steam Summer Getaway Emoticon',     u'Professor GenkiSaints Row: The Third Uncommon Profile Background',     u':Perseverance:Empire: Total War Uncommon Emoticon',     u'Infantry MenEmpire: Total War Profile Background',     u'Pyro (Profile Background)Team Fortress 2 Profile Background',     u'Vault HuntersBorderlands 2 Profile Background',     u"Washington (Trading Card)Sid Meier's Civilization V Trading Card",     u":SocialPolicy:Sid Meier's Civilization V Emoticon",     u'Banner (Foil)Rome: Total War Foil Trading Card',     u"SpaceSid Meier's Civilization V Profile Background",     u':diaxe:Dead Island Emoticon',     u'Purna (Profile Background)Dead Island Uncommon Profile Background',     u':borderlands2:Borderlands 2 Emoticon',     u':postcardb:Steam Summer Getaway Emoticon',     u'Portal 2 LogoPortal 2 Profile Background',     u'BotsPortal 2 Profile Background',     u":Uranium:Sid Meier's Civilization V Emoticon",     u"CatapultSid Meier's Civilization V Profile Background",     u':pandastunned:Saints Row: The Third Emoticon',     u"CivilizationSid Meier's Civilization V Profile Background",     u":CapitalDome:Sid Meier's Civilization V Emoticon",     u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background',     u':alyx:Half-Life 2 Emoticon',     u'UndergroundPortal 2 Trading Card',     u'GeneralNapoleon: Total War Trading Card'])
    #Set1=Multiset([u'BannerRome: Total War Trading Card', u'FleetNapoleon: Total War Trading Card', u'Combine TechnologyHalf-Life 2 Profile Background', u':CrossedBlades:Total War: SHOGUN 2 Emoticon', u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background', u':alyx:Half-Life 2 Emoticon', u':witch:Left 4 Dead 2 Uncommon Emoticon', u':p2orange:Portal 2 Emoticon', u'The HandLeft 4 Dead 2 Uncommon Profile Background', u'StealthRome: Total War Trading Card', u'TurretsPortal 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u'Attack the LineMedieval II: Total War Trading Card', u'Medic (Profile Background)Team Fortress 2 Profile Background', u'Zero (Profile Background)Borderlands 2 Profile Background', u'Fortress AttackMedieval II: Total War Trading Card', u'Attack the LineMedieval II: Total War Trading Card', u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background', u':postcardf:Steam Summer Getaway Emoticon', u":Uranium:Sid Meier's Civilization V Emoticon", u'Professor GenkiSaints Row: The Third Uncommon Profile Background', u'Vault HuntersBorderlands 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"Washington (Trading Card)Sid Meier's Civilization V Trading Card", u"CatapultSid Meier's Civilization V Profile Background", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u'Banner (Foil)Rome: Total War Foil Trading Card', u":SocialPolicy:Sid Meier's Civilization V Emoticon", u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u':borderlands2:Borderlands 2 Emoticon', u':postcardb:Steam Summer Getaway Emoticon', u'Portal 2 LogoPortal 2 Profile Background', u'BotsPortal 2 Profile Background', u"CatapultSid Meier's Civilization V Profile Background", u':pandastunned:Saints Row: The Third Emoticon', u"CivilizationSid Meier's Civilization V Profile Background", u":CapitalDome:Sid Meier's Civilization V Emoticon", u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background', u'Infantry MenEmpire: Total War Profile Background', u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u':Perseverance:Empire: Total War Uncommon Emoticon', u":Uranium:Sid Meier's Civilization V Emoticon", u'UndergroundPortal 2 Trading Card', u"SpaceSid Meier's Civilization V Profile Background", u'GeneralNapoleon: Total War Trading Card'])
    #Set2=Multiset([u'BannerRome: Total War Trading Card', u'FleetNapoleon: Total War Trading Card', u'Combine TechnologyHalf-Life 2 Profile Background', u':CrossedBlades:Total War: SHOGUN 2 Emoticon', u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background', u':witch:Left 4 Dead 2 Uncommon Emoticon', u':p2orange:Portal 2 Emoticon', u'The HandLeft 4 Dead 2 Uncommon Profile Background', u'StealthRome: Total War Trading Card', u'TurretsPortal 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u'Medic (Profile Background)Team Fortress 2 Profile Background', u'Zero (Profile Background)Borderlands 2 Profile Background', u'Fortress AttackMedieval II: Total War Trading Card', u'Attack the LineMedieval II: Total War Trading Card', u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background', u':postcardf:Steam Summer Getaway Emoticon', u'Professor GenkiSaints Row: The Third Uncommon Profile Background', u':Perseverance:Empire: Total War Uncommon Emoticon', u'Infantry MenEmpire: Total War Profile Background', u'Vault HuntersBorderlands 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"Washington (Trading Card)Sid Meier's Civilization V Trading Card", u"CatapultSid Meier's Civilization V Profile Background", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u'Banner (Foil)Rome: Total War Foil Trading Card', u"SpaceSid Meier's Civilization V Profile Background", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u':borderlands2:Borderlands 2 Emoticon', u':postcardb:Steam Summer Getaway Emoticon', u'Portal 2 LogoPortal 2 Profile Background', u'BotsPortal 2 Profile Background', u":Uranium:Sid Meier's Civilization V Emoticon", u"CatapultSid Meier's Civilization V Profile Background", u':pandastunned:Saints Row: The Third Emoticon', u"CivilizationSid Meier's Civilization V Profile Background", u":CapitalDome:Sid Meier's Civilization V Emoticon", u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background', u':alyx:Half-Life 2 Emoticon', u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u":Uranium:Sid Meier's Civilization V Emoticon", u'UndergroundPortal 2 Trading Card', u'GeneralNapoleon: Total War Trading Card'])
    
    #great tests sets to see if this script can utilize multisets correctly
    Set1 = Multiset(['1','2','3','3','3','6','7','7'])
    Set2 = Multiset(['2','3','3','7','7','7','7','4','4'])
    print
    print "Set1"
    print sorted(Set1.elements)
    print "Set2"
    print sorted(Set2.elements)
    print
    print "Find the intersection of Set1 and Set2"
    print sorted(Set1.intersection(Set2))
    print
    print "Find the intersection of Set2 and Set1"
    print sorted(Set2.intersection(Set1))
    print
    print "Subtract Set1 from Set2: (Set2 - Set1)"
    print Set2.subtract(Set1)
    print
    print "Subtract Set2 from Set1: (Set1 - Set2)"
    print Set1.subtract(Set2)
   
if __name__ == "__main__":   
    main()
