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
        list1 = self.elements
        list2 = anotherSet.elements
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
    Set1=Multiset([u':Uranium:', u'Fleet', u'Purna (Profile Background)', u'Dead Island Booster Pack', u'Banner (Foil)', u'Prison Architect', u':diaxe:', u'Catapult', u':SocialPolicy:', u':borderlands2:', u':postcardb:', u'Portal 2 Logo', u'Bots', u'Cannon Battle', u'Catapult', u':pandastunned:', u'Civilization', u':CapitalDome:', u'Summer Getaway Postcards - Bioshock Infinite', u'Dead Island Riptide', u':diaxe:', u'Purna (Profile Background)', u':SocialPolicy:', u'Underground', u':alyx:', u'Space', u'General', u'Banner', u'Fleet', u'Combine Technology', u':CrossedBlades:', u'Cherry Blossoms', u'Attack the Line', u':p2orange:', u'Stealth', u'Turrets', u'Reign Fire', u'Attack the Line', u'Medic (Profile Background)', u'Naval Battle (Trading Card)', u'Zero (Profile Background)', u'Fortress Attack', u'Summer Getaway Postcards - Dead Island', u':postcardf:', u':Uranium:', u'Professor Genki', u'Vault Hunters', u'Washington (Trading Card)'])
    #Set1          [u':Uranium:', u'Fleet', u'Purna (Profile Background)', u'Dead Island Booster Pack', u'Banner (Foil)', u'Prison Architect', u':diaxe:', u'Catapult', u':SocialPolicy:', u':borderlands2:', u':postcardb:', u'Portal 2 Logo', u'Bots', u'Cannon Battle', u'Catapult', u':pandastunned:', u'Civilization', u':CapitalDome:', u'Summer Getaway Postcards - Bioshock Infinite', u'Dead Island Riptide', u':diaxe:', u'Purna (Profile Background)', u':SocialPolicy:', u'Underground', u':alyx:', u'Space', u'General', u'Banner', u'Fleet', u'Combine Technology', u':CrossedBlades:', u'Cherry Blossoms', u'Attack the Line', u':p2orange:', u'Stealth', u'Turrets', u'Reign Fire', u'Attack the Line', u'Medic (Profile Background)', u'Naval Battle (Trading Card)', u'Zero (Profile Background)', u'Fortress Attack', u'Summer Getaway Postcards - Dead Island', u':postcardf:', u':Uranium:', u'Professor Genki', u'Vault Hunters', u'Washington (Trading Card)']

    Set2=Multiset([u'Banner', u'Fleet', u'Combine Technology', u':CrossedBlades:', u'Cherry Blossoms', u'Attack the Line', u':p2orange:', u'Stealth', u'Turrets', u'Pyramids', u'Reign Fire', u'Attack the Line', u'Medic (Profile Background)', u'Naval Battle (Trading Card)', u'Zero (Profile Background)', u'Fortress Attack', u'Summer Getaway Postcards - Dead Island', u':postcardf:', u':Uranium:', u'Professor Genki', u'Vault Hunters', u'Pyramids', u'Washington (Trading Card)', u'Catapult', u':SocialPolicy:', u'Dead Island Booster Pack', u'Banner (Foil)', u'Prison Architect', u':SocialPolicy:', u':diaxe:', u'Purna (Profile Background)', u':borderlands2:', u':postcardb:', u'Portal 2 Logo', u'Bots', u'Cannon Battle', u'Catapult', u':pandastunned:', u'Civilization', u':CapitalDome:', u'Summer Getaway Postcards - Bioshock Infinite', u'Dead Island Riptide', u':diaxe:', u'Purna (Profile Background)', u'Fleet', u':Uranium:', u'Underground', u':alyx:', u'Space', u'General'])
    #Set2          [u'Banner', u'Fleet', u'Combine Technology', u':CrossedBlades:', u'Cherry Blossoms', u'Attack the Line', u':p2orange:', u'Stealth', u'Turrets', u'Pyramids', u'Reign Fire', u'Attack the Line', u'Medic (Profile Background)', u'Naval Battle (Trading Card)', u'Zero (Profile Background)', u'Fortress Attack', u'Summer Getaway Postcards - Dead Island', u':postcardf:', u':Uranium:', u'Professor Genki', u'Vault Hunters', u'Pyramids', u'Washington (Trading Card)', u'Catapult', u':SocialPolicy:', u'Dead Island Booster Pack', u'Banner (Foil)', u'Prison Architect', u':SocialPolicy:', u':diaxe:', u'Purna (Profile Background)', u':borderlands2:', u':postcardb:', u'Portal 2 Logo', u'Bots', u'Cannon Battle', u'Catapult', u':pandastunned:', u'Civilization', u':CapitalDome:', u'Summer Getaway Postcards - Bioshock Infinite', u'Dead Island Riptide', u':diaxe:', u'Purna (Profile Background)', u'Fleet', u':Uranium:', u'Underground', u':alyx:', u'Space', u'General']
    #Set1 = Multiset(['1','2','3','3','6'])
    #Set2 = Multiset(['2','3','7'])
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
