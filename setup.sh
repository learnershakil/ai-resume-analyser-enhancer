#!/bin/bash

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Verify activation worked
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo "ERROR: Virtual environment activation failed."
  exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create uploads directory
mkdir -p static/uploads

# Create a run script
echo "#!/bin/bash
source \"$(pwd)/venv/bin/activate\"
python app.py" > run.sh
chmod +x run.sh

echo ""
echo "Setup complete! To run the app, use either:"
echo "1. ./run.sh"
echo "   OR"
echo "2. source venv/bin/activate && python app.py"
echo ""
echo "IMPORTANT: Make sure to always run the app with the virtual environment activated!"
