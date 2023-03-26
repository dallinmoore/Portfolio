#Dallin Moore

#test: alexander clayton (2 entries)

#import the necessary module
import sqlite3

#establish connection to .db file
conn = sqlite3.connect("dbvac_sqlite.db")

#create a database cursor
cursor = conn.cursor()


# 1 - ask for first and last name and assign the info to the list customer
customer = []
firstname = ""
lastname = ""
def names():
    firstname = input("Input customer first name > ")
    while firstname == "": #only runs if the input was blank, then loops until it is not blank
        print("Input must not be blank.")
        firstname = input("Input customer first name > ")
    
    lastname = input("Input customer last name > ")
    while lastname == "": #only runs if the input was blank, then loops until it is not blank
        print("Input must not be blank.")
        lastname = input("Input customer last name > ")
        
    #ask the database cursor to run a query for the specified customer
    cursor.execute("SELECT CustID, FName, LName, StateName, HHI, Marital, Children, HasPets FROM Customer, USState WHERE (fname = '%s' AND lname = '%s') AND Customer.CustState = USState.StateID;" % (firstname, lastname))
    for x in cursor:
        customer.append([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]])


# 2 - output the customer information
def customerinfo():
    
    if len(customer) > 1: #if there is more than one customer
        print("It appears there are multiple records with that name. \nChoose which number of customer you wish to view.")
        for x in range(len(customer)): #iterate through each of the multiples of users
            print((x+1),"- Customer ID:", customer[x][0],"First Name:",customer[x][1],"Last Name:",customer[x][2],"State:",customer[x][3])
        while True: #take input and assure its an int and in acceptable range
            verifycust = input("Input customer number > ") #ask the user what number the customer is
            try:
                verifycust = int(verifycust)
                if (verifycust-1) > len(customer): #verify in acceptable range
                    print("Try again. Must be 1 -", (len(customer)+1))
                else:
                    break
            except:
                print("Must be an integer.")
        
        customer[0] = customer[(verifycust-1)] #make the desired customer first in the list
            
    #print out the details on the customer
    print("Customer ID:", customer[0][0],"\nFirst Name:",customer[0][1],"\nLast Name:",customer[0][2],"\nState:",customer[0][3],"\nHousehold Income:",customer[0][4],"\nMarital:",customer[0][5],"\nChildren:",customer[0][6],"\nHas pets?:",customer[0][7])
    

# 3 - output product history info
def orderinfo():
    print("Sales Orders:")
    cursor.execute("SELECT SalesOrder.SOID, SODate, OrderTotal, Qty FROM SalesOrder, OrderLine WHERE SalesOrder.SOID = OrderLine.SOID AND CustID = %d;" % (customer[0][0]))
    orders = []
    orders.clear()
    for x in cursor:
        orders.append([x[0],x[1],x[2],x[3]])
    if len(orders) == 0:
        print("No records found.")
    else:
        for x in range(len(orders)): 
            print("Sales Order ID: %s, Date: %s, Order Total: $%s, Quantity: %s" % (orders[x][0],orders[x][1],orders[x][2],orders[x][3]))
            
count = 0
while True: #loop through the whole program
    count+=1
    names()
    while len(customer) == 0: #if there aren't any records in this search, run the loop
        print("Try again. That name is not in the database.")
        names()
    customerinfo()
    orderinfo()
    customer.clear()
    nextcust = input("Would you like to search for another customer? (y/n) > ")
    if nextcust.lower() == "n":
        print("You searched for a total of %d names. Have a nice day." % count)
        break
    while nextcust.lower() != "y":
        print("Try again. Input must be 'y' or 'n'.")
        nextcust = input("Would you like to search for another customer? (y/n) > ")
        