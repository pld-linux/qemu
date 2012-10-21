# TODO:
# - package virtfs-proxy-helper, qemu-bridge-helper.
# - update patches
# - qemu-system-ppc -hda ac-ppc.img says:
#   qemu: could not open disk image ac-ppc.img: error "Success"
#   qemu-0.12.2-2.x86_64.rpm - broken
#   qemu-0.12.3-3.x86_64/qemu-0.12.4-1.x86_64 - stops on "returning from prom_init"
#   qemu-0.15.0-2.x86_64.rpm - qemu-system-sparc/ppc booting with -kernel, -initrd options stalls in openbios prompt
#   qemu-0.11.1-*.x86_64.rpm - OK
#
# Conditional build:
%bcond_with	nosdlgui		# do not use SDL gui (use X11 instead)

Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu
Version:	1.2.0
Release:	4
License:	GPL
Group:		Applications/Emulators
Source0:	http://wiki.qemu.org/download/%{name}-%{version}.tar.bz2
# Source0-md5:	78eb1e984f4532aa9f2bdd3c127b5b61
Patch0:		%{name}-cflags.patch
Patch1:		vgabios-widescreens.patch
Patch6:		%{name}-nosdlgui.patch
# Proof of concept, for reference, do not remove
Patch8:		%{name}-kde_virtual_workspaces_hack.patch
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
BuildRequires:	texinfo
BuildRequires:	which
BuildRequires:	xen-devel
BuildRequires:	xorg-lib-libX11-devel
Requires:	%{name}-img = %{version}-%{release}
Requires:	%{name}-system-alpha = %{version}-%{release}
Requires:	%{name}-system-arm = %{version}-%{release}
Requires:	%{name}-system-cris = %{version}-%{release}
Requires:	%{name}-system-lm32 = %{version}-%{release}
Requires:	%{name}-system-m68k = %{version}-%{release}
Requires:	%{name}-system-microblaze = %{version}-%{release}
Requires:	%{name}-system-mips = %{version}-%{release}
Requires:	%{name}-system-ppc = %{version}-%{release}
Requires:	%{name}-system-or32 = %{version}-%{release}
Requires:	%{name}-system-s390x = %{version}-%{release}
Requires:	%{name}-system-sh4 = %{version}-%{release}
Requires:	%{name}-system-sparc = %{version}-%{release}
Requires:	%{name}-system-unicore32 = %{version}-%{release}
Requires:	%{name}-system-x86 = %{version}-%{release}
Requires:	%{name}-system-xtensa = %{version}-%{release}
Requires:	%{name}-user = %{version}-%{release}
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
ExclusiveArch:	%{ix86} %{x8664} %{?with_userspace:ppc}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some PPC/SPARC boot image in ELF format
%define		_noautostrip	.*%{_datadir}/qemu/.*-.*

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

%package  common
Summary:	QEMU common files needed by all QEMU targets
Group:		Development/Tools
Requires:	SDL >= 1.2.1
Conflicts:	qemu < 1.0-2

%description common
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets.

%package  img
Summary:	QEMU command line tool for manipulating disk images
Group:		Development/Tools
Conflicts:	qemu < 1.0-2

%description img
This package provides a command line tool for manipulating disk images

%package user
Summary:	QEMU user mode emulation of qemu targets
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description user
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the user mode emulation of QEMU targets.

%package system-alpha
Summary:	QEMU system emulator for alpha
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-alpha
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for alpha.

%package system-arm
Summary:	QEMU system emulator for arm
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-arm
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for arm.

%package system-cris
Summary:	QEMU system emulator for cris
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-cris
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for cris.

%package system-lm32
Summary:	QEMU system emulator for lm32
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-lm32
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for lm32.

%package system-m68k
Summary:	QEMU system emulator for m68k
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-m68k
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for m68k.

%package system-microblaze
Summary:	QEMU system emulator for microblaze
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-microblaze
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for microblaze.

%package system-mips
Summary:	QEMU system emulator for mips
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-mips
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for mips.

%package system-or32
Summary:	QEMU system emulator for or32
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-or32
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for or32.

%package system-ppc
Summary:	QEMU system emulator for ppc
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-ppc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for ppc.

%package system-s390x
Summary:	QEMU system emulator for s390x
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-s390x
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for s390x.

%package system-sh4
Summary:	QEMU system emulator for sh4
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-sh4
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for sh4.

%package system-sparc
Summary:	QEMU system emulator for sparc
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-sparc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for sparc/sparc64.

%package system-unicore32
Summary:	QEMU system emulator for unicore32
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-unicore32
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for unicore32.

%package system-x86
Summary:	QEMU system emulator for x86
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-x86
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a
x86 machine that supports it, this package also provides the KVM
virtualization platform.

%package system-xtensa
Summary:	QEMU system emulator for xtensa
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for xtensa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{?with_nosdlgui:%patch6 -p1}
#patch8 -p1
%patch17 -p0

# workaround for conflict with alsa/error.h
ln -s ../error.h qapi/error.h

%build
./configure \
	--extra-cflags="%{rpmcflags} -I/usr/include/ncurses" \
	--extra-ldflags="%{rpmldflags}" \
	--disable-strip \
	--sysconfdir=%{_sysconfdir} \
	--prefix=%{_prefix} \
	--cc="%{__cc}" \
	--host-cc="%{__cc}" \
	--enable-mixemu \
	--audio-drv-list="alsa" \
	--interp-prefix=%{_libdir}/%{name}
%{__make} V=1

# rebuild patched vesa tables with additional widescreen modes.
%{__make} -C roms/vgabios stdvga-bios

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

# install patched vesa tables with additional widescreen modes.
install -m 644 roms/vgabios/VGABIOS-lgpl-latest.stdvga.bin $RPM_BUILD_ROOT%{_datadir}/%{name}/vgabios-stdvga.bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%files common
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu/target-*.conf
%dir %{_sysconfdir}/qemu
%attr(755,root,root) %{_bindir}/qemu-nbd
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*

%dir %{_datadir}/qemu
%{_datadir}/%{name}/cpus-*.conf
%{_datadir}/%{name}/keymaps
# various bios images
%{_datadir}/%{name}/*.bin
%{_datadir}/%{name}/*.rom
%{_datadir}/%{name}/*.dtb
%{_datadir}/%{name}/openbios-ppc
%{_datadir}/%{name}/openbios-sparc*
%{_datadir}/%{name}/palcode-clipper

%files img
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%files user
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-x86_64
%attr(755,root,root) %{_bindir}/qemu-i386
%attr(755,root,root) %{_bindir}/qemu-alpha
%attr(755,root,root) %{_bindir}/qemu-arm
%attr(755,root,root) %{_bindir}/qemu-armeb
%attr(755,root,root) %{_bindir}/qemu-cris
%attr(755,root,root) %{_bindir}/qemu-ga
%attr(755,root,root) %{_bindir}/qemu-io
%attr(755,root,root) %{_bindir}/qemu-m68k
%attr(755,root,root) %{_bindir}/qemu-microblaze
%attr(755,root,root) %{_bindir}/qemu-microblazeel
%attr(755,root,root) %{_bindir}/qemu-mips
%attr(755,root,root) %{_bindir}/qemu-mipsel
%attr(755,root,root) %{_bindir}/qemu-or32
%attr(755,root,root) %{_bindir}/qemu-ppc
%attr(755,root,root) %{_bindir}/qemu-ppc64
%attr(755,root,root) %{_bindir}/qemu-ppc64abi32
%attr(755,root,root) %{_bindir}/qemu-s390x
%attr(755,root,root) %{_bindir}/qemu-sh4
%attr(755,root,root) %{_bindir}/qemu-sh4eb
%attr(755,root,root) %{_bindir}/qemu-sparc
%attr(755,root,root) %{_bindir}/qemu-sparc32plus
%attr(755,root,root) %{_bindir}/qemu-sparc64
%attr(755,root,root) %{_bindir}/qemu-unicore32

%files system-alpha
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-alpha

%files system-arm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-arm

%files system-cris
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-cris

%files system-lm32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-lm32

%files system-m68k
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-m68k

%files system-microblaze
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-microblaze
%attr(755,root,root) %{_bindir}/qemu-system-microblazeel

%files system-mips
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-mips
%attr(755,root,root) %{_bindir}/qemu-system-mipsel
%attr(755,root,root) %{_bindir}/qemu-system-mips64
%attr(755,root,root) %{_bindir}/qemu-system-mips64el

%files system-or32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-or32

%files system-ppc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-ppc
%attr(755,root,root) %{_bindir}/qemu-system-ppc64
%attr(755,root,root) %{_bindir}/qemu-system-ppcemb

%files system-s390x
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-s390x

%files system-sh4
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-sh4
%attr(755,root,root) %{_bindir}/qemu-system-sh4eb

%files system-sparc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-sparc
%attr(755,root,root) %{_bindir}/qemu-system-sparc64

%files system-unicore32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-unicore32

%files system-x86
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-i386
%attr(755,root,root) %{_bindir}/qemu-system-x86_64

%files system-xtensa
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-xtensa
%attr(755,root,root) %{_bindir}/qemu-system-xtensaeb
