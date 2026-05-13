# QassemRPM v0.1

QassemRPM is a modern RPM packaging assistant. The first version focuses on a clean CLI, safe SPEC parsing, Markdown documentation generation, and a base for future containerized RPM builds.

## Vision

Turn source code into RPM packages through a simple workflow:

```text
Source Code → Analyze → Generate/Read SPEC → Build RPM → Test → Publish Repository → Documentation
```

## Current Features

- Read RPM `.spec` metadata
- Extract `Requires` and `BuildRequires`
- Generate clean Markdown documentation
- Run `rpmbuild` locally when available
- Docker base image for reproducible tooling
- Tests for the SPEC parser and documentation generator

## Install for development

```bash
python3 -m pip install -e .[dev]
```

## Usage

Show SPEC information:

```bash
qassemrpm info examples/hello.spec
```

Generate Markdown documentation:

```bash
qassemrpm doc examples/hello.spec -o docs/hello.md
```

Build with local rpmbuild:

```bash
qassemrpm build examples/hello.spec --topdir ./rpmbuild
```

Run inside Docker:

```bash
docker build -t qassemrpm:0.1 .
docker run --rm qassemrpm:0.1 info examples/hello.spec
```

## Roadmap

### v0.1

- CLI foundation
- SPEC parser
- Markdown documentation
- Local rpmbuild wrapper
- Tests

### v0.2

- Containerized builds with Docker/Podman
- Build logs
- Config file support
- Better error reports

### v0.3

- Repository generation with `createrepo_c`
- GPG signing workflow
- Artifact index

### v0.4

- FastAPI backend
- Build queue
- Live logs API

### v0.5

- React dashboard
- Package pages
- Dependency graph

### Future

- AI SPEC generator
- Auto dependency suggestions
- Git integration
- CI/CD templates
- Multi-distro builds

## Project Structure

```text
QassemRPM-v0.1/
├── qassemrpm/
│   ├── cli.py
│   ├── spec.py
│   └── builder.py
├── examples/
├── tests/
├── docs/
├── Dockerfile
├── pyproject.toml
└── README.md
```
