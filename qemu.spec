Summary:	QEMU CPU Emulator
Summary(pl):	QEMU - emulator procesora
Name:		qemu
Version:	0.6.0
Release:	0.2
License:	GPL
Group:		Applications/Emulators
Source0:	http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
# Source0-md5:	cdbc7258f122f381cba7ac1ca6ce0722
# Source0-size:	874397
Patch0:		%{name}-nostatic.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-amd64.patch
Patch3:		%{name}-longjmp.patch
Patch4:		%{name}-gcc34.patch
Patch5:		%{name}-ppc.patch
#Patch0:		qemu-0.5.0-cvsupdates.patch.bz2
#Patch1:		qemu-0.1.6-glibc23-ldscripts.patch.bz2
#Patch2:		qemu-0.5.0-sdl-static-libs.patch.bz2
#Patch3:		qemu-0.5.0-DESTDIR.patch.bz2
#Patch4:		qemu-0.5.0-lib64.patch.bz2
#Patch5:		qemu-0.5.0-amd64.patch.bz2
#Patch6:		qemu-0.5.0-vl-amd64.patch.bz2
URL:		http://fabrice.bellard.free.fr/qemu/
BuildRequires:	SDL-devel
ExclusiveArch:	%{ix86} amd64 ppc sparc
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
  w��czaj�c w to procesor i r�ne urz�dzenia peryferyjne. Aktualnie
  dzia�a to tylko przy uruchamianiu j�dra Linuksa x86 na systemie
  linuksowym x86, pozwalaj�c na �atwiejsze testowanie i odpluskwianie
  kodu systemu. Mo�e by� tak�e u�ywane do wirtualnego hostowania kilku
  wirtualnych pecet�w na pojedynczym serwerze.

%prep
%setup -q
%patch0	-p1
%patch1	-p1
%patch2	-p1
%patch3	-p1
%patch4	-p1
%patch5	-p1

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
	--make=%{__make} \
%ifarch %{ix86} amd64
	--target-list="i386-user i386 i386-softmmu"
%endif
%ifarch ppc powerpc
	--target-list="ppc-user ppc-softmmu"
%endif
%ifarch sparc
	--target-list="sparc-user"
%endif

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
