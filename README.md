# Resume Analyzer & Enhancer

An AI-powered application that analyzes resumes, extracts key information, and provides suggestions for improvement using the Gemini API.

## Setup Instructions

This project requires Python 3.9+ and uses a virtual environment to manage dependencies.

### Option 1: Using the setup script (Linux/macOS)

1. Make the setup script executable:

   ```
   chmod +x setup.sh run.sh
   ```

2. Run the setup script:
   ```
   ./setup.sh
   ```

3. Run the main script:
   ```
   ./run.sh
   ```

## Running the Application

IMPORTANT: The application MUST be run with the virtual environment activated.

### Option 1: Using the run script (recommended)

Simply use the run script which automatically activates the virtual environment:

```
./run.sh
```

### Option 2: Manual activation

1. Activate the virtual environment:

   ```
   source venv/bin/activate
   ```

   You'll know it's activated when you see `(venv)` at the beginning of your terminal prompt.

2. Then run the app:
   ```
   python app.py
   ```

## Troubleshooting

If you get a "No module named 'flask'" error, it means you're not using the Python interpreter from the virtual environment. Make sure to:

1. Activate the virtual environment with `source venv/bin/activate`
2. Verify it's activated (you should see `(venv)` in your terminal prompt)
3. Then run `python app.py`

Alternatively, just use `./run.sh` which handles this automatically.

## Features

- Upload resumes in PDF format
- Extract key information using AI
- Receive personalized improvement suggestions
- Download enhanced resume with suggestions
