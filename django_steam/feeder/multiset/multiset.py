import sys

class Multiset:
    def __init__(self, elements):
        self.elements = elements

    def addElement(self, x):
        if self.member(x) == False:
            self.elements.append(x)
            return self.elements
        else:
            return "Element is already in the set"

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
        #always go by the smaller list
        if (len(self.elements) < len(anotherSet.elements)):
            list1 = self.elements
            list2 = anotherSet.elements
        else:
            list1 = anotherSet.elements
            list2 = self.elements
            
        common = []
        i = 0
        while i < len(list1):
            j = 0
            once = []
            while j < len(list2):
                if list1[i] == list2[j] and list1[i] not in once:
                    common.append(list1[i])
                    once.append(list1[i])
                j = j + 1
            i = i + 1

        return common

    def union(self, anotherSet):
        list1 = self.elements
        list2 = anotherSet.elements
        united = list1 + list2
        return united
    
    def subtract(self, anotherSet):
        list1 = self.elements + []
        list2 = anotherSet.elements
        intersect = self.intersection(anotherSet)
        for i in range(len(intersect)):
            list1.remove(intersect[i])
        return list1

def main():
    #[u":CapitalDome:Sid Meier's Civilization V Emoticon", u':CrossedBlades:Total War: SHOGUN 2 Emoticon', u':Perseverance:Empire: Total War Uncommon Emoticon', u":SocialPolicy:Sid Meier's Civilization V Emoticon", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u":Uranium:Sid Meier's Civilization V Emoticon", u":Uranium:Sid Meier's Civilization V Emoticon", u':alyx:Half-Life 2 Emoticon', u':borderlands2:Borderlands 2 Emoticon', u':diaxe:Dead Island Emoticon', u':diaxe:Dead Island Emoticon', u':p2orange:Portal 2 Emoticon', u':pandastunned:Saints Row: The Third Emoticon', u':postcardb:Steam Summer Getaway Emoticon', u':postcardf:Steam Summer Getaway Emoticon', u':witch:Left 4 Dead 2 Uncommon Emoticon', u'Attack the LineMedieval II: Total War Trading Card', u'Attack the LineMedieval II: Total War Trading Card', u'Banner (Foil)Rome: Total War Foil Trading Card', u'BannerRome: Total War Trading Card', u'BotsPortal 2 Profile Background', u"CatapultSid Meier's Civilization V Profile Background", u"CatapultSid Meier's Civilization V Profile Background", u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background', u"CivilizationSid Meier's Civilization V Profile Background", u'Combine TechnologyHalf-Life 2 Profile Background', u'FleetNapoleon: Total War Trading Card', u'Fortress AttackMedieval II: Total War Trading Card', u'GeneralNapoleon: Total War Trading Card', u'Infantry MenEmpire: Total War Profile Background', u'Medic (Profile Background)Team Fortress 2 Profile Background', u'Portal 2 LogoPortal 2 Profile Background', u'Professor GenkiSaints Row: The Third Uncommon Profile Background', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"SpaceSid Meier's Civilization V Profile Background", u'StealthRome: Total War Trading Card', u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background', u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background', u'The HandLeft 4 Dead 2 Uncommon Profile Background', u'TurretsPortal 2 Profile Background', u'UndergroundPortal 2 Trading Card', u'Vault HuntersBorderlands 2 Profile Background', u"Washington (Trading Card)Sid Meier's Civilization V Trading Card", u'Zero (Profile Background)Borderlands 2 Profile Background']
    #[u":CapitalDome:Sid Meier's Civilization V Emoticon", u':CrossedBlades:Total War: SHOGUN 2 Emoticon', u':Perseverance:Empire: Total War Uncommon Emoticon', u":SocialPolicy:Sid Meier's Civilization V Emoticon", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u":Uranium:Sid Meier's Civilization V Emoticon", u":Uranium:Sid Meier's Civilization V Emoticon", u':alyx:Half-Life 2 Emoticon', u':borderlands2:Borderlands 2 Emoticon', u':diaxe:Dead Island Emoticon', u':diaxe:Dead Island Emoticon', u':p2orange:Portal 2 Emoticon', u':pandastunned:Saints Row: The Third Emoticon', u':postcardb:Steam Summer Getaway Emoticon', u':postcardf:Steam Summer Getaway Emoticon', u':witch:Left 4 Dead 2 Uncommon Emoticon', u'Attack the LineMedieval II: Total War Trading Card', u'Banner (Foil)Rome: Total War Foil Trading Card', u'BannerRome: Total War Trading Card', u'BotsPortal 2 Profile Background', u"CatapultSid Meier's Civilization V Profile Background", u"CatapultSid Meier's Civilization V Profile Background", u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background', u"CivilizationSid Meier's Civilization V Profile Background", u'Combine TechnologyHalf-Life 2 Profile Background', u'FleetNapoleon: Total War Trading Card', u'Fortress AttackMedieval II: Total War Trading Card', u'GeneralNapoleon: Total War Trading Card', u'Infantry MenEmpire: Total War Profile Background', u'Medic (Profile Background)Team Fortress 2 Profile Background', u'Portal 2 LogoPortal 2 Profile Background', u'Professor GenkiSaints Row: The Third Uncommon Profile Background', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"SpaceSid Meier's Civilization V Profile Background", u'StealthRome: Total War Trading Card', u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background', u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background', u'The HandLeft 4 Dead 2 Uncommon Profile Background', u'TurretsPortal 2 Profile Background', u'UndergroundPortal 2 Trading Card', u'Vault HuntersBorderlands 2 Profile Background', u"Washington (Trading Card)Sid Meier's Civilization V Trading Card", u'Zero (Profile Background)Borderlands 2 Profile Background']

    #Set1=Multiset([u'BannerRome: Total War Trading Card', u'FleetNapoleon: Total War Trading Card', u'Combine TechnologyHalf-Life 2 Profile Background', u':CrossedBlades:Total War: SHOGUN 2 Emoticon', u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background', u':alyx:Half-Life 2 Emoticon', u':witch:Left 4 Dead 2 Uncommon Emoticon', u':p2orange:Portal 2 Emoticon', u'The HandLeft 4 Dead 2 Uncommon Profile Background', u'StealthRome: Total War Trading Card', u'TurretsPortal 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u'Attack the LineMedieval II: Total War Trading Card', u'Medic (Profile Background)Team Fortress 2 Profile Background', u'Zero (Profile Background)Borderlands 2 Profile Background', u'Fortress AttackMedieval II: Total War Trading Card', u'Attack the LineMedieval II: Total War Trading Card', u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background', u':postcardf:Steam Summer Getaway Emoticon', u":Uranium:Sid Meier's Civilization V Emoticon", u'Professor GenkiSaints Row: The Third Uncommon Profile Background', u'Vault HuntersBorderlands 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"Washington (Trading Card)Sid Meier's Civilization V Trading Card", u"CatapultSid Meier's Civilization V Profile Background", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u'Banner (Foil)Rome: Total War Foil Trading Card', u":SocialPolicy:Sid Meier's Civilization V Emoticon", u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u':borderlands2:Borderlands 2 Emoticon', u':postcardb:Steam Summer Getaway Emoticon', u'Portal 2 LogoPortal 2 Profile Background', u'BotsPortal 2 Profile Background', u"CatapultSid Meier's Civilization V Profile Background", u':pandastunned:Saints Row: The Third Emoticon', u"CivilizationSid Meier's Civilization V Profile Background", u":CapitalDome:Sid Meier's Civilization V Emoticon", u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background', u'Infantry MenEmpire: Total War Profile Background', u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u':Perseverance:Empire: Total War Uncommon Emoticon', u":Uranium:Sid Meier's Civilization V Emoticon", u'UndergroundPortal 2 Trading Card', u"SpaceSid Meier's Civilization V Profile Background", u'GeneralNapoleon: Total War Trading Card'])
    #Set2=Multiset([u'BannerRome: Total War Trading Card', u'FleetNapoleon: Total War Trading Card', u'Combine TechnologyHalf-Life 2 Profile Background', u':CrossedBlades:Total War: SHOGUN 2 Emoticon', u'Cherry BlossomsTotal War: SHOGUN 2 Profile Background', u':witch:Left 4 Dead 2 Uncommon Emoticon', u':p2orange:Portal 2 Emoticon', u'The HandLeft 4 Dead 2 Uncommon Profile Background', u'StealthRome: Total War Trading Card', u'TurretsPortal 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u'Medic (Profile Background)Team Fortress 2 Profile Background', u'Zero (Profile Background)Borderlands 2 Profile Background', u'Fortress AttackMedieval II: Total War Trading Card', u'Attack the LineMedieval II: Total War Trading Card', u'Summer Getaway Postcards - Dead IslandSteam Summer Getaway Profile Background', u':postcardf:Steam Summer Getaway Emoticon', u'Professor GenkiSaints Row: The Third Uncommon Profile Background', u':Perseverance:Empire: Total War Uncommon Emoticon', u'Infantry MenEmpire: Total War Profile Background', u'Vault HuntersBorderlands 2 Profile Background', u"PyramidsSid Meier's Civilization V Uncommon Profile Background", u"Washington (Trading Card)Sid Meier's Civilization V Trading Card", u"CatapultSid Meier's Civilization V Profile Background", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u'Banner (Foil)Rome: Total War Foil Trading Card', u"SpaceSid Meier's Civilization V Profile Background", u":SocialPolicy:Sid Meier's Civilization V Emoticon", u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u':borderlands2:Borderlands 2 Emoticon', u':postcardb:Steam Summer Getaway Emoticon', u'Portal 2 LogoPortal 2 Profile Background', u'BotsPortal 2 Profile Background', u":Uranium:Sid Meier's Civilization V Emoticon", u"CatapultSid Meier's Civilization V Profile Background", u':pandastunned:Saints Row: The Third Emoticon', u"CivilizationSid Meier's Civilization V Profile Background", u":CapitalDome:Sid Meier's Civilization V Emoticon", u'Summer Getaway Postcards - Bioshock InfiniteSteam Summer Getaway Profile Background', u':alyx:Half-Life 2 Emoticon', u':diaxe:Dead Island Emoticon', u'Purna (Profile Background)Dead Island Uncommon Profile Background', u":Uranium:Sid Meier's Civilization V Emoticon", u'UndergroundPortal 2 Trading Card', u'GeneralNapoleon: Total War Trading Card'])
    
    #great tests sets to see if this script can utilize multisets correctly
    Set1 = Multiset(['1','2','3','3','3','6'])
    Set2 = Multiset(['2','3','3','7'])
    print
    print "Set1"
    print sorted(Set1.elements)
    print "Set2"
    print sorted(Set2.elements)
    print
    print "Is 6 a member of Set1"
    print Set1.member('6')
    print
    print "Find the intersection of Set1 and Set2"
    print sorted(Set1.intersection(Set2))
    print
    print "Find the intersection of Set2 and Set1"
    print sorted(Set2.intersection(Set1))
    print
    print "Find union of Set1 and Set2"
    print Set1.union(Set2)
    print
    print "Find the intersection of Set2 and Set1"
    print Set2.intersection(Set1)
    print
    print "Subtract Set2 from Set1: (Set1 - Set2)"
    print Set1.subtract(Set2)
    print
    print "Find the intersection of Set2 and Set1"
    print Set2.intersection(Set1)
    print
    print "Find union of Set2 and Set1"
    print Set2.union(Set1)
    print
    print "Subtract Set1 from Set2: (Set2 - Set1)"
    print Set2.subtract(Set1)
   
if __name__ == "__main__":   
    main()
