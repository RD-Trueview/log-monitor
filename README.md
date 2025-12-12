# Log Monitor

A simple Python-based log monitoring tool that watches a directory for log files and prints any error lines in real time.

## 📌 Features
- Monitors a directory for any `.log` file
- Reads new lines as they are appended
- Automatically highlights lines containing the word **ERROR**
- Lightweight and easy to run

## 📁 Project Structure
log-monitor/
├── main.py
├── config.yaml
├── monitor/
│ ├── init.py
│ └── watcher.py
└── README.md

markdown
Copy code

## ⚙️ Configuration
Edit the directory to watch in **config.yaml**:

watch_directory: "/tmp"

r
Copy code

You can change `/tmp` to any folder you want to monitor.

## ▶️ How to Run

### 1️⃣ Install required package
pip install watchdog

graphql
Copy code

### 2️⃣ Run the main script
python3 main.py

yaml
Copy code

### 3️⃣ Test with a sample log file
In another terminal:

echo "This is a test line" >> /tmp/test-log.log
echo "ERROR: something went wrong" >> /tmp/test-log.log

yaml
Copy code

You will instantly see the output in the main program.

---

# 🤝 Contribution
Feel free to fork, modify, and improve the tool.

---

# 🏁 License
MIT License

