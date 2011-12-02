# TODO:
# - update patches
# - qemu-system-ppc -hda ac-ppc.img says:
#   qemu: could not open disk image ac-ppc.img: Success
#   qemu-0.12.2-2.x86_64.rpm - broken
#   qemu-0.12.3-3.x86_64/qemu-0.12.4-1.x86_64 - stops on "returning from prom_init"
#   qemu-0.11.1-7k.x86_64.rpm - OK
#
# Conditional build:
%bcond_with	cflags_passing		# with passing rpmcflags to Makefiles
%bcond_with	dosguest		# add special patch when use with DOS as guest os
%bcond_with	nosdlgui		# do not use SDL gui (use X11 instead)

Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu
Version:	1.0
Release:	0.1
License:	GPL
Group:		Applications/Emulators
# Source0Download: http://fabrice.bellard.free.fr/qemu/download.html
#Source0:	http://download.savannah.gnu.org/releases/qemu/%{name}-%{version}.tar.gz
Source0:	http://wiki.qemu.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	a64b36067a191451323b0d34ebb44954
Patch0:		%{name}-ncurses.patch
Patch6:		%{name}-nosdlgui.patch
# Proof of concept, for reference, do not remove
Patch8:		%{name}-kde_virtual_workspaces_hack.patch
#Patch12: %{name}-0.7.2-dyngen-check-stack-clobbers.patch
Patch13:	%{name}-dosguest.patch
Patch14:	%{name}-ppc_old_binutils.patch
Patch15:	%{name}-isa-bios-ram.patch
# below one fixes problems with passing ram size to bios/bootloader
# which affects coreboot/linuxbios
Patch16:	%{name}-piix-ram-size.patch
Patch17:	%{name}-whitelist.patch
URL:		http://wiki.qemu.org/Index.html
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	gnutls-devel
BuildRequires:	ncurses-devel
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	texi2html
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
Requires:	SDL >= 1.2.1
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
ExclusiveArch:	%{ix86} %{x8664} %{?with_userspace:ppc}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some PPC/SPARC boot image in ELF format
%define		_noautostrip	.*%{_datadir}/qemu/openbios-.*

%description
QEMU is a FAST! processor emulator. By using dynamic translation it
achieves a reasonnable speed while being easy to port on new host
CPUs. QEMU has two operating modes:

- User mode emulation. In this mode, QEMU can launch Linux processes
  compiled for one CPU on another CPU. Linux system calls are converted
  because of endianness and 32/64 bit mismatches. Wine (Windows
  emulation) and DOSEMU (DOS emulation) are the main targets for QEMU.

- Full system emulation. In this mode, QEMU emulates a full system,
  including a processor and various peripherials. It can also be used to
  provide virtual hosting of several virtual PC on a single server.

%description -l pl.UTF-8
QEMU to szybki(!) emulator procesora. Poprzez użycie dynamicznego
tłumaczenia osiąga rozsądną szybkość i jest łatwy do przeportowania,
aby działał na kolejnych procesorach. QEMU ma dwa tryby pracy:

- Emulacja trybu użytkownika. W tym trybie QEMU może uruchamiać
  procesy linuksowe skompilowane dla jednego procesora na innym
  procesorze. Linuksowe wywołania systemowe są tłumaczone ze względu na
  niezgodność kolejności bajtów w słowie i 32/64-bitowego rozmiaru
  słowa. Wine (emulacja Windows) i DOSEMU (emulacja DOS-a) to główne
  cele QEMU.

- Pełna emulacja systemu. W tym trybie QEMU emuluje cały system,
  włączając w to procesor i różne urządzenia peryferyjne. Może być także
  używane do wirtualnego hostowania kilku wirtualnych pecetów na
  pojedynczym serwerze.

%prep
%setup -q
%patch0 -p1
%{?with_nosdlgui:%patch6 -p1}
#patch8 -p1
%patch17 -p0

%{__sed} -i -e 's/sdl_static=yes/sdl_static=no/' configure
%{__sed} -i 's/.*MAKE) -C kqemu$//' Makefile

# cannot use optflags on x86 - they cause "no register to spill" errors
%if %{with cflags_passing}
%{__sed} -i -e 's/-g $CFLAGS/-Wall %{rpmcflags}/' configure
%else
%{__sed} -i 's/-g $CFLAGS/-Wall -fno-var-tracking-assignments/' configure
%endif

# workaround for conflict with alsa/error.h
ln -s ../error.h qapi/error.h

%build
# --extra-cflags don't work (overridden by CFLAGS in Makefile*)
# they can be passed if the cflags_passing bcond is used
./configure \
	--prefix=%{_prefix} \
	--cc="%{__cc}" \
	--host-cc="%{__cc}" \
	--enable-mixemu \
	--audio-drv-list="alsa" \
	--interp-prefix=%{_libdir}/%{name}
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ifup
#!/bin/sh

EOF

# already packaged
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-{doc,tech}.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%attr(755,root,root) %{_bindir}/*
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
