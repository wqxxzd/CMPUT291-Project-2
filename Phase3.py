from bsddb3 import db
import sys


global mode


def GetFileName():
    #Get the name of the input file from sys.argv
    if (len(sys.argv) != 2):
        print('Invalid command line.')
        sys.exit()
    fname = sys.argv[1]
    return fname



def CheckDatabase(dname, word, idx):
    #This function will check the databse based on the filename, key word and the index.
    database = db.DB()
    database.open(dname)
    cur = database.cursor()
    result = cur.set(word.encode('utf-8'))
    rlist = []
    if(result != None):
        rlist.append(result[idx].decode("utf-8"))
        dup = cur.next_dup()
        while(dup != None):
            if (dup[idx].decode("utf-8") not in rlist):
                rlist.append(dup[idx].decode("utf-8"))
            dup = cur.next_dup()
    cur.close() 
    database.close()
    return rlist


    
def CheckPrice(word):
    key,value,symbol = SymbolsandStuff(word, 'price')
    if (key == None and value == None and symbol == None):
        flag = 0
        return [], flag
    else:
        #Run the CheckRange function with the given values
        rlist = CheckRange(value, symbol, 'pr.idx')
        flag = 1
        return rlist, flag


        
def SymbolP2(word,symbol):
    if (symbol in word):
        wordlist = word.split(symbol)
        return wordlist[0], wordlist[1]
    return None        


        
def SymbolsandStuff(word, keyword):
    #This function will splite the word to get key, vlaue and symbol 
    key = None
    value = None
    symbol = None
    slist = ['<=', '>=', '=', '<', '>']
    for i in slist:
        if (i in word):
            key, value = SymbolP2(word, i)
            if (key == keyword):
                symbol = i
                return key, value, symbol
            else:
                return None, None, None
    return key, value, symbol        
    
    
    
def getAIDOnly(result):
    #Get only aid
    words = result.split(',')
    string = words[0]
    return string        


           
def CheckRange(keystring, sign, filename):
    database = db.DB()
    database.open(filename)
    cur = database.cursor()
    if (filename == 'pr.idx'):
        keystring = keystring.rjust(12, ' ')
    result = cur.set_range(keystring.encode('utf-8'))
    rlist = []
    iterated = False
    reverse = None
    if(result != None):
        if (sign == '<='):
            #So the result can go back to its previous result
            reverse = result
        while(result != None):
            string = str(result[0].decode("utf-8"))
            string2 = result[1].decode("utf-8") 
            #print(string, sign, keystring, string2)
            if (string2 not in rlist):
                if (sign == '>'):  
                    #Get all greater than so just keep going next
                    if (str.isdigit(string) and str.isdigit(keystring)):
                        if (int(string) > int(keystring)):
                            rlist.append(getAIDOnly(string2))
                    else:
                        if (string > keystring):
                            rlist.append(getAIDOnly(string2))
                    result = cur.next()    
                elif (sign == '<' ):
                    #Get all less than so don't check anything equal to so just go previous
                    if (str.isdigit(string) and str.isdigit(keystring)):
                        if (string < keystring):
                            rlist.append(getAIDOnly(string2))
                    else:
                        if (string < keystring):
                            rlist.append(getAIDOnly(string2))
                    result = cur.prev() 
                elif (sign == '>='):
                    if (str.isdigit(string) and str.isdigit(keystring)):
                        if (string >= keystring):
                            rlist.append(getAIDOnly(string2))
                    else:
                        if (string >= keystring):
                            rlist.append(getAIDOnly(string2)) 
                    #Get all greater than and equal to so just go next
                    result = cur.next()
                elif (sign == '<='):
                    #Get all less and EQUAL to so first gotta iterate through all prev then go back
                    #To get the things equal to....
                    if (str.isdigit(string) and str.isdigit(keystring)):
                        if (string <= keystring):
                            rlist.append(getAIDOnly(string2))
                    else:
                        if (string <= keystring):
                            rlist.append(getAIDOnly(string2))
                    if (iterated is False):
                        result = cur.prev()
                    elif (iterated is True):
                        result = cur.next()
                    if (result is None):
                        #Reached the endpoint so either go back to original result or not at all
                        if (iterated is False):
                            result = reverse
                            iterated = True
                        else:
                            break
                elif (sign == '='):
                    #Only get the equals so if the value is not equal then stop iterating
                    #print(string)
                    #print(keystring)
                    if (string == keystring):
                        #print('gdshkafsdgsdgfsdhgfsjlg')
                        #print(string)
                        rlist.append(getAIDOnly(string2))
                    result = cur.next()
                    #print(result)
                    if(result == None or str(result[0].decode("utf-8")) != keystring): 
                        break
                else:
                    #Something went wrong or something so just iterate through??
                    #Or maybe break?
                    result = cur.next()
                     
            else:
                result = cur.next() 
    cur.close() 
    database.close()
    return rlist     



              
def CheckDate(word):
    key,value,symbol = SymbolsandStuff(word,'date')
    if (key == None and value == None and symbol == None):
        flag = 0
        return [], flag
    else:
        #Run the CheckRange function with the given values
        rlist = CheckRange(value, symbol, 'da.idx')
        flag = 1
        return rlist, flag
        
        
     
def CheckLocation(word):
    #This function will check keword location first and return all aids if matched
    llist = []
    flag = 0
    if ('location' in word.lower()):
        ind = word.lower().find('location')
        if (word[ind+8: ind+9] == '='):
            loc = word[ind+9:]
            database = db.DB()
            database.open('da.idx')
            cur = database.cursor()
            iter = cur.first()
            while iter:
                result = iter[1].decode('utf-8')
                rlist = result.split(',')
                if (loc == rlist[2].lower()):
                    llist.append(rlist[0])
                iter = cur.next()
            cur.close() 
            database.close()
            flag = 1
    return llist, flag      



def CheckCat(word):
    #This function will check keyword cat first and return all aids if matched
    clist = []
    flag = 0
    if ('cat' in word.lower()):
        ind = word.lower().find('cat')
        if (word[ind+3: ind+4] == '='):
            cat = word[ind+4:]
            database = db.DB()
            database.open('da.idx')
            cur = database.cursor()
            iter = cur.first()
            while iter:
                result = iter[1].decode('utf-8')
                rlist = result.split(',')
                if (cat == rlist[1].lower()):
                    clist.append(rlist[0])
                iter = cur.next()
            cur.close() 
            database.close()
            flag = 1
    return clist, flag
    
    
    
def CompareFunc(word1, word2):
    #This function can compare word1 and word2 (Partial match)
    if (len(word1) <= len(word2)):
        if (word2.find(word1) == 0):
            return True
        else:
            return False
    else:
        return False
        
        

def CheckOthers(word, check):
    #This function will check the index te.idx, and retrieve the aid of matching terms
    #Flag:    0: Functin is not run   1: Functin is run and nothing found
    resultlist = []
    if (check == 1):
        flag = 0
        return resultlist, flag
    else:
        flag = 1
    if ('%' in word):
        #Partial match is done by iterate all terms and do the comparision
        if (word.find('%') == len(word)-1):
            database = db.DB()
            database.open('te.idx')
            cur = database.cursor()
            iter = cur.first()
            while iter:
                if (CompareFunc(word[:len(word)-1], iter[0].decode('utf-8'))):
                    resultlist.append(iter[1].decode('utf-8'))
                iter = cur.next()
            cur.close() 
            database.close()
    else:
        aidlist = CheckDatabase('te.idx', word, 1)
        resultlist += aidlist
    return resultlist, flag
    
    
    
def presimplified(word):
    #This function can ONLY delete the space BEFORE the sign
    ind = 0
    symblist1 = ['>', '<', '=', ' ']
    newkey = ''
    for ch in word:
        if (word[ind] == ' '):
            if ((ind+1) == len(word)):
                return newkey[:ind]
            elif (word[ind+1] not in symblist1):
                newkey = newkey + ch
        else:
            newkey = newkey + ch
        ind = ind + 1
    return newkey



def simplify(key):
    #This function will delete all the space before and after the sign  
    key = presimplified(key)#Delete the space before the sign 
    key = presimplified(key[::-1])#Reverse the string so it will delete the space after the sign 
    return key[::-1]
    
    
    
def substraction(line, str1, str2):
    #obtain the string between str1 and str2 in line
    #If nothing found, return -1 
    index1 = -1
    index1 = line.find(str1)
    index2 = line.find(str2)
    if (index1!= -1):
        if (index2 > index1 + len(str1)):
            return line[index1 + len(str1): index2]
        else:
            return -1
    return -1  
    
    
    
def GetTitle(fname):
    #This function will create a dictionary from the file that in sys.argv
    #dict[aird] : title
    titledict = {}
    infile = open(fname, 'r')
    for line in infile:
        aid = substraction(line, '<aid>', '</aid>')
        if (aid != -1):
            title = substraction(line, '<ti>', '</ti>')
            titledict[aid] = title 
    return titledict
    
    
def CheckFormat(ind, word):
    #This function checks if output=full or output=brief is equal to word
    #Flag:    0: Functin is not run   1: Functin is run and nothing found
    #Since this function only check the format, it won't deal with any terms, so decrase the index to make it consistent
    global mode
    flag = 0
    if (word == 'output=full'):
        mode = 'full'
        ind -= 1
        print('Format Changed to FULL')
        flag = 1
    elif (word == 'output=brief'):
        mode = 'brief'
        ind -= 1
        print('Format Changed to BRIEF')
        flag = 1
    return ind, flag


def DisplayResult(rlist, titledict):
    #Dsiplay the final result based on the mode
    #If mode is brief, display Title and Aid
    #If mode is full, display the full record
    global mode
    print('-------------[RESULT]-------------')
    if not rlist:
        print('|         No item found          |')
    else:
        if (mode == 'brief'):
            print('|      Title     |      Aid      |')
            for t in rlist:
                print('| ' + str(titledict[t]) + ' | ' + str(t) + ' |')
        else:
            resultlist = []
            for t in rlist:
                resultlist = resultlist + CheckDatabase('ad.idx', t, 1)
            ind = 1
            for r in resultlist:
                print('Record ' + str(ind) + ':')
                print(str(r) + '\n')
                ind += 1
    print('----------------------------------')
    return 0



def Combine(r, f, lst1, lst2):
    #Combine lst1 and lst 2 according to index r and flag f
    if (r == 1):
        l = lst1 + lst2
        return l
    else:
        if (f == 0):
            return lst1
        else:
            return list(set(lst1) & set(lst2))
    
    
          
def DealQuery(fname):
    global mode
    titledict = GetTitle(fname)
    key = input('Please input the conditions you want to search: ')
    key = simplify(key.lower())
    #Check if the input = 'output=full' or 'output=brief' (EXACT MATCH)
    if (key == 'output=full'):
        mode = 'full'
        print('Format Changed to FULL, now return to home page.')
        return 0
    elif (key == 'output=brief'):
        mode = 'brief'
        print('Format Changed to BRIEF, now return to home page.')
        return 0
        
    rlist = []
    wordlist = key.split(' ')
    #ind: the count of runs in for loop
    ind = 1
    for word in wordlist:
        #Check:   0: Not Checked yet  1: Visited
        #Flag:    0: Functin is not run   1: Functin is run and nothing found
        check = 0
        ind, flag = CheckFormat(ind, word)
        if (flag == 1): check = 1# If flag is 1 (function is run), then check is 0 (the current word is checked)

        templist, flag = CheckPrice(word.lower())
        if (flag == 1): check = 1
        rlist = Combine(ind, flag, rlist, templist)

        templist, flag = CheckDate(word.lower())
        if (flag == 1): check = 1
        rlist = Combine(ind, flag, rlist, templist)

        templist, flag = CheckLocation(word.lower())
        if (flag == 1): check = 1
        rlist = Combine(ind, flag, rlist, templist)

        templist, flag = CheckCat(word.lower())
        if (flag == 1): check = 1
        rlist = Combine(ind, flag, rlist, templist)

        templist, flag = CheckOthers(word.lower(), check)
        rlist = Combine(ind, flag, rlist, templist)
        ind += 1
    
    #Display the final result
    DisplayResult(rlist, titledict)
    return 0



def menu(fname):
    #Display the home menu
    while (1):
        print('-------------[Home]--------------')
        print('|        Retrieve Data : t       |')
        print('|        Quit program : q        |')
        print('----------------------------------')
        key = input('Please select: ')
        if (key.lower() == 'q'):
            sys.exit(0)
        elif (key.lower() == 't'):
            DealQuery(fname)
        else:
            print('wrong input')            



def main():
    global mode
    fname = GetFileName()
    mode = 'brief'
    menu(fname)
    return 0

main()
