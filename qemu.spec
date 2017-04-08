#
# Conditional build:
%bcond_without	sdl		# SDL UI and audio support
%bcond_without	gl		# Don't require gl deps
%bcond_without	ceph		# Ceph/RBD support
%bcond_without	glusterfs	# GlusterFS backend
%bcond_without	rdma		# RDMA-based migration support
%bcond_with	xseg		# Archipelago backend [non-distributable: GPLv3+ vs GPLv2-only]
%bcond_with	gtk2		# GTK+ 2.x instead of 3.x
%bcond_without	gtk3		# Do not build GTK+ UI
%bcond_without	vte		# VTE support in GTK+ UI
%bcond_without	spice		# SPICE support
%bcond_with	esd		# EsounD audio support
%bcond_without	oss		# OSS audio support
%bcond_without	pulseaudio	# PulseAudio audio support
%bcond_without	xen		# Xen backend driver support
%bcond_without	bluetooth	# bluetooth support
%bcond_without	brlapi		# brlapi support
%bcond_without	smartcard	# smartcard-nss support
%bcond_without	iscsi		# iscsi support
%bcond_without	libnfs		# NFS support
%bcond_without	seccomp		# seccomp support
%bcond_without	usbredir	# usb network redirection support
%bcond_without	system_seabios	# system seabios binary
%bcond_without	snappy		# snappy compression library
%bcond_without	user_static	# build linux-user static packages
%bcond_with	lttng		# lttng-ust trace backend support
%bcond_with	systemtap	# SystemTap/dtrace trace backend support

%if %{with gtk2}
%undefine with_gtk3
%endif

%ifarch x32
%undefine	with_xen
%endif

Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu
Version:	2.8.0
Release:	2
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://wiki.qemu-project.org/download/%{name}-%{version}.tar.bz2
# Source0-md5:	17940dce063b6ce450a12e719a6c9c43
Source2:	%{name}.binfmt
# Loads kvm kernel modules at boot
Source3:	kvm-modules-load.conf
# Creates /dev/kvm
Source4:	80-kvm.rules
# KSM control scripts
Source5:	ksm.service
Source6:	ksm.sysconfig
Source7:	ksmctl.c
Source8:	ksmtuned.service
Source9:	ksmtuned
Source10:	ksmtuned.conf
Source11:	%{name}-guest-agent.service
Source12:	99-%{name}-guest-agent.rules
Patch0:		%{name}-cflags.patch
Patch1:		vgabios-widescreens.patch
Patch2:		%{name}-whitelist.patch
Patch3:		%{name}-user-execve.patch
Patch4:		%{name}-xattr.patch
Patch5:		libjpeg-boolean.patch
Patch6:		x32.patch
URL:		http://www.qemu-project.org/
%{?with_gl:BuildRequires:	OpenGL-GLX-devel}
%{?with_gl:BuildRequires:	OpenGL-devel}
%{?with_sdl:BuildRequires:	SDL2-devel >= 2.0}
BuildRequires:	alsa-lib-devel
BuildRequires:	bcc >= 0.16.21-2
%{?with_bluetooth:BuildRequires:	bluez-libs-devel}
%{?with_brlapi:BuildRequires:	brlapi-devel}
BuildRequires:	bzip2-devel
%{?with_ceph:BuildRequires:	ceph-devel}
BuildRequires:	curl-devel
BuildRequires:	cyrus-sasl-devel >= 2
%{?with_esd:BuildRequires:	esound-devel}
BuildRequires:	glib2-devel >= 1:2.22
%{?with_glusterfs:BuildRequires:	glusterfs-devel >= 3.4}
BuildRequires:	gnutls-devel > 2.10.0
BuildRequires:	libaio-devel
%{?with_smartcard:BuildRequires:	libcacard-devel}
BuildRequires:	libcap-devel
BuildRequires:	libcap-ng-devel
%{?with_gl:BuildRequires:	libepoxy-devel}
BuildRequires:	libfdt-devel
%{?with_rdma:BuildRequires:	libibverbs-devel}
%{?with_iscsi:BuildRequires:	libiscsi-devel >= 1.9.0}
BuildRequires:	libjpeg-devel
%{?with_libnfs:BuildRequires:	libnfs-devel >= 1.9.3}
BuildRequires:	libpng-devel
%{?with_rdma:BuildRequires:	librdmacm-devel}
%{?with_seccomp:BuildRequires:	libseccomp-devel >= 2.1.1}
BuildRequires:	libssh2-devel >= 1.2.8
BuildRequires:	libusb-devel >= 1.0.13
BuildRequires:	libuuid-devel
%{?with_xseg:BuildRequires:	libxseg-devel}
%{?with_lttng:BuildRequires:	lttng-ust-devel}
BuildRequires:	lzo-devel >= 2
BuildRequires:	ncurses-devel
%{?with_smartcard:BuildRequires:	nss-devel >= 1:3.12.8}
BuildRequires:	numactl-devel
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pixman-devel >= 0.21.8
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpmbuild(macros) >= 1.644
%{?with_system_seabios:BuildRequires:	seabios}
BuildRequires:	sed >= 4.0
%{?with_snappy:BuildRequires:	snappy-devel}
%if %{with spice}
BuildRequires:	spice-protocol >= 0.12.3
BuildRequires:	spice-server-devel >= 0.12.0
%endif
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	texi2html
BuildRequires:	texinfo
%{?with_usbredir:BuildRequires:	usbredir-devel >= 0.6}
%{?with_lttng:BuildRequires:	userspace-rcu-devel}
BuildRequires:	vde2-devel
BuildRequires:	which
%{?with_xen:BuildRequires:	xen-devel >= 3.4}
BuildRequires:	xfsprogs-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
%if %{with gtk2}
BuildRequires:	gtk+2-devel >= 2:2.18.0
%{?with_vte:BuildRequires:	vte0-devel >= 0.24.0}
%endif
%if %{with gtk3}
BuildRequires:	gtk+3-devel >= 3.0.0
%{?with_vte:BuildRequires:	vte2.90-devel >= 0.32.0}
%endif
%if %{with user_static}
BuildRequires:	glib2-static
BuildRequires:	glibc-static
BuildRequires:	pcre-static
BuildRequires:	zlib-static
%endif
Requires:	%{name}-img = %{version}-%{release}
Requires:	%{name}-system-aarch64 = %{version}-%{release}
Requires:	%{name}-system-alpha = %{version}-%{release}
Requires:	%{name}-system-arm = %{version}-%{release}
Requires:	%{name}-system-cris = %{version}-%{release}
Requires:	%{name}-system-lm32 = %{version}-%{release}
Requires:	%{name}-system-m68k = %{version}-%{release}
Requires:	%{name}-system-microblaze = %{version}-%{release}
Requires:	%{name}-system-mips = %{version}-%{release}
Requires:	%{name}-system-moxie = %{version}-%{release}
Requires:	%{name}-system-or32 = %{version}-%{release}
Requires:	%{name}-system-ppc = %{version}-%{release}
Requires:	%{name}-system-s390x = %{version}-%{release}
Requires:	%{name}-system-sh4 = %{version}-%{release}
Requires:	%{name}-system-sparc = %{version}-%{release}
Requires:	%{name}-system-tricore = %{version}-%{release}
Requires:	%{name}-system-unicore32 = %{version}-%{release}
Requires:	%{name}-system-x86 = %{version}-%{release}
Requires:	%{name}-system-xtensa = %{version}-%{release}
Requires:	%{name}-user = %{version}-%{release}
Obsoletes:	qemu-kvm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	systempkg_req \
%if %{with sdl} \
Requires:	SDL2 \
%endif \
%if %{with seccomp} \
Requires:	libseccomp >= 2.1.0 \
%endif \
Requires:	libusb >= 1.0.13 \
Requires:	pixman >= 0.21.8 \
%if %{with usbredir} \
Requires:	usbredir >= 0.6 \
%endif \
%if %{with gtk2} \
Requires:	gtk+2 >= 2:2.18.0 \
%{?with_vte:Requires:	vte0 >= 0.24.0} \
%endif \
%if %{with gtk3} \
Requires:	gtk+3 >= 3.0.0 \
%{?with_vte:Requires:	vte2.90 >= 0.32.0} \
%endif

# don't strip/chrpath anything in there; these are boot images, roms etc
%define		_noautostrip	.*%{_datadir}/qemu/.*
%define		_noautochrpath	.*%{_datadir}/qemu/.*

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

%package common
Summary:	QEMU common files needed by all QEMU targets
Summary(pl.UTF-8):	Wspólne pliki QEMU wymagane przez wszystkie środowiska QEMU
Group:		Development/Tools
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	glib2 >= 1:2.22
%{?with_libnfs:Requires:	libnfs >= 1.9.3}
Requires:	libssh2 >= 1.2.8
Requires:	systemd-units >= 38
Provides:	group(qemu)
Provides:	user(qemu)
Obsoletes:	qemu-kvm-common
Conflicts:	qemu < 1.0-2

%description common
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets.

%description common -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet udostępnia wspólne pliki wymagane przez wszystkie
środowiska QEMU.

%package img
Summary:	QEMU command line tool for manipulating disk images
Summary(pl.UTF-8):	Narzędzie QEMU do operacji na obrazach dysków
Group:		Development/Tools
Obsoletes:	qemu-kvm-img
Conflicts:	qemu < 1.0-2

%description img
This package provides a command line tool for manipulating disk
images.

%description img -l pl.UTF-8
Ten pakiet udostępnia działające z linii poleceń narzędzia do operacji
na obrazach dysków.

%package user
Summary:	QEMU user mode emulation of qemu targets
Summary(pl.UTF-8):	QEMU - emulacja trybu użytkownika środowisk qemu
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
Requires(post,postun):	systemd-units >= 38
Requires:	systemd-units >= 38
Obsoletes:	qemu-kvm-user

%description user
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the user mode emulation of QEMU targets.

%description user -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet udostępnia emulację trybu użytkownika środowisk QEMU.

%package user-static
Summary:	QEMU user mode emulation of qemu targets static build
Group:		Development/Tools
Requires(post,postun):	systemd-units >= 38
Requires:	systemd-units >= 38

%description user-static
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets built as
static binaries

%package system-aarch64
Summary:	QEMU system emulator for AArch64
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem AArch64
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-aarch64

%description system-aarch64
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with AArch64 CPU.

%description system-aarch64 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem AArch64.

%package system-alpha
Summary:	QEMU system emulator for Alpha
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem Alpha
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-alpha

%description system-alpha
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with Alpha CPU.

%description system-alpha -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem Alpha.

%package system-arm
Summary:	QEMU system emulator for ARM
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem ARM
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-arm

%description system-arm
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for ARM.

%description system-arm -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem ARM.

%package system-cris
Summary:	QEMU system emulator for CRIS
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem CRIS
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-cris

%description system-cris
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with CRIS CPU.

%description system-cris -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem CRIS.

%package system-lm32
Summary:	QEMU system emulator for LM32
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem LM32
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-lm32

%description system-lm32
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with LM32 CPU.

%description system-lm32 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem LM32.

%package system-m68k
Summary:	QEMU system emulator for m68k
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem m68k
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-m68k

%description system-m68k
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with m68k CPU.

%description system-m68k -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem m68k.

%package system-microblaze
Summary:	QEMU system emulator for MicroBlaze
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem MicroBlaze
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-microblaze

%description system-microblaze
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with MicroBlaze CPU.

%description system-microblaze -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem MicroBlaze.

%package system-mips
Summary:	QEMU system emulator for MIPS
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem MIPS
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-mips

%description system-mips
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with MIPS CPU.

%description system-mips -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem MIPS.

%package system-moxie
Summary:	QEMU system emulator for Moxie
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem Moxie
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req

%description system-moxie
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with Moxie CPU.

%description system-moxie -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem Moxie.

%package system-or32
Summary:	QEMU system emulator for OpenRISC
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem OpenRISC
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-or32

%description system-or32
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with OpenRISC CPU.

%description system-or32 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem OpenRISC.

%package system-ppc
Summary:	QEMU system emulator for PowerPC
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem PowerPC
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-ppc

%description system-ppc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with PowerPC CPU.

%description system-ppc -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem PowerPC.

%package system-s390x
Summary:	QEMU system emulator for S390
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem S390
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-s390x

%description system-s390x
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with S390 CPU.

%description system-s390x -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem S390.

%package system-sh4
Summary:	QEMU system emulator for SH4
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem SH4
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-sh4

%description system-sh4
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with SH4 CPU.

%description system-sh4 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem SH4.

%package system-sparc
Summary:	QEMU system emulator for SPARC
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem SPARC
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-sparc

%description system-sparc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with SPARC/SPARC64 CPU.

%description system-sparc -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem SPARC/SPARC64.

%package system-tricore
Summary:	QEMU system emulator for TriCore
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem TriCore
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req

%description system-tricore
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with TriCore CPU.

%description system-sparc -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem TriCore.

%package system-unicore32
Summary:	QEMU system emulator for UniCore32
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem UniCore32
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-unicore32

%description system-unicore32
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with UniCore32 CPU.

%description system-unicore32 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem UniCore32.

%package system-x86
Summary:	QEMU system emulator for x86
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem x86
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%{?with_system_seabios:Requires:	seabios}
%systempkg_req
Obsoletes:	kvm
Obsoletes:	qemu-kvm-system-x86

%description system-x86
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

%description system-x86 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

%package system-xtensa
Summary:	QEMU system emulator for Xtensa
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem Xtensa
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-xtensa

%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with Xtensa CPU.

%description system-xtensa -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem Xtensa.

%package guest-agent
Summary:	QEMU guest agent
Summary(pl.UTF-8):	Agent gościa QEMU
Group:		Daemons
Requires(post,preun,postun):	systemd-units >= 38
Requires:	glib2 >= 1:2.22
Requires:	systemd-units >= 38
Obsoletes:	qemu-kvm-guest-agent

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which
communicates with the host over a virtio-serial channel named
"org.qemu.guest_agent.0".

This package does not need to be installed on the host OS.

%description guest-agent -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet udostępnia agenta przeznaczonego do uruchomienia w
systemach-gościach, komunikującego się kanałem virtio-serial o nazwie
"org.qemu.guest_agent.0".

Ten pakiet nie musi być zainstalowany w systemie hosta.

%package module-block-archipelago
Summary:	QEMU module for Archipelago block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych Archipelago
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description module-block-archipelago
Archipelago block device support for QEMU.

%description module-block-archipelago -l pl.UTF-8
Moduł QEMU dla urządeń blokowych Archipelago.

%package module-block-curl
Summary:	QEMU module for 'curl' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'curl'
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description module-block-curl
'curl' block device support for QEMU.

%description module-block-curl -l pl.UTF-8
Moduł QEMU dla urządeń blokowych typu 'curl'.

%package module-block-gluster
Summary:	QEMU module for 'gluster' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'gluster'
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
Requires:	glusterfs-libs >= 3.4

%description module-block-gluster
'gluster' block device support for QEMU.

%description module-block-gluster -l pl.UTF-8
Moduł QEMU dla urządeń blokowych typu 'gluster'.

%package module-block-iscsi
Summary:	QEMU module for 'iscsi' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'iscsi'
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
Requires:	libiscsi >= 1.9.0

%description module-block-iscsi
'iscsi' block device support for QEMU.

%description module-block-iscsi -l pl.UTF-8
Moduł QEMU dla urządeń blokowych typu 'iscsi'.

%package module-block-rbd
Summary:	QEMU module for 'rbd' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'rbd'
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description module-block-rbd
'rbd' block device support for QEMU.

%description module-block-rbd -l pl.UTF-8
Moduł QEMU dla urządeń blokowych typu 'rbd'.

%package module-block-ssh
Summary:	QEMU module for 'ssh' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'ssh'
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description module-block-ssh
'ssh' block device support for QEMU.

%description module-block-ssh -l pl.UTF-8
Moduł QEMU dla urządeń blokowych typu 'ssh'.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# workaround for conflict with alsa/error.h
ln -s ../error.h qapi/error.h

%build

build() {
	local target=$1
	shift

	install -d build-$target
	cd build-$target

	../configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=%{_localstatedir} \
	--interp-prefix=%{_libdir}/qemu/lib-%%M \
	--cc="%{__cc}" \
	--host-cc="%{__cc}" \
	--disable-strip \
	--enable-trace-backends="nop%{?with_systemtap:,dtrace}%{?with_lttng:,ust}" \
	--enable-kvm \
	"$@"

	%{__make} \
		V=1 \
		%{!?with_smartcard:CONFIG_USB_SMARTCARD=n}

	cd ..
}

build dynamic \
	--extra-cflags="%{rpmcflags} %{rpmcppflags} -fPIE -DPIE" \
	--extra-ldflags="%{rpmldflags} -pie -Wl,-z,relro -Wl,-z,now" \
	%{__enable_disable xseg archipelago} \
	--enable-attr \
	%{__enable_disable bluetooth bluez} \
	%{__enable_disable brlapi} \
	--enable-cap-ng \
	--enable-curl \
	--enable-curses \
	--enable-docs \
	--enable-fdt \
	%{__enable_disable glusterfs} \
	%{__enable_disable iscsi libiscsi} \
	%{__enable_disable ceph rbd} \
	%{__enable_disable rdma} \
	%{__enable_disable sdl} \
	--with-sdlabi=2.0 \
	%{__enable_disable seccomp} \
	%{__enable_disable spice} \
	%{__enable_disable smartcard smartcard} \
	--enable-tpm \
	%{__enable_disable usbredir usb-redir} \
	--enable-uuid \
	--enable-vde \
	--enable-virtfs \
	--enable-vnc-jpeg \
	--enable-vnc-png \
	--enable-vnc-sasl \
	%{!?with_vte:--disable-vte} \
	%{__enable_disable xen} \
	--enable-modules \
	--disable-netmap \
	%{__enable_disable libnfs} \
	--enable-lzo \
	%{__enable_disable snappy} \
	--audio-drv-list="alsa%{?with_iss:,oss}%{?with_sdl:,sdl}%{?with_esd:,esd}%{?with_pulseaudio:,pa}" \
%if %{without gtk2} && %{without gtk3}
	--disable-gtk
%else
	--with-gtkabi="%{?with_gtk2:2.0}%{!?with_gtk2:3.0}"
%endif

%if %{with user_static}
build static \
	--disable-brlapi \
	--disable-cap-ng \
	--disable-curl \
	--disable-curses \
	--disable-gcrypt \
	--disable-gnutls \
	--disable-gtk \
	--disable-guest-agent \
	--disable-guest-agent-msi \
	--disable-libnfs \
	--disable-nettle \
	--disable-pie \
	--disable-sdl \
	--disable-spice \
	--disable-tcmalloc \
	--disable-tools \
	--disable-uuid \
	--enable-user \
	--disable-system \
	--static

%endif

# rebuild patched vesa tables with additional widescreen modes.
%{__make} -C roms/vgabios stdvga-bios

%{__cc} %{SOURCE7} %{rpmcflags} -o ksmctl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{systemdunitdir},/usr/lib/binfmt.d} \
	$RPM_BUILD_ROOT/etc/{qemu,sysconfig,udev/rules.d,modules-load.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/sasl,%{_sbindir}}

%if %{with user_static}
%{__make} -C build-static install \
	%{!?with_smartcard:CONFIG_USB_SMARTCARD=n} \
	DESTDIR=$RPM_BUILD_ROOT

# Give all QEMU user emulators a -static suffix
for src in $RPM_BUILD_ROOT%{_bindir}/qemu-*; do
	mv $src $src-static
done

%endif

%{__make} -C build-dynamic install \
	%{!?with_smartcard:CONFIG_USB_SMARTCARD=n} \
	DESTDIR=$RPM_BUILD_ROOT

echo "#allow br0" > $RPM_BUILD_ROOT/etc/qemu/bridge.conf

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ifup
#!/bin/sh

EOF

install -p qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl/qemu.conf

%ifarch %{ix86} %{x8664} x32
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/modules-load.d/kvm.conf
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
%endif

install -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/ksm.service
install -p %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/ksm
install -p ksmctl $RPM_BUILD_ROOT%{_sbindir}

install -p %{SOURCE8} $RPM_BUILD_ROOT%{systemdunitdir}/ksmtuned.service
install -p %{SOURCE9} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -p %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
install -p %{SOURCE11} $RPM_BUILD_ROOT%{systemdunitdir}
install -p %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

# Install binfmt
for i in dummy \
%ifnarch %{ix86} %{x8664} x32
	qemu-i386 \
%endif
%ifnarch alpha
	qemu-alpha \
%endif
%ifnarch %{arm}
	qemu-arm \
%endif
	qemu-armeb \
	qemu-cris \
	qemu-microblaze qemu-microblazeel \
%ifnarch mips64
	qemu-mips64 \
%ifnarch mips
	qemu-mips \
%endif
%endif
%ifnarch mips64el
	qemu-mips64el \
%ifnarch mipsel
	qemu-mipsel \
%endif
%endif
%ifnarch m68k
	qemu-m68k \
%endif
%ifnarch ppc ppc64 ppc64le
	qemu-ppc qemu-ppc64abi32 qemu-ppc64 \
%endif
%ifnarch sparc sparc64
	qemu-sparc qemu-sparc32plus qemu-sparc64 \
%endif
%ifnarch s390 s390x
	qemu-s390x \
%endif
%ifnarch sh4
	qemu-sh4 \
%endif
	qemu-sh4eb \
; do
	test $i = dummy && continue
	grep /$i:\$ %{SOURCE2} > $RPM_BUILD_ROOT/usr/lib/binfmt.d/$i-dynamic.conf

	%if %{with user_static}
	grep /$i:\$ %{SOURCE2} > $RPM_BUILD_ROOT/usr/lib/binfmt.d/$i-static.conf
	%{__sed} -i -e "s/$i/$i-static/" $RPM_BUILD_ROOT/usr/lib/binfmt.d/$i-static.conf
	%endif
done < %{SOURCE2}

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-doc.html
%{__rm} $RPM_BUILD_ROOT%{_docdir}/qemu/qmp-commands.txt

# install patched vesa tables with additional widescreen modes.
cp -p roms/vgabios/VGABIOS-lgpl-latest.stdvga.bin $RPM_BUILD_ROOT%{_datadir}/%{name}/vgabios-stdvga.bin

%if %{with system_seabios}
ln -sf /usr/share/seabios/bios.bin $RPM_BUILD_ROOT%{_datadir}/%{name}/bios-256k.bin
# bios.bin provided by qemu is stripped to 128k, with no Xen support, keep it
for f in $RPM_BUILD_ROOT%{_datadir}/%{name}/*.aml ; do
	bn="$(basename $f)"
	if [ -e "/usr/share/seabios/$bn" ] ; then
		ln -sf "/usr/share/seabios/$bn" "$f"
	fi
done
%endif

%if %{with gtk2} || %{with gtk3}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{de_DE,de}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{fr_FR,fr}
%find_lang %{name}
%else
: > qemu.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
%groupadd -g 160 kvm
%groupadd -g 276 qemu
%useradd -u 276 -g qemu -G kvm -c "QEMU User" qemu

%post common
%systemd_post ksm.service
%systemd_post ksmtuned.service

%preun common
%systemd_preun ksm.service
%systemd_preun ksmtuned.service

%postun common
if [ "$1" = "0" ]; then
	%userremove qemu
	%groupremove qemu
	%groupremove kvm
fi
%systemd_reload

%triggerpostun common -- qemu-common < 1.6.1-4
%systemd_trigger ksm.service
%systemd_trigger ksmtuned.service

%post user
%systemd_service_restart systemd-binfmt.service

%postun user
%systemd_service_restart systemd-binfmt.service

%post user-static
%systemd_service_restart systemd-binfmt.service

%postun user-static
%systemd_service_restart systemd-binfmt.service

%post guest-agent
%systemd_reload

%preun guest-agent
%systemd_preun qemu-guest-agent.service

%postun guest-agent
%systemd_reload

%files
%defattr(644,root,root,755)

%files common -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENSE README
%doc build-dynamic/qemu-doc.html
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%config(noreplace) %verify(not md5 mtime size) /etc/ksmtuned.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sasl/qemu.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ksm
%dir /etc/qemu
%attr(640,root,qemu) %config(noreplace) %verify(not md5 mtime size) /etc/qemu/bridge.conf
%{systemdunitdir}/ksm.service
%{systemdunitdir}/ksmtuned.service
%attr(755,root,root) %{_bindir}/ivshmem-client
%attr(755,root,root) %{_bindir}/ivshmem-server
%attr(755,root,root) %{_bindir}/virtfs-proxy-helper
%attr(755,root,root) %{_bindir}/qemu-nbd
%attr(755,root,root) %{_bindir}/qemu-tilegx
%attr(755,root,root) %{_libdir}/qemu-bridge-helper
%attr(755,root,root) %{_sbindir}/ksmctl
%attr(755,root,root) %{_sbindir}/ksmtuned
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man8/qemu-nbd.8*

%dir %{_datadir}/qemu
%{_datadir}/%{name}/keymaps
%{_datadir}/%{name}/qemu-icon.bmp
%{_datadir}/%{name}/trace-events-all

# various bios images
# all should be probably moved to the right system subpackage
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/efi-e1000e.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/efi-eepro100.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/efi-vmxnet3.rom
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/linuxboot_dma.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/openbios-ppc
%{_datadir}/%{name}/openbios-sparc*
%{_datadir}/%{name}/palcode-clipper
%{_datadir}/%{name}/petalogix-ml605.dtb
%{_datadir}/%{name}/petalogix-s3adsp1800.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/pxe-eepro100.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/QEMU,cgthree.bin
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/s390-ccw.img
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/slof.bin
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/vgabios-vmware.bin

%dir %{_libdir}/%{name}

# modules without too many external dependencies
%attr(755,root,root) %{_libdir}/%{name}/block-dmg-bz2.so
%attr(755,root,root) %{_libdir}/%{name}/block-nfs.so

%files img
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%files user
%defattr(644,root,root,755)
/usr/lib/binfmt.d/qemu-*-dynamic.conf
%attr(755,root,root) %{_bindir}/qemu-aarch64
%attr(755,root,root) %{_bindir}/qemu-alpha
%attr(755,root,root) %{_bindir}/qemu-arm
%attr(755,root,root) %{_bindir}/qemu-armeb
%attr(755,root,root) %{_bindir}/qemu-cris
%attr(755,root,root) %{_bindir}/qemu-i386
%attr(755,root,root) %{_bindir}/qemu-io
%attr(755,root,root) %{_bindir}/qemu-m68k
%attr(755,root,root) %{_bindir}/qemu-microblaze
%attr(755,root,root) %{_bindir}/qemu-microblazeel
%attr(755,root,root) %{_bindir}/qemu-mips
%attr(755,root,root) %{_bindir}/qemu-mipsel
%attr(755,root,root) %{_bindir}/qemu-mips64
%attr(755,root,root) %{_bindir}/qemu-mips64el
%attr(755,root,root) %{_bindir}/qemu-mipsn32
%attr(755,root,root) %{_bindir}/qemu-mipsn32el
%attr(755,root,root) %{_bindir}/qemu-or32
%attr(755,root,root) %{_bindir}/qemu-ppc
%attr(755,root,root) %{_bindir}/qemu-ppc64
%attr(755,root,root) %{_bindir}/qemu-ppc64abi32
%attr(755,root,root) %{_bindir}/qemu-ppc64le
%attr(755,root,root) %{_bindir}/qemu-s390x
%attr(755,root,root) %{_bindir}/qemu-sh4
%attr(755,root,root) %{_bindir}/qemu-sh4eb
%attr(755,root,root) %{_bindir}/qemu-sparc
%attr(755,root,root) %{_bindir}/qemu-sparc32plus
%attr(755,root,root) %{_bindir}/qemu-sparc64
%attr(755,root,root) %{_bindir}/qemu-x86_64

%if %{with user_static}
%files user-static
%defattr(644,root,root,755)
/usr/lib/binfmt.d/qemu-*-static.conf
%attr(755,root,root) %{_bindir}/qemu-aarch64-static
%attr(755,root,root) %{_bindir}/qemu-alpha-static
%attr(755,root,root) %{_bindir}/qemu-arm-static
%attr(755,root,root) %{_bindir}/qemu-armeb-static
%attr(755,root,root) %{_bindir}/qemu-cris-static
%attr(755,root,root) %{_bindir}/qemu-i386-static
%attr(755,root,root) %{_bindir}/qemu-m68k-static
%attr(755,root,root) %{_bindir}/qemu-microblaze-static
%attr(755,root,root) %{_bindir}/qemu-microblazeel-static
%attr(755,root,root) %{_bindir}/qemu-mips-static
%attr(755,root,root) %{_bindir}/qemu-mips64-static
%attr(755,root,root) %{_bindir}/qemu-mips64el-static
%attr(755,root,root) %{_bindir}/qemu-mipsel-static
%attr(755,root,root) %{_bindir}/qemu-mipsn32-static
%attr(755,root,root) %{_bindir}/qemu-mipsn32el-static
%attr(755,root,root) %{_bindir}/qemu-or32-static
%attr(755,root,root) %{_bindir}/qemu-ppc-static
%attr(755,root,root) %{_bindir}/qemu-ppc64-static
%attr(755,root,root) %{_bindir}/qemu-ppc64abi32-static
%attr(755,root,root) %{_bindir}/qemu-ppc64le-static
%attr(755,root,root) %{_bindir}/qemu-s390x-static
%attr(755,root,root) %{_bindir}/qemu-sh4-static
%attr(755,root,root) %{_bindir}/qemu-sh4eb-static
%attr(755,root,root) %{_bindir}/qemu-sparc-static
%attr(755,root,root) %{_bindir}/qemu-sparc32plus-static
%attr(755,root,root) %{_bindir}/qemu-sparc64-static
%attr(755,root,root) %{_bindir}/qemu-tilegx-static
%attr(755,root,root) %{_bindir}/qemu-x86_64-static
%endif

%files system-aarch64
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-aarch64

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

%files system-moxie
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-moxie

%files system-or32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-or32

%files system-ppc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-ppc
%attr(755,root,root) %{_bindir}/qemu-system-ppc64
#%attr(755,root,root) %{_bindir}/qemu-system-ppc64le
%attr(755,root,root) %{_bindir}/qemu-system-ppcemb
%{_datadir}/%{name}/u-boot.e500

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

%files system-tricore
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-tricore

%files system-unicore32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-unicore32

%files system-x86
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-i386
%attr(755,root,root) %{_bindir}/qemu-system-x86_64
%ifarch %{ix86} %{x8664} x32
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/kvm.conf
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/80-kvm.rules
%endif
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/acpi-dsdt.aml

%files system-xtensa
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-xtensa
%attr(755,root,root) %{_bindir}/qemu-system-xtensaeb

%files guest-agent
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/99-qemu-guest-agent.rules
%{systemdunitdir}/qemu-guest-agent.service
%attr(755,root,root) %{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*

%if %{with xseg}
%files module-block-archipelago
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-archipelago.so
%endif

%files module-block-curl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-curl.so

%if %{with glusterfs}
%files module-block-gluster
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-gluster.so
%endif

%if %{with iscsi}
%files module-block-iscsi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-iscsi.so
%endif

%if %{with ceph}
%files module-block-rbd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-rbd.so
%endif

%files module-block-ssh
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-ssh.so
