from bsddb3 import db
#Get an instance of BerkeleyDB

def main():

    database = db.DB()
    database.open("te.idx")
    curs = database.cursor()
    iter = curs.first()
    while iter:
        print(iter)
        iter = curs.next()
    curs.close()
    database.close() 
    return 0
    
    
main()
