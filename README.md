```markdown
<h1 align="center">🔎 ReconX - Automated Reconnaissance Framework</h1>

<p align="center">
  <img src="https://img.shields.io/github/license/tanveer2417/ReconX?style=flat-square" />
  <img src="https://img.shields.io/github/languages/top/tanveer2417/ReconX?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/tanveer2417/ReconX?style=flat-square" />
</p>

> ⚔️ A modular, CLI-based automated reconnaissance framework for ethical hackers, bug bounty hunters, and red teamers.

---

## 📌 Overview

**ReconX** is a Python-powered automated recon tool that helps gather intelligence on a target domain. It brings together several essential reconnaissance stages—from subdomain enumeration and DNS lookups to live host detection and technology fingerprinting—in a single, modular and extensible CLI utility.

---

## 🚀 Features

- 📡 Subdomain Enumeration (crt.sh, DNS brute-force)
- 🧠 Live Domain Detection (HTTP probing)
- 🕷️ Web Crawler & Parameter Discovery
- ⏳ Old Technology Detection (version leakage)
- 🛡️ Built-in Error Handling and CLI Flags
- 📂 Output saved in structured directories
- ⚙️ Easy-to-extend modular architecture
- 🧪 Designed for automation in your recon workflows

---

## 📁 Directory Structure

```

ReconX/
├── core/
│   ├── subdomain.py         # Subdomain enumeration
│   ├── live.py              # Live domain detection
│   ├── crawler.py           # Web crawling logic
│   ├── params.py            # Parameter discovery
│   └── oldversion.py        # Version detection
├── utils/                   # Utility scripts
├── wordlists/               # Custom wordlists
├── results/                 # Output storage
├── main.py / reconx         # CLI entry point
├── requirements.txt
└── README.md

````

---

## 🧰 Installation

```bash
# Clone the repository
git clone https://github.com/tanveer2417/ReconX.git
cd ReconX

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
````

---

## ⚙️ Usage

Use the CLI command `reconx` to run modules:

### 🔘 Subdomain Enumeration

```bash
python3 reconx subdomain --domain example.com
```

### 🔘 Live Domain Detection

```bash
python3 reconx live --input results/example.com/subdomains.txt
```

### 🔘 Web Crawler

```bash
python3 reconx crawler --url https://example.com
```

### 🔘 Parameter Discovery

```bash
python3 reconx params --url https://example.com
```

### 🔘 Old Version Detector

```bash
python3 reconx oldversion --url https://example.com
```

📁 All outputs will be saved in:

```
results/
└── example.com/
    ├── subdomains.txt
    ├── live.txt
    ├── crawler.txt
    ├── params.txt
    └── old_versions.txt
```

---

## 🔩 Modules & Functionalities

| Module       | Description                                         |
| ------------ | --------------------------------------------------- |
| `subdomain`  | Extracts subdomains using APIs and brute-force      |
| `live`       | Detects which subdomains are live via HTTP(S) probe |
| `crawler`    | Crawls and extracts links/pages                     |
| `params`     | Discovers query parameters in URLs                  |
| `oldversion` | Detects outdated frameworks or technologies         |

---

## 📦 Requirements

* Python 3.7+
* Required packages:

  * `requests`, `beautifulsoup4`, `argparse`, `colorama`

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🧠 Contributing

Contributions are welcome! 🚀

* Fork the project
* Create your feature branch: `git checkout -b feature/awesome-feature`
* Commit changes: `git commit -m 'Add some feature'`
* Push to the branch: `git push origin feature/awesome-feature`
* Open a Pull Request

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Tanveer Afifa**
✉️ [tanviafifa@gmail.com](mailto:tanviafifa@gmail.com)
🔗 [GitHub](https://github.com/tanveer2417)

---

## 📸 Screenshot Preview *(optional)*

> *You can add screenshots of your terminal output here later.*

---

## 💡 Roadmap (Future Enhancements)

* [ ] Add WAF detection module
* [ ] DNS zone transfer attempt module
* [ ] Auto-report generation in Markdown/PDF
* [ ] Web GUI using Flask

---

> 🔐 ReconX helps automate repetitive recon work, giving you more time to focus on analysis, exploitation, and finding real bugs.

```

---

Let me know if you want:

- A version with collapsible sections (`<details>`)
- Multi-target scanning example
- A logo/banner for the top
- GitHub Action CI badge integration

Would you like me to push this `README.md` as a file or help you auto-generate it from the CLI later?
```
