import os 
def product_add():    
    while True:
        while True:
            print("which Product you want to ADD?")
            item_code1 = input("Enter Item Code(Example = 120) : ")
            if item_code1.isnumeric():
                if len(item_code1) == 3:
                    break
                else:
                    print("Invalid Item Code. Item code Should be 3 Digits")
            else:
                print("Only numbers are allowed for Item code. Try again!")
        while True:
            if os.path.exists(f"Items\\{item_code1}.txt"):
                break
            else:
                print("No items in your Inventory with this product code.")
                while True:
                    b = input("Do you want to add another product code ? (1 = Y& 0 = No): ")
                    if b == "1" or b == "0":
                        break
                    else:
                        print("Invalid Input! Try Again")
                        pass
                if b == "1":
                    repet = 1
                    break
                elif b == "0":
                    escape_num = 1
                    break
                else:
                    print("Invalid Input! Try Again")
                if escape_num == 1:
                    break
        if escape_num == 1:
            escape_num = 0
            break
        while True:
            if repet == 1:
                repet = 0
                break
            f = open(f"Items\\{item_code1}.txt", "r")
            itemname1 = f.readline()
            itemprice1 = f.readline()
            itemstock1 = f.readline()
            itemname1 = itemname1.strip()
            itemprice1 = itemprice1.strip()
            itemstock1 =itemstock1.strip()
            itemprice1 = int(itemprice1)
            itemstock1 = int(itemstock1)
            print(f"_ _ _ Product Details _ _ _\nItem Name = {itemname1}\nItem MRP/Unit ={itemprice1}\nItem Stock = {itemstock1}")
            while True:
                item1qty = input("Enter Quantity : ")
                if item1qty.isnumeric():
                    if int(item1qty) > 0 and int(item1qty) <100:
                        item1qty = int(item1qty)
                        if item1qty < itemstock1:
                            break
                        else:
                            print("You don't have enough stock to fulfill the order")
                    else:
                        print("Invalid Item Code. Item code Should be less than 2 Digits")
                else:
                    print("Only numbers are allowed for Item code. Try again!")
            print("Item Added")
            break
        break
    return itemname1, item1qty
product_add()

