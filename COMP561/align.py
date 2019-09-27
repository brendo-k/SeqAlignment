import sys
import numpy as np

def globalAlign(S, T, matchScore, missmatchScore, B):
    
    match = np.empty([len(S)+1, len(T)+1])
    deletionT = np.empty([len(S)+1, len(T)+1])
    deletionS = np.empty([len(S)+1, len(T)+1])
    #first dimension = match, second = deletionT, third = deletionS
    pointerArray = [[[(-1,-1,-1),(-1,-1,-1),(-1,-1,-1)] for j in range(len(S) +1)] for i in range(len(T) + 1)]
    match[0][0] = 0
    deletionT[0][0] = 0
    deletionS[0][0] = 0
    deletionT[1][0] =  B
    deletionS[0][1] =  B
    for i in range(1,len(S)+1):
        match[i][0] = float('-inf')
        deletionS[i][0] = float('-inf')
        if i != 1:
            deletionT[i][0] = float('-inf')

    for i in range(1,len(T)+1):
        match[0][i] = float('-inf')
        deletionT[0][i] = float('-inf')
        if i != 1:
            deletionS[0][i] = float('-inf')
            
    pointerArray[0][1][1] = (0,0,0)
    pointerArray[1][0][2] = (0,0,0)
    pointerArray[0][0][0] = (-1,-1,-1)
    



    for i in range(1,len(S)+1):
        for j in range(1,len(T)+1):
            #updating the match matrix
            [maximum, index] =  maxPlusIndex(match[i-1][j-1], deletionS[i-1][j-1], deletionT[i-1][j-1])
            match[i][j] = compare(S[i-1], T[j-1], matchScore, missmatchScore) + maximum
            if index == 0: 
                pointerArray[i][j][0] = (i-1, j-1, 0)
            elif index == 1:
                pointerArray[i][j][0] = (i-1, j-1, 1)
            else:
                pointerArray[i][j][0] = (i-1,j-1,2) 
                

            #updating the deletionT matrix
            #if deletionT[i-1][j] != float("-inf"):
            #    deletionTScore = float("-inf")
            #else:
            #    deletionTScore = del
            [maximum, index] = maxPlusIndex(match[i-1][j] - 1, deletionS[i-1][j] - 1)
            deletionT[i][j] = maximum
            if index == 0: 
                pointerArray[i][j][2] = (i-1, j, 0)
            else:
                pointerArray[i][j][2] = (i-1, j, 1)

            #updating the deletionS matrix
            #if deletionS[i][j-1] != float("-inf"):
            #    deletionS = float("-inf")
            #else:
            [maximum, index] = maxPlusIndex(match[i][j-1] - 1, deletionT[i][j-1] - 1)
            deletionS[i][j] = maximum
            if index == 0: 
                pointerArray[i][j][1] = (i, j-1, 0)
            else:
                pointerArray[i][j][1] = (i, j-1, 2)
    
    #backtracking
    [score, index] = maxPlusIndex(match[-1][-1], deletionT[-1][-1], deletionS[-1][-1])
    alignment = ['','']
    end = pointerArray[len(S)][len(T)][index]
    sCur = len(S)
    tCur = len(T)
    while (end != (-1,-1,-1)):
        positionS = end[0]
        positionT = end[1]
        diffS = sCur - positionS
        diffT = tCur - positionT
        sCur = positionS
        tCur = positionT
        end = pointerArray[end[0]][end[1]][end[2]]
        if (diffS == 1 and diffT == 0):
            alignment[0] = S[sCur] + alignment[0]
            alignment[1] = '-' + alignment[1]
        elif (diffT == 1 and diffS == 0):
            alignment[0] = '-' + alignment[0]
            alignment[1] = T[tCur] + alignment[1]
        else:
            alignment[0] = S[sCur] + alignment[0]
            alignment[1] = T[tCur] + alignment[1]

    return [score, alignment]

def compare(S, T, matchScore, missmatchScore):
    if (S == T):
        return matchScore
    else:
        return missmatchScore
   
def maxPlusIndex(num1, num2, num3=float("-inf")):
    maximum = max(num1,num2, num3)
    if maximum == num1:
        return [maximum, 0]
    if maximum == num2:
        return [maximum, 1]
    if maximum == num3:
        return [maximum, 2]


    

def main():
    
    f = open(sys.argv[1],"r")
    S = ''
    T = ''
    flag = 0 
    for x in f:
        if(x[0] == '>'):
            continue
        if(x[0] == '\n'):
            flag = 1
            continue
        if(flag == 0 ):
            S += x.strip()
        else:
            T += x.strip()
    f.close()
    [score, alignment] = globalAlign(S, T, 1, -1, -1)
    print (score)
    print (alignment)

if __name__ == '__main__':
    main()