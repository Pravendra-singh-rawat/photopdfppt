import streamlit as st
import tempfile
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import shutil

# ======================
# Configuration
# ======================
SLIDE_WIDTH = Inches(13.33)  # 16:9 aspect ratio for PPT
SLIDE_HEIGHT = Inches(7.5)
PDF_PAGE_SIZE = A4
TITLE_HEIGHT = Inches(0.8)    # Space for title
GAP_BETWEEN = Inches(0.3)     # Space between title and image
MARGIN = Inches(0.4)          # Page margins

# ======================
# Core Functions
# ======================
def scale_image(img_path, max_width, max_height):
    """Optimized scaling for both orientations with max utilization"""
    with Image.open(img_path) as img:
        width, height = img.size
        aspect = height / width
        
        # Calculate both possible scaling options
        width_based = min(max_width, (max_height - GAP_BETWEEN) / aspect)
        height_based = min(max_height - GAP_BETWEEN, max_width * aspect)
        
        # Choose the option that gives larger area
        if (width_based * (width_based * aspect)) > (height_based * (height_based / aspect)):
            return width_based, width_based * aspect
        else:
            return height_based / aspect, height_based

def create_ppt(photo_paths, output_path):
    """Create PPT with optimized spacing and sizing"""
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    
    for img_path in photo_paths:
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide
        
        # Add title with spacing
        title = os.path.splitext(os.path.basename(img_path))[0]
        textbox = slide.shapes.add_textbox(
            left=Inches(0.5),
            top=Inches(0.3),
            width=SLIDE_WIDTH - Inches(1),
            height=TITLE_HEIGHT
        )
        p = textbox.text_frame.add_paragraph()
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(24)
        p.font.bold = True
        
        # Calculate available space for image
        max_width = SLIDE_WIDTH - (2 * MARGIN)
        max_height = SLIDE_HEIGHT - TITLE_HEIGHT - GAP_BETWEEN
        
        # Scale image
        img_width, img_height = scale_image(img_path, max_width, max_height)
        
        # Center image with gap
        left = (SLIDE_WIDTH - img_width) / 2
        top = TITLE_HEIGHT + GAP_BETWEEN
        
        slide.shapes.add_picture(
            img_path,
            left, top,
            width=img_width,
            height=img_height
        )
    
    prs.save(output_path)

def create_pdf(photo_paths, output_path):
    """Create PDF with A4 sizing and proper gaps"""
    c = canvas.Canvas(output_path, pagesize=PDF_PAGE_SIZE)
    page_width, page_height = PDF_PAGE_SIZE
    title_font_size = 24
    gap_points = GAP_BETWEEN.inches * 72  # Convert inches to points
    
    for img_path in photo_paths:
        c.showPage()  # New page per image
        
        # Add title
        title = os.path.splitext(os.path.basename(img_path))[0]
        c.setFont("Helvetica-Bold", title_font_size)
        title_y = page_height - 50  # 50 points from top
        c.drawCentredString(page_width/2, title_y, title)
        
        # Calculate available space
        max_width = page_width - (MARGIN.inches * 72 * 2)
        max_height = page_height - 70 - gap_points  # Title space + gap
        
        # Scale image
        with Image.open(img_path) as img:
            img_width, img_height = scale_image(img_path, max_width, max_height)
        
        # Center image with gap
        x = (page_width - img_width) / 2
        y = title_y - gap_points - img_height
        
        c.drawImage(img_path, x, y, 
                   width=img_width, 
                   height=img_height,
                   preserveAspectRatio=True)
    
    c.save()

# ======================
# Streamlit UI
# ======================
st.set_page_config(page_title="Professional Photo Converter", layout="wide")
st.title("📸 Smart Photo Converter")
st.write("Upload photos to create perfect presentations with automatic sizing!")

uploaded_files = st.file_uploader(
    "Drag & drop photos (multiple selection)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    photo_paths = []
    
    # Save uploaded files
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        photo_paths.append(file_path)
    
    # Preview images
    st.subheader("Photo Preview")
    cols = st.columns(3)
    for idx, path in enumerate(photo_paths):
        try:
            cols[idx % 3].image(
                path, 
                use_column_width=True,  # Older Streamlit compatibility
                caption=os.path.basename(path))
        except Exception as e:
            st.error(f"Error previewing {os.path.basename(path)}: {str(e)}")
    
    # Output settings
    st.subheader("Output Settings")
    output_name = st.text_input("Base filename:", "MyPresentation")
    output_format = st.radio("Output format:", ["PPTX", "PDF", "Both"])
    
    if st.button("🚀 Generate Files"):
        with st.spinner("Creating professional outputs..."):
            try:
                generated_files = []
                
                if output_format in ["PPTX", "Both"]:
                    ppt_path = os.path.join(temp_dir, f"{output_name}.pptx")
                    create_ppt(photo_paths, ppt_path)
                    generated_files.append(ppt_path)
                
                if output_format in ["PDF", "Both"]:
                    pdf_path = os.path.join(temp_dir, f"{output_name}.pdf")
                    create_pdf(photo_paths, pdf_path)
                    generated_files.append(pdf_path)
                
                # Create download buttons
                if generated_files:
                    st.success("✅ Files created successfully!")
                    for file_path in generated_files:
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label=f"📥 Download {os.path.basename(file_path)}",
                                data=f,
                                file_name=os.path.basename(file_path),
                                mime="application/octet-stream" if "pptx" in file_path 
                                     else "application/pdf"
                            )
                
            except Exception as e:
                # st.error(f"⚠️ Error during generation: {str(e)}")
            finally:
                # Cleanup temp files
                shutil.rmtree(temp_dir, ignore_errors=True)

