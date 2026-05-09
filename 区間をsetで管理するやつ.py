
from sortedcontainers import SortedSet 


class Pairset():
    data = None
    
    def __init__(self, lst: list) -> None:
        if lst:
            lst = sorted(list(set(lst)))
            data = []
            start = lst[0]
            end = lst[0]
            for i in range(1, len(lst)):
                if end + 1 == lst[i]:
                    end = lst[i]
                else:
                    data.append((start, end + 1))
                    start = lst[i]
                    end = lst[i]
            data.append((start, end + 1))
            self.data = SortedSet(data)
        else:
            self.data = SortedSet()
        self.data.add((-10**20,-10**20))
        self.data.add((10**20,10**20))
    
    def contains(self,x):
        idx = self.data.bisect_right((x,10**20))-1
        L_start,L_end = self.data[idx]
        return x < L_end
    
    def add(self,x):
        idx = self.data.bisect_right((x,10**20))-1
        L_start,L_end = self.data[idx]
        R_start,R_end = self.data[idx+1]
        if x < L_end:
            return False
        if L_end < x and x+1 < R_start:
            self.data.add((x,x+1))
        elif L_end == x and x+1 < R_start:
            self.data.pop(idx)
            self.data.add((L_start,x+1))
        elif L_end < x and x+1 == R_start:
            self.data.pop(idx+1)
            self.data.add((x,R_end))
        else:
            self.data.pop(idx+1)
            self.data.pop(idx)
            self.data.add((L_start,R_end))
        return True
    
    def mex(self,x):
        idx = self.data.bisect_right((x,10**20))-1
        L_start,L_end = self.data[idx]
        if L_end <= x:
            return x
        else:
            return L_end
        
    def expand(self,x):
        idx = self.data.bisect_right((x,10**20))-1
        L_start,L_end = self.data[idx]
        if L_end <= x:
            return x,x            
        else:
            return L_start, L_end
    
    def remove(self,x):
        idx = self.data.bisect_right((x,10**20))-1
        L_start,L_end = self.data[idx]
        if L_end <= x:
            return False
        self.data.pop(idx)
        if L_start < x:
            self.data.add((L_start,x))
        if x+1 < L_end:
            self.data.add((x+1,L_end))
        return True
    def add_interval(self, xL, xR):
        idx = self.data.bisect_left((xL, xR))
        if idx > 0:
            prev_start, prev_end = self.data[idx - 1]
            if xL <= prev_end:
                xL = prev_start
                xR = max(xR, prev_end)
                self.data.pop(idx - 1)
                idx -= 1
        while idx < len(self.data):
            next_start, next_end = self.data[idx]
            if next_start > xR:
                break
            xR = max(xR, next_end)
            self.data.pop(idx)

        self.data.add((xL, xR))

    def remove_interval(self, xL, xR):
        idx = self.data.bisect_left((xL, xL))
        if idx > 0:
            L_start, L_end = self.data[idx - 1]
            if L_start <= xL < L_end:
                self.data.pop(idx - 1)
                if L_start < xL:
                    self.data.add((L_start, xL))
                if xR < L_end:
                    self.data.add((xR, L_end))

        while idx < len(self.data):
            L_start, L_end = self.data[idx]
            if L_start >= xR:
                break
            self.data.pop(idx)
            if xR < L_end:
                self.data.add((xR, L_end))

