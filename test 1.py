import os

fileCounter = 0
for root, dirs, files in os.walk("Invoices//"):
    for file in files:    
        if file.endswith('.docx'):
            fileCounter += 1
print(fileCounter)