from bsddb3 import db


def CheckPrice(word):
    ind = -99
    symblist1 = ['>', '<', '=']
    symblist2 = ['>=', '<=']
    if ('price' in word.lower()):
        #print(word)
        for ch in word:
            if (ch in symblist1):
                sign = ch
                ind = word.find(ch)
                #print(word[ind:ind+2])
                break
        if (ind == -99):
            return 0 
        if word[ind:ind+2] in symblist2:
            sign = word[ind:ind+2]
        print(word)
        print(sign)
        return 0
    else:
        return 0
                
def CheckDate(word):
    ind = -99
    symblist1 = ['>', '<', '=']
    symblist2 = ['>=', '<=']
    if ('date' in word.lower()):
        #print(word)
        for ch in word:
            if (ch in symblist1):
                sign = ch
                ind = word.find(ch)
                #print(word[ind:ind+2])
                break
        if (ind == -99):
            return 0 
        if word[ind:ind+2] in symblist2:
            sign = word[ind:ind+2]
        print(word)
        print(sign)
        return 0
    else:
        return 0
        
        
def CheckLocation(word):
    if ('location' in word.lower()):
        ind = word.lower().find('location')
        if (word[ind+8: ind+9] == '='):
            print(word[ind+8: ind+9])
            print(word[ind+9:])
    return 0      

def CheckCat(word):
    if ('cat' in word.lower()):
        ind = word.lower().find('cat')
        if (word[ind+3: ind+4] == '='):
            print(word[ind+3: ind+4])
            print(word[ind+4:])
    return 0     


def CheckOthers(word):
    aidlist = CheckDatabase('te.idx', word)
    for a in aidlist:
        alist = CheckDatabase('ad.idx', a)
        print(alist)
    return 0



def CheckDatabase(dname, word):
    database = db.DB()
    database.open(dname)
    cur = database.cursor()
    result = cur.set(word.encode('utf-8'))
    rlist = []
    if(result != None):
        #print(result)
        #print("Term: " + str(result[0].decode("utf-8")) + ", Aid: " + str(result[1].decode("utf-8")))
        rlist.append(result[1].decode("utf-8"))
        
        #iterating through duplicates:
        dup = cur.next_dup()
        while(dup != None):
            #print("Term: " + str(dup[0].decode("utf-8")) + ", Aid: " + str(dup[1].decode("utf-8")))
            if (result[1].decode("utf-8") not in rlist):
                rlist.append(result[1].decode("utf-8"))
            dup = cur.next_dup()
    else:
        print("No Term Found.")
        
    #print(rlist)
    cur.close() 
    database.close()
    return rlist

def presimplified(word):
    ind = 0
    symblist1 = ['>', '<', '=', ' ']
    newkey = ''
    for ch in word:
        if (word[ind] == ' '):
            if (word[ind+1] not in symblist1):
                newkey = newkey + ch
        else:
            newkey = newkey + ch
        ind = ind + 1
    return newkey

def simplify(key):
    key = presimplified(key)
    key = presimplified(key[::-1])
    return key[::-1]
            
def main():
    key = 'camera date >=2018/11/05 date<=           2018/11/07 price > 20 price < 40'
    #key = 'camErA'
    key = simplify(key)
    print(key)
    #wordlist = key.split(' ')
    #for word in wordlist:
        #print(word)
        #CheckPrice(word)
        #CheckDate(word)
        #CheckLocation(word)
        #CheckCat(word)
        #CheckOthers(word.lower())  
    return 0
    
main()
            
