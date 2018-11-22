from bsddb3 import db


global mode

def changeMode():
    global mode
    selected = False
    while (selected == False):
        key = input('Please input a new output format: ')
        if (key.lower == 'output=full'):
            mode = 'full'
            selected = True
        elif (key.lower == 'output=brief'):
            mode = 'brief'
            selected = True
        else:
            print('BAD INPUT\n')
            
def IsKeyword(wordlist):
    keywords = ['price', 'cat', 'location', 'date', ]#output not included
    for word in wordlist:
        for keyword in keywords:
            if keyword in word:
                return True
    return False
            

def IsPrice()



            
def inputtingquery():
    global mode
    selected = False
    while (selected == False):
        key = input('Input a query : ')
        #Split with ','
        wordlist = key.split(',')
        if (IsKeyword(wordlist):

            
            
        else:#Check if in title or description
            

def menu():
    selection = False
    while (selected == False):
        print("Quit program : q, Change output format : f, Retrieve Data : t")
        key = input('Please select whatever: ')
        if (key == 'q'):
            selected = True
        elif (key == 'f'):
            changeMode()
        elif (key == 't'):
            inputtingquery()
        else:
            print('wrong input')
    while()            

def main():
    global mode
    mode = 'brief'
    
    print(output)
    return 0

