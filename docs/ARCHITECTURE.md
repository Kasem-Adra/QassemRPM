# QassemRPM Architecture

QassemRPM v0.1 is intentionally small. It separates the core into three parts:

1. `spec.py`: reads and documents RPM SPEC files.
2. `builder.py`: wraps RPM build execution.
3. `cli.py`: exposes commands to the user.

Future versions can add:

- `container.py` for Docker/Podman isolation
- `repo.py` for repository publishing
- `api/` for FastAPI
- `worker/` for background builds
- `web/` for the dashboard
