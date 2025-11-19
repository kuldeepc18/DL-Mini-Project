# 🎨 Neural Style Transfer

Transform your photos into beautiful artworks using artificial intelligence! Apply the artistic style of famous paintings to your own images.

---

## ✨ What is This?

Neural Style Transfer is a technique that takes two images:
1. **Content Image** - Your photo or any image
2. **Style Image** - A painting or artwork

And combines them to create a new image that looks like your photo but painted in the style of the artwork!

**Example:** Make your selfie look like a Van Gogh painting! 🎨

---

## 🚀 Quick Start

### Option 1: Easy Web Interface (Recommended!)

No command line needed - just use the web app!

```bash
python -m streamlit run app.py
```

Then open: **http://localhost:8502** in your browser

**Steps:**
1. Upload your photo (Content Image)
2. Upload an artwork (Style Image)
3. Click "Generate Stylized Image"
4. Download your result!

### Option 2: Command Line

For advanced users who want more control:

```bash
python neural_style.py --content your_photo.jpg --styles painting.jpg --output result.jpg --iterations 500
```

---

## 📋 What You Need

1. **Python 3.10 or higher** - [Download Python](https://www.python.org/)
2. **These Python packages:**
   ```bash
   pip install tensorflow numpy pillow scipy streamlit
   ```
3. **VGG Neural Network** (download below)

---

## 📥 Setup (3 Steps)

### Step 1: Download the Pre-trained Model

This is a special neural network that we need to download (about 500 MB):

**On Windows (PowerShell):**
```powershell
$url = "https://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat"
curl.exe -L -o imagenet-vgg-verydeep-19.mat $url
```

**Or download manually:** [Click here to download VGG Model](https://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat)

**Then place the file in the project folder** (same location as `app.py`)

### Step 2: Install Python Packages

```bash
pip install tensorflow numpy pillow scipy streamlit
```

### Step 3: Run the App

**Web Interface (Easy!):**
```bash
python -m streamlit run app.py
```

Or **Command Line:**
```bash
python neural_style.py --content content.jpg --styles style.jpg --output output.jpg
```

---

## 📸 Example Results

### Example 1: Photo Transformed by Starry Night

**Your Photo + Style:**

![Input Photo](examples/1-content.jpg)
![Style](examples/1-style.jpg)

**Result:**

![Output](examples/1-output.jpg)

---

### Example 2: Multiple Styles Combined

**Photo:**
![Photo](examples/2-content.jpg)

**Styles:**
![Style 1](examples/2-style1.jpg)
![Style 2](examples/2-style2.jpg)

**Result:**
![Result](examples/2-output.jpg)

---

## 🎯 Tips for Best Results

| Tip | What to Do |
|-----|-----------|
| **Image Size** | Start with 400-600 pixel wide images (faster processing) |
| **Iterations** | Try 500-1000 for good results (higher = better but slower) |
| **Keep Original Look** | Increase "Content Weight" (5-10) |
| **Strong Style** | Increase "Style Weight" (400-800) |
| **Smooth Output** | Increase "TV Weight" (100-200) |
| **Different Results** | Adjust "Learning Rate" (5-20) |

---

## 🔧 Web Interface Settings Explained

When using the web app, you can adjust:

| Setting | What It Does | Default | Try This |
|---------|-------------|---------|----------|
| **Iterations** | How many times to refine (more = better) | 100 | 500 for great results |
| **Content Weight** | Keep more of your original photo | 5.0 | 8.0 to preserve more |
| **Style Weight** | Apply more artistic style | 500.0 | 800.0 for stronger style |
| **Learning Rate** | Speed of processing | 10.0 | 15.0 for faster processing |
| **TV Weight** | Make output smoother | 100.0 | 150.0 for smoothness |
| **Pooling** | Style detail level | max | Try avg for smoothness |
| **Preserve Colors** | Keep original image colors | Off | Check for color preservation |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| **VGG model not found error** | Download the model file and place it in the project folder |
| **Processing is slow** | Use smaller images or reduce iterations to 100 |
| **Memory/RAM issues** | Close other programs and use smaller images |
| **Out of memory error** | Try resizing images to 400x400 pixels |
| **Streamlit won't start** | Make sure all packages are installed: `pip install streamlit tensorflow` |

---

## 📚 How It Works (Simple Explanation)

The AI looks at:
1. **Your Photo** - What should the result look like?
2. **The Painting** - What style should it have?

Then it combines them by:
- Keeping the shapes and content from your photo
- Applying the colors and patterns from the painting
- Making it smooth and natural looking

All this happens using a deep neural network trained on millions of images!

---

## 📚 Advanced Settings (Command Line)

```bash
python neural_style.py --help
```

Common options:
- `--iterations 500` - More = better quality
- `--content-weight 10` - Higher = keep more of original
- `--style-weight 800` - Higher = stronger style
- `--learning-rate 15` - Higher = faster but less stable
- `--width 400` - Resize output width in pixels
- `--preserve-colors` - Keep original colors from photo

---

## 🎓 Research Behind This

Based on the famous paper: **"A Neural Algorithm of Artistic Style"** by Gatys et al. (2015)
- [Read the Paper](http://arxiv.org/pdf/1508.06576v2.pdf)

Uses: **VGG-19 Deep Neural Network** trained on ImageNet

---

## 📄 License

**Released under GPLv3 License** - You can use and modify freely! See [LICENSE.txt](LICENSE.txt)

---

## 🎬 Get Started Now!

1. Download this project
2. Download the VGG model (see Setup above)
3. Install packages: `pip install tensorflow numpy pillow scipy streamlit`
4. Run: `python -m streamlit run app.py`
5. Open http://localhost:8502 in browser
6. Upload images and create art! 🎨

---

**Have fun creating amazing artworks!** ✨ If you have questions, check the troubleshooting section above.
