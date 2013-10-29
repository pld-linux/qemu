# TODO:
# - merge missing bits from qemu-kvm
# - qemu-system-ppc -hda ac-ppc.img says:
#   qemu: could not open disk image ac-ppc.img: error "Success"
#   qemu-0.12.2-2.x86_64.rpm - broken
#   qemu-0.12.3-3.x86_64/qemu-0.12.4-1.x86_64 - stops on "returning from prom_init"
#   qemu-0.15.0-2.x86_64.rpm - qemu-system-sparc/ppc booting with -kernel, -initrd options stalls in openbios prompt
#   qemu-0.11.1-*.x86_64.rpm - OK
#
# Conditional build:
%bcond_without	sdl		# SDL UI and audio support
%bcond_without	glx		# OpenGL/GLX support
%bcond_without	ceph		# Ceph/RBD support
%bcond_without	glusterfs	# GlusterFS backend
%bcond_without	rdma		# RDMA-based migration support
%bcond_with	gtk2		# GTK+ 2.x instead of 3.x
%bcond_without	spice		# SPICE support
%bcond_with	esd		# EsounD audio support
%bcond_without	oss		# OSS audio support
%bcond_without	pulseaudio	# PulseAudio audio support
%bcond_without	xen		# Xen backend driver support

Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu
Version:	1.6.1
Release:	2
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://wiki.qemu-project.org/download/%{name}-%{version}.tar.bz2
# Source0-md5:	3a897d722457c5a895cd6ac79a28fda0
Patch0:		%{name}-cflags.patch
Patch1:		vgabios-widescreens.patch
Patch2:		%{name}-whitelist.patch
Patch3:		%{name}-system-libcacard.patch
# Proof of concept, for reference, do not remove
Patch4:		%{name}-kde_virtual_workspaces_hack.patch
URL:		http://www.qemu-project.org/
%{?with_opengl:BuildRequires:	OpenGL-GLX-devel}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.2.1}
BuildRequires:	alsa-lib-devel
BuildRequires:  bcc
BuildRequires:	bluez-libs-devel
BuildRequires:	brlapi-devel
%{?with_ceph:BuildRequires:	ceph-devel}
BuildRequires:	curl-devel
BuildRequires:	cyrus-sasl-devel >= 2
%{?with_esd:BuildRequires:	esound-devel}
BuildRequires:	glib2-devel >= 1:2.12
%{?with_glusterfs:BuildRequires:	glusterfs-devel >= 3.4}
BuildRequires:	gnutls-devel
BuildRequires:	libaio-devel
BuildRequires:	libcacard-devel
BuildRequires:	libcap-devel
BuildRequires:	libcap-ng-devel
BuildRequires:	libfdt-devel
%{?with_rdma:BuildRequires:	libibverbs-devel}
BuildRequires:	libiscsi-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%{?with_rdma:BuildRequires:	librdmacm-devel}
BuildRequires:	libseccomp-devel
BuildRequires:	libssh2-devel >= 1.2.8
# for usb passthrough, when available
#BuildRequires:	libusb-devel >= 1.0.13
BuildRequires:	libuuid-devel
BuildRequires:	ncurses-devel
BuildRequires:	nss-devel >= 3.12.8
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	sed >= 4.0
%if %{with spice}
BuildRequires:	spice-protocol >= 0.12.0
BuildRequires:	spice-server-devel >= 0.12.0
%endif
BuildRequires:	texi2html
BuildRequires:	texinfo
BuildRequires:	usbredir-devel >= 0.6
BuildRequires:	vde2-devel
BuildRequires:	which
%{?with_xen:BuildRequires:	xen-devel >= 3.4}
BuildRequires:	xfsprogs-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
%if %{with gtk2}
BuildRequires:	gtk+2-devel >= 2:2.18.0
BuildRequires:	vte0-devel >= 0.24.0
%else
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	vte-devel >= 0.32.0
%endif
Requires:	%{name}-img = %{version}-%{release}
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
Requires:	%{name}-system-unicore32 = %{version}-%{release}
Requires:	%{name}-system-x86 = %{version}-%{release}
Requires:	%{name}-system-xtensa = %{version}-%{release}
Requires:	%{name}-user = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	systempkg_req \
Requires:	SDL >= 1.2.1 \
Requires:	usbredir >= 0.6 \
%if %{with gtk2} \
Requires:	gtk+2 >= 2:2.18.0 \
Requires:	vte0 >= 0.24.0 \
%else \
Requires:	gtk+3 >= 3.0.0 \
Requires:	vte >= 0.32.0 \
%endif

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

%package common
Summary:	QEMU common files needed by all QEMU targets
Summary(pl.UTF-8):	Wspólne pliki QEMU wymagane przez wszystkie środowiska QEMU
Group:		Development/Tools
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	glib2 >= 1:2.12
Requires:	libssh2 >= 1.2.8
Provides:	group(qemu)
Provides:	user(qemu)
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

%description user
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the user mode emulation of QEMU targets.

%description user -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet udostępnia emulację trybu użytkownika środowisk QEMU.

%package system-alpha
Summary:	QEMU system emulator for Alpha
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem Alpha
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req

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

%description system-sparc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with SPARC/SPARC64 CPU.

%description system-sparc -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem SPARC/SPARC64.

%package system-unicore32
Summary:	QEMU system emulator for UniCore32
Summary(pl.UTF-8):	QEMU - emulator systemu z procesorem UniCore32
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
%systempkg_req

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
%systempkg_req

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

%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator with Xtensa CPU.

%description system-xtensa -l pl.UTF-8
QEMU to ogólny, mający otwarte źródła emulator procesora, osiągający
dobrą szybkość emulacji dzięki użyciu translacji dynamicznej.

Ten pakiet zawiera emulator systemu z procesorem Xtensa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1

%{__mv} libcacard libcacard-use-system-lib

# workaround for conflict with alsa/error.h
ln -s ../error.h qapi/error.h

%build
./configure \
	--extra-cflags="%{rpmcflags} -I/usr/include/ncurses" \
	--extra-ldflags="%{rpmldflags}" \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--cc="%{__cc}" \
	--host-cc="%{__cc}" \
	--disable-strip \
	--enable-attr \
	--enable-bluez \
	--enable-brlapi \
	--enable-cap-ng \
	--enable-curl \
	--enable-curses \
	--enable-docs \
	--enable-fdt \
	%{__enable_disable glusterfs} \
	--enable-libiscsi \
	--enable-mixemu \
	%{__enable_disable glx} \
	%{__enable_disable ceph rbd} \
	%{__enable_disable rdma} \
	%{__enable_disable sdl} \
	--enable-seccomp \
	%{__enable_disable spice} \
	--enable-smartcard-nss \
	--enable-tpm \
	--enable-usb-redir \
	--enable-uuid \
	--enable-vde \
	--enable-virtfs \
	--enable-vnc-jpeg \
	--enable-vnc-png \
	--enable-vnc-sasl \
	--enable-vnc-tls \
	%{__enable_disable xen} \
	--audio-drv-list="alsa%{?with_iss:,oss}%{?with_sdl:,sdl}%{?with_esd:,esd}%{?with_pulseaudio:,pa}" \
	--interp-prefix=%{_libdir}/qemu/lib-%%M \
	--with-gtkabi="%{?with_gtk2:2.0}%{!?with_gtk2:3.0}"

# note: CONFIG_QEMU_HELPERDIR is used when compiling, libexecdir when installing;
# --libexecdir in configure is nop
%{__make} \
	V=1 \
	CONFIG_QEMU_HELPERDIR="%{_libdir}"

# rebuild patched vesa tables with additional widescreen modes.
%{__make} -C roms/vgabios stdvga-bios

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	libexecdir=%{_libdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ifup
#!/bin/sh

EOF

# already packaged
%{__rm} $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-{doc,tech}.html
%{__rm} $RPM_BUILD_ROOT%{_docdir}/qemu/qmp-commands.txt

# install patched vesa tables with additional widescreen modes.
cp -p roms/vgabios/VGABIOS-lgpl-latest.stdvga.bin $RPM_BUILD_ROOT%{_datadir}/%{name}/vgabios-stdvga.bin

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{de_DE,de}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{fr_FR,fr}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
%groupadd -g 276 qemu
%useradd -u 276 -g qemu -c "QEMU User" qemu

%postun common
if [ "$1" = "0" ]; then
	%userremove qemu
	%groupremove qemu
fi

%files
%defattr(644,root,root,755)

%files common -f %{name}.lang
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html QMP/qmp-commands.txt
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu/target-*.conf
%dir %{_sysconfdir}/qemu
%attr(755,root,root) %{_bindir}/virtfs-proxy-helper
%attr(755,root,root) %{_bindir}/qemu-nbd
%attr(755,root,root) %{_libdir}/qemu-bridge-helper
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man8/qemu-nbd.8*

%dir %{_datadir}/qemu
%{_datadir}/%{name}/keymaps
%{_datadir}/%{name}/qemu-icon.bmp
# various bios images
%{_datadir}/%{name}/*.aml
%{_datadir}/%{name}/*.bin
%{_datadir}/%{name}/*.rom
%{_datadir}/%{name}/*.dtb
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/openbios-ppc
%{_datadir}/%{name}/openbios-sparc*
%{_datadir}/%{name}/palcode-clipper
%{_datadir}/%{name}/s390-ccw.img

%files img
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%files user
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-alpha
%attr(755,root,root) %{_bindir}/qemu-arm
%attr(755,root,root) %{_bindir}/qemu-armeb
%attr(755,root,root) %{_bindir}/qemu-cris
%attr(755,root,root) %{_bindir}/qemu-ga
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
%attr(755,root,root) %{_bindir}/qemu-s390x
%attr(755,root,root) %{_bindir}/qemu-sh4
%attr(755,root,root) %{_bindir}/qemu-sh4eb
%attr(755,root,root) %{_bindir}/qemu-sparc
%attr(755,root,root) %{_bindir}/qemu-sparc32plus
%attr(755,root,root) %{_bindir}/qemu-sparc64
%attr(755,root,root) %{_bindir}/qemu-unicore32
%attr(755,root,root) %{_bindir}/qemu-x86_64

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
