Summary:	QEMU CPU Emulator
Name:		qemu
Version:	0.5.2
Release:	0.1
Source0:	http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
Patch0:		%{name}-nostatic.patch
Patch1:		%{name}-DESTDIR.patch
#Patch0:		qemu-0.5.0-cvsupdates.patch.bz2
#Patch1:		qemu-0.1.6-glibc23-ldscripts.patch.bz2
#Patch2:		qemu-0.5.0-sdl-static-libs.patch.bz2
#Patch3:		qemu-0.5.0-DESTDIR.patch.bz2
#Patch4:		qemu-0.5.0-lib64.patch.bz2
#Patch5:		qemu-0.5.0-amd64.patch.bz2
#Patch6:		qemu-0.5.0-vl-amd64.patch.bz2
License:	GPL
URL:		http://fabrice.bellard.free.fr/qemu/
Group:		Applications/Emulators
BuildRequires:	SDL-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QEMU is a FAST! processor emulator. By using dynamic translation it
achieves a reasonnable speed while being easy to port on new host
CPUs. QEMU has two operating modes:

- User mode emulation. In this mode, QEMU can launch Linux processes
  compiled for one CPU on another CPU. Linux system calls are converted
  because of endianness and 32/64 bit mismatches. Wine (Windows
  emulation) and DOSEMU (DOS emulation) are the main targets for QEMU.

- Full system emulation. In this mode, QEMU emulates a full system,
  including a processor and various peripherials. Currently, it is only
  used to launch an x86 Linux kernel on an x86 Linux system. It enables
  easier testing and debugging of system code. It can also be used to
  provide virtual hosting of several virtual PC on a single server.

%prep
%setup -q
%patch0	-p1
%patch1	-p1
#%patch0 -p1 -b .cvsupdates
#%patch1 -p1 -b .glibc23-ldscripts
#%patch2 -p1 -b .sdl-static-libs
#%patch3 -p1 -b .DESTDIR
#%patch4 -p1 -b .lib64
#%patch5 -p1 -b .amd64
# needs to 64-bit clean softmmu code or MAP_32BIT physical_ram_base
# but other problems remain.
#%patch6 -p1 -b .vl-amd64

%build
./configure \
	--prefix=%{_prefix} \
	--cc=%{__cc} \
	--make=%{__make}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README qemu-doc.html
%ifarch %{ix86}
%attr(755,root,root) %{_bindir}/qemu-fast
%endif
%ifarch %{ix86} ppc
%{_bindir}/qemu
%endif
%{_bindir}/qemu-mkcow
%{_bindir}/qemu-arm
%{_bindir}/qemu-i386
%{_bindir}/qemu-sparc
%{_bindir}/qemu-ppc
%{_mandir}/man1/qemu.1*
%dir %{_datadir}/qemu
%{_datadir}/qemu/bios.bin
%{_datadir}/qemu/vgabios.bin
