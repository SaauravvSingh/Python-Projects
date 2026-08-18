from pypdf import PdfReader, PdfWriter

reader = PdfReader("Saurav_Singh_TCS_Certificate.pdf")

writer = PdfWriter()
writer.append(reader)

writer.encrypt("54321")

with open("protected.pdf", "wb") as file:
    writer.write(file)

print("PDF password protected successfully!")