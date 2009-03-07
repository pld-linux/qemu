#
# TODO:
# - fix ncurses detection
# - update patches
#
# Conditional build:
%bcond_without	kqemu			# disable KQEMU ACCELERATOR support in QEMU
%bcond_with	cflags_passing		# with passing rpmcflags to Makefiles
%bcond_with	dosguest		# add special patch when use with DOS as guest os
%bcond_with	nosdlgui		# do not use SDL gui (use X11 instead)
%bcond_without	dist_kernel		# without distribution kernel
%bcond_without	kernel			# build kqemu KERNEL MODULES
%bcond_without	userspace		# don't build userspace utilities

# no kernel kqemu module for ppc
%ifarch ppc
%undefine      with_kqemu
%undefine      with_kernel
%endif

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel	0.1

%define		kqemu_version	1.4.0pre1
%define		qemu_version	0.10.0
%define		pname	qemu
Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		%{pname}%{_alt_kernel}
Version:	%{qemu_version}
Release:	%{rel}%{?with_kqemu:k}
License:	GPL
Group:		Applications/Emulators
# Source0Download: http://fabrice.bellard.free.fr/qemu/download.html
Source0:	http://download.savannah.gnu.org/releases/qemu/%{pname}-%{version}.tar.gz
# Source0-md5:	8dc50b834fa3f5f6a17d7bc3d0559e53
Source1:	http://www.nongnu.org/qemu/k%{pname}-%{kqemu_version}.tar.gz
# Source1-md5:	d738d8ca7332211ab716ec3213d82ee1
Patch6:		%{pname}-nosdlgui.patch
# Proof of concept, for reference, do not remove
Patch8:		%{pname}-kde_virtual_workspaces_hack.patch
#Patch12:	%{pname}-0.7.2-dyngen-check-stack-clobbers.patch
Patch13:	%{pname}-dosguest.patch
Patch14:	%{pname}-ppc_old_binutils.patch
Patch15:	%{pname}-isa-bios-ram.patch
# below one fixes problems with passing ram size to bios/bootloader
# which affects coreboot/linuxbios
Patch16:	%{pname}-piix-ram-size.patch
URL:		http://www.nongnu.org/qemu/
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
%if %{with userspace}
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	blues-libs-devel
BuildRequires:	ncurses-devel
BuildRequires:	perl-tools-pod
BuildRequires:	sed >= 4.0
BuildRequires:	tetex
BuildRequires:	which
%endif
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

%package -n kernel%{_alt_kernel}-misc-kqemu
Summary:	kqemu - kernel module
Summary(pl.UTF-8):	kqemu - moduł jądra
Version:	%{kqemu_version}
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
License:	GPL v2
Obsoletes:	kernel%{_alt_kernel}-smp-misc-kqemu
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-misc-kqemu
kqemu - kernel module.

%description -n kernel%{_alt_kernel}-misc-kqemu -l pl.UTF-8
kqemu - moduł jądra.

%prep
%setup -q -n %{pname}-%{qemu_version} %{?with_kernel:-a1}
%{?with_nosdlgui:%patch6 -p1}
#%patch8 -p1

%{__sed} -i -e 's/sdl_static=yes/sdl_static=no/' configure
%{__sed} -i 's/.*MAKE) -C kqemu$//' Makefile

# cannot use optflags on x86 - they cause "no register to spill" errors
%if %{with cflags_passing}
%{__sed} -i -e 's/-Wall -O2 -g/-Wall %{rpmcflags}/' Makefile Makefile.target
%else
%{__sed} -i 's/-Wall -O2 -g/-Wall -O2/' Makefile Makefile.target
%endif

%if %{with kernel}
echo -n > kqemu-%{kqemu_version}/install.sh

cat <<'EOF' > modprobe.conf
# enable dynamic major
options kqemu major=0
# for autoloading from static dev
#alias char-major-250 kqemu
EOF

cat <<'EOF' > udev.conf
KERNEL=="kqemu", NAME="%k", MODE="0666"
EOF

%if %{with dosguest}
%patch13 -p1
%endif
%patch14 -p1
#%patch15 -p1
%patch16 -p1

cd kqemu-%{kqemu_version}
%{__sed} -i 's#include ../config-host.mak##' ./common/Makefile
%ifarch %{x8664}
%{__sed} -i 's/^#ARCH=x86_64/ARCH=x86_64/' ./common/Makefile
%{__make} -C common -j1
mv -f kqemu-mod-x86_64.o{,.bin}
%else
%{__sed} -i 's/^#ARCH=i386/ARCH=i386/' ./common/Makefile
%{__make} -C common -j1
mv -f kqemu-mod-i386.o{,.bin}
%endif

mv -f kqemu-linux.c{,.orig}
cat > Makefile <<'EOF'
obj-m := kqemu.o
kqemu-objs:= kqemu-linux.o kqemu-mod.o

$(obj)/kqemu-mod.o: $(src)/kqemu-mod-$(ARCH).o.bin
	cp $< $@
EOF
cd -
%endif

%build
%if %{with kernel}
cd kqemu-%{kqemu_version}
%build_kernel_modules -m kqemu <<'EOF'
if grep -q "CONFIG_PREEMPT_RT" o/.config; then
	sed 's/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(kqemu_lock)/' \
		kqemu-linux.c.orig > kqemu-linux.c
else
	cat kqemu-linux.c.orig > kqemu-linux.c
fi
EOF
cd -
%endif

%if %{with userspace}
# --extra-cflags don't work (overridden by CFLAGS in Makefile*)
# they can be passed if the cflags_passing bcond is used
./configure \
	--prefix=%{_prefix} \
	--cc="%{__cc}" \
	--host-cc="%{__cc}" \
	--make="%{__make}" \
%if %{without kqemu}
	--disable-kqemu \
%endif
	--audio-drv-list="alsa" \
	--interp-prefix=%{_libdir}/%{pname}
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ifup
#!/bin/sh

EOF
%endif

%if %{with kernel}
%install_kernel_modules -m kqemu-%{kqemu_version}/kqemu -d misc
install -d $RPM_BUILD_ROOT/etc/{modprobe.d/%{_kernel_ver}{,smp},udev/rules.d}
install modprobe.conf $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/kqemu.conf
install udev.conf $RPM_BUILD_ROOT/etc/udev/rules.d/kqemu.rules
%endif

# already packaged
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-{doc,tech}.html

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%post
%banner %{pname} -e <<EOF
To enable qemu accelerator (kqemu), the kqemu kernel module must be loaded:
modprobe kqemu
EOF
%endif

%post	-n kernel%{_alt_kernel}-misc-kqemu
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-kqemu
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%attr(755,root,root) %{_bindir}/*
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-kqemu
%defattr(644,root,root,755)
%doc kqemu-%{kqemu_version}/LICENSE
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/kqemu.rules
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/%{_kernel_ver}/kqemu.conf
/lib/modules/%{_kernel_ver}/misc/kqemu.ko*
%endif
