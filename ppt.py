
# from pptx import Presentation
# from pptx.util import Inches
# from pptx.enum.text import PP_ALIGN  # Explicit import for alignment
# import os
# from PIL import Image

# # ======================
# # CONFIGURATION
# # ======================
# photo_directory = "C:\Users\Pravendra Singh\Downloads\mpesbaudit1_enrollments_data_2025-02-28 18_56_13.448959 (1)\mpesbaudit1\28 Feb'25\T051__IPS DIGITAL CENTER - 2 IPS ACADEMY INSTITUTE OF ENGINEERING  SCIENCE\photo"         # Folder containing your images
# output_filename = "Centered_Title_Photos.pptx"  # Output file
# title_height = Inches(1)            # Height reserved for title
# slide_margin = Inches(0.5)          # Margin around the slide
# # ======================

# # Create presentation
# prs = Presentation()
# prs.slide_width = Inches(13.33)     # 16:9 aspect ratio (width)
# prs.slide_height = Inches(7.5)      # 16:9 aspect ratio (height)

# for img_file in os.listdir(photo_directory):
#     if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
#         img_path = os.path.join(photo_directory, img_file)
#         slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide

#         # ======================
#         # ADD CENTERED TITLE
#         # ======================
#         title = os.path.splitext(img_file)[0]  # Remove file extension

#         # Calculate textbox width and position to center horizontally
#         textbox_width = prs.slide_width - (2 * slide_margin)
#         textbox_left = (prs.slide_width - textbox_width) / 2  # Center

#         textbox = slide.shapes.add_textbox(
#             left=textbox_left,
#             top=slide_margin,
#             width=textbox_width,
#             height=title_height
#         )
#         text_frame = textbox.text_frame
#         text_frame.vertical_anchor = 3  # Middle vertical alignment (optional)
#         p = text_frame.add_paragraph()
#         p.text = title
#         p.alignment = PP_ALIGN.CENTER  # Use enum for clarity

#         # Customize font
#         p.font.name = "Arial"
#         p.font.size = Inches(0.4)
#         p.font.bold = True

#         # ======================
#         # ADD PHOTO BELOW TITLE
#         # ======================
#         try:
#             with Image.open(img_path) as img:
#                 img_aspect_ratio = img.height / img.width

#             # Available space for photo (below title)
#             max_photo_width = prs.slide_width - (2 * slide_margin)
#             max_photo_height = prs.slide_height - title_height - (2 * slide_margin)

#             # Calculate photo dimensions to fit while preserving aspect ratio
#             photo_width = max_photo_width
#             photo_height = photo_width * img_aspect_ratio

#             # Adjust if height exceeds available space
#             if photo_height > max_photo_height:
#                 photo_height = max_photo_height
#                 photo_width = photo_height / img_aspect_ratio

#             # Center horizontally and position below title
#             photo_left = (prs.slide_width - photo_width) / 2
#             photo_top = title_height + slide_margin

#             slide.shapes.add_picture(
#                 img_path,
#                 left=photo_left,
#                 top=photo_top,
#                 width=photo_width,
#                 height=photo_height
#             )

#             print(f"Added: {img_file}")

#         except Exception as e:
#             print(f"Failed to add {img_file}: {e}")

# # Save the presentation
# prs.save(output_filename)
# print(f"\nPresentation saved as: {output_filename}")










# import streamlit as st
# import zipfile
# import tempfile
# import os
# from pptx import Presentation
# from pptx.util import Inches
# from pptx.enum.text import PP_ALIGN
# from PIL import Image
# import shutil

# st.set_page_config(page_title="Photo to PPT Converter", layout="wide")

# # ======================
# # Functions
# # ======================
# def create_presentation(photo_folder, output_filename):
#     prs = Presentation()
#     prs.slide_width = Inches(13.33)
#     prs.slide_height = Inches(7.5)
    
#     image_files = [f for f in os.listdir(photo_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
#     for img_file in image_files:
#         img_path = os.path.join(photo_folder, img_file)
#         slide = prs.slides.add_slide(prs.slide_layouts[6])
        
#         # Add title
#         title = os.path.splitext(img_file)[0]
#         textbox = slide.shapes.add_textbox(Inches(1), Inches(0.5), prs.slide_width - Inches(2), Inches(1))
#         text_frame = textbox.text_frame
#         p = text_frame.add_paragraph()
#         p.text = title
#         p.alignment = PP_ALIGN.CENTER
#         p.font.name = "Arial"
#         p.font.size = Inches(0.4)
#         p.font.bold = True
        
#         # Add image
#         with Image.open(img_path) as img:
#             aspect_ratio = img.height / img.width
#         max_width = prs.slide_width - Inches(2)
#         max_height = prs.slide_height - Inches(3)
#         width = min(max_width, max_height / aspect_ratio)
#         height = width * aspect_ratio
        
#         slide.shapes.add_picture(
#             img_path,
#             left=(prs.slide_width - width) / 2,
#             top=Inches(2),
#             width=width,
#             height=height
#         )
    
#     prs.save(output_filename)

# # ======================
# # Streamlit UI
# # ======================
# st.title("📷 Photo to PowerPoint Converter")
# st.write("Upload a zip file containing photos to create a PowerPoint presentation!")

# # Step 1: Upload zip file
# uploaded_zip = st.file_uploader("Upload a ZIP file of photos", type=["zip"])

# if uploaded_zip:
#     # Step 2: Extract zip to temp folder
#     temp_dir = tempfile.mkdtemp()
#     zip_path = os.path.join(temp_dir, "uploaded.zip")
    
#     with open(zip_path, "wb") as f:
#         f.write(uploaded_zip.getbuffer())
    
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(temp_dir)
    
#     # Get folder name for output file
#     folder_name = os.path.splitext(uploaded_zip.name)[0]
#     output_ppt = os.path.join(temp_dir, f"{folder_name}.pptx")
    
#     # Step 3: Show photo grid preview
#     st.subheader("Preview of Photos")
#     image_files = [f for f in os.listdir(temp_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
#     if not image_files:
#         st.error("No valid images found in the ZIP file!")
#     else:
#         # Display 3-column grid
#         cols = st.columns(3)
#         for idx, img_file in enumerate(image_files):
#             img_path = os.path.join(temp_dir, img_file)
#             cols[idx % 3].image(img_path, caption=img_file, use_column_width=True)
        
#         # Step 4: Generate and download PPT
#         if st.button("✨ Generate PowerPoint"):
#             with st.spinner("Creating presentation..."):
#                 try:
#                     create_presentation(temp_dir, output_ppt)
#                     st.success("Presentation created!")
                    
#                     # Add download button
#                     with open(output_ppt, "rb") as f:
#                         st.download_button(
#                             label="📥 Download PowerPoint",
#                             data=f,
#                             file_name=f"{folder_name}.pptx",
#                             mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
#                         )
#                 except Exception as e:
#                     st.error(f"Error: {str(e)}")
    
#     # Cleanup temp files
#     shutil.rmtree(temp_dir)

















import streamlit as st
import tempfile
import os
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Photo to Presentation Converter", layout="wide")

# ======================
# Core Functions
# ======================
def scale_image(img_path, max_width, max_height):
    """Calculate dimensions to fit image within bounds while maintaining aspect ratio"""
    with Image.open(img_path) as img:
        width, height = img.size
        aspect = height / width
        
        # Calculate maximum possible dimensions
        scaled_width = min(max_width, max_height / aspect)
        scaled_height = scaled_width * aspect
        
        if scaled_height > max_height:
            scaled_height = max_height
            scaled_width = scaled_height / aspect
            
        return scaled_width, scaled_height

def create_ppt(photo_paths, output_path):
    """Create PowerPoint with properly scaled images"""
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    for img_path in photo_paths:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        filename = os.path.basename(img_path)
        title = os.path.splitext(filename)[0]
        
        # Add title
        textbox = slide.shapes.add_textbox(Inches(1), Inches(0.5), 
                                         prs.slide_width - Inches(2), Inches(1))
        p = textbox.text_frame.add_paragraph()
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Inches(0.4)
        p.font.bold = True
        
        # Calculate image position
        max_width = prs.slide_width - Inches(2)
        max_height = prs.slide_height - Inches(3)
        img_width, img_height = scale_image(img_path, max_width, max_height)
        
        slide.shapes.add_picture(
            img_path,
            left=(prs.slide_width - img_width) / 2,
            top=(prs.slide_height - img_height) / 2 + Inches(1),  # Center below title
            width=img_width,
            height=img_height
        )
    
    prs.save(output_path)

# def create_pdf(photo_paths, output_path):
#     """Create PDF with properly scaled images"""
#     c = canvas.Canvas(output_path, pagesize=letter)
#     page_width, page_height = letter
    
#     for img_path in photo_paths:
#         # Add new page
#         c.showPage()
        
#         # Calculate available space
#         max_width = page_width - 144  # 2-inch margins (72 pts/inch)
#         max_height = page_height - 144
#         title_height = 36  # 0.5 inch
        
#         # Add title
#         filename = os.path.basename(img_path)
#         title = os.path.splitext(filename)[0]
#         c.setFont("Helvetica-Bold", 14)
#         c.drawCentredString(page_width/2, page_height - 72, title)
        
#         # Add image
#         img_width, img_height = scale_image(img_path, max_width, max_height - title_height)
#         x = (page_width - img_width) / 2
#         y = (page_height - img_height - 144) / 2  # Center below title
        
#         c.drawImage(img_path, x, y, width=img_width, height=img_height,
#                    preserveAspectRatio=True, mask='auto')
    
#     c.save()



def create_pdf(photo_paths, output_path):
    """Create PDF with properly scaled images"""
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    
    for i, img_path in enumerate(photo_paths):
        if i > 0:  # Only create new page for subsequent images
            c.showPage()
        
        # Calculate available space
        max_width = page_width - 144  # 2-inch margins (72 pts/inch)
        max_height = page_height - 144
        title_height = 36  # 0.5 inch
        
        # Add title
        filename = os.path.basename(img_path)
        title = os.path.splitext(filename)[0]
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(page_width/2, page_height - 72, title)
        
        # Add image
        img_width, img_height = scale_image(img_path, max_width, max_height - title_height)
        x = (page_width - img_width) / 2
        y = (page_height - img_height - 144) / 2  # Center below title
        
        c.drawImage(img_path, x, y, 
                   width=img_width, 
                   height=img_height,
                   preserveAspectRatio=True)
    
    c.save()




# ======================
# Streamlit UI
# ======================
st.title("📷 Photo to Presentation Converter")
st.write("Upload photos to create perfect PPT/PDF slides!")

uploaded_files = st.file_uploader(
    "Select photos (multiple allowed)",
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
    
    # Preview
    st.subheader("Photo Preview")
    cols = st.columns(3)
    for idx, path in enumerate(photo_paths):
        cols[idx % 3].image(path, caption=os.path.basename(path), use_column_width=True)
    
    # Output options
    st.subheader("Output Settings")
    output_name = st.text_input("Base filename:", "MyPresentation")
    output_format = st.radio("Format:", ["PPTX", "PDF", "Both"])
    
    if st.button("🛠️ Generate Files"):
        with st.spinner("Processing..."):
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
                st.success("Files created successfully!")
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
                st.error(f"Error: {str(e)}")