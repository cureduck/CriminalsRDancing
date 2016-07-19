import players
from players import player

class table():
    def __init__(self,players):
        self._players=players
        i=0
        c=len(players)

        for p in self._players:
            p.num=i
            i+=1
            p.nums=c



p1=player('p1',0,3,['common_ones','common_ones','common_ones','common_ones'])
p2=player('p2',1,3,['common_ones','common_ones','common_ones','common_ones'])
p3=player('p3',2,3,['common_ones','common_ones','common_ones','common_ones'])

t=table([p1,p2,p3])

print('1')