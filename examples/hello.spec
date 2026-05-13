Name:           hello-qassem
Version:        0.1.0
Release:        1%{?dist}
Summary:        Example package for QassemRPM
License:        MIT
URL: https://example.com/qassemrpm
BuildArch:      noarch
BuildRequires:  python3, make
Requires:       python3

%description
A tiny example SPEC file used to demonstrate QassemRPM documentation generation.

%prep
# prepare source

%build
# build commands

%install
# install commands

%files
%license LICENSE

%changelog
* Wed May 13 2026 Qassem <qassemadra@gmail.com> - 0.1.0-1
- Initial example package
