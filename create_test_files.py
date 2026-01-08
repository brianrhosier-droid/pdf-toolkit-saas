"""Create test PDF files for testing the application"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import os

# Create test_files directory
os.makedirs('test_files', exist_ok=True)

# Create Test PDF 1
print("Creating test PDF 1...")
c = canvas.Canvas('test_files/test1.pdf', pagesize=letter)
c.setFont("Helvetica", 24)
c.drawString(100, 700, "Test PDF File #1")
c.setFont("Helvetica", 12)
c.drawString(100, 650, "This is a test PDF for merge functionality")
c.drawString(100, 630, "Page 1 of Test Document 1")
c.showPage()
c.save()

# Create Test PDF 2
print("Creating test PDF 2...")
c = canvas.Canvas('test_files/test2.pdf', pagesize=letter)
c.setFont("Helvetica", 24)
c.drawString(100, 700, "Test PDF File #2")
c.setFont("Helvetica", 12)
c.drawString(100, 650, "This is another test PDF for merge functionality")
c.drawString(100, 630, "Page 1 of Test Document 2")
c.showPage()
c.save()

# Create Multi-page PDF for splitting
print("Creating multi-page PDF...")
c = canvas.Canvas('test_files/multipage.pdf', pagesize=letter)
for page in range(1, 4):
    c.setFont("Helvetica", 24)
    c.drawString(100, 700, f"Page {page} of 3")
    c.setFont("Helvetica", 12)
    c.drawString(100, 650, "This is a multi-page PDF for testing split functionality")
    c.showPage()
c.save()

# Create a large-ish PDF for compression testing
print("Creating PDF for compression...")
c = canvas.Canvas('test_files/large.pdf', pagesize=letter)
c.setFont("Helvetica", 12)
c.drawString(100, 700, "Large PDF for Compression Testing")
for i in range(50):
    c.drawString(100, 650 - (i * 10), f"Line {i+1}: This is some text content to make the file larger")
c.showPage()
c.save()

# Create test images
print("Creating test images...")
# Red image
img1 = Image.new('RGB', (800, 600), color='red')
img1.save('test_files/image1.jpg')

# Blue image
img2 = Image.new('RGB', (800, 600), color='blue')
img2.save('test_files/image2.jpg')

# Green image
img3 = Image.new('RGB', (600, 800), color='green')
img3.save('test_files/image3.png')

print("\n" + "="*50)
print("✅ Test files created successfully!")
print("="*50)
print("\nFiles created in 'test_files' directory:")
print("  - test1.pdf (for merging)")
print("  - test2.pdf (for merging)")
print("  - multipage.pdf (for splitting)")
print("  - large.pdf (for compression)")
print("  - image1.jpg (for conversion)")
print("  - image2.jpg (for conversion)")
print("  - image3.png (for conversion)")
print("\nYou can now use these files to test the PDF Toolkit!")
print("="*50)
