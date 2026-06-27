---
name: pdf
description: "MCM/ICM PDF Processing & Submission Handler. Use when the team needs to: (1) Extract text, equations, or tables from academic papers (PDFs) during literature review, (2) Merge the final submission PDF with the Code Appendix, (3) Validate submission compliance (page limits, formatting). Optimized for MCM/ICM workflow with literature research and final submission assembly."
---

# MCM/ICM PDF Processing Specialist

## Overview

You are the PDF Handler for an MCM/ICM team. Your dual mission:
1. **Literature Review Support** (Hours 0-48): Extract information from academic papers to inform model building
2. **Submission Assembly** (Hours 90-96): Merge final paper with code appendix and validate compliance

**Critical Understanding**: MCM/ICM has strict submission rules. A technically correct solution can be disqualified for formatting violations (e.g., exceeding 25 pages, missing control sheet). This skill ensures compliance.

## Core Capabilities

### Capability 1: Literature Review Support

**Scenario**: Team finds a relevant paper on epidemic modeling. Need to extract key equations, parameter values, or data tables quickly.

#### 1.1: Text Extraction from PDFs

**Use Cases**:
- Extract equations from methodology sections
- Copy parameter values with citations
- Pull data tables for comparison

**Tech Stack**: `pypdf` (basic), `pdfplumber` (advanced), `PyMuPDF` (fitz) for complex layouts.

**Quick Extraction (pypdf)**:
```python
import pypdf

# Extract all text from PDF
def extract_text_basic(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Usage
text = extract_text_basic('reference_paper.pdf')
print(text[:500])  # Preview first 500 chars
```

**Advanced Extraction (pdfplumber)**:
```python
import pdfplumber

# Extract text with better formatting preservation
def extract_text_advanced(pdf_path, page_range=None):
    """
    Extract text from PDF with layout preservation.
    
    Args:
        pdf_path: Path to PDF file
        page_range: Tuple (start, end) or None for all pages (0-indexed)
    """
    with pdfplumber.open(pdf_path) as pdf:
        if page_range:
            pages = pdf.pages[page_range[0]:page_range[1]]
        else:
            pages = pdf.pages
        
        text = ""
        for page in pages:
            text += page.extract_text() + "\n\n"
    return text

# Extract specific pages (e.g., methodology section)
methodology_text = extract_text_advanced('paper.pdf', page_range=(5, 10))
```

#### 1.2: Table Extraction from PDFs

**Scenario**: Paper contains a table of parameter values or experimental results.

**pdfplumber Table Extraction**:
```python
import pdfplumber
import pandas as pd

def extract_tables(pdf_path, page_numbers=None):
    """
    Extract tables from PDF pages.
    
    Args:
        pdf_path: Path to PDF file
        page_numbers: List of page numbers (0-indexed) or None for all
    
    Returns:
        List of pandas DataFrames
    """
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        pages = [pdf.pages[i] for i in page_numbers] if page_numbers else pdf.pages
        
        for i, page in enumerate(pages):
            page_tables = page.extract_tables()
            for table in page_tables:
                # Convert to DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append({
                    'page': page_numbers[i] if page_numbers else i,
                    'data': df
                })
    return tables

# Usage
tables = extract_tables('data_paper.pdf', page_numbers=[3, 4, 5])
for i, table in enumerate(tables):
    print(f"Table {i+1} from page {table['page']}:")
    print(table['data'])
    table['data'].to_csv(f'extracted_table_{i+1}.csv', index=False)
```

**Handling Poorly Formatted Tables**:
```python
# If automatic extraction fails, use OCR-like approach
import pdfplumber

def extract_table_manual(pdf_path, page_num, table_bbox):
    """
    Extract table from specific bounding box.
    
    Args:
        pdf_path: Path to PDF
        page_num: Page number (0-indexed)
        table_bbox: Tuple (x0, y0, x1, y1) defining table area
    """
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        # Crop to table area
        table_crop = page.crop(table_bbox)
        table = table_crop.extract_table()
        return pd.DataFrame(table[1:], columns=table[0])

# Find bbox by trial: print(page.bbox) to see page dimensions
# Then visually estimate table location
table_df = extract_table_manual('paper.pdf', page_num=5, 
                                 table_bbox=(50, 200, 550, 400))
```

#### 1.3: Equation Extraction

**Challenge**: PDFs store equations as images or complex text. Extraction is imperfect.

**Strategy 1: Text-based (for simple equations)**:
```python
import re

def find_equations(text):
    """
    Find potential equations in extracted text.
    Looks for patterns like: x = ..., f(x) = ..., etc.
    """
    # Pattern: variable = expression
    pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+?)(?:\n|$)'
    equations = re.findall(pattern, text)
    return [(var, expr.strip()) for var, expr in equations]

# Usage
text = extract_text_advanced('model_paper.pdf', page_range=(3, 6))
equations = find_equations(text)
for var, expr in equations:
    print(f"{var} = {expr}")
```

**Strategy 2: Screenshot + Manual LaTeX (recommended for complex equations)**:
```python
# For complex equations, extract as images
import fitz  # PyMuPDF

def extract_equation_images(pdf_path, page_num, bbox_list):
    """
    Extract specific regions as images (for equations).
    
    Args:
        pdf_path: Path to PDF
        page_num: Page number (0-indexed)
        bbox_list: List of (x0, y0, x1, y1) tuples for each equation
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    
    for i, bbox in enumerate(bbox_list):
        rect = fitz.Rect(bbox)
        pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2, 2))  # 2x zoom
        pix.save(f'equation_{i+1}.png')
    
    doc.close()

# Then manually transcribe to LaTeX (fastest for accuracy)
```

---

### Capability 2: Submission Assembly (The 24-Hour Rule)

**MCM/ICM Submission Requirements**:
- **Main Paper**: Up to 25 pages (including figures, tables, references)
- **Code Appendix**: Unlimited pages (optional but recommended)
- **Control Sheet**: 1 page (team info, problem choice)
- **Final PDF**: `Control Sheet + Main Paper + Code Appendix` merged into one file

**Deadline**: Submissions close at a strict time. Late = disqualified.

#### 2.1: PDF Merging

**Scenario**: You have three PDFs to merge:
1. `control_sheet.pdf` (1 page, provided by COMAP)
2. `main_paper.pdf` (20 pages)
3. `code_appendix.pdf` (15 pages)

**pypdf Merging**:
```python
import pypdf

def merge_pdfs(output_path, input_paths):
    """
    Merge multiple PDFs into one.
    
    Args:
        output_path: Path for merged PDF
        input_paths: List of PDF paths in order
    """
    merger = pypdf.PdfMerger()
    
    for pdf_path in input_paths:
        merger.append(pdf_path)
    
    merger.write(output_path)
    merger.close()
    print(f"✓ Merged {len(input_paths)} PDFs → {output_path}")

# Usage
merge_pdfs('final_submission.pdf', [
    'control_sheet.pdf',
    'main_paper.pdf',
    'code_appendix.pdf'
])
```

**Advanced: Add Blank Page Between Sections** (for clarity):
```python
import pypdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def create_separator_page(text):
    """Create a blank page with centered text."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 24)
    can.drawCentredString(300, 400, text)
    can.save()
    packet.seek(0)
    return pypdf.PdfReader(packet)

def merge_with_separators(output_path, sections):
    """
    Merge PDFs with separator pages.
    
    Args:
        output_path: Output file path
        sections: List of tuples (pdf_path, separator_text or None)
    """
    merger = pypdf.PdfMerger()
    
    for pdf_path, separator_text in sections:
        if separator_text:
            separator = create_separator_page(separator_text)
            merger.append(separator)
        merger.append(pdf_path)
    
    merger.write(output_path)
    merger.close()

# Usage
merge_with_separators('final_submission.pdf', [
    ('control_sheet.pdf', None),
    ('main_paper.pdf', None),
    (None, "Code Appendix"),  # Separator page
    ('code_appendix.pdf', None)
])
```

#### 2.2: Submission Validation

**Critical Checks** (automate to avoid human error):

**Check 1: Page Count**:
```python
import pypdf

def validate_page_count(pdf_path, max_pages=25, exclude_first=1, exclude_last=None):
    """
    Validate that main paper doesn't exceed page limit.
    
    Args:
        pdf_path: Path to merged PDF
        max_pages: Maximum allowed pages (25 for MCM)
        exclude_first: Number of pages to exclude from count (control sheet)
        exclude_last: Number of pages to exclude from end (code appendix)
    """
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        total_pages = len(reader.pages)
        
        # Calculate main paper pages
        main_pages = total_pages - exclude_first
        if exclude_last:
            main_pages -= exclude_last
        
        print(f"Total pages: {total_pages}")
        print(f"Main paper pages: {main_pages} (limit: {max_pages})")
        
        if main_pages > max_pages:
            print(f"⚠ ERROR: Exceeds page limit by {main_pages - max_pages} pages!")
            return False
        else:
            print("✓ Page count valid")
            return True

# Usage
validate_page_count('final_submission.pdf', max_pages=25, exclude_first=1)
```

**Check 2: Font Size Legibility**:
```python
import fitz  # PyMuPDF

def check_font_sizes(pdf_path, min_font_size=10):
    """
    Check for text smaller than minimum readable size.
    
    Args:
        pdf_path: Path to PDF
        min_font_size: Minimum font size in points (MCM recommends ≥10pt)
    """
    doc = fitz.open(pdf_path)
    violations = []
    
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_size = span["size"]
                        if font_size < min_font_size:
                            violations.append({
                                'page': page_num + 1,
                                'font_size': round(font_size, 1),
                                'text': span["text"][:50]
                            })
    
    doc.close()
    
    if violations:
        print(f"⚠ Found {len(violations)} text blocks below {min_font_size}pt:")
        for v in violations[:10]:  # Show first 10
            print(f"  Page {v['page']}: {v['font_size']}pt - '{v['text']}'")
        return False
    else:
        print(f"✓ All text ≥ {min_font_size}pt")
        return True

# Usage
check_font_sizes('final_submission.pdf', min_font_size=10)
```

**Check 3: Control Sheet Presence**:
```python
import pypdf

def validate_control_sheet(pdf_path):
    """
    Check if first page contains control sheet identifiers.
    """
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        first_page_text = reader.pages[0].extract_text()
        
        # Control sheet should contain these keywords
        required_keywords = ['Control Number', 'Problem Chosen', 'Team']
        found = [kw for kw in required_keywords if kw in first_page_text]
        
        if len(found) == len(required_keywords):
            print("✓ Control sheet detected on first page")
            return True
        else:
            print(f"⚠ Control sheet missing or incomplete (found: {found})")
            return False

# Usage
validate_control_sheet('final_submission.pdf')
```

**Comprehensive Validation**:
```python
def validate_submission(pdf_path):
    """
    Run all validation checks.
    """
    print("="*50)
    print("MCM/ICM Submission Validation")
    print("="*50)
    
    checks = [
        ("Control Sheet", validate_control_sheet(pdf_path)),
        ("Page Count", validate_page_count(pdf_path, max_pages=25, exclude_first=1)),
        ("Font Sizes", check_font_sizes(pdf_path, min_font_size=10))
    ]
    
    print("\n" + "="*50)
    print("Validation Summary:")
    for check_name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {check_name}: {status}")
    
    all_passed = all(passed for _, passed in checks)
    print("="*50)
    if all_passed:
        print("✓✓✓ SUBMISSION READY ✓✓✓")
    else:
        print("⚠⚠⚠ FIX ERRORS BEFORE SUBMITTING ⚠⚠⚠")
    return all_passed

# Usage
validate_submission('final_submission.pdf')
```

---

## MCM-Specific Workflows

### Workflow 1: Literature Review (Hours 0-24)

**Scenario**: Found 5 relevant papers, need to extract key information quickly.

**Process**:
```python
import os

def batch_extract_literature(pdf_folder, output_folder):
    """
    Extract text from all PDFs in a folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            text = extract_text_advanced(pdf_path)
            
            # Save as text file
            txt_path = os.path.join(output_folder, filename.replace('.pdf', '.txt'))
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✓ Extracted: {filename}")

# Usage
batch_extract_literature('references/', 'extracted_texts/')
```

**Then search extracted texts**:
```python
import os

def search_in_texts(folder, keyword):
    """
    Search for keyword in all extracted text files.
    """
    results = []
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                if keyword.lower() in text.lower():
                    # Find context (50 chars before and after)
                    idx = text.lower().find(keyword.lower())
                    context = text[max(0, idx-50):idx+len(keyword)+50]
                    results.append({
                        'file': filename,
                        'context': context
                    })
    return results

# Search for parameter values
results = search_in_texts('extracted_texts/', 'transmission rate')
for r in results:
    print(f"{r['file']}: ...{r['context']}...")
```

---

### Workflow 2: Code Appendix Generation (Hours 84-90)

**Scenario**: Need to create a well-formatted code appendix PDF from Python/MATLAB scripts.

**Strategy 1: Use Jupyter Notebook** (recommended):
```bash
# Convert notebook to PDF with code highlighting
jupyter nbconvert --to pdf analysis.ipynb --output code_appendix.pdf
```

**Strategy 2: LaTeX Listings** (for plain scripts):
```latex
\documentclass{article}
\usepackage{listings}
\usepackage{xcolor}

\lstset{
    language=Python,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue},
    commentstyle=\color{gray},
    stringstyle=\color{red},
    numbers=left,
    numberstyle=\tiny,
    frame=single,
    breaklines=true
}

\begin{document}

\section*{Code Appendix}

\subsection*{Data Preprocessing (data\_cleaner.py)}
\lstinputlisting{../code/data_cleaner.py}

\subsection*{TOPSIS Model (topsis.py)}
\lstinputlisting{../code/topsis.py}

\end{document}
```

**Strategy 3: Python Script to PDF** (automated):
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_code_appendix(code_folder, output_pdf):
    """
    Create a PDF appendix from all code files in a folder.
    """
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    story.append(Paragraph("Code Appendix", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Add each code file
    for filename in sorted(os.listdir(code_folder)):
        if filename.endswith(('.py', '.m', '.r')):
            story.append(Paragraph(f"File: {filename}", styles['Heading2']))
            
            with open(os.path.join(code_folder, filename), 'r') as f:
                code = f.read()
            
            # Use Preformatted for code (monospace)
            story.append(Preformatted(code, styles['Code']))
            story.append(Spacer(1, 12))
    
    doc.build(story)
    print(f"✓ Code appendix created: {output_pdf}")

# Usage
create_code_appendix('code/', 'code_appendix.pdf')
```

---

### Workflow 3: Final Submission Assembly (Hours 92-96)

**Checklist-Driven Process**:
```python
def final_submission_workflow():
    """
    Step-by-step submission assembly with validation.
    """
    print("MCM/ICM Final Submission Workflow")
    print("="*50)
    
    # Step 1: Check all files exist
    required_files = ['control_sheet.pdf', 'main_paper.pdf', 'code_appendix.pdf']
    for file in required_files:
        if not os.path.exists(file):
            print(f"✗ Missing: {file}")
            return
    print("✓ All required files present")
    
    # Step 2: Merge PDFs
    print("\nMerging PDFs...")
    merge_pdfs('final_submission.pdf', required_files)
    
    # Step 3: Validate
    print("\nRunning validation checks...")
    if validate_submission('final_submission.pdf'):
        print("\n✓✓✓ READY TO SUBMIT ✓✓✓")
        print(f"File: final_submission.pdf")
        print(f"Size: {os.path.getsize('final_submission.pdf') / 1024:.1f} KB")
    else:
        print("\n⚠ VALIDATION FAILED - FIX ERRORS")

# Run final workflow
final_submission_workflow()
```

---

## Best Practices for MCM/ICM

### Time Management

**Literature Review Phase** (Hours 0-24):
- Batch extract all PDFs at once (30 min)
- Search extracted texts for keywords (faster than reading)
- Screenshot complex equations (faster than transcribing)

**Submission Phase** (Hours 90-96):
- Start assembling at Hour 90 (don't wait until Hour 95!)
- Validate early and often
- Keep backup copies of all PDFs

### Common Pitfalls

**Pitfall 1: Exceeding Page Limit**
- **Problem**: Main paper is 27 pages, but limit is 25.
- **Fix**: Remove less critical figures, tighten prose, or move details to appendix.

**Pitfall 2: Corrupted PDF Merge**
- **Problem**: Merged PDF won't open or displays incorrectly.
- **Fix**: Validate individual PDFs before merging. Re-export from LaTeX if needed.

**Pitfall 3: Missing Control Sheet**
- **Problem**: Forgot to include control sheet as first page.
- **Fix**: Always merge in order: Control Sheet → Main Paper → Code Appendix.

**Pitfall 4: Unreadable Code Appendix**
- **Problem**: Code printed in 6pt font, illegible.
- **Fix**: Use 10-12pt monospace font, syntax highlighting, line breaks.

---

## Integration with Other Skills

**Before pdf**:
- Use `latex-coauthoring` to generate `main_paper.pdf`
- Use `xlsx`, `topsis-scorer`, etc. to generate code for appendix

**After pdf**:
- No downstream skills (pdf is final output)

**Parallel with pdf**:
- Literature review (pdf extraction) happens early (Hours 0-24)
- Submission assembly (pdf merging) happens late (Hours 90-96)

---

## Output Standards

### File Naming Convention
```
submission/
├── control_sheet.pdf          # Provided by COMAP
├── main_paper.pdf             # From LaTeX compilation
├── code_appendix.pdf          # Generated from code files
├── final_submission.pdf       # Merged final PDF
└── validation_report.txt      # Validation results
```

### Validation Report Template
```python
def save_validation_report(pdf_path, output_txt):
    """
    Save validation results to text file.
    """
    with open(output_txt, 'w') as f:
        f.write("MCM/ICM Submission Validation Report\n")
        f.write("="*50 + "\n")
        f.write(f"File: {pdf_path}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Run checks and write results
        checks = {
            'Control Sheet': validate_control_sheet(pdf_path),
            'Page Count': validate_page_count(pdf_path, max_pages=25, exclude_first=1),
            'Font Sizes': check_font_sizes(pdf_path, min_font_size=10)
        }
        
        for check_name, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            f.write(f"{check_name}: {status}\n")
        
        f.write("\n" + "="*50 + "\n")
        if all(checks.values()):
            f.write("STATUS: READY FOR SUBMISSION\n")
        else:
            f.write("STATUS: ERRORS DETECTED - DO NOT SUBMIT\n")
    
    print(f"✓ Validation report saved: {output_txt}")

# Usage
save_validation_report('final_submission.pdf', 'validation_report.txt')
```

---

## Quick Reference: PDF Operations

| Task | Library | Function |
|------|---------|----------|
| Extract text (basic) | pypdf | `PdfReader.pages[i].extract_text()` |
| Extract text (advanced) | pdfplumber | `pdfplumber.open().pages[i].extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Extract images | PyMuPDF (fitz) | `page.get_pixmap()` |
| Merge PDFs | pypdf | `PdfMerger.append()` |
| Split PDFs | pypdf | `PdfWriter.add_page()` |
| Add watermark | pypdf | `PageObject.merge_page()` |
| Rotate pages | pypdf | `PageObject.rotate()` |
| Get metadata | pypdf | `PdfReader.metadata` |
| Count pages | pypdf | `len(PdfReader.pages)` |

---

## Advanced Techniques

### OCR for Scanned PDFs

**Scenario**: PDF is a scanned image (no selectable text).

**Solution**: Use `pytesseract` with `pdf2image`:
```python
from pdf2image import convert_from_path
import pytesseract

def ocr_pdf(pdf_path):
    """
    Extract text from scanned PDF using OCR.
    """
    images = convert_from_path(pdf_path)
    text = ""
    for i, image in enumerate(images):
        page_text = pytesseract.image_to_string(image)
        text += f"\n--- Page {i+1} ---\n{page_text}"
    return text

# Usage (requires Tesseract installed)
text = ocr_pdf('scanned_paper.pdf')
```

### Password-Protected PDFs

**Scenario**: Reference paper is password-protected.

**Solution**:
```python
import pypdf

def unlock_pdf(pdf_path, password, output_path):
    """
    Decrypt password-protected PDF.
    """
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        
        if reader.is_encrypted:
            reader.decrypt(password)
        
        writer = pypdf.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
    
    print(f"✓ Unlocked PDF saved: {output_path}")

# Usage
unlock_pdf('protected.pdf', 'password123', 'unlocked.pdf')
```

---

## Final Reminder: The Submission Deadline is Absolute

**Competition Reality**:
- COMAP submission portal closes at the exact deadline (e.g., 8:00 PM EST)
- No extensions, no exceptions
- A 1-minute delay = disqualification

**Strategy**:
1. **Hour 90**: Generate code appendix PDF
2. **Hour 91**: Merge all PDFs
3. **Hour 92**: Run validation
4. **Hour 93-94**: Fix any validation errors
5. **Hour 95**: Upload to COMAP portal (leave 1 hour buffer!)
6. **Hour 96**: Backup submission (email to yourself, save to cloud)

**The Golden Rule**: Submit at Hour 95, not Hour 96. Network issues, slow uploads, and portal crashes are common. The buffer saves teams every year.
