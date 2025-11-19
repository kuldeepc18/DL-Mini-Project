import io
import os
import tempfile
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image

from stylize import stylize

# Configure Streamlit page
st.set_page_config(
    page_title="Neural Style Transfer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS
st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title and description
st.title("🎨 Neural Style Transfer")
st.markdown(
    """
    Transform your images by applying the artistic style of another image.
    Upload a content image and a style image, and watch the magic happen!
    """
)

# VGG network path
VGG_PATH = "imagenet-vgg-verydeep-19.mat"

# Check if VGG model exists
if not os.path.isfile(VGG_PATH):
    st.error(f"❌ VGG model not found at {VGG_PATH}")
    st.info("Please download the pre-trained VGG model from: https://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat")
    st.stop()

# Sidebar for parameters
st.sidebar.header("⚙️ Settings")

iterations = st.sidebar.slider(
    "Number of Iterations",
    min_value=50,
    max_value=1000,
    value=100,
    step=50,
    help="More iterations = better quality but slower processing",
)

content_weight = st.sidebar.slider(
    "Content Weight",
    min_value=0.1,
    max_value=10.0,
    value=5.0,
    step=0.1,
    help="How much to preserve the original image content",
)

style_weight = st.sidebar.slider(
    "Style Weight",
    min_value=10.0,
    max_value=1000.0,
    value=500.0,
    step=10.0,
    help="How strongly to apply the style",
)

learning_rate = st.sidebar.slider(
    "Learning Rate",
    min_value=0.1,
    max_value=50.0,
    value=10.0,
    step=0.1,
    help="Higher values = faster convergence but less stable",
)

tv_weight = st.sidebar.slider(
    "TV Weight (smoothness)",
    min_value=10.0,
    max_value=1000.0,
    value=100.0,
    step=10.0,
    help="Higher values = smoother output",
)

style_layer_weight_exp = st.sidebar.slider(
    "Style Layer Weight Exponent",
    min_value=0.1,
    max_value=3.0,
    value=1.0,
    step=0.1,
    help="Lower = finer details, Higher = coarser features",
)

preserve_colors = st.sidebar.checkbox(
    "Preserve Original Colors",
    value=False,
    help="Keep the colors from the content image",
)

pooling_type = st.sidebar.radio(
    "Pooling Type",
    ("max", "avg"),
    help="max = finer details, avg = smoother",
)

# Main content area
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📷 Content Image")
    content_file = st.file_uploader(
        "Upload your content image",
        type=["jpg", "jpeg", "png"],
        key="content",
    )

with col2:
    st.subheader("🎭 Style Image")
    style_file = st.file_uploader(
        "Upload your style image",
        type=["jpg", "jpeg", "png"],
        key="style",
    )

with col3:
    st.subheader("✨ Output")
    st.write("Result will appear here")

# Display uploaded images
col1_display, col2_display, col3_display = st.columns(3)

content_image = None
style_image = None

with col1_display:
    if content_file:
        content_image = Image.open(content_file)
        st.image(content_image, use_column_width=True, caption="Content Image")

with col2_display:
    if style_file:
        style_image = Image.open(style_file)
        st.image(style_image, use_column_width=True, caption="Style Image")

with col3_display:
    placeholder = st.empty()

# Process button
if st.button("🚀 Generate Stylized Image", use_container_width=True, type="primary"):
    if content_image is None or style_image is None:
        st.error("❌ Please upload both content and style images!")
    else:
        try:
            # Convert PIL images to numpy arrays
            content_array = np.array(content_image).astype(np.float32)
            style_array = np.array(style_image).astype(np.float32)

            # Handle grayscale images
            if len(content_array.shape) == 2:
                content_array = np.dstack((content_array, content_array, content_array))
            if len(style_array.shape) == 2:
                style_array = np.dstack((style_array, style_array, style_array))

            # Handle PNG with alpha channel
            if content_array.shape[2] == 4:
                content_array = content_array[:, :, :3]
            if style_array.shape[2] == 4:
                style_array = style_array[:, :, :3]

            # Display progress
            with st.spinner("🎨 Processing... This may take a while..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Process with stylize function
                iteration_count = 0
                final_image = None

                for iteration, image, loss_vals in stylize(
                    network=VGG_PATH,
                    initial=None,
                    initial_noiseblend=1.0,
                    content=content_array,
                    styles=[style_array],
                    preserve_colors=preserve_colors,
                    iterations=iterations,
                    content_weight=content_weight,
                    content_weight_blend=1.0,
                    style_weight=style_weight,
                    style_layer_weight_exp=style_layer_weight_exp,
                    style_blend_weights=[1.0],
                    tv_weight=tv_weight,
                    learning_rate=learning_rate,
                    beta1=0.9,
                    beta2=0.999,
                    epsilon=1e-08,
                    pooling=pooling_type,
                    print_iterations=None,
                    checkpoint_iterations=None,
                ):
                    iteration_count = iteration
                    if image is not None:
                        final_image = image
                    
                    # Update progress bar (clamped between 0 and 1)
                    progress = min(max((iteration + 1) / iterations, 0.0), 1.0)
                    progress_bar.progress(progress)
                    status_text.text(f"✨ Processing: Iteration {iteration + 1}/{iterations}")

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                if final_image is not None:
                    # Convert to PIL image
                    output_image = Image.fromarray(
                        np.clip(final_image, 0, 255).astype(np.uint8)
                    )

                    # Display result
                    with col3_display:
                        placeholder.image(output_image, use_column_width=True, caption="Stylized Image")

                    # Download button
                    img_bytes = io.BytesIO()
                    output_image.save(img_bytes, format="JPEG", quality=95)
                    img_bytes.seek(0)

                    st.download_button(
                        label="⬇️ Download Stylized Image",
                        data=img_bytes,
                        file_name="stylized_image.jpg",
                        mime="image/jpeg",
                        use_container_width=True,
                    )

                    st.success("✅ Style transfer completed successfully!")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please try with different images or adjust the settings.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <small>
            Powered by TensorFlow & VGG-19 Neural Network<br>
            Based on "A Neural Algorithm of Artistic Style" (Gatys et al., 2015)
        </small>
    </div>
    """,
    unsafe_allow_html=True,
)
