from glob import escape
import os
from timeit import repeat


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen()
escape_num = 0
repet = 0
discard = 0
esc = 0
while True:
    while True:
        clear_screen()
        print("Welcome to Invoicing Software")
        print("Choose numbers below \n1. Generate Invoice\n2. Reprint Invoice\n3. View Bills\n4. Products Available\n5. Search Product\n6. Admin Panel")
        choice = input("Enter Your Choice: ")
        if (choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5" or choice == "6"):
            break
        else:
            print("Invalid Input! Try Again")
            # Invoice Generation
    if choice == "1":
        pass
            # Reprint Invoice
    elif choice == "2":
        pass
            # View Bills
    elif choice == "3":
        pass
            # Products Available 
    elif choice == "4":
        pass
            # Search Products
    elif choice == "5":
        pass
            # Admin Panel
    elif choice == "6":
        while True:
            admin_code = "5"
            a = input("Enter Admin Pass Code: ")
            if a == admin_code:
                print("Login Success")
                break
            else:
                print("Invalid Input! Try Again")
        while True:
            while True:
                print("1. Add Item")
                print("2. Edit Item")
                print("3. Update Stock")
                print("4. Remove Item")
                print("5. Exit")
                choice = input("Enter Your Choice: ")
                if choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5":
                    break
                else:
                    print("Invalid Input! Try Again")
            if choice == "1":
                # add item
                while True:
                    while True:
                        new_item_code = input("Enter Item Code(Example = 120) : ")
                        if new_item_code.isnumeric():
                            if len(new_item_code) == 3:
                                break
                            else:
                                print("Invalid Item Code. Item code Should be 3 Digits")
                        else:
                            print("Only numbers are allowed for Item code. Try again!")
                    if os.path.exists(f"Items\\{new_item_code}.txt"):
                        print("A item with the same code is available in your inventory.")
                        while True:
                            b = input("Do you want to add another product code ? (1 = Yes & 0 = No): ")
                            if b == "1" or b == "0":
                                if b == "1":
                                    break
                                elif b == "0":
                                    escape_num = 1
                                    break
                                else:
                                    print("Invalid Input! Try Again")
                            else:
                                print("Invalid Input! Try Again")
                                pass
                    else:
                        print("This is a new item. Let's Continue..")
                        break
                    if escape_num == 1:

                        break
                if escape_num == 1:
                    escape_num = 0
                    break
                while True:
                    new_item_name = input("Enter Product Name : ")
                    if len(new_item_name)< 20:
                        break
                    else:
                        print("Only 20 characters are allowed in Item Name!")
                        print("Try Again")
                        pass
                while True:
                    new_item_price = input("Enter MRP/Unit = ")
                    if new_item_price.isnumeric():
                        new_item_price = int(new_item_price)
                        if new_item_price > 0 and new_item_price < 10000:
                            break
                        else:
                            print("Invalid Input! Try Again")
                    else:
                        print("Invalid Input! Try Again")
                        pass
                while True:
                    new_item_stock = input("Enter opening stock = ")
                    if new_item_stock.isnumeric():
                        new_item_stock = int(new_item_stock)
                        if new_item_stock > 0 and new_item_stock < 1000:
                            break
                        else:
                            print("Invalid Input! Try Again")
                    else:
                        print("Invalid Input! Try Again")
                        pass
                new_item_name = new_item_name.capitalize()
                print(f"_ _ _ _ _ Preview _ _ _ _ _\nItem Code = {new_item_code}\nItem Name = {new_item_name}\nItem MRP/Unit = {new_item_price}\nOpening Stock = {new_item_stock}")
                while True:
                    c = input("Do you want to save It? (1 = Yes & 0 = No): ")
                    if c == "1" or c == "0":
                        if c == "1":
                            f = open(f"Items\\{new_item_code}.txt", "w")
                            f.write(f"{new_item_name}\n{new_item_price}\n{new_item_stock}")
                            f.close()
                            print("Item registered Successfully")
                            break
                        elif c == "0":
                            print("Item Discarded")
                            break
                        else:
                            print("Invalid Input! Try Again")
                            pass
                    else:
                        print("Invalid Input! Try Again")
             
            elif choice == "2":
                while True:
                    while True:
                        print("which Product you want to Edit")
                        item_code = input("Enter Item Code(Example = 120) : ")
                        if item_code.isnumeric():
                            if len(item_code) == 3:
                                break
                            else:
                                print("Invalid Item Code. Item code Should be 3 Digits")
                        else:
                            print("Only numbers are allowed for Item code. Try again!")
                    while True:
                        if os.path.exists(f"Items\\{item_code}.txt"):
                            break
                        else:
                            print("No items in your Inventory with this product code.")
                            while True:
                                b = input("Do you want to edit another product code ? (1 = Yes & 0 = No): ")
                                if b == "1" or b == "0":
                                    break
                                else:
                                    print("Invalid Input! Try Again")
                                    pass
                            if b == "1":
                                repet = 1
                                # print(f"repet = {repet}")
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
                        f = open(f"Items\\{item_code}.txt", "r")
                        old_name = f.readline()
                        old_price = f.readline()
                        old_stock = f.readline()
                        old_name = old_name.strip()
                        old_price = old_price.strip()
                        old_stock = old_stock.strip()
                        print(f"_ _ _ Product Details _ _ _\nItem Name = {old_name}\nItem MRP/Unit = {old_price}")
                        while True:
                            print("Which you want to Edit?\n1. Item Name\n2. MRP/Unit")
                            d = input("Enter your Choice : ")
                            if d == "1" or d == "0":
                                break
                            else:
                                print("Invalid Input! Try Again")
                        if d == "1":
                            while True:
                                new_name = input("Enter New Name : ")
                                if len(new_name) < 20:
                                    break
                                else:
                                    print("Invalid Input! Try Again")
                            print(f"_ _ _ Preview _ _ _\nItem Name = {new_name}\n Item MRP/Unit = {old_price}")
                            while True:
                                e = input("Do you want to save It? (1 = Yes & 0 = No): ")
                                if e == "1" or e == "0":
                                    if e == "1":
                                        f = open(f"Items\\{item_code}.txt", "w")
                                        f.write(f"{new_name}\n{old_price}\n{old_stock}")
                                        f.close()
                                        print("Item Updated Successfully")
                                        break
                                    elif e == "0":
                                        discard = 1
                                        print("Item Discarded")
                                        break
                                    else:
                                        print("Invalid Input! Try Again")
                                        pass
                                else:
                                    print("Invalid Input! Try Again")
                            if discard == 1:
                                discard = 0
                                while True:
                                    esca = input("Do you want to edit another Item? (1 = Yes & 0 = No): ")
                                    if esca == "1" or esca == "0":
                                        break
                                    else:
                                        print("Invalid Input! Try Again")
                                if esca == "0":
                                    esc = 1
                                break
                        elif d == 2:
                            
                    if esc == 1:
                        esc = 0
                        break

            elif choice == "3":
                # update stock
                pass
            elif choice == "4":
                # remove item
                pass
            elif choice == "5":
                # exit
                escape_num = 1
                break
                 
            
            
                    
        

    