# QassemRPM 🚀

![CI](https://github.com/Kasem-Adra/QassemRPM/actions/workflows/main.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Version](https://img.shields.io/badge/version-0.2-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

> **QassemRPM** is a modern and professional RPM packaging assistant, designed to simplify the workflows of system engineers and digital project managers. It automates the process of turning source code into stable RPM packages through a clean CLI and advanced validation tools.

---

## 🎯 Vision

Automate the full package lifecycle for reliability and performance:

```
Source Code → Analyze → Robust SPEC Parsing → Build (Isolated) → Test → Documentation
```

---

## ✨ Current Features

Completed in **v0.1** and **v0.2**:

| Feature | Description | Status |
|---------|-------------|--------|
| **SPEC Parser** | Extract metadata, `Requires` & `BuildRequires` | ✅ Done |
| **CLI Interface** | Colorful ANSI command-line interface | ✅ Done |
| **Auto Documentation** | Generate clean Markdown docs from SPEC files | ✅ Done |
| **CI/CD** | Automated testing on Python 3.11 via GitHub Actions | ✅ Done |
| **Validator Engine** | Core `validate` command to check SPEC files before building | ✅ Done |

---

## 🛠 Installation

### Development & Contributing

```bash
git clone https://github.com/Kasem-Adra/QassemRPM.git
cd QassemRPM
python3 -m pip install -e .[dev]
```

### Via Docker

```bash
docker build -t qassemrpm:0.2 .
docker run --rm qassemrpm:0.2 info examples/hello.spec
```

> 🚧 **PyPI release** is planned for **v0.3**

---

## 📖 Usage

### Show SPEC info

```bash
qassemrpm info examples/hello.spec
```

### Validate a SPEC file

```bash
qassemrpm validate examples/hello.spec
```

### Generate Markdown documentation

```bash
qassemrpm doc examples/hello.spec -o docs/hello.md
```

### Build locally with `rpmbuild`

```bash
qassemrpm build examples/hello.spec --topdir ./rpmbuild
```

---

## 🗺 Roadmap

### ✅ v0.1 — Foundation
- CLI foundation
- SPEC parser
- Markdown documentation
- Local rpmbuild wrapper
- Tests

### ✅ v0.2 — Improvements
- Colorful ANSI CLI
- CI/CD via GitHub Actions
- Validator engine (`validate` command)

### 🔄 v0.3 — In Progress
- [ ] Containerized builds (Docker / Podman)
- [ ] Publish Docker image to **GitHub Container Registry (GHCR)**
- [ ] Improved error reports and build logs

### 🔜 v0.4 — Repository Management
- [ ] Repository generation via `createrepo_c`
- [ ] Package signing with **GPG**
- [ ] Artifact index

### 🔜 v0.5 — Backend
- [ ] **FastAPI backend** for build queue management
- [ ] Live logs API
- [ ] Build queue

### 🔜 v0.6+ — Advanced UI
- [ ] **React dashboard** for live operation monitoring
- [ ] Package pages
- [ ] Dependency graph

### 🤖 Future — AI Integration
- [ ] AI-powered SPEC generator based on source code analysis
- [ ] Auto dependency suggestions
- [ ] Git integration
- [ ] CI/CD templates
- [ ] Multi-distro builds

---

## 📂 Project Structure

```text
QassemRPM/
├── .github/
│   └── workflows/
│       └── main.yml        # CI/CD automation (Python 3.11)
├── qassemrpm/
│   ├── cli.py              # Command-line interface
│   ├── spec.py             # SPEC parser engine
│   └── builder.py          # Build logic
├── tests/                  # Automated tests (Pytest)
├── examples/               # Sample SPEC files
├── docs/                   # Generated documentation
├── Dockerfile              # Docker image
├── pyproject.toml          # Package configuration & dependencies
├── LICENSE                 # MIT License (2026)
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Open an **Issue** first to discuss your proposed change
2. Fork the repository
3. Create a new branch: `git checkout -b feature/your-feature`
4. Commit your changes: `git commit -m 'Add: your feature'`
5. Open a **Pull Request**

---

## 📄 License

This project is licensed under the **MIT License** — 2026.

Copyright © 2026 **Kasem Adra**
