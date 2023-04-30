from glob import escape
import os
from timeit import repeat
from xmlrpc.client import TRANSPORT_ERROR
import datetime
from xml.dom.minidom import Document
import docx
import os
import qrcode
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

directory_path = 'Invoices'

def rep_word(doc_name, old_word, new_word):
    doc = docx.Document(doc_name)

    for p in doc.paragraphs:
        if old_word in p.text:
            inline = p.runs
            for i in range(len(inline)):
                if old_word in inline[i].text:
                    text = inline[i].text.replace(old_word, new_word)
                    inline[i].text = text
    new_doc_name = f"{invno}.docx"
    doc.save(f"Invoices//{new_doc_name}")
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen()
escape_num = 0
repet = 0
discard = 0
esc = 0
items = 0
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
                f.close()
                print(f"_ _ _ Product Details _ _ _\nItem Name = {itemname1}\nItem MRP/Unit = {itemprice1}\nItem Stock = {itemstock1}")
                while True:
                    item1qty = input("Enter Quantity : ")
                    if item1qty.isnumeric():
                        if int(item1qty) > 0 and int(item1qty) <100:
                            item1qty = int(item1qty)
                            if item1qty <= itemstock1:
                                new_item_stock = (itemstock1 - item1qty)
                                f = open(f"Items\\{item_code1}.txt", "w")
                                f.write(f"{itemname1}\n{itemprice1}\n{new_item_stock}")
                                f.close()
                                break
                            else:
                                print("You don't have enough stock to fulfill the order")
                        else:
                            print("Invalid Item Code. Item Quantity Should be less than 2 Digits")
                    else:
                        print("Only numbers are allowed for Item code. Try again!")
                print("Item Added")
                items = 1
                item1amount = item1qty * itemprice1
                print(f"Current Bill Amount is = {item1amount}")
                while True:
                    in1 = input("1. Add another item\n2. Generate Incoice")
                    if in1 == "1" or in1 == "2":
                        if in1 == "1":
                            add_item1 = 1
                            generateinvoice1 = 0
                            break
                        elif in1 == "2":
                            generateinvoice1 = 1
                            add_item1 = 0
                            break
                        else:
                            print("Invalid Input! Please Try Again.")
                    else:
                        print("Invalid Input! Please Try Again.")
                if generateinvoice1 == 1:
                    while True:
                        paymode = input("Payment Mode:\n1. Cash Payment\n2. Upi Payment")
                        if paymode == "1" or paymode == "2":
                            if paymode == "1":
                                file = "Templetes//1.docx"
                                break
                            elif paymode == "2":
                                file = "Templetes//1QR.docx"
                                link = f"upi://pay?pa=rajlakshmi.mohanty@ybl&pn=abcd&am={item1amount}&tn=Tasty Confectionary&cu=INR"
                                img = qrcode.make(link)
                                img.save("qrcode.png")
                                break
                        else:
                            print("Invalid Input! Please Try Again.")
                    files = os.listdir(directory_path)
                    num_files = len(files)
                    invno = num_files + 1
                    print("Invoice Number is = ", invno)
                    now = datetime.datetime.now()
                    current_datetime = now.strftime("%d-%m-%Y        Time - %H:%M:%S")
                    rep_word(f"{file}", "111", f"INV {invno}")
                    rep_word(f"Invoices//{invno}.docx", "112", f"{current_datetime}")
                    rep_word(f"Invoices//{invno}.docx", "114", f"{itemname1}")
                    rep_word(f"Invoices//{invno}.docx", "115", f"{item1qty}")
                    rep_word(f"Invoices//{invno}.docx", "116", f"{item1amount}")
                    rep_word(f"Invoices//{invno}.docx", "117", f"{item1qty}")
                    rep_word(f"Invoices//{invno}.docx", "118", f"{item1amount}")
                    if paymode == "2":
                        document = Document(f"Invoices//{invno}.docx")
                        paragraph = document.add_paragraph()
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = paragraph.add_run()
                        run.add_picture('qrcode.png', width=Inches(0.85), height=Inches(0.85))

                        document.save(f"Invoices//{invno}.docx")
                    while True:
                        if os.path.exists(f"Invoices//{invno}.docx"):
                            break
                    file = f"Invoices\\{invno}.docx"
                    os.startfile(file,'print')
                    break
                elif add_item1 == 1:
                    add_item1 = 0
                    while True:
                        print("which Product you want to ADD?")
                        item_code2 = input("Enter Item Code(Example = 120) : ")
                        if item_code2.isnumeric():
                            if len(item_code2) == 3:
                                break
                            else:
                                print("Invalid Item Code. Item code Should be 3 Digits")
                        else:
                            print("Only numbers are allowed for Item code. Try again!")
                    while True:
                        if os.path.exists(f"Items\\{item_code2}.txt"):
                            break
                        else:
                            print("No items in your Inventory with this product code.")
                            while True:
                                repet = 0
                                escape_num = 0
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
                        f = open(f"Items\\{item_code2}.txt", "r")
                        itemname2 = f.readline()
                        itemprice2 = f.readline()
                        itemstock2 = f.readline()
                        itemname2 = itemname2.strip()
                        itemprice2 = itemprice2.strip()
                        itemstock2 =itemstock2.strip()
                        itemprice2 = int(itemprice2)
                        itemstock2 = int(itemstock2)
                        f.close()
                        print(f"_ _ _ Product Details _ _ _\nItem Name = {itemname2}\nItem MRP/Unit = {itemprice2}\nItem Stock = {itemstock2}")
                        while True:
                            item2qty = input("Enter Quantity : ")
                            if item2qty.isnumeric():
                                if int(item2qty) > 0 and int(item2qty) <100:
                                    item2qty = int(item2qty)
                                    if item2qty <= itemstock2:
                                        new_item_stock = (itemstock2 - item2qty)
                                        f = open(f"Items\\{item_code2}.txt", "w")
                                        f.write(f"{itemname2}\n{itemprice2}\n{new_item_stock}")
                                        f.close()
                                        break
                                    else:
                                        print("You don't have enough stock to fulfill the order")
                                else:
                                    print("Invalid Item Code. Item Quantity Should be less than 2 Digits")
                            else:
                                print("Only numbers are allowed for Item code. Try again!")
                        print("Item Added")
                        items = 2
                        item1amount = item1qty * itemprice1
                        item2amount = item2qty * itemprice2
                        item2total = item1amount+item2amount
                        item2qtytotal = item1qty + item2qty

                        print(f"Current Bill Amount is = {item2total}")
                        while True:
                            in2 = input("1. Add another item\n2. Generate Incoice")
                            if in2 == "1" or in2 == "2":
                                if in2 == "1":
                                    add_item2 = 1
                                    break
                                elif in2 == "2":
                                    generateinvoice2 = 1
                                    break
                                else:
                                    print("Invalid Input! Please Try Again.")
                            else:
                                print("Invalid Input! Please Try Again.")

                        if generateinvoice2 == 1:
                            generateinvoice2 = 0
                            while True:
                                paymode2 = input("Payment Mode:\n1. Cash Payment\n2. Upi Payment")
                                if paymode2 == "1" or paymode2 == "2":
                                    if paymode2 == "1":
                                        file2 = "Templetes//2.docx"
                                        break
                                    elif paymode2 == "2":
                                        file2 = "Templetes//2QR.docx"
                                        link = f"upi://pay?pa=rajlakshmi.mohanty@ybl&pn=abcd&am={item2total}&tn=Tasty Confectionary&cu=INR"
                                        img = qrcode.make(link)
                                        img.save("qrcode.png")
                                        break
                                else:
                                    print("Invalid Input! Please Try Again.")
                            files = os.listdir(directory_path)
                            num_files = len(files)
                            invno = num_files + 1
                            print("Invoice Number is = ", invno)
                            now = datetime.datetime.now()
                            current_datetime = now.strftime("%d-%m-%Y        Time - %H:%M:%S")
                            rep_word(f"{file2}", "111", f"INV {invno}")
                            rep_word(f"Invoices//{invno}.docx", "112", f"{current_datetime}")
                            rep_word(f"Invoices//{invno}.docx", "114", f"{itemname1}")
                            rep_word(f"Invoices//{invno}.docx", "115", f"{item1qty}")
                            rep_word(f"Invoices//{invno}.docx", "116", f"{item1amount}")
                            rep_word(f"Invoices//{invno}.docx", "117", f"{itemname2}")
                            rep_word(f"Invoices//{invno}.docx", "118", f"{item2qty}")
                            rep_word(f"Invoices//{invno}.docx", "119", f"{item2amount}")
                            rep_word(f"Invoices//{invno}.docx", "120", f"{item2qtytotal}")
                            rep_word(f"Invoices//{invno}.docx", "121", f"{item2total}")
                            if paymode2 == "2":
                                document = Document(f"Invoices//{invno}.docx")
                                paragraph = document.add_paragraph()
                                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                run = paragraph.add_run()
                                run.add_picture('qrcode.png', width=Inches(0.8), height=Inches(0.8))

                                document.save(f"Invoices//{invno}.docx")
                            while True:
                                if os.path.exists(f"Invoices//{invno}.docx"):
                                    break
                            file = f"Invoices\\{invno}.docx"
                            os.startfile(file,'print')
                            break
                            # break        
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
                        if new_item_stock >= 0 and new_item_stock < 1000:
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
                        print("which Product you want to Edit?")
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
                            print("Which you want to Edit?\n1. Item Name\n2. MRP/Unit\n3. Both")
                            d = input("Enter your Choice : ")
                            if d == "1" or d == "2" or d == "3":
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
                                        discard = 1
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
                        elif d == "2":
                            while True:
                                new_price = input("Enter MRP/Unit = ")
                                if new_price.isnumeric():
                                    new_price = int(new_price)
                                    if new_price > 0 and new_price < 10000:
                                        break
                                    else:
                                        print("Invalid Input! Try Again")
                                else:
                                    print("Invalid Input! Try Again")
                                    pass
                            print(f"_ _ _ Preview _ _ _\nItem Name = {old_name}\n Item MRP/Unit = {new_price}")
                            while True:
                                e = input("Do you want to save It? (1 = Yes & 0 = No): ")
                                if e == "1" or e == "0":
                                    if e == "1":
                                        f = open(f"Items\\{item_code}.txt", "w")
                                        f.write(f"{old_name}\n{new_price}\n{old_stock}")
                                        f.close()
                                        print("Item Updated Successfully")
                                        discard = 1
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
                        elif d == "3":
                            while True:
                                new_name = input("Enter New Name : ")
                                if len(new_name) < 20:
                                    break
                                else:
                                    print("Invalid Input! Try Again")
                            while True:
                                new_price = input("Enter MRP/Unit = ")
                                if new_price.isnumeric():
                                    new_price = int(new_price)
                                    if new_price > 0 and new_price < 10000:
                                        break
                                    else:
                                        print("Invalid Input! Try Again")
                                else:
                                    print("Invalid Input! Try Again")
                                    pass
                            print(f"_ _ _ Preview _ _ _\nItem Name = {new_name}\n Item MRP/Unit = {new_price}")
                            while True:
                                e = input("Do you want to save It? (1 = Yes & 0 = No): ")
                                if e == "1" or e == "0":
                                    if e == "1":
                                        f = open(f"Items\\{item_code}.txt", "w")
                                        f.write(f"{new_name}\n{new_price}\n{old_stock}")
                                        f.close()
                                        print("Item Updated Successfully")
                                        discard = 1
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
                 
            
            
                    
        

    