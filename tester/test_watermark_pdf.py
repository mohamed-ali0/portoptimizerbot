"""
Test script to add watermark to an existing PDF file
Usage: python test_watermark_pdf.py <input_pdf_path> [output_pdf_path] [watermark_text] [use_pdf_name]
"""
import os
import sys
from datetime import datetime

# Add parent directory to path to import app functions
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib.colors import gray
    from reportlab.lib.units import inch
    PDF_LIBRARIES_AVAILABLE = True
except ImportError:
    PDF_LIBRARIES_AVAILABLE = False
    print("ERROR: PyPDF2 or reportlab not available.")
    print("Install with: pip install PyPDF2 reportlab")
    sys.exit(1)


def add_watermark_to_pdf(pdf_path, output_path=None, watermark_text=None, use_pdf_name=False):
    """
    Add watermark to PDF file
    pdf_path: Path to input PDF file
    output_path: Path to output PDF file (if None, adds '_watermarked' to input filename)
    watermark_text: Custom watermark text (optional)
    use_pdf_name: If True, use PDF filename (date) as the main watermark text
    """
    if not PDF_LIBRARIES_AVAILABLE:
        print("ERROR: PDF libraries not available")
        return False
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        return False
    
    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_path = f"{base_name}_watermarked.pdf"
    
    try:
        print("=" * 60)
        print("PDF WATERMARK TEST")
        print("=" * 60)
        print(f"Input PDF: {pdf_path}")
        print(f"Output PDF: {output_path}")
        
        # Create watermark text
        watermark_lines = []
        
        # If use_pdf_name is True, use the full PDF filename (without extension) as watermark
        if use_pdf_name:
            pdf_filename = os.path.basename(pdf_path)
            # Remove .pdf extension to get the full name (e.g., POLA_Empty_Returns_2025-11-02_23-23-10)
            filename_without_ext = os.path.splitext(pdf_filename)[0]
            watermark_lines.append(filename_without_ext)
            print(f"Using full PDF filename as watermark: {filename_without_ext}")
        
        # Add custom text if provided (but no timestamp when use_pdf_name is True)
        if watermark_text:
            watermark_lines.append(watermark_text)
            print(f"Adding custom watermark text: {watermark_text}")
        elif not use_pdf_name:
            # Only add timestamp if not using PDF name
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            watermark_lines.append(f"Generated: {timestamp}")
        
        watermark_text_final = "\n".join(watermark_lines)
        print(f"Final watermark text (ONLY DATE): {watermark_text_final}")
        print()
        
        # Read the original PDF
        print("Reading PDF file...")
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        num_pages = len(reader.pages)
        print(f"PDF has {num_pages} page(s)")
        
        # Get page dimensions from first page
        first_page = reader.pages[0]
        page_width = float(first_page.mediabox.width)
        page_height = float(first_page.mediabox.height)
        
        print(f"Page dimensions: {page_width:.2f} x {page_height:.2f} points")
        
        # Create watermark overlay
        print("Creating watermark overlay...")
        watermark_path = output_path.replace('.pdf', '_temp_watermark.pdf')
        c = canvas.Canvas(watermark_path, pagesize=(page_width, page_height))
        
        # Set watermark properties (light gray, rotated, semi-transparent)
        # Increase font size by 80%: 24 * 1.8 = 43.2, round to 43
        font_size = int(24 * 1.8)  # 43
        c.setFillColor(gray, alpha=0.3)  # 30% opacity
        c.setFont("Helvetica-Bold", font_size)
        
        print(f"Font size: {font_size} (80% increase from 24)")
        print(f"Watermark text: {watermark_text_final}")
        print(f"Position: Horizontal, top of page, 2 pixels from top")
        
        # Position at top of page, 2 pixels from top (horizontal, not rotated)
        # PDF coordinates: origin (0,0) is at bottom-left, top is at page_height
        # 2 pixels = 2 points (ReportLab uses points as units)
        top_offset = 2  # 2 pixels from top
        
        # Split text into lines for multiline support
        watermark_lines_list = watermark_text_final.split('\n')
        line_height = font_size * 1.2  # Line spacing (120% of font size)
        
        # Draw each line of watermark text (horizontal, top-aligned)
        # Position: 2 pixels from top, centered horizontally
        for i, line in enumerate(watermark_lines_list):
            if line.strip():  # Only draw non-empty lines
                text_width = c.stringWidth(line, "Helvetica-Bold", font_size)
                # X position: centered horizontally
                x_pos = (page_width - text_width) / 2
                # Y position: top of page minus 2 pixels, then down for each line
                # drawString uses baseline, so subtract font_size to position top of text at offset
                y_pos = page_height - top_offset - font_size - (i * line_height)
                c.drawString(x_pos, y_pos, line)
                print(f"  Drawing line {i+1}: '{line}' at ({x_pos:.1f}, {y_pos:.1f})")
        
        c.save()
        
        # Read watermark PDF
        watermark_reader = PdfReader(watermark_path)
        watermark_page = watermark_reader.pages[0]
        
        # Overlay watermark on all pages
        print(f"Applying watermark to {num_pages} page(s)...")
        for i, page in enumerate(reader.pages, 1):
            # Merge watermark with page
            page.merge_page(watermark_page)
            writer.add_page(page)
            if i % 10 == 0:
                print(f"  Processed {i}/{num_pages} pages...")
        
        # Write watermarked PDF
        print(f"Writing watermarked PDF to: {output_path}")
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Clean up temporary watermark file
        if os.path.exists(watermark_path):
            os.remove(watermark_path)
        
        # Verify output file
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"\nSUCCESS: Watermarked PDF created!")
            print(f"Output file: {output_path}")
            print(f"File size: {file_size:,} bytes")
            return True
        else:
            print("ERROR: Output file was not created")
            return False
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python test_watermark_pdf.py <input_pdf_path> [output_pdf_path] [watermark_text] [use_pdf_name]")
        print("\nExamples:")
        print("  python test_watermark_pdf.py downloads/pdfs/2025-10-26_12-00-00.pdf")
        print("  python test_watermark_pdf.py test.pdf output.pdf")
        print("  python test_watermark_pdf.py test.pdf output.pdf \"CONFIDENTIAL\"")
        print("  python test_watermark_pdf.py test.pdf output.pdf None true")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    watermark_text = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3].lower() != 'none' else None
    use_pdf_name = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else True  # Default to True
    
    # If output_pdf is None and watermark_text is provided, treat watermark_text as output
    if output_pdf is None and watermark_text and watermark_text.lower() != 'none':
        # Check if it looks like a path (has .pdf extension)
        if watermark_text.endswith('.pdf'):
            output_pdf = watermark_text
            watermark_text = None
    
    success = add_watermark_to_pdf(input_pdf, output_pdf, watermark_text, use_pdf_name)
    
    if success:
        print("\n" + "=" * 60)
        print("TEST COMPLETED SUCCESSFULLY")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("TEST FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()

