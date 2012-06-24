#
# Conditional build:
%bcond_with	kqemu			# with QEMU accelerator module
#
Summary:	QEMU CPU Emulator
Summary(pl):	QEMU - emulator procesora
Name:		qemu
Version:	0.7.0
Release:	1
License:	GPL
Group:		Applications/Emulators
#Source0Download: http://fabrice.bellard.free.fr/qemu/download.html
Source0:	http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
# Source0-md5:	234e9ace03b00259bb57dc5a9c633056
%if %{with kqemu}
Source1:	http://fabrice.bellard.free.fr/qemu/kqemu-0.6.2-1.tar.gz
# NoSource1-md5:	c6bb3b40fb3d526d731eb0f1f9dee7ee
NoSource:	1
%endif
Patch0:		%{name}-nostatic.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-longjmp.patch
Patch3:		%{name}-dot.patch
URL:		http://fabrice.bellard.free.fr/qemu/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664} ppc
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some SPARC boot image in ELF format
%define		_noautostrip	.*%{_datadir}/qemu/proll.elf

%description
QEMU is a FAST! processor emulator. By using dynamic translation it
achieves a reasonnable speed while being easy to port on new host
CPUs. QEMU has two operating modes:

- User mode emulation. In this mode, QEMU can launch Linux processes
  compiled for one CPU on another CPU. Linux system calls are converted
  because of endianness and 32/64 bit mismatches. Wine (Windows
  emulation) and DOSEMU (DOS emulation) are the main targets for QEMU.

- Full system emulation. In this mode, QEMU emulates a full system,
  including a processor and various peripherials. 
  It can also be used to provide virtual hosting of several 
  virtual PC on a single server.

%description -l pl
QEMU to szybki(!) emulator procesora. Poprzez u�ycie dynamicznego
t�umaczenia osi�ga rozs�dn� szybko�� i jest �atwy do przeportowania,
aby dzia�a� na kolejnych procesorach. QEMU ma dwa tryby pracy:

- Emulacja trybu u�ytkownika. W tym trybie QEMU mo�e uruchamia�
  procesy linuksowe skompilowane dla jednego procesora na innym
  procesorze. Linuksowe wywo�ania systemowe s� t�umaczone ze wzgl�du
  na niezgodno�� kolejno�ci bajt�w w s�owie i 32/64-bitowego rozmiaru
  s�owa. Wine (emulacja Windows) i DOSEMU (emulacja DOS-a) to g��wne
  cele QEMU.

- Pe�na emulacja systemu. W tym trybie QEMU emuluje ca�y system,
  w��czaj�c w to procesor i r�ne urz�dzenia peryferyjne.
  Mo�e by� tak�e u�ywane do wirtualnego hostowania kilku wirtualnych 
  pecet�w na pojedynczym serwerze.

%prep
%setup -q %{?with_kqemu:-a1}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e 's/sdl_static=yes/sdl_static=no/' configure
# cannot use optflags on x86 - they cause "no register to spill" errors
#sed -i -e 's/-Wall -O2 -g/-Wall %{rpmcflags}/' Makefile Makefile.target

%{?with_kqemu:echo -n > kqemu/install.sh}

%build
# --extra-cflags don't work (overridden by CFLAGS in Makefile*)
./configure \
	--prefix=%{_prefix} \
	--cc="%{__cc}" \
	--make="%{__make}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) %{_bindir}/*
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
