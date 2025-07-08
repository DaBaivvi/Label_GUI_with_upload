# Label_GUI_with_upload

A graphical user interface (GUI) for labeling and visualizing flow data, now with an integrated file upload feature.

## 🧩 Features

- Interactive GUI for flow data visualization and labeling
- Real-time plotting of flowrate and time series
- Supports multi-class labeling (e.g., Normal, Staccato, Compressive, etc.)
- 🆕 **File Upload Functionality**: Upload flow data (CSV) directly through the interface
- Export labeled data for downstream machine learning

## 📁 File Structure

Label_GUI_with_upload/
├── main.py              # Entry point for GUI
├── gui_components/      # Custom widgets and UI elements
├── utils/               # Helper functions (e.g., file parsing)
├── sample_data/         # Example CSV files
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

## ⚙️ Requirements

- Python 3.7+
- tkinter
- pandas
- matplotlib

Install required packages using:

```bash
pip install -r requirements.txt

🚀 How to Use
	1.	Clone this repository:
git clone https://github.com/DaBaivvi/Label_GUI_with_upload.git
cd Label_GUI_with_upload

	2.	Run the GUI:
python main.py

	3.	Use the interface to:
	•	Load a CSV file
	•	View flow data plots
	•	Label and save your annotations

## 📜 License

This project is intended for non-commercial academic and research use only.  
For any other use, please contact the author.  
© 2025 Wei Zhou, TU Darmstadt – Institute of Adaptive Lighting Systems and Visual Processing
