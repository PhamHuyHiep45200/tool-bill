import fitz  # PyMuDPDF
myfont = "myfont.otf"

doc = fitz.open("input.pdf")
page = doc[pno]  # load page with number pno (0-based)
page.insert_font(fontname="F0", fontfile=myfont)

# now start inserting text on the page. Use insertion point (100,100) at first
page.insert_text((100,100), "Hello world", fontname="F0", fontsize=14, ...)

# some text in a box
rect = fitz.Rect(100, 120, 300, 200)  # a rectangle
page.insert_textbox(rect, "this is text in a rectangle with auto line breaks",
    fontname="F0", ...)
# etc.

# Before saving, optionally build a subset of myfont:
doc.subset_fonts()
doc.save("output.pdf", garbage=4, deflate=True)