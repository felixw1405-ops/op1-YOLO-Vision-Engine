# YOLO Vision Engine

A real-time computer vision engine built with Python, YOLO, and an asynchronous capture/detection pipeline.
v5.3a
model version: 4.5

---

## 🪟 Windows Installation

### 1. Install Requirements

Install **Python 3.10+**:
👉 https://python.org

During installation:
- ✅ Enable **"Add Python to PATH"**

Verify your installation in Command Prompt (CMD) or PowerShell:
```cmd
python --version
```

---

### 2. Clone the Repository

Install Git:
👉 https://git-scm.com

Clone the project:
```cmd
git clone https://github.com
```

Enter the folder:
```cmd
cd op1-YOLO-Vision-Engine
```

---

### 3. Create Virtual Environment

Create the environment:
```cmd
python -m venv venv
```

Activate it:
```cmd
venv\Scripts\activate
```
You should see `(venv)` appear in your terminal prompt.

---

### 4. Install Dependencies

Install the required packages:
```cmd
pip install -r requirements.txt
```

---

### 5. Add Model Files

Place your required YOLO model files inside a `models/` directory at the root of the project:
```text
models/
└── v5_best.pt
```

---

### 6. Run the Engine

Start the preview:
```cmd
python preview.py
```
Press **`Q`** to exit.

---

## 🍏 macOS Installation

### 1. Clone & Enter Repository

Open your Terminal and run:
```bash
git clone https://github.com
```

Enter the folder:
```bash
cd op1-YOLO-Vision-Engine
```

---

### 2. Create Virtual Environment

Create the environment:
```bash
python3 -m venv venv
```

Activate it:
```bash
source venv/bin/activate
```
You should see `(venv)` appear in your terminal prompt.

---

### 3. Install Dependencies

Install the required packages:
```bash
pip install -r requirements.txt
```

*Note: If your requirements file is not available, install them manually:*
```bash
pip install ultralytics opencv-python numpy mss torch
```

---

### 4. macOS System Permissions

Because this engine uses real-time screen capture, macOS requires explicit security clearance.

1. Open **System Settings** → **Privacy & Security** → **Screen & System Audio Recording**.
2. Flip the toggle to **Enable** permission for **Terminal** (and **VS Code** if running from an integrated terminal).
3. Restart your Terminal or code editor for changes to apply.

---

### 5. Run the Engine

Start the preview:
```bash
python preview.py
```
Press **`Q`** to exit.

---

## 🛠️ Troubleshooting

### Windows Execution Policy Error
If PowerShell blocks you from activating the virtual environment (`venv\Scripts\activate`), run this command first to grant permission:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### Script/Command Not Found
If running `python` or `git` returns an error saying the command is not found:
* **Windows:** Re-run the Python installer and ensure the **"Add Python to PATH"** checkbox is selected.
* **macOS:** Ensure you are using `python3` instead of `python`.

### CUDA / GPU Acceleration (Windows)
To leverage an Nvidia GPU on Windows for lightning-fast inference, ensure you have the matching CUDA Toolkit installed and reinstall PyTorch with CUDA support:
```cmd
pip uninstall torch torchvision
pip install torch torchvision --index-url https://pytorch.org
```

---

## 📝 Project Notes

- **Hardware:** A dedicated GPU (Windows) or Apple Silicon Mac (M1/M2/M3/M4) is highly recommended for optimal inference performance.
- **Environment:** Always ensure your virtual environment (`venv`) is activated before running the engine.
- **Repository Hygiene:** Do not commit large model files (`.pt`) or raw datasets to GitHub. Keep them locally in your `models/` folder.

## 📌 Current Version

```text
v5.2 - Async Vision Engine Architecture
```
