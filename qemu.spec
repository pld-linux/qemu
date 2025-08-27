# TODO:
# plugins? (probes)
#
# Conditional build:
%bcond_without	sdl		# SDL UI and audio support
%bcond_without	opengl		# Don't require GL deps
%bcond_with	canokey		# CanoKey support
%bcond_without	ceph		# Ceph/RBD support
%bcond_without	glusterfs	# GlusterFS backend
%bcond_without	rdma		# RDMA-based migration support
%bcond_without	gtk3		# Do not build GTK+ UI
%bcond_without	vte		# VTE support in GTK+ UI
%bcond_without	spice		# SPICE support
%bcond_without	oss		# OSS audio support
%bcond_without	pulseaudio	# PulseAudio audio support
%bcond_without	xen		# Xen backend driver support
%bcond_without	brlapi		# brlapi support
%bcond_without	smartcard	# smartcard-nss support
%bcond_without	iscsi		# iscsi support
%bcond_without	libnfs		# NFS support
%bcond_without	multipath	# Multipath support
%bcond_without	pmem		# libpmem (persistent memory) support
%bcond_without	seccomp		# seccomp support
%bcond_without	usbredir	# usb network redirection support
%bcond_without	system_seabios	# system seabios binary
%bcond_without	snappy		# snappy compression library
%bcond_without	user_static	# build linux-user static packages
%bcond_with	vfio_user	# vfio-user server support
%bcond_with	lttng		# lttng-ust trace backend support [needs update]
%bcond_without	systemtap	# SystemTap/dtrace trace backend support
%bcond_without	virgl		# build virgl support
%bcond_without	xkbcommon	# xkbcommon support
%bcond_without	qatzip	# QATzip support

%if %{without gtk3}
%undefine	with_vte
%endif
%ifarch x32
%undefine	with_xen
%endif
%ifnarch %{x8664} aarch64
%undefine	with_pmem
%endif
%ifnarch %{ix86} %{x8664} x32
%undefine	with_qatzip
%endif

Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu
Version:	10.0.3
Release:	2
License:	GPL v2, BSD (edk2 firmware files)
Group:		Applications/Emulators
Source0:	https://download.qemu.org/%{name}-%{version}.tar.xz
# Source0-md5:	4a244f485c9d7ac3d40f958f13eae298
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
Source13:	%{name}-guest-agent.init
Source14:	%{name}-guest-agent.logrotate
Source15:	%{name}-pr-helper.service
Source16:	%{name}-pr-helper.socket
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-user-execve.patch
Patch3:		libjpeg-boolean.patch
Patch5:		%{name}-u2f-emu.patch
Patch6:		%{name}-linux-mount.patch
Patch7:		libvfio-user-types.patch
Patch8:		libvfio-user-alloca.patch
URL:		https://www.qemu.org/
%{?with_opengl:BuildRequires:	Mesa-libgbm-devel}
%{?with_opengl:BuildRequires:	OpenGL-GLX-devel}
%{?with_opengl:BuildRequires:	OpenGL-devel}
%{?with_qatzip:BuildRequires:	QATzip-devel}
%{?with_sdl:BuildRequires:	SDL2-devel >= 2.0}
%{?with_sdl:BuildRequires:	SDL2_image-devel >= 2.0}
BuildRequires:	alsa-lib-devel
BuildRequires:	bison
%{?with_brlapi:BuildRequires:	brlapi-devel}
BuildRequires:	bzip2-devel
%{?with_canokey:BuildRequires:	canokey-qemu-devel}
BuildRequires:	capstone-devel >= 4.0
%{?with_ceph:BuildRequires:	ceph-devel >= 12}
BuildRequires:	curl-devel >= 7.29.0
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	daxctl-devel >= 57
BuildRequires:	flex
BuildRequires:	gcc >= 6:7.4
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.75.3
# minimal is 3.4 but new features are used up to 6
%{?with_glusterfs:BuildRequires:	glusterfs-devel >= 6}
BuildRequires:	gnutls-devel >= 3.6.14
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.22.0}
BuildRequires:	jack-audio-connection-kit-devel
%{?with_vfio_user:BuildRequires:	json-c-devel >= 0.11}
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel >= 0.3.111
BuildRequires:	libblkio-devel >= 1.3.0
BuildRequires:	libbpf-devel >= 1.1.0
%{?with_smartcard:BuildRequires:	libcacard-devel >= 2.5.1}
BuildRequires:	libcap-ng-devel
BuildRequires:	libcbor-devel >= 0.7.0
BuildRequires:	libdrm-devel
%{?with_opengl:BuildRequires:	libepoxy-devel}
BuildRequires:	libfdt-devel >= 1.5.1
BuildRequires:	libfuse3-devel >= 3.8
%{?with_rdma:BuildRequires:	libibumad-devel}
%{?with_rdma:BuildRequires:	libibverbs-devel}
%{?with_iscsi:BuildRequires:	libiscsi-devel >= 1.9.0}
BuildRequires:	libjpeg-devel
%{?with_libnfs:BuildRequires:	libnfs-devel >= 1.9.3}
BuildRequires:	libpng-devel >= 2:1.6.34
%{?with_rdma:BuildRequires:	librdmacm-devel}
%{?with_seccomp:BuildRequires:	libseccomp-devel >= 2.3.0}
BuildRequires:	libselinux-devel
BuildRequires:	libslirp-devel >= 4.7
BuildRequires:	libssh-devel >= 0.8.7
BuildRequires:	libstdc++-devel >= 6:4.7
# for tests only
#BuildRequires:	libtasn1-devel
BuildRequires:	libu2f-emu-devel
BuildRequires:	liburing-devel >= 2.2
BuildRequires:	libusb-devel >= 1.0.22
BuildRequires:	libuuid-devel
BuildRequires:	libxdp-devel >= 1.4.0
BuildRequires:	libxml2-devel >= 2.0
%{?with_lttng:BuildRequires:	lttng-ust-devel >= 2.1}
BuildRequires:	lzfse-devel
BuildRequires:	lzo-devel >= 2
BuildRequires:	meson >= 1.5.0
%{?with_multipath:BuildRequires:	multipath-tools-devel}
BuildRequires:	ncurses-devel
# also libgcrypt-devel >= 1.8 possible, but gnutls already pulls nettle
BuildRequires:	nettle-devel >= 3.9
BuildRequires:	ninja >= 1.5
%{?with_smartcard:BuildRequires:	nss-devel >= 1:3.12.8}
BuildRequires:	numactl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pipewire-devel >= 0.3.60
BuildRequires:	pixman-devel >= 0.21.8
BuildRequires:	pkgconfig
%{?with_pmem:BuildRequires:	pmdk-devel}
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-distlib
BuildRequires:	python3-pycotap >= 1.1.0
BuildRequires:	python3-sphinx_rtd_theme >= 0.5
BuildRequires:	python3-tomli >= 1.2.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.644
%{?with_system_seabios:BuildRequires:	seabios}
BuildRequires:	sed >= 4.0
%{?with_snappy:BuildRequires:	snappy-devel}
BuildRequires:	sphinx-pdg >= 3.4.3
%if %{with spice}
BuildRequires:	spice-protocol >= 0.14.0
BuildRequires:	spice-server-devel >= 0.14.0
%endif
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	tar >= 1:1.22
BuildRequires:	texi2html
BuildRequires:	texinfo
%{?with_multipath:BuildRequires:	udev-devel}
%{?with_usbredir:BuildRequires:	usbredir-devel >= 0.6}
%{?with_lttng:BuildRequires:	userspace-rcu-devel}
BuildRequires:	vde2-devel
%{?with_virgl:BuildRequires:	virglrenderer-devel}
%{?with_vte:BuildRequires:	vte-devel >= 0.32.0}
BuildRequires:	which
# xencontrol xenstore xenguest xenforeignmemory xengnttab xenevtchn xendevicemodel; xentoolcore for xen 4.10+
# min version is 4.2, more features up to 4.11
%{?with_xen:BuildRequires:	xen-devel >= 4.11}
BuildRequires:	xfsprogs-devel
%if %{with xkbcommon}
BuildRequires:	xkeyboard-config
BuildRequires:	xorg-lib-libxkbcommon-devel
%endif
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 1.4.0
%if %{with user_static}
BuildRequires:	glib2-static >= 1:2.75.3
BuildRequires:	glibc-static
BuildRequires:	libatomic-static
BuildRequires:	libstdc++-static >= 6:4.7
BuildRequires:	pcre2-8-static >= 10.32
BuildRequires:	zlib-static
%endif
Requires:	%{name}-img = %{version}-%{release}
%ifnarch %{ix86} x32
Requires:	%{name}-system-aarch64 = %{version}-%{release}
Requires:	%{name}-system-alpha = %{version}-%{release}
Requires:	%{name}-system-hppa = %{version}-%{release}
Requires:	%{name}-system-microblaze = %{version}-%{release}
Requires:	%{name}-system-s390x = %{version}-%{release}
%endif
Requires:	%{name}-system-arm = %{version}-%{release}
Requires:	%{name}-system-avr = %{version}-%{release}
Requires:	%{name}-system-m68k = %{version}-%{release}
Requires:	%{name}-system-mips = %{version}-%{release}
Requires:	%{name}-system-or1k = %{version}-%{release}
Requires:	%{name}-system-ppc = %{version}-%{release}
Requires:	%{name}-system-riscv = %{version}-%{release}
Requires:	%{name}-system-rx = %{version}-%{release}
Requires:	%{name}-system-sh4 = %{version}-%{release}
Requires:	%{name}-system-sparc = %{version}-%{release}
Requires:	%{name}-system-tricore = %{version}-%{release}
Requires:	%{name}-system-x86 = %{version}-%{release}
Requires:	%{name}-system-xtensa = %{version}-%{release}
Requires:	%{name}-user = %{version}-%{release}
Obsoletes:	qemu-kvm < 2
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	systempkg_req \
Requires:	capstone >= 4.0 \
Requires:	daxctl-libs >= 57 \
Requires:	libaio >= 0.3.111 \
Requires:	libbpf >= 1.1.0 \
%{?with_smartcard:Requires:	libcacard >= 2.5.1} \
Requires:	libfdt >= 1.5.1 \
Requires:	libfuse3 >= 3.8 \
%{?with_iscsi:Requires:	libiscsi >= 1.9.0} \
Requires:	libpng >= 2:1.6.34 \
%if %{with seccomp} \
Requires:	libseccomp >= 2.3.0 \
%endif \
Requires:	libslirp >= 4.7 \
Requires:	liburing >= 2.2 \
Requires:	libusb >= 1.0.22 \
Requires:	libxdp >= 1.4.0 \
Requires:	pixman >= 0.21.8 \
%if %{with spice} \
Requires:	spice-server-libs >= 0.14.0 \
%endif \
%if %{with usbredir} \
Requires:	usbredir >= 0.6 \
%endif

# don't strip/chrpath anything in there; these are boot images, roms etc
%define		_noautostrip	.*%{_datadir}/qemu/.*
%define		_noautochrpath	.*%{_datadir}/qemu/.*

# include/qemu/osdep.h:290: #error building with NDEBUG is not supported
%define		filterout	-DNDEBUG

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

%package devel
Summary:	Header file for QEMU plugins development
Summary(pl.UTF-8):	Plik nagłówkowy do tworzenia wtyczek QEMU
Group:		Development/Libraries
BuildArch:	noarch

%description devel
Header file for QEMU plugins development.

%description devel -l pl.UTF-8
Plik nagłówkowy do tworzenia wtyczek QEMU.

%package common
Summary:	QEMU common files needed by all QEMU targets
Summary(pl.UTF-8):	Wspólne pliki QEMU wymagane przez wszystkie środowiska QEMU
Group:		Applications/Emulators
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	glib2 >= 1:2.75.3
Requires:	gnutls-libs >= 3.6.14
%{?with_gtk3:Requires:	gtk+3 >= 3.22.0}
Requires:	libaio >= 0.3.111
Requires:	libblkio >= 1.3.0
Requires:	liburing >= 2.2
Requires:	nettle >= 3.9
Requires:	systemd-units >= 38
%{?with_vte:Requires:	vte >= 0.32.0}
Requires:	zstd >= 1.4.0
Suggests:	virtiofsd
Provides:	group(qemu)
Provides:	user(qemu)
Obsoletes:	qemu-kvm-common < 2
Obsoletes:	qemu-module-block-archipelago < 2.9.0
Obsoletes:	qemu-system-cris < 10.0.0
Obsoletes:	qemu-system-lm32 < 5.2
Obsoletes:	qemu-system-moxie < 6.1
Obsoletes:	qemu-system-nios2 < 10.0.0
Obsoletes:	qemu-system-unicore32 < 5.2
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
Group:		Applications/Emulators
Requires:	libaio >= 0.3.111
Requires:	liburing >= 2.2
Obsoletes:	qemu-kvm-img < 2
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
Group:		Applications/Emulators
Requires(post,postun):	systemd-units >= 38
Requires:	%{name}-common = %{version}-%{release}
Requires:	libaio >= 0.3.111
Requires:	liburing >= 2.2
Requires:	systemd-units >= 38
Obsoletes:	qemu-kvm-user < 2

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
Summary(pl.UTF-8):	QEMU - emulacja trybu użytkownika środowisk qemu - wersja statyczna
Group:		Applications/Emulators
Requires(post,postun):	systemd-units >= 38
Requires:	systemd-units >= 38

%description user-static
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets built as
static binaries.

%description user-static -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet udostępnia emulację trybu użytkownika środowisk QEMU w
oparciu o programy wykonywalne zbudowane statycznie.

%package system-aarch64
Summary:	QEMU system emulator for AArch64
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem AArch64
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-aarch64 < 2

%description system-aarch64
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with AArch64 (ARM64) CPU.

%description system-aarch64 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem AArch64 (ARM64).

%package system-alpha
Summary:	QEMU system emulator for Alpha
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem Alpha
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-alpha < 2

%description system-alpha
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with Alpha CPU.

%description system-alpha -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem Alpha.

%package system-arm
Summary:	QEMU system emulator for 32-bit ARM
Summary(pl.UTF-8):	QEMU - emulator systemu z 32-bitowym procesorem ARM
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-arm < 2

%description system-arm
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for 32-bit ARM.

%description system-arm -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z 32-bitowym procesorem ARM.

%package system-avr
Summary:	QEMU system emulator for AVR
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem AVR
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-avr < 2

%description system-avr
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for AVR.

%description system-avr -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem AVR.

%package system-hppa
Summary:	QEMU system emulator for HP/PA
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem HP/PA
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req

%description system-hppa
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with HP/PA (PA-RISC) CPU.

%description system-hppa -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem HP/PA (PA-RISC).

%package system-m68k
Summary:	QEMU system emulator for m68k
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem m68k
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-m68k < 2

%description system-m68k
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with m68k (Motorola 68xxx)
CPU.

%description system-m68k -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem m68k (Motorola
68xxx).

%package system-microblaze
Summary:	QEMU system emulator for MicroBlaze
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem MicroBlaze
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-microblaze < 2

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
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-mips < 2

%description system-mips
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with MIPS CPU.

%description system-mips -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem MIPS.

%package system-or1k
Summary:	QEMU system emulator for OpenRISC
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem OpenRISC
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-or1k < 2
Obsoletes:	qemu-system-or32 < 2.9.0

%description system-or1k
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with OpenRISC CPU.

%description system-or1k -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem OpenRISC.

%package system-ppc
Summary:	QEMU system emulator for PowerPC
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem PowerPC
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-ppc < 2

%description system-ppc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with PowerPC CPU.

%description system-ppc -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem PowerPC.

%package system-riscv
Summary:	QEMU system emulator for RISC-V
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem RISC-V
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Obsoletes:	qemu-system-riscv32 < 10.0.0
Obsoletes:	qemu-system-riscv64 < 10.0.0
%systempkg_req

%description system-riscv
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with RISC-V CPUs.

%description system-riscv -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorami RISC-V.

%package system-rx
Summary:	QEMU system emulator for Renesas RX
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem Renesas RX
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req

%description system-rx
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with Renesas RX CPU.

%description system-rx -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem Renesas RX.

%package system-s390x
Summary:	QEMU system emulator for S390x (IBM Z)
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem S390x (IBM Z)
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-s390x < 2

%description system-s390x
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with S390x (IBM Z) CPU.

%description system-s390x -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem S390x (IBM Z).

%package system-sh4
Summary:	QEMU system emulator for SH4
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem SH4
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-sh4 < 2

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
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-sparc < 2

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
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req

%description system-tricore
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with TriCore CPU.

%description system-tricore -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem TriCore.

%package system-x86
Summary:	QEMU system emulator for x86
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem x86
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	libcbor >= 0.7.0
%{?with_vfio_user:Requires:	libvfio-user = %{version}-%{release}}
%{?with_system_seabios:Requires:	seabios >= 1.11.0}
%systempkg_req
Obsoletes:	kvm < 89
Obsoletes:	qemu-kvm-system-x86 < 2

%description system-x86
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with x86 CPU.

%description system-x86 -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem x86.

%package system-xtensa
Summary:	QEMU system emulator for Xtensa
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem Xtensa
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req
Obsoletes:	qemu-kvm-system-xtensa < 2

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
Requires:	glib2 >= 1:2.75.3
Requires:	liburing >= 2.2
Requires:	systemd-units >= 38
Obsoletes:	qemu-kvm-guest-agent < 2
Conflicts:	SysVinit < 2.96-2

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

%package module-audio-jack
Summary:	QEMU module for JACK audio output
Summary(pl.UTF-8):	Moduł QEMU z wyjściem dźwięku JACK
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}

%description module-audio-jack
QEMU module for JACK audio output.

%description module-audio-jack -l pl.UTF-8
Moduł QEMU z wyjściem dźwięku JACK.

%package module-audio-pipewire
Summary:	QEMU module for PipeWire audio output
Summary(pl.UTF-8):	Moduł QEMU z wyjściem dźwięku PipeWire
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	pipewire-libs >= 0.3.60

%description module-audio-pipewire
QEMU module for PipeWire audio output.

%description module-audio-pipewire -l pl.UTF-8
Moduł QEMU z wyjściem dźwięku PipeWire.

%package module-block-curl
Summary:	QEMU module for 'curl' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'curl'
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	curl-libs >= 7.29.0

%description module-block-curl
QEMU block device support for CURL. It allows to access remote disks
over http, https, ftp and other transports provided by the CURL
library.

%description module-block-curl -l pl.UTF-8
Moduł QEMU dla urządeń blokowych CURL. Pozwala na dostęp do zdalnych
dysków poprzez http, https, ftp i inne protokoły obsługiwane przez
bibliotekę CURL.

%package module-block-gluster
Summary:	QEMU module for 'gluster' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'gluster'
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	glusterfs-libs >= 6

%description module-block-gluster
QEMU block device support for remote Gluster storage.

%description module-block-gluster -l pl.UTF-8
Moduł urządzeń blokowych QEMU do dostępu do zdalnej przestrzeni
dyskowej Gluster.

%package module-block-iscsi
Summary:	QEMU module for 'iscsi' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'iscsi'
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	libiscsi >= 1.9.0

%description module-block-iscsi
QEMU block device support for iSCSI volumes.

%description module-block-iscsi -l pl.UTF-8
Moduł urządzeń blokowych QEMU do dostępu do wolumenów iSCSI.

%package module-block-nfs
Summary:	QEMU module for 'nfs' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'nfs'
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	libnfs >= 1.9.3

%description module-block-nfs
QEMU block device support for remote NFS storage.

%description module-block-nfs -l pl.UTF-8
Moduł urządzeń blokowych QEMU do dostępu do zdalnej przestrzeni po
NFS.

%package module-block-rbd
Summary:	QEMU module for 'rbd' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'rbd'
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	ceph-libs >= 12

%description module-block-rbd
QEMU block device support for Ceph/RBD volumes.

%description module-block-rbd -l pl.UTF-8
Moduł urządzeń blokowych QEMU do wolumenów Ceph/RBD.

%package module-block-ssh
Summary:	QEMU module for 'ssh' block devices
Summary(pl.UTF-8):	Moduł QEMU dla urządeń blokowych typu 'ssh'
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}
Requires:	libssh >= 0.8.7

%description module-block-ssh
QEMU block device support for accessing remote disks using the Secure
Shell (SSH) protocol.

%description module-block-ssh -l pl.UTF-8
Moduł urządzeń blokowych QEMU do dostępu do zdalnych dysków poprzez
protokół SSH (Secure Shell).

%package module-ui-dbus
Summary:	QEMU DBus UI driver
Summary(pl.UTF-8):	Sterownik interfejsu użytkownika DBus dla QEMU
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}

%description module-ui-dbus
QEMU DBus UI driver.

%description module-ui-dbus -l pl.UTF-8
Sterownik interfejsu użytkownika DBus dla QEMU.

%package module-ui-gtk
Summary:	QEMU GTK UI driver
Summary(pl.UTF-8):	Sterownik interfejsu użytkownika GTK dla QEMU
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}

%description module-ui-gtk
QEMU GTK UI driver.

%description module-ui-gtk -l pl.UTF-8
Sterownik interfejsu użytkownika GTK dla QEMU.

%package module-ui-sdl
Summary:	QEMU SDL UI and audio driver
Summary(pl.UTF-8):	Sterownik interfejsu użytkownika i dźwięku SDL dla QEMU
Group:		Applications/Emulators
Requires:	%{name}-common = %{version}-%{release}

%description module-ui-sdl
QEMU SDL UI and audio driver.

%description module-ui-sdl -l pl.UTF-8
Sterownik interfejsu użytkownika i dźwięku SDL dla QEMU.

%package -n systemtap-qemu
Summary:	systemtap/dtrace probes for QEMU
Summary(pl.UTF-8):	Sondy systemtap/dtrace dla QEMU
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
Requires:	systemtap-client

%description -n systemtap-qemu
systemtap/dtrace probes for QEMU.

%description -n systemtap-qemu -l pl.UTF-8
Sondy systemtap/dtrace dla QEMU.

%package -n libvfio-user
Summary:	vfio-user library
Summary(pl.UTF-8):	Biblioteka vfio-user
Group:		Libraries
Requires:	json-c >= 0.11

%description -n libvfio-user
vfio-user is a framework that allows implementing PCI devices in
userspace. Clients (such as qemu) talk the vfio-user protocol over a
UNIX socket to a server. This library, libvfio-user, provides an API
for implementing such servers.

%description -n libvfio-user -l pl.UTF-8
vfio-user to szkielet pozwalający implementować urządzenia PCI w
przestrzeni użytkownika. Klienci (jak qemu) komunikują się z serwerem
protokołem vfio-user przez gniazdo uniksowe.

%package -n libvfio-user-devel
Summary:	Header files for vfio-user library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki vfio-user
Group:		Development/Libraries
Requires:	libvfio-user = %{version}-%{release}

%description -n libvfio-user-devel
Header files for vfio-user library.

%description -n libvfio-user-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki vfio-user.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1

%{__sed} -i '1s,/usr/bin/env python3,%{__python3},' scripts/qemu-trace-stap

%if %{with systemtap}
# don't require stap binary during build
%{__sed} -i -e "s/stap.found()/true/" meson.build docs/meson.build scripts/meson.build
%endif

%if %{without smartcard}
%{__sed} -i -e '/^config USB_SMARTCARD/,/^$/ s/default y/default n/' hw/usb/Kconfig
%endif
%ifarch x32
# xen-emu supports only LP64 __x86_64__ case
%{__sed} -i -e '/^config XEN_EMU/,$ s/default y/default n/' hw/i386/Kconfig

# plain x32 doesn't provide __sync_bool_compare_and_swap_16 - fail int128_t/ATOMIC128 tests earlier
%{__sed} -i -e '/^has_int128_type = / s/$/FAILME/' meson.build
%endif

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
	--cxx="%{__cxx}" \
	--host-cc="%{__cc}" \
	--disable-strip \
	--enable-trace-backends="nop%{?with_systemtap:,dtrace}%{?with_lttng:,ust}" \
	--enable-kvm \
	"$@"

	%{__make} \
		V=1

	cd ..
}

build dynamic \
	--extra-cflags="%{rpmcflags} %{rpmcppflags}" \
	--extra-ldflags="%{rpmldflags} -Wl,-z,relro -Wl,-z,now" \
	--audio-drv-list="alsa,jack%{?with_oss:,oss}%{?with_pulseaudio:,pa}%{?with_sdl:,sdl}" \
	--enable-attr \
	%{__enable_disable brlapi} \
	%{__enable_disable canokey} \
	--enable-cap-ng \
	--enable-capstone \
	--enable-curl \
	--enable-curses \
	--enable-docs \
	--enable-fdt \
	%{__enable_disable glusterfs} \
	%{!?with_gtk3:--disable-gtk} \
	%{__enable_disable iscsi libiscsi} \
	--enable-libcbor \
	%{__enable_disable libnfs} \
	%{__enable_disable pmem libpmem} \
	--enable-lzo \
	%{__enable_disable multipath mpath} \
	--enable-modules \
	--disable-netmap \
	--enable-nettle \
	%{__enable_disable qatzip} \
	%{__enable_disable ceph rbd} \
	%{__enable_disable rdma} \
	%{__enable_disable sdl} \
	%{__enable_disable seccomp} \
	--enable-slirp \
	%{__enable_disable spice} \
	%{__enable_disable smartcard} \
	%{__enable_disable snappy} \
	--enable-tpm \
	%{__enable_disable usbredir usb-redir} \
	--enable-vde \
	%{?with_vfio_user:--enable-vfio-user-server} \
	%{__enable_disable virgl virglrenderer} \
	--enable-virtfs \
	--enable-vnc-jpeg \
	--enable-vnc-sasl \
	%{!?with_vte:--disable-vte} \
	%{__enable_disable xen} \
	%{__enable_disable xkbcommon}

%if %{with user_static}
build static \
	--disable-brlapi \
	--disable-canokey \
	--disable-cap-ng \
	--disable-capstone \
	--disable-curl \
	--disable-curses \
	--disable-gcrypt \
	--disable-gnutls \
	--disable-gtk \
	--disable-guest-agent \
	--disable-guest-agent-msi \
	--disable-libcbor \
	--disable-libnfs \
	--disable-linux-io-uring \
	--disable-mpath \
	--disable-nettle \
	--disable-pie \
	--disable-qatzip \
	--disable-sdl \
	--disable-slirp \
	--disable-spice \
	--disable-system \
	--disable-tools \
	--enable-user \
	--disable-xkbcommon \
	--disable-zstd \
	--static
%endif

%{__cc} %{SOURCE7} %{rpmcflags} -o ksmctl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{systemdunitdir},/usr/lib/binfmt.d} \
	$RPM_BUILD_ROOT/etc/{qemu,sysconfig,modules-load.d,rc.d/init.d,logrotate.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/sasl,/lib/udev/rules.d,%{_sbindir}}

%if %{with user_static}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT

# Give all QEMU user emulators a -static suffix
for src in $RPM_BUILD_ROOT%{_bindir}/qemu-*; do
	%{__mv} $src $src-static
done

%endif

%{__make} -C build-dynamic install \
	DESTDIR=$RPM_BUILD_ROOT

# let rpm generate dependencies
chmod 755 $RPM_BUILD_ROOT%{_libdir}/%{name}/*.so

echo "#allow br0" > $RPM_BUILD_ROOT/etc/qemu/bridge.conf

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ifup
#!/bin/sh

EOF

install -p qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl/qemu.conf

%ifarch %{ix86} %{x8664} x32
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/modules-load.d/kvm.conf
install -p %{SOURCE4} $RPM_BUILD_ROOT/lib/udev/rules.d
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
install -p %{SOURCE12} $RPM_BUILD_ROOT/lib/udev/rules.d

install -p %{SOURCE13} $RPM_BUILD_ROOT/etc/rc.d/init.d/qemu-ga
install -p %{SOURCE14} $RPM_BUILD_ROOT/etc/logrotate.d/qemu-ga

cp -p %{SOURCE15} %{SOURCE16} $RPM_BUILD_ROOT%{systemdunitdir}

%ifarch %{ix86} %{x8664} x32
cp -p contrib/systemd/qemu-vmsr-helper.{service,socket} $RPM_BUILD_ROOT%{systemdunitdir}
%endif

# Install binfmt
BINFMT_CPUS=" \
%ifnarch %{ix86} %{x8664} x32
	i386 x86_64 \
%endif
%ifnarch aarch64
	aarch64 \
%endif
%ifnarch alpha
	alpha \
%endif
%ifnarch %{arm}
	arm \
%endif
	aarch64_be \
	armeb \
	microblaze microblazeel \
%ifnarch mips64
	mips64 \
%ifnarch mips
	mips \
%endif
%endif
%ifnarch mips64el
	mips64el \
%ifnarch mipsel
	mipsel \
%endif
%endif
%ifnarch m68k
	m68k \
%endif
%ifnarch ppc ppc64 ppc64le
	ppc ppc64 ppc64le \
%endif
%ifnarch sparc sparc64
	sparc sparc32plus sparc64 \
%endif
%ifnarch s390 s390x
	s390x \
%endif
%ifnarch sh4
	sh4 \
%endif
	sh4eb \
"

if [ -n "$BINFMT_CPUS" ]; then
	for cpu in $BINFMT_CPUS; do
		bash ./scripts/qemu-binfmt-conf.sh --systemd "$cpu" --exportdir $RPM_BUILD_ROOT/usr/lib/binfmt.d --qemu-path %{_bindir}
	done
	for i in $RPM_BUILD_ROOT/usr/lib/binfmt.d/*.conf; do
		%{__mv} $i ${i%.conf}-dynamic.conf
	done

	%if %{with user_static}
	for regularfmt in $RPM_BUILD_ROOT/usr/lib/binfmt.d/*; do
		staticfmt="${regularfmt%\-dynamic.conf}-static.conf"
		cat $regularfmt | tr -d '\n' | sed "s/:$/-static:F/" > $staticfmt
	done
	%endif
fi

%if %{with system_seabios}
ln -sf /usr/share/seabios/bios.bin $RPM_BUILD_ROOT%{_datadir}/%{name}/bios-256k.bin
# bios.bin provided by qemu is stripped to 128k, with no Xen support, keep it
%endif

%if %{with gtk3}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{de_DE,de}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{fr_FR,fr}
%find_lang %{name}
%else
: > qemu.lang
%endif

for t in client server; do
	cp -p build-dynamic/contrib/ivshmem-$t/ivshmem-$t $RPM_BUILD_ROOT%{_bindir}
done

# test modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/accel-qtest-*.so
# Windows installer icon, not used
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/qemu-nsis.bmp
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/edk2-licenses.txt

# cleanup Sphinx files
%{__rm} $RPM_BUILD_ROOT%{_docdir}/qemu/{.buildinfo,objects.inv}

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
%systemd_trigger qemu-pr-helper.service

%post user
%systemd_post systemd-binfmt.service

%postun user
%systemd_post systemd-binfmt.service

%post user-static
%systemd_post systemd-binfmt.service

%postun user-static
%systemd_post systemd-binfmt.service

%post guest-agent
/sbin/chkconfig --add qemu-ga
%service qemu-ga restart "qemu-ga"
%systemd_reload

%preun guest-agent
if [ "$1" = "0" ]; then
	%service qemu-ga stop
	/sbin/chkconfig --del qemu-ga
fi
%systemd_preun qemu-guest-agent.service

%postun guest-agent
%systemd_reload

%post	-n libvfio-user -p /sbin/ldconfig
%postun	-n libvfio-user -p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%files devel
%defattr(644,root,root,755)
%{_includedir}/qemu-plugin.h

%files common -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENSE README.rst pc-bios/edk2-licenses.txt
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%config(noreplace) %verify(not md5 mtime size) /etc/ksmtuned.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sasl/qemu.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ksm
%dir /etc/qemu
%attr(640,root,qemu) %config(noreplace) %verify(not md5 mtime size) /etc/qemu/bridge.conf
%{systemdunitdir}/ksm.service
%{systemdunitdir}/ksmtuned.service
%{systemdunitdir}/qemu-pr-helper.service
%{systemdunitdir}/qemu-pr-helper.socket
%ifarch %{ix86} %{x8664} x32
%{systemdunitdir}/qemu-vmsr-helper.service
%{systemdunitdir}/qemu-vmsr-helper.socket
%endif
%attr(755,root,root) %{_bindir}/elf2dmp
%attr(755,root,root) %{_bindir}/ivshmem-client
%attr(755,root,root) %{_bindir}/ivshmem-server
%attr(755,root,root) %{_bindir}/qemu-edid
%if %{with xkbcommon}
%attr(755,root,root) %{_bindir}/qemu-keymap
%endif
%attr(755,root,root) %{_bindir}/qemu-nbd
%attr(755,root,root) %{_bindir}/qemu-pr-helper
%attr(755,root,root) %{_bindir}/qemu-storage-daemon
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_bindir}/qemu-vmsr-helper
%endif
%attr(755,root,root) %{_sbindir}/ksmctl
%attr(755,root,root) %{_sbindir}/ksmtuned
%attr(755,root,root) %{_libexecdir}/qemu-bridge-helper
%if %{with virgl}
%attr(755,root,root) %{_libexecdir}/vhost-user-gpu
%endif
%dir %{_libdir}/%{name}
# modules without too many external dependencies
%attr(755,root,root) %{_libdir}/%{name}/block-blkio.so
%attr(755,root,root) %{_libdir}/%{name}/block-dmg-bz2.so
%attr(755,root,root) %{_libdir}/%{name}/block-dmg-lzfse.so
%attr(755,root,root) %{_libdir}/%{name}/audio-alsa.so
%if %{with oss}
%attr(755,root,root) %{_libdir}/%{name}/audio-oss.so
%endif
%if %{with pulseaudio}
%attr(755,root,root) %{_libdir}/%{name}/audio-pa.so
%endif
%if %{with brlapi}
%attr(755,root,root) %{_libdir}/%{name}/chardev-baum.so
%endif
%attr(755,root,root) %{_libdir}/%{name}/hw-display-qxl.so
%attr(755,root,root) %{_libdir}/%{name}/hw-display-virtio-gpu.so
%{?with_virgl:%attr(755,root,root) %{_libdir}/%{name}/hw-display-virtio-gpu-gl.so}
%attr(755,root,root) %{_libdir}/%{name}/hw-display-virtio-gpu-pci.so
%{?with_virgl:%attr(755,root,root) %{_libdir}/%{name}/hw-display-virtio-gpu-pci-gl.so}
%attr(755,root,root) %{_libdir}/%{name}/hw-display-virtio-vga.so
%{?with_virgl:%attr(755,root,root) %{_libdir}/%{name}/hw-display-virtio-vga-gl.so}
%attr(755,root,root) %{_libdir}/%{name}/hw-s390x-virtio-gpu-ccw.so
%attr(755,root,root) %{_libdir}/%{name}/hw-uefi-vars.so
%attr(755,root,root) %{_libdir}/%{name}/hw-usb-host.so
%attr(755,root,root) %{_libdir}/%{name}/ui-curses.so
%if %{with usbredir}
%attr(755,root,root) %{_libdir}/%{name}/hw-usb-redirect.so
%endif
%if %{with smartcard}
%attr(755,root,root) %{_libdir}/%{name}/hw-usb-smartcard.so
%endif
%if %{with opengl}
%attr(755,root,root) %{_libdir}/%{name}/ui-egl-headless.so
%attr(755,root,root) %{_libdir}/%{name}/ui-opengl.so
%endif
%if %{with spice}
%attr(755,root,root) %{_libdir}/%{name}/audio-spice.so
%attr(755,root,root) %{_libdir}/%{name}/chardev-spice.so
%attr(755,root,root) %{_libdir}/%{name}/ui-spice-app.so
%attr(755,root,root) %{_libdir}/%{name}/ui-spice-core.so
%endif
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/firmware
%{_datadir}/%{name}/keymaps
%{_datadir}/%{name}/trace-events-all
%if %{with virgl}
%dir %{_datadir}/%{name}/vhost-user
%{_datadir}/%{name}/vhost-user/50-qemu-gpu.json
%endif
%{_desktopdir}/qemu.desktop
%{_iconsdir}/hicolor/*x*/apps/qemu.png
%{_iconsdir}/hicolor/32x32/apps/qemu.bmp
%{_iconsdir}/hicolor/scalable/apps/qemu.svg
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-storage-daemon.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%{_mandir}/man7/qemu-storage-daemon-qmp-ref.7*
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man8/qemu-pr-helper.8*
%{_docdir}/qemu

%files img
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%files user
%defattr(644,root,root,755)
/usr/lib/binfmt.d/qemu-*-dynamic.conf
%ifnarch %{ix86} x32
%attr(755,root,root) %{_bindir}/qemu-aarch64
%attr(755,root,root) %{_bindir}/qemu-aarch64_be
%attr(755,root,root) %{_bindir}/qemu-alpha
%attr(755,root,root) %{_bindir}/qemu-hppa
%attr(755,root,root) %{_bindir}/qemu-loongarch64
%attr(755,root,root) %{_bindir}/qemu-mips64
%attr(755,root,root) %{_bindir}/qemu-mips64el
%attr(755,root,root) %{_bindir}/qemu-mipsn32
%attr(755,root,root) %{_bindir}/qemu-mipsn32el
%attr(755,root,root) %{_bindir}/qemu-ppc64
%attr(755,root,root) %{_bindir}/qemu-ppc64le
%attr(755,root,root) %{_bindir}/qemu-riscv64
%attr(755,root,root) %{_bindir}/qemu-s390x
%attr(755,root,root) %{_bindir}/qemu-sparc32plus
%attr(755,root,root) %{_bindir}/qemu-sparc64
%attr(755,root,root) %{_bindir}/qemu-x86_64
%endif
%attr(755,root,root) %{_bindir}/qemu-arm
%attr(755,root,root) %{_bindir}/qemu-armeb
%attr(755,root,root) %{_bindir}/qemu-hexagon
%attr(755,root,root) %{_bindir}/qemu-i386
%attr(755,root,root) %{_bindir}/qemu-io
%attr(755,root,root) %{_bindir}/qemu-m68k
%attr(755,root,root) %{_bindir}/qemu-microblaze
%attr(755,root,root) %{_bindir}/qemu-microblazeel
%attr(755,root,root) %{_bindir}/qemu-mips
%attr(755,root,root) %{_bindir}/qemu-mipsel
%attr(755,root,root) %{_bindir}/qemu-or1k
%attr(755,root,root) %{_bindir}/qemu-ppc
%attr(755,root,root) %{_bindir}/qemu-riscv32
%attr(755,root,root) %{_bindir}/qemu-sh4
%attr(755,root,root) %{_bindir}/qemu-sh4eb
%attr(755,root,root) %{_bindir}/qemu-sparc
%attr(755,root,root) %{_bindir}/qemu-xtensa
%attr(755,root,root) %{_bindir}/qemu-xtensaeb

%if %{with user_static}
%files user-static
%defattr(644,root,root,755)
/usr/lib/binfmt.d/qemu-*-static.conf
%ifnarch %{ix86} x32
%attr(755,root,root) %{_bindir}/qemu-aarch64-static
%attr(755,root,root) %{_bindir}/qemu-aarch64_be-static
%attr(755,root,root) %{_bindir}/qemu-alpha-static
%attr(755,root,root) %{_bindir}/qemu-hppa-static
%attr(755,root,root) %{_bindir}/qemu-loongarch64-static
%attr(755,root,root) %{_bindir}/qemu-mips64-static
%attr(755,root,root) %{_bindir}/qemu-mips64el-static
%attr(755,root,root) %{_bindir}/qemu-mipsn32-static
%attr(755,root,root) %{_bindir}/qemu-mipsn32el-static
%attr(755,root,root) %{_bindir}/qemu-ppc64-static
%attr(755,root,root) %{_bindir}/qemu-ppc64le-static
%attr(755,root,root) %{_bindir}/qemu-riscv64-static
%attr(755,root,root) %{_bindir}/qemu-s390x-static
%attr(755,root,root) %{_bindir}/qemu-sparc32plus-static
%attr(755,root,root) %{_bindir}/qemu-sparc64-static
%attr(755,root,root) %{_bindir}/qemu-x86_64-static
%endif
%attr(755,root,root) %{_bindir}/qemu-arm-static
%attr(755,root,root) %{_bindir}/qemu-armeb-static
%attr(755,root,root) %{_bindir}/qemu-hexagon-static
%attr(755,root,root) %{_bindir}/qemu-i386-static
%attr(755,root,root) %{_bindir}/qemu-m68k-static
%attr(755,root,root) %{_bindir}/qemu-microblaze-static
%attr(755,root,root) %{_bindir}/qemu-microblazeel-static
%attr(755,root,root) %{_bindir}/qemu-mips-static
%attr(755,root,root) %{_bindir}/qemu-mipsel-static
%attr(755,root,root) %{_bindir}/qemu-or1k-static
%attr(755,root,root) %{_bindir}/qemu-ppc-static
%attr(755,root,root) %{_bindir}/qemu-riscv32-static
%attr(755,root,root) %{_bindir}/qemu-sh4-static
%attr(755,root,root) %{_bindir}/qemu-sh4eb-static
%attr(755,root,root) %{_bindir}/qemu-sparc-static
%attr(755,root,root) %{_bindir}/qemu-xtensa-static
%attr(755,root,root) %{_bindir}/qemu-xtensaeb-static
%{?with_systemtap:%attr(755,root,root) %{_bindir}/qemu-trace-stap-static}
%endif

%ifnarch %{ix86} x32
%files system-aarch64
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-aarch64
%{_datadir}/%{name}/edk2-aarch64-code.fd
%{_datadir}/%{name}/firmware/60-edk2-aarch64.json

%files system-alpha
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-alpha
%{_datadir}/%{name}/palcode-clipper
%endif

%files system-arm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-arm
%{_datadir}/%{name}/edk2-arm-code.fd
%{_datadir}/%{name}/edk2-arm-vars.fd
%{_datadir}/%{name}/firmware/60-edk2-arm.json
%{_datadir}/%{name}/npcm7xx_bootrom.bin
%{_datadir}/%{name}/npcm8xx_bootrom.bin

%files system-avr
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-avr

%ifnarch %{ix86} x32
%files system-hppa
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-hppa
%{_datadir}/%{name}/hppa-firmware.img
%{_datadir}/%{name}/hppa-firmware64.img
%endif

%files system-m68k
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-m68k

%ifnarch %{ix86} x32
%files system-microblaze
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-microblaze
%attr(755,root,root) %{_bindir}/qemu-system-microblazeel
%endif

%files system-mips
%defattr(644,root,root,755)
%ifnarch %{ix86} x32
%attr(755,root,root) %{_bindir}/qemu-system-loongarch64
%attr(755,root,root) %{_bindir}/qemu-system-mips64
%attr(755,root,root) %{_bindir}/qemu-system-mips64el
%endif
%attr(755,root,root) %{_bindir}/qemu-system-mips
%attr(755,root,root) %{_bindir}/qemu-system-mipsel
%{_datadir}/%{name}/edk2-loongarch64-code.fd
%{_datadir}/%{name}/edk2-loongarch64-vars.fd
%{_datadir}/%{name}/firmware/60-edk2-loongarch64.json

%files system-or1k
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-or1k

%files system-ppc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-ppc
%ifnarch %{ix86} x32
%attr(755,root,root) %{_bindir}/qemu-system-ppc64
%endif
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/canyonlands.dtb
%{_datadir}/%{name}/openbios-ppc
%{_datadir}/%{name}/petalogix-ml605.dtb
%{_datadir}/%{name}/petalogix-s3adsp1800.dtb
%{_datadir}/%{name}/pnv-pnor.bin
%{_datadir}/%{name}/qemu_vga.ndrv
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/slof.bin
%{_datadir}/%{name}/u-boot.e500
%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%{_datadir}/%{name}/vof.bin
%{_datadir}/%{name}/vof-nvram.bin

%files system-riscv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-riscv32
%ifnarch %{ix86} x32
%attr(755,root,root) %{_bindir}/qemu-system-riscv64
%endif
%{_datadir}/%{name}/edk2-riscv-code.fd
%{_datadir}/%{name}/edk2-riscv-vars.fd
%{_datadir}/%{name}/firmware/60-edk2-riscv64.json
%{_datadir}/%{name}/opensbi-riscv32-generic-fw_dynamic.bin
%{_datadir}/%{name}/opensbi-riscv64-generic-fw_dynamic.bin

%files system-rx
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-rx

%ifnarch %{ix86} x32
%files system-s390x
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-s390x
%{_datadir}/%{name}/s390-ccw.img
%endif

%files system-sh4
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-sh4
%attr(755,root,root) %{_bindir}/qemu-system-sh4eb

%files system-sparc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-sparc
%ifnarch %{ix86} x32
%attr(755,root,root) %{_bindir}/qemu-system-sparc64
%endif
%{_datadir}/%{name}/QEMU,cgthree.bin
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/openbios-sparc32
%{_datadir}/%{name}/openbios-sparc64

%files system-tricore
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-tricore

%files system-x86
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-i386
%ifnarch %{ix86} x32
%attr(755,root,root) %{_bindir}/qemu-system-x86_64
%endif
%ifarch %{ix86} %{x8664} x32
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/kvm.conf
/lib/udev/rules.d/80-kvm.rules
%endif
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/bios-microvm.bin
%{_datadir}/%{name}/edk2-i386-code.fd
%{_datadir}/%{name}/edk2-i386-secure-code.fd
%{_datadir}/%{name}/edk2-i386-vars.fd
%{_datadir}/%{name}/edk2-x86_64-code.fd
%{_datadir}/%{name}/edk2-x86_64-secure-code.fd
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
%{_datadir}/%{name}/multiboot_dma.bin
%{_datadir}/%{name}/pvh.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/pxe-eepro100.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/qboot.rom
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-ati.bin
%{_datadir}/%{name}/vgabios-bochs-display.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-ramfb.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/firmware/50-edk2-i386-secure.json
%{_datadir}/%{name}/firmware/50-edk2-x86_64-secure.json
%{_datadir}/%{name}/firmware/60-edk2-i386.json
%{_datadir}/%{name}/firmware/60-edk2-x86_64.json

%files system-xtensa
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-xtensa
%attr(755,root,root) %{_bindir}/qemu-system-xtensaeb

%files guest-agent
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-ga
/lib/udev/rules.d/99-qemu-guest-agent.rules
%{systemdunitdir}/qemu-guest-agent.service
%attr(754,root,root) /etc/rc.d/init.d/qemu-ga
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/qemu-ga
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man8/qemu-ga.8*

%files module-audio-jack
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/audio-jack.so

%files module-audio-pipewire
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/audio-pipewire.so

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

%if %{with libnfs}
%files module-block-nfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-nfs.so
%endif

%if %{with ceph}
%files module-block-rbd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-rbd.so
%endif

%files module-block-ssh
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/block-ssh.so

%files module-ui-dbus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/audio-dbus.so
%attr(755,root,root) %{_libdir}/%{name}/ui-dbus.so

%if %{with gtk3}
%files module-ui-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/ui-gtk.so
%endif

%if %{with sdl}
%files module-ui-sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/audio-sdl.so
%attr(755,root,root) %{_libdir}/%{name}/ui-sdl.so
%endif

%if %{with systemtap}
%files -n systemtap-qemu
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-trace-stap
%{_datadir}/systemtap/tapset/qemu-*.stp
%{_mandir}/man1/qemu-trace-stap.1*
%endif

%if %{with vfio_user}
%files -n libvfio-user
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvfio-user.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvfio-user.so.0

%files -n libvfio-user-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvfio-user.so
%{_includedir}/vfio-user
%endif
