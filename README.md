# 👋 Welcome to FingerReader

**FingerReader** is a custom-built application designed for specialized finger reader devices that generate `.dat` files in external storage.  
Please note: This app may not be compatible with your device if it doesn't support `.dat` output or have different structure in `.dat` file.

If you encounter any bugs or issues, feel free to report them to my Gmail with the subject line **"Finger Reader"**.

## ⚙️ Installation Guide

### 🐧 Linux :

```bash
cd .../FingerReader
python3 -m venv venv
source venv/bin/activate
pip install jdatetime kivy pyinstaller
pyinstaller --onefile --windowed main.py
cp -r data dist/
```


### 🪟 Windows (CMD) :

```bash
cd ...\FingerReader
pyhton -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
pyinstaller --onefile --windowed main.py
xcopy data dist /E /I
```

### 📁 Output

After completing the steps above, your executable file will be available in the dist folder. Enjoy using FingerReader! 😄

## 🤝 Contributing

We welcome contributions from the community to improve FingerReader! Whether it's fixing bugs, adding new features, improving documentation, or sharing feedback — your help is appreciated.

### How to contribute:

    Fork the repository and create your branch (git checkout -b feature-name)

    Make your changes and commit them (git commit -m 'Add some feature')

    Push to the branch (git push origin feature-name)

    Open a pull request and describe your changes

If you're unsure where to start, feel free to reach out via email. Let's build something great together!

## 📬 Bug Reports
Please send any bug reports or suggestions to:
```bash
email:mr.alimohammadi001@gmail.com
📌 Subject: "Finger Reader"
```

