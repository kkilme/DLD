import copy
import random

def solution(minterm):
    numVar = minterm[0] #변수 개수
    size = minterm[1] #minterm 개수
    del minterm[:2]
    minterm.sort()

    piConsist = dict()   #pi를 이루는 minterm 기록 / ex: piConsist = {'00-': [0,1]}에서 pi 00-는 minterm 0과 1을 합친 결과라는 것을 의미
    mintermConsist = dict() #minterm이 들어가는 pi 기록 / ex : mintermConsist = {8: ['1020', '2200']}에서 minterm 8은 pi 1020과 2200을 만드는 데 사용됐다는 것을 의미
    for m in minterm:
        mintermConsist[m] = [];

    sortedMin = [[] for col in range(numVar+1)] #합칠 minterm이 모인 배열
    sortedMin2 = [[] for col in range(numVar+1)] #minterm이 합쳐진 결과들이 모이는 배열
    answer = [] # pi가 모이는 배열
    for i in range(size): # 입력받은 minterm을 2진수로 변환해서 sortedMin에 1의 개수에 따라 저장 (sortedMin: 2차원배열)
        minstr = format(minterm[i], 'b')
        while(len(minstr)<numVar):
            minstr = '0' + minstr # 변수의 개수에 맞춰서 0을 추가. 예를들어 변수가 3개일 때 이진수 11같은 경우 011로 표기해야함
        piConsist[minstr] = [minterm[i]]
        sortedMin[minstr.count('1')].append(minstr)

    #find PI
    for k in range(numVar):
        isCombined = copy.deepcopy(sortedMin) # pi인지 체크할 부울 배열. sortedMin과 같은 크기의 배열. 모든 값은 False로 초기화
        for i in range(len(isCombined)):
            for j in range(len(isCombined[i])):
                isCombined[i][j] = False
                
        for i in range(len(sortedMin)-1): # 두 minterm 합치기
            if (len(sortedMin[i]) != 0): 
                for m in sortedMin[i]:
                    for m2 in sortedMin[i+1]:
                        combinedMin = combine(m, m2) # combinedMin: 두 minterm이 합쳐진 결과값, 안합쳐지면 0을 리턴
                        if(combinedMin): # 합쳐지면 두 값에 해당하는 isCombined 값을 True로 변경. 이 둘은 PI가 아님
                            isCombined[i][sortedMin[i].index(m)] = True
                            isCombined[i+1][sortedMin[i+1].index(m2)] = True
                            if(combinedMin not in sortedMin2[i]): # sortedMin2에 합쳐진 결과 추가
                                sortedMin2[i].append(combinedMin)
                                piConsist[combinedMin] = [] # 일단 piConsist배열에도 합쳐진 결과를 추가함.
                                for fm1 in piConsist[m]: piConsist[combinedMin].append(fm1)
                                for fm2 in piConsist[m2]: piConsist[combinedMin].append(fm2)
        
        for i in range(len(isCombined)):
            for j in range(len(isCombined[i])):
                if(not isCombined[i][j]): #isCombined가 False라면 합쳐지지 않은 것이므로 pi에 해당하고 answer에 추가함.
                    answer.append(sortedMin[i][j])
                    for m in piConsist[sortedMin[i][j]]:
                        mintermConsist[m].append(sortedMin[i][j])
                elif (sortedMin[i][j] in piConsist): # 합쳐졌다면 해당 값은 pi가 아니므로 piConsist배열에 있다면 삭제 
                    del piConsist[sortedMin[i][j]]
        sortedMin = copy.deepcopy(sortedMin2) # 합쳐진 결과들이 모인 배열을 다시 합치는 배열로
        sortedMin2 = [[] for col in range(numVar-k)] # 결과 배열은 다시 초기화
    print("----------------------------------- Start -----------------------------------")
    print("Row after finding PI", piConsist)
    print("Column after finding PI", mintermConsist)

    epi = findEpi(piConsist, mintermConsist)
    answer.sort()
    for i in range(len(answer)): #정답 형식에 맞게 2를 -로 변경
        answer[i] = answer[i].replace('2','-')
    
    print('--------------------PI(except EPI)--------------------')
    for pi in answer:
        if pi not in epi: print(pi, end=', ')
    print()
    print('-------------------------EPI-------------------------')
    for e in epi:
        print(e)
    # answer.append("EPI")
    # for e in epi: answer.append(e)
       
    # return answer

# 두 minterm 합치기
def combine(m1, m2): 
    combined = ''
    count = 0 # 1과 0이 만나 합쳐진 횟수. 이 값이 1일때만 두 minterm이 합쳐지는 것에 해당함
    for i in range(len(m1)):
        if((m1[i] == '2' and m2[i] != '2') or (m1[i] == '2' and m2[i] != '2')):
            return 0
        elif((m1[i] == '1' and m2[i] == '0') or (m1[i] == '0' and m2[i] == '1')):
            count += 1
            combined += '2' # pi의 '-'는 일단 '2'로 저장. 오름차순 정렬을 하기 위함.
        else: combined += m1[i]

    if(count == 1): return combined 
    else: return 0 #안합쳐지면 0리턴

#ColumnDominance 구현, return값: 삭제된 column이 모인 배열
def columnDominance(mintermConsist, deletedColumn):
    tempMC = copy.deepcopy(mintermConsist)
    mintermConsistKeys = list(mintermConsist.keys())
    for i in range(len(mintermConsist)-1):
        for j in range(i+1, len(mintermConsist)):
            l = tempMC[mintermConsistKeys[i]]
            l2 = tempMC[mintermConsistKeys[i+1]]
            tempSet = set(l+l2) #합친 후 중복 제거
            if(len(l) == len(tempSet) or len(l2) == len(tempSet)): # 합친 set의 길이가 합치는데 사용한 리스트 중 하나와 길이가 같다면 dominance가 존재함
                if(len(l) >= len(l2)):
                    deletedColumn.append(mintermConsistKeys[i]) 
                    del mintermConsist[mintermConsistKeys[i]]
                else:
                    deletedColumn.append(mintermConsistKeys[j]) 
                    del mintermConsist[mintermConsistKeys[j]]
                return columnDominance(mintermConsist, deletedColumn)
    return deletedColumn

#RowDominance 구현, return값: 삭제된 row가 모인 배열
def rowDominance(piConsist, deletedRow):
    tempPC = copy.deepcopy(piConsist)
    piConsistKeys = list(piConsist.keys())
    for i in range(len(piConsist)-1):
        for j in range(i+1, len(piConsist)):
            l = tempPC[piConsistKeys[i]]
            l2 = tempPC[piConsistKeys[j]]
            tempSet = set(l+l2)
            if(len(l) == len(tempSet) or len(l2) == len(tempSet)):
                if(len(l) >= len(l2)):
                    deletedRow.append(piConsistKeys[j])
                    del piConsist[piConsistKeys[j]]
                else:
                    deletedRow.append(piConsistKeys[i]) 
                    del piConsist[piConsistKeys[i]]
                return rowDominance(piConsist, deletedRow)
    return deletedRow

#find epi
def findEpi(piConsist, mintermConsist):
    epi = list()
    count = 1
    while(True):     
        print(count,"회차----------------------------------------------------------------------------")
        #find EPI
        deletedEPI = [] #삭제된 EPI
        deletedMin = [] #삭제된 minterm
        for k in sorted(piConsist.keys()):
            for v in piConsist[k]:
                if(len(mintermConsist[v]) == 1 and k.replace('2','-') not in epi):
                    print("EPI: " + k)
                    epi.append(k.replace('2','-'))# 어떤 pi를 이루는 minterm이 한번만 사용되었다면, 그 pi는 epi임
                    deletedEPI.append(k)
                    for m in piConsist[k]: deletedMin.append(m)
                    del piConsist[k] #epi는 제거
        #deletedEPI와 deletedMin을 사용하여 테이블 축소
        for dm in deletedMin:
            for k in piConsist.keys():
                if dm in piConsist[k]: piConsist[k].remove(dm)
        tempDic = copy.deepcopy(piConsist)
        for m in tempDic.keys():
            if len(tempDic[m]) == 0: del piConsist[m]
        tempDic = copy.deepcopy(mintermConsist)
        for m in tempDic.keys():
            for e in deletedEPI:
                if e in tempDic[m] and m in mintermConsist.keys(): del mintermConsist[m]

        print("Row after finding EPI:",piConsist)
        print("Column after finding EPI",mintermConsist)
        
        #Find Column Dominance
        deletedColumn = columnDominance(mintermConsist, [])
        print("deleted column:", deletedColumn)
        for dc in deletedColumn: # 삭제된 column을 사용하여 테이블 축소
            for k in piConsist.keys():
                if dc in piConsist[k]: piConsist[k].remove(dc)
        tempDic = copy.deepcopy(piConsist)
        for m in tempDic.keys():
            if len(tempDic[m]) == 0: del piConsist[m]

        #Find Row Dominance
        deletedRow = rowDominance(piConsist, [])
        print("deleted row:", deletedRow)
        for dr in deletedRow: # 삭제된 row를 사용하여 테이블 축소
            for k in mintermConsist.keys():
                if dr in mintermConsist[k]: mintermConsist[k].remove(dr)
        tempDic = copy.deepcopy(mintermConsist)
        for m in tempDic.keys():
            if len(tempDic[m]) == 0: del mintermConsist[m]

        print("Row after dominance check",piConsist)
        print("Column after dominance check",mintermConsist)
        count+=1
        if(len(deletedColumn)+len(deletedRow) == 0): break
        
    return epi

def testRandom(numval, nummin):
    if(nummin > 2**numval-1):
        print("Error: too many minterms")
        return
    problem = [numval, nummin]
    while(len(problem) < nummin+2):
        a = random.randint(0, 2**numval-1)
        if a not in problem: problem.append(a)
    solution(problem)

#solution([3, 6, 0, 1, 2, 5, 6, 7])
# solution([4, 8, 0, 4, 8, 10, 11, 12, 13, 15])
#solution([4,11,0,2,5,6,7,8,10,12,13,14,15])
# solution([5, 25, 0,1,2,3,5,6,7,10,11,14,15,16,17,18,20,21,22,23,24,26,27,28,29,30,31])
#solution([4,11,0,2,5,6,7,8,10,12,13,14,15])
#solution([4,12,0,2,3,4,5,6,7,8,9,10,11,12,13])
#solution([3,6,0,1,2,5,6,7])) #no epi

testRandom(8,100)
