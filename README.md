<h1 align="center">🔎 ReconX – eXecute Reconnaissance Smarter.</h1>

<p align="center">
  <img src="https://img.shields.io/github/license/tanveer2417/ReconX?style=flat-square" />
  <img src="https://img.shields.io/github/languages/top/tanveer2417/ReconX?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/tanveer2417/ReconX?style=flat-square" />
</p>

<p align="center">
  <b>Modular | CLI-based | Python Powered | Plug & Play Recon</b><br>
  Automate your reconnaissance workflow with one powerful toolset.
</p>

---

## 📌 Overview

**ReconX** is a Python-based automated reconnaissance framework that consolidates key recon tasks into a modular CLI-driven utility. From subdomain enumeration to outdated tech detection, ReconX streamlines information gathering for ethical hackers, bug bounty hunters, and red teamers.

---

## 🚀 Features

- 📡 **Subdomain Enumeration** via APIs and brute-force
- 🧠 **Live Domain Detection** using HTTP probe
- 🕷️ **Web Crawling** for links and directories
- 📥 **Parameter Discovery** from input fields and URLs
- ⏳ **Outdated Technology Detection** from headers and versions
- ⚙️ Fully modular and extensible via `core/`
- 💾 Results saved neatly in `results/` directory
- 🧪 CLI-based interface for automation or integration

---

## 🧰 Installation

```bash
# Clone the repository
git clone https://github.com/tanveer2417/ReconX.git
cd ReconX

# (Optional) Set up a virtual environment
python3 -m venv venv
source venv/bin/activate        # For Linux/macOS
venv\Scripts\activate           # For Windows

# Install required Python packages
pip install -r requirements.txt


## ⚙️ Usage

Each module is accessed via the CLI command:
`python reconx <module> [--options]`

### 🔘 Subdomain Enumeration

```bash
python reconx subdomain --domain example.com
```

### 🔘 Live Domain Detection

```bash
python reconx live --input results/example.com/subdomains.txt
```

### 🔘 Web Crawler

```bash
python reconx crawler --url https://example.com
```

### 🔘 Parameter Discovery

```bash
python reconx params --url https://example.com
```

### 🔘 Old Technology Detection

```bash
python reconx oldversion --url https://example.com
```

🗂️ Output will be saved in:

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

## 📁 Project Structure

```
ReconX/
├── core/
│   ├── subdomain.py         # Subdomain enumeration
│   ├── live.py              # Live domain identification
│   ├── crawler.py           # Crawler for endpoint discovery
│   ├── params.py            # Parameter extractor
│   └── oldversion.py        # Detects old/vulnerable tech
├── utils/                   # Helper scripts
├── wordlists/               # Wordlists for fuzzing/bruteforce
├── results/                 # Output directory
├── reconx                   # CLI entry point (executable)
├── requirements.txt
└── README.md
```

---

## 🧩 Module Details

| Module       | Description                                    |
| ------------ | ---------------------------------------------- |
| `subdomain`  | Finds subdomains using crt.sh + wordlists      |
| `live`       | Probes HTTP/HTTPS for live hosts               |
| `crawler`    | Extracts internal/external links from webpages |
| `params`     | Extracts query parameters from forms/URLs      |
| `oldversion` | Detects outdated headers, CMS, server versions |

---

## 🧪 Example Workflow

```bash
python reconx subdomain --domain hackerone.com
python reconx live --input results/hackerone.com/subdomains.txt
python reconx crawler --url https://hackerone.com
python reconx params --url https://hackerone.com
python reconx oldversion --url https://hackerone.com
```

---

## 📦 Dependencies

* Python 3.7+
* `requests`, `argparse`, `beautifulsoup4`, `colorama`

Install them via:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Future Enhancements

* [ ] Add WAF Detection
* [ ] Add DNS Zone Transfer Module
* [ ] Auto-report Generation (Markdown/PDF)
* [ ] Flask Web Dashboard Integration

---

## 👤 Author

**Mariya Fareed**
🔗 [GitHub Profile][(https://github.com/mariyafareed)]

**Tanveer Afifa**
🔗 [GitHub Profile](https://github.com/tanveer2417)

**Ruheena Begum**

---

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> 💡 ReconX simplifies your recon process—use it in CTFs, bug bounty, or red teaming for powerful intelligence at your fingertips.

```

---


