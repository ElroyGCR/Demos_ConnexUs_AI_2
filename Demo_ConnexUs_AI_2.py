# First, try to handle import errors gracefully
import streamlit as st

# Set page configuration first
st.set_page_config(page_title="ConnexUS AI ROI Calculator", layout="wide", page_icon="favicon.ico")

# Try importing plotly with error handling
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("Error: The plotly package is not installed. Please install it using 'pip install plotly'.")
    st.stop()  # Stop execution if plotly is missing

# Other imports
try:
    from PIL import Image
    from io import BytesIO
    import base64
    from decimal import Decimal, ROUND_HALF_UP
except ImportError as e:
    st.error(f"Error importing required packages: {str(e)}")
    st.stop()

# Display a helpful message at the top
st.info("If you're seeing this message, basic imports are working. Now loading the rest of the calculator...")

# Continue with the rest of your code below (the full code from the previous response)
# ─── Helper to load favicon and watermark ───────────────
def load_base64(path):
    try:
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.warning(f"Could not load image from {path}: {str(e)}")
        return None

# Rest of your code follows...
favicon_b64 = load_base64("favicon-32x32.png")
if favicon_b64:
    st.markdown(
        f"""<link rel="icon" href="data:image/png;base64,{favicon_b64}" type="image/png">""",
        unsafe_allow_html=True,
    )

# Just show a simple title to confirm the app is running
st.title("ConnexUS AI ROI Calculator")
st.markdown("---")
st.write("Initial imports completed successfully. Proceed with loading the rest of the calculator.")

# Add a troubleshooting section
with st.expander("Troubleshooting Information"):
    st.markdown("""
    ### Common Issues
    
    1. **Missing Plotly package**: This app requires the plotly package. Install it with:
       ```
       pip install plotly
       ```
       
    2. **Image file paths**: Make sure the favicon-32x32.png and connexus_logo_watermark.png files are in the same directory as this script.
    
    3. **Other dependencies**: This calculator requires:
       - streamlit
       - plotly
       - pillow (PIL)
       
    4. **Installation command**:
       ```
       pip install streamlit plotly pillow
       ```
    """)
