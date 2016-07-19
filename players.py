import cards
import orm


class player():
    def __init__(self,id,num=0,nums=0,handcard=[]):
        self._id=id
        self._num=num
        self._nums=nums
        self._handcard=handcard

    @property
    def id(self):
        return self._id

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self,num):
        self._num=num


    @property
    def handcard(self):
        return self._handcard

    @handcard.setter
    def handcard(self,handcard):
        self._handcard=handcard

    def myTurn(self):
        pick_one=False
        while not(pick_one):
           temp = orm.play_card()
           if (self._handcard[temp[0]].name) in ('witness','trade','detective','dog'):
              if isinstance(temp[1],int) and temp>-1 and temp<self._nums:
                  pick_one=True
              else: pick_one=False

           else:
               if temp[1]==None :
                   pick_one=True

        return temp

    def GetInvolved(self):
        temp=orm.choose_card()
        return temp
