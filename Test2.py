from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# create a new document
document = Document("abcd.docx")

# add a heading
# document.add_heading('My Image')

# add an image
paragraph = document.add_paragraph()
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = paragraph.add_run()
run.add_picture('upi.png', width=Inches(0.3), height=Inches(0.3), )

# save the document
document.save('my_doc.docx')