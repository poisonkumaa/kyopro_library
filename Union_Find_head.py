#https://atcoder.jp/contests/abc372/submissions/5806737

from sortedcontainers import SortedSet

class dsu():
	def __init__(self,N):
		self.parent_or_size=[-1 for i in range(N)]
		self.vs=[SortedSet([i]) for i in range(N)]
	def merge(self,x,y):
		x=self.leader(x)
		y=self.leader(y)
		if x==y:
			return x
		if (-self.parent_or_size[x]<-self.parent_or_size[y]):
			x,y=y,x
		self.parent_or_size[x]+=self.parent_or_size[y]
		self.parent_or_size[y]=x
		for v in self.vs[y]: self.vs[x].add(v)
		return x
	def query(self,v,k):
		v=self.leader(v)
		if len(self.vs[v])<k:
			return -1
		return self.vs[v][-k]+1
	def same(self,a,b):
		return self.leader(a)==self.leader(b)
	def leader(self,a):
		if (self.parent_or_size[a]<0):
			return a
		self.parent_or_size[a]=self.leader(self.parent_or_size[a])
		return self.parent_or_size[a]
	def size(self,a):
		return -self.parent_or_size[self.leader(a)]

