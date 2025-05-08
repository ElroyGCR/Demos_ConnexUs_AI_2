# ─── Use these updated logo display and favicon code ───────────────────
# Replace your logo display code with this:

# Logo display - moved down with more padding
try:
    # Try to load logo for display (not as favicon)
    logo_path = "connexus_logo.png"
    logo_b64 = load_base64(logo_path)
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:50px; margin-top:30px; margin-bottom:20px;" alt="ConnexUS Logo">'
        st.write(f'<div style="margin-bottom:20px;margin-top:20px;padding-top:20px;">{logo_html}</div>', unsafe_allow_html=True)
    else:
        # If logo not found, display text version
        st.write('<div style="margin-bottom:20px;margin-top:30px;padding-top:20px;"><span style="font-size:24px;font-weight:bold;color:#00FFAA;">ConnexUS</span></div>', unsafe_allow_html=True)
except Exception:
    # Fallback to simple text if any issues
    st.write('<div style="margin-top:30px;padding-top:20px;"></div>', unsafe_allow_html=True)
    st.write("# ConnexUS")

# ─── For favicon, add this code right after set_page_config ───────────────────
try:
    # Multiple approaches to set favicon
    favicon_path = "favicon-32x32.png"
    
    # Fallback favicon as base64
    fallback_favicon = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAAB3RJTUUH5QQHBhkSsGCo6wAAA5RJREFUWMPtl09IVFEUxr97Z0zzX6TmKANqRBB/wIXQznQ0GHURRLUIggKxRRi0KBftWreqdRBC0KJFLcOsRQtbRGEjQmGMSOmMojYmpdF05r5vjhMzc9+bGVsFLjpw4d1zz/fde+5998EsZjGLWcxi5oLpIXYA2AdgB4AWADxabgE4BOA4gBMATkZGzMrk9GqrDGUAZwCcsHAWCjFUVlbiAO5Z+H4CHwZQWm4DNBXkRHl5ef81awGyFsA9W+UKxf8CsPVfFcDB+liBDGcNrEY+wJ9oQFhYWoLQzGEK4AfMZwNLwMK3wE/TlWVo1ZeUXf0CoQezbSAH/I4bP4L/uWIToKeAI6AYxnSVPGaADSFDaw2UJwFqDq74Pqam/gEAUxc4NHdB9t2GrqS52tYd2QX4+oAJOwbZVMHvlGn7ND9BaO6BYQ2QVAiQ+wHXcmjVz9EYXQdcaSjPF8jBJ8D3Z1O1XjG4jLQlkWjG1gSI3QUMa0BI0jqg2YEfL+GQf8RK6jN0R+xW0uMvgcRrUwPGEnB1sPP0HYhwZgPE7gKOgKKpCkUGsAtIjkJY/gjPy4lNJyHH38Ad2HCYzaGA/B6YHDTMl9WtHBbsAGLX5Hj03mBfmygOWNYUKFcTdtWRTSqGICyZtDYS0bqQGHkPN1h/EF2XQCUnUZ77Z8i0RzFX35YYkCoICEtmrcTe8hB0MuIuLPQDcgDk1pxkl6GUQnflWwIPSZtTwF3B5rRaJnJxY8XZEvD4INGvvvZAJ8MVQHoY0vKDXFQWNYBDxSDDUjCpQc0RQVtKFcP8LnXm8xLgTRLFtxHXI9qSzQZCFp8DMm1AbGvxhp+DGHkISQkh/tWUDFemDcRQJC8uAcVVnB3F54DMy/RLXiSkTUukJMbNySCZxPJF0DJSWjG5YghT0zIaSgqLG63xyIxCivcI8W9mIp5NWE4FG9FbHlztfqhiZAGyWlHc6OXlCnZCRQekXg+Z1gbxbgZZwNbMHt7JqxpJofvYVgFJKIwCZBiZUEyMsw1SGKQQ9+I8aIAT9S2Jpwwqf1TGdXDdmS60mHVWt48Ks3yC8kQkUcRXdnJnwZLxT1iCzU0qjwOkUJbIPGWMnmtD87t59kKnQfpulXqwvvIoRDnTBvYUrYXkQHt3b8/y83a+9LkD7j0DnlcFRvbcUwM7Vj9qiO6i7fEjsI3eDRGUdvd+OnP++HKAjz/s6rF/28KYG/LE+CQAAAAASUVORK5CYII="
    
    # Try multiple approaches to set favicon
    if os.path.exists(favicon_path):
        st.write(f'<link rel="icon" type="image/png" href="{favicon_path}">', unsafe_allow_html=True)
    else:
        st.write(f'<link rel="icon" type="image/png" href="data:image/png;base64,{fallback_favicon}">', unsafe_allow_html=True)
except Exception:
    pass

# ─── For the FAQ section, replace with this code ───────────────────
# This uses the same heading size as Savings Breakdown

# Use a header with the same size as "Savings Breakdown"
st.header("Frequently Asked Questions")

# Simple text description with larger font
st.write("Common questions about AI automation and how it can benefit your contact center operations.")

# Use tabs to organize FAQs without nesting expanders
faq_tabs = st.tabs([
    "Why Choose AI", 
    "Cost Savings", 
    "Implementation", 
    "Capabilities",
    "Getting Started"
])

# Tab contents remain the same...
