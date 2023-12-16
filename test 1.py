print("---------------------------------")
print("        Available Products       ")
print("---------------------------------")
print("Code    Item Name   Price/Unit  Stock")
print("-------------------------------------")
length = len(first_line)
first_line = first_line + (17-length)*" "
print(f"{file_name} : {first_line}: {second_line} \t{third_line}")