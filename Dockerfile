FROM rockylinux:9

RUN dnf -y install python3 python3-pip rpm-build make git && dnf clean all
WORKDIR /workspace
COPY . /workspace
RUN python3 -m pip install --no-cache-dir -e .

ENTRYPOINT ["qassemrpm"]
