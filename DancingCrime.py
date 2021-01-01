import socket
import threading
import time

socks=[]
class Player(object):

	def __init__(self,NoX,sock):
		self.__NoX=NoX
		self.__handCard=[]
		self.__Identity='common'
		self.sock=sock

	def giveCard(self,CardX):
		#把第CardX张牌扔掉,返回牌的名字

		return self.__handCard.pop(int(CardX))

	def getCard(self,CardName):
		#拿到一张牌CardName
		temp=CardName
		self.__handCard.append(temp)
		

	def showHand(self):
		#将自己的手牌展示出来，返回一个card的list
		return(self.__handCard)

	def changeID(self):
		#犯人方，其他人身份方的转变
		self.__Identity='criminal'

	def ChoAim(self):
		#给出牌的作用目标，返回No
		aimNo=self.Contract('请选择玩家',True)
		#接口
		return aimNo

	def WashHand(self):
		#游戏结束,弃之所有牌
		self.handCard=[]

	def ChoCard(self):
		#输出选择的手牌,返回No
		aimCard=self.Contract('请选择手牌',True)
		return aimCard

	def isCriminal(self):
		#犯人和不在场证明的处理，返回一个真或假
		if ('犯人' in self.__handCard)and('不在场证明' not in self.__handCard):
			return True
		else:
			return False

	def SeeCard(self,handCard):
		#通过目击者看别人的手牌
		self.Contract('看到的牌为'+''.join(handCard),False)

	def Contract(self,message,reply):
		temp=message.encode('utf-8')
		self.sock.send(temp)
		if reply:
			time.sleep(0.05)
			self.sock.send('请您发言'.encode('utf-8'))
			return(self.sock.recv(1024).decode('utf-8'))


	def justTell(self,message):
		#将message送达
		temp=message.encode('utf-8')
		self.sock.send(temp)

	def getAnswer(self,message):
		#将message送达并等待回答
		temp=message.encode('utf-8')
		self.sock.send(temp)
		time.sleep(0.05)
		self.sock.send('请您发言'.encode('utf-8'))
		return(self.sock.recv(1024).decode('utf-8'))


class Tabbbbbble(object):


	def __init__(self):
		self.pnum=0
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



	def getFriend(self):
		self.s.bind(('127.0.0.1', 9999))
		self.s.listen(5)
		print('Waiting for connection...')
		self.pnum=0
		while self.pnum<2:
			print(self.pnum,'进入牌桌')
			sock, addr = self.s.accept()
			socks.append((sock,addr))
			self.pnum=self.pnum+1
		self.getStart()

	def getStart(self):
		Players=[]
		for i in range(0,self.pnum):
			Players.append(Player(i,socks[i][0]))
		ruler=RRRRRRuler(Players)
		ruler.GameStart()



class RRRRRRuler(object):

	def broadcast(self,message):
		print(message)
		for p in self.__Players:
			p.Contract(message,False)

	def washCards(self):
		#将必备的牌放入，将其他的牌随机放入牌组CardPool
		self.__CardPool=['犯人','目击者','共犯','侦探','谣言','交易','不在场证明','情报交换','犯人','普通人','犯人','普通人']

	def GameStart(self):
		#游戏开始
		self.washCards()
		for i in range(0,self.pnum):
			self.broadcast(str(i)+'位玩家分配手牌')
			self.AllocCards(i)
			print(self.__Players[i].showHand())

		self.TurnAndTurn(0)


	def AllocCards(self,NoX):
		#给第NoX位玩家分配从CardPool中的4张牌
		for i in range(4*NoX,4*NoX+4):
			self.__Players[NoX].getCard(self.__CardPool[i])

	def GameOver(self,endCode):
		#按照endCode结束规则
		for i in range(0,self.pnum):
			self.Players[i].WashHand()
		self.GameStart()

	def playCard(self,cardName,NoX):
		#按照cardName的规则进行游戏，牌是NoX位玩家打出的
		self.broadcast(str(NoX)+'位玩家使用了'+cardName)

		if cardName=='侦探':
			aimPlayer=int(self.__Players[NoX].ChoAim())
			self.broadcast('被查对象为:',aimPlayer)
			result=self.__Players[aimPlayer].isCriminal()
			if result:
				GameOver('查到了犯人！')
			else:
				self.broadcast('很遗憾不是')
		
		elif cardName=='不在场证明':
			pass
		elif cardName=='情报交换':
			savePool=[]
			for p in range(0,self.pnum):
				self.broadcast(str(p)+'位玩家选择手牌')
				savePool.append(self.__Players[p].giveCard( self.__Players[p].ChoCard()))
			for p in range(0,self.pnum):
				self.broadcast(str(p)+'位玩家获得手牌')
				self.__Players[p].getCard(savePool[(p+1)%self.pnum])
				

		elif cardName=='目击者':
			aimPlayer=self.__Players[NoX].ChoAim()
			self.broadcast('被要求展示手牌玩家为'+str(aimPlayer))
			handCard=self.__Players[int(aimPlayer)].showHand()
			self.__Players[NoX].SeeCard(handCard)

		elif cardName=='交易':
			self.broadcast(str(NoX)+'位玩家选择对象')
			tempAim=int(self.__Players[NoX].ChoAim())
			self.broadcast('选择的对象为'+str(tempAim))
			tempPool=[]
			self.broadcast(str(NoX)+'位玩家选择手牌')
			tempPool.append(self.__Players[NoX].giveCard(self.__Players[NoX].ChoCard()))
			self.broadcast(str(tempAim)+'位玩家选择手牌')
			tempPool.append(self.__Players[tempAim].giveCard(self.__Players[tempAim].ChoCard()))
			self.broadcast(str(NoX)+'位玩家获得手牌')
			self.Players[NoX].getCard(tempPool[1])
			self.broadcast(str(tempAim)+'位玩家获得手牌')
			self.Players[tempAim].getCard(tempPool[0])



		elif cardName=='谣言':
			for p in range(0,self.pnum):
				self.broadcast(str(p)+'位玩家选择下家手牌')
				savePool.append(self.__Players[(p+1)%self.pnum].giveCard( self.__Players[p].ChoCard()))
			for p in range(0,self.pnum):
				self.broadcast(str(p)+'位玩家获得手牌')
				self.__Players[p].getCard(savePool[p])
				

		elif cardName=='普通人':
			pass
		elif cardName=='狗':
			pass
		elif cardName=='共犯':
			self.broadcast(str(NoX)+'位玩家成为共犯')
			self.__Players[NoX].changeID()

		else :
			pass

	def TurnAndTurn(self,NoX):
		#第NoX位玩家有第一发现者
		turning=NoX
		while True:

			print(turning,'位玩家有手牌')
			print(self.__Players[turning].showHand())

			for p in self.__Players:
				p.Contract('你的手牌为:'+''.join(p.showHand()),False)

			self.broadcast(str(turning)+'玩家出牌')
			cardPlaying=self.__Players[turning].giveCard(self.__Players[turning].ChoCard())
			self.broadcast('出牌为'+str(cardPlaying))
			self.playCard(cardPlaying,turning)
			turning=(turning+1)%self.pnum
			

	def __init__(self,Players):
		self.__Players=[]
		for player in Players:
			self.__Players.append(player)
		self.pnum=len(self.__Players)





table1=Tabbbbbble()
table1.getFriend()
c=input()