# 📝 Resume Analyzer & Enhancer

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
[![Gemini AI](https://img.shields.io/badge/powered%20by-Gemini%20AI-purple)](https://ai.google.dev/)

</div>

 **Transform your resume with AI-powered analysis and personalized enhancement suggestions**

## ✨ Features

- 🔍 **Intelligent Analysis** - Extracts key information from your resume
- 🧠 **AI-Powered Insights** - Uses Gemini AI to analyze and provide feedback
- 🚀 **Personalized Suggestions** - Get tailored recommendations to improve your resume
- 💼 **Complete Resume Profile** - Identifies education, experience, skills, and personal info
- 📊 **Professional Report** - Download a beautifully formatted enhanced analysis

## 📋 Table of Contents

- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Troubleshooting](#-troubleshooting)
- [Technology Stack](#-technology-stack)
- [Contributing](#-contributing)
- [License](#-license)

## 🎮 Demo

<p align="center">
  <img src="https://raw.githubusercontent.com/learnershakil/ai-resume-analyser-enhancer/refs/heads/main/static/img/demo.jpeg" alt="Demo Screenshot" width="70%" height="auto">
</p>

## 🔧 Installation

### Prerequisites

- Python 3.9+
- Gemini API Key (Get it from [Google AI Studio](https://ai.google.dev/))

### Setup Instructions

#### Option 1: Using the setup script (Linux/macOS)

```bash
# Clone the repository
git clone https://github.com/learnershakil/resume_ai_app.git

cd resume_ai_app

# Make scripts executable
chmod +x setup.sh run.sh

# Run the setup script
./setup.sh
```

#### Option 2: Manual setup

```bash
# Clone the repository
git clone https://github.com/learnershakil/resume_ai_app.git

cd resume_ai_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Running the Application

#### Option 1: Using the run script (recommended)

```bash
./run.sh
```

#### Option 2: Manual activation

```bash
source venv/bin/activate
python app.py
```

Then open your browser and navigate to: `http://127.0.0.1:5000`

### How it works

1. 📤 **Upload** your resume in PDF format
2. ⚙️ **Process** - Our AI analyzes your resume and extracts key information
3. 📊 **Review** - Get personalized suggestions to improve your resume
4. 📥 **Download** - Get an enhanced analysis with tailored recommendations

## ⚠️ Troubleshooting

If you encounter a "No module named 'flask'" error, it means you're not using the Python interpreter from the virtual environment. Make sure to:

1. Activate the virtual environment with `source venv/bin/activate`
2. Verify it's activated (you should see `(venv)` in your terminal prompt)
3. Then run `python app.py`

Alternatively, just use `./run.sh` which handles this automatically.

## 🔧 Technology Stack

- **Backend**: Flask, Python
- **AI/ML**: Google Gemini API
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Processing**: PyPDF2, FPDF

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/learnershakil/resume_ai_app/issues).

## 📝 License

This project is [MIT](LICENSE) licensed.

---

<div align="center">
  Created with ❤️ by <a href="https://github.com/learnershakil">Learnershakil</a>
</div>
