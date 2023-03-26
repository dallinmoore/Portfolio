#Dallin Moore

#import the necessary module
import sqlite3

#establish connection to .db file
conn = sqlite3.connect("dbvac_sqlite.db")

#create a database cursor
cursor = conn.cursor()

#recieve and validate user input for model id
inthelist = 0 #marker variable
while inthelist == 0:
    model = input("Input model ID > ")
    while len(model) != 2: #only run loop if the model id is not two letters
        print("Try again. Model ID must be two letters.")
        model = input("Input model ID > ")
    model = model.upper() #after getting a correct model id, make it uppercase
    cursor.execute("SELECT ModelID FROM Product;")
    for x in cursor: #check if model is in the database
        if model in x:
            inthelist = 1
    if inthelist == 0: #if the model isn't found in the database inthelist will still be 0
        print("Try again. That model isn't in the list.")
        
#recieve and validate user input for new price
while True:
    price = input("Input new price > ")
    try: #assure that the price is a float/integer then that it's positive
        price = float(price)
        if price <= 0: #if it's negative
            print("Try again. Price must be greater than zero.")
        else:
            break
    except: #if the price is not a float/integer
        print("Try again. Price must be float/integer.")

#look up the current price for the product
cursor.execute("SELECT ModelName, MSRP FROM Product WHERE ModelID = '%s'" % model)
for row in cursor: #output the information in the cursor object
    print("%s current price: $%f \n%s updated price: $%f" % (row[0],row[1],row[0],price))

#execute the price change
while True: #loop until it accepts y or n
    complete = input("Execute price change? (y/n) > ")
    if complete.lower() == "y":
        #execute the change
        cursor.execute("UPDATE Product SET MSRP = %f WHERE ModelID = '%s'" % (price, model))
        conn.commit()
        print("Price update complete.")
        cursor.execute("SELECT ModelID, ModelName, MSRP, ProdType FROM Product WHERE ModelID = '%s'" % model)
        for row in cursor: #print out the query from above
            print("Updated record:", row)
        break
    elif complete.lower() == "n":
        print("Change will not be executed.")
        break
    else: #when it isn't y or n
        print("Try again. Not a vaild answer.")