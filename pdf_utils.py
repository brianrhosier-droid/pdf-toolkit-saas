import os
import io
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import tempfile


class PDFProcessor:
    """Handles all PDF processing operations"""

    @staticmethod
    def merge_pdfs(pdf_files):
        """
        Merge multiple PDF files into one
        Args:
            pdf_files: List of file objects or file paths
        Returns:
            BytesIO object containing merged PDF
        """
        merger = PdfMerger()

        try:
            for pdf_file in pdf_files:
                if hasattr(pdf_file, 'read'):
                    # It's a file object
                    merger.append(pdf_file)
                else:
                    # It's a file path
                    merger.append(pdf_file)

            output = io.BytesIO()
            merger.write(output)
            output.seek(0)
            merger.close()
            return output

        except Exception as e:
            merger.close()
            raise Exception(f"Error merging PDFs: {str(e)}")

    @staticmethod
    def split_pdf(pdf_file, page_ranges=None):
        """
        Split PDF into separate files
        Args:
            pdf_file: PDF file object or path
            page_ranges: List of tuples (start, end) for page ranges, or None for all pages
        Returns:
            List of BytesIO objects containing split PDFs
        """
        try:
            reader = PdfReader(pdf_file)
            total_pages = len(reader.pages)
            outputs = []

            if page_ranges is None:
                # Split each page into separate PDF
                for page_num in range(total_pages):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[page_num])

                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    outputs.append(output)
            else:
                # Split by page ranges
                for start, end in page_ranges:
                    writer = PdfWriter()
                    for page_num in range(start - 1, min(end, total_pages)):
                        writer.add_page(reader.pages[page_num])

                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    outputs.append(output)

            return outputs

        except Exception as e:
            raise Exception(f"Error splitting PDF: {str(e)}")

    @staticmethod
    def compress_pdf(pdf_file, quality='medium'):
        """
        Compress PDF by reducing image quality and removing unnecessary data
        Args:
            pdf_file: PDF file object or path
            quality: 'low', 'medium', or 'high'
        Returns:
            BytesIO object containing compressed PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            for page in reader.pages:
                # Compress content streams
                page.compress_content_streams()
                writer.add_page(page)

            # Remove duplicate objects
            writer.add_metadata(reader.metadata)

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)

            return output

        except Exception as e:
            raise Exception(f"Error compressing PDF: {str(e)}")

    @staticmethod
    def image_to_pdf(image_files):
        """
        Convert images to PDF
        Args:
            image_files: List of image file objects
        Returns:
            BytesIO object containing PDF
        """
        try:
            output = io.BytesIO()
            c = canvas.Canvas(output, pagesize=letter)
            width, height = letter

            for img_file in image_files:
                # Open image
                img = Image.open(img_file)

                # Calculate dimensions to fit page while maintaining aspect ratio
                img_width, img_height = img.size
                aspect = img_height / float(img_width)

                if img_width > width or img_height > height:
                    if aspect > 1:
                        # Portrait
                        new_height = height - 40
                        new_width = new_height / aspect
                    else:
                        # Landscape
                        new_width = width - 40
                        new_height = new_width * aspect
                else:
                    new_width = img_width
                    new_height = img_height

                # Center image
                x = (width - new_width) / 2
                y = (height - new_height) / 2

                # Save image to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    img.save(tmp.name, 'PNG')
                    c.drawImage(tmp.name, x, y, width=new_width, height=new_height)
                    os.unlink(tmp.name)

                c.showPage()

            c.save()
            output.seek(0)
            return output

        except Exception as e:
            raise Exception(f"Error converting images to PDF: {str(e)}")

    @staticmethod
    def extract_pages(pdf_file, page_numbers):
        """
        Extract specific pages from PDF
        Args:
            pdf_file: PDF file object or path
            page_numbers: List of page numbers (1-indexed)
        Returns:
            BytesIO object containing PDF with extracted pages
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            for page_num in page_numbers:
                if 1 <= page_num <= len(reader.pages):
                    writer.add_page(reader.pages[page_num - 1])

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output

        except Exception as e:
            raise Exception(f"Error extracting pages: {str(e)}")

    @staticmethod
    def rotate_pdf(pdf_file, rotation=90):
        """
        Rotate all pages in PDF
        Args:
            pdf_file: PDF file object or path
            rotation: Rotation angle (90, 180, 270)
        Returns:
            BytesIO object containing rotated PDF
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            for page in reader.pages:
                page.rotate(rotation)
                writer.add_page(page)

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output

        except Exception as e:
            raise Exception(f"Error rotating PDF: {str(e)}")

    @staticmethod
    def get_pdf_info(pdf_file):
        """
        Get information about a PDF file
        Args:
            pdf_file: PDF file object or path
        Returns:
            Dictionary with PDF information
        """
        try:
            reader = PdfReader(pdf_file)
            info = {
                'pages': len(reader.pages),
                'metadata': reader.metadata,
                'encrypted': reader.is_encrypted
            }
            return info

        except Exception as e:
            raise Exception(f"Error reading PDF info: {str(e)}")
