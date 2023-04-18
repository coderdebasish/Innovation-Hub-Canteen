import datetime

# get the current date and time
now = datetime.datetime.now()

# store the current date and time in a variable
current_datetime = now.strftime("%d-%m-%Y %H:%M:%S")

# print the current date and time
print("Current Date and Time:", current_datetime)