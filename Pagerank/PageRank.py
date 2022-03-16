#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None, index = None):
        self.origin = origin # write appropriate value
        self.weight = 1.0 # write appropriate value
        self.index = index

    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None, index = None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict() #(IATA code, routes index)
        self.outweight = 0.0
        self.index = index

    def newEdge(self, originCode):
        if originCode in self.routeHash:
            e = self.routes[self.routeHash[originCode]]
            e.weight += 1.0
        else :
            e = Edge(originCode, airportHash[originCode].index)
            self.routes.append(e)
            self.routeHash[originCode] = len(self.routes)-1

    def __repr__(self):
        return f"{self.code}\t{self.pageIndex}\t{self.name}"

#edgeList = [] # list of Edge
#edgeHash = dict() # hash of edge to ease the match

airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
pageRank = [] #solution
totalOut = 0

def readAirports(fd):
    print("Reading airport file...")
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            aux = line.split(',')
            if len(aux[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=aux[1][1:-1] + ", " + aux[3][1:-1]
            a.code=aux[4][1:-1]
            a.index = cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()

def getAirportbyCode(code):
     if code in airportHash:
         index = airportHash[code].index
         a = airportList[index]
         return a
     else :
         raise Exception ("IATA code not found.")

def readRoutes(fd):
    print("Reading routes file...")
    routesTxt = open(fd, "r");
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[4]) != 3 or len(temp[2]) != 3: raise Exception('not an IATA code')
            originCode = temp[2]
            destinationCode = temp[4]

            originAirport = getAirportbyCode(originCode)
            destinationAirport = getAirportbyCode(destinationCode)

            destinationAirport.newEdge(originCode)
            originAirport.outweight += 1.0

        except Exception as inst:
            pass

def sum1Test(list):
    sum = 0
    for x in list:
        sum += x
    print(sum)

def checkConvergence(dif, P, Q):
    val = [a_i - b_i for a_i, b_i in zip(P, Q)]
    absolut = map(lambda v: abs(v), val)
    return all(map(lambda v: v < dif, absolut)) 

def computePageRanks(dumping, senseCond):
    # write your code
    print("Computing pagerank...")
    n = len(airportList) #number of vertices in G
    nInv = 1.0/n
    P = [nInv]*n
    L = dumping                #damping factor
    iterations = 0
    stoppingCondition = False

    const = (1.0-L)/n
    nOut = L/float(n)*totalOut
    aux = 1.0/n

    while not stoppingCondition:
        Q = [0.0]*n
        for i in range(n):
            a = airportList[i]
            sum = 0
            for edge in a.routes:
                w = edge.weight
                out = airportList[edge.index].outweight
                sum += P[edge.index]*w/out
            Q[i] = L*sum+const+aux*nOut

        aux = const+aux*nOut
        stoppingCondition = checkConvergence(senseCond,P,Q)
        #sum1Test(Q)
        P = Q
        iterations += 1

    global pageRank
    pageRank = P.copy()
    return iterations


def outputPageRanks(y, sC):
    print("SOLUTION FOUND")
    print("With: ")
    print(" -Dumping factor = ", y)
    print(" -Convergence condition : difference less than ", sC)
    print("-------------------------------------------------------------------")
    print("-----------------------(Page rank, Airport)------------------------")
    print("-------------------------------------------------------------------")

    S = []
    i = 0
    for k in airportHash:
        a = airportHash[k]
        x = (a.name, pageRank[i])
        S.append(x)
        i+=1
    S.sort(key = lambda x: x[1], reverse = True)
    sum = 0
    for (a,p) in S:
        sum += p
        print("(%s : %s)\n"%(p, a))
    print("Pagerank sum = ", sum)


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")

    global totalOut
    totalOut = len(list(filter(lambda n: n.outweight == 0, airportList)))
    dumpingF = 0.8
    stopCond = 1*10**(-15)
    time1 = time.time()
    iterations = computePageRanks(dumpingF, stopCond)
    time2 = time.time()
    outputPageRanks(dumpingF, stopCond)
    print("Iterations number = ", iterations)
    print("Compute time = ", time2-time1)



if __name__ == "__main__":
    sys.exit(main())
