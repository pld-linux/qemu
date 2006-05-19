#
# TODO:
# - wait till the gcc bug http://gcc.gnu.org/PR16185 is fixed.
#
# Conditional build:
%bcond_with	kqemu			# with QEMU accelerator module
%bcond_with	cflags_passing		# with passing rpmcflags to Makefiles
%bcond_with	nosdlgui		# do not use SDL gui (use X11 instead)
%bcond_with	gcc4			# use gcc4 patches (broke build on gcc33)
%bcond_without	dist_kernel		# without distribution kernel
%bcond_without	kernel			# don't build kernel modules
%bcond_without	smp			# don't build SMP module
%bcond_without	userspace		# don't build userspace utilities
#
%if %{without kqemu}
%undefine	with_kernel
%endif
#
%define	_kqemu_version	1.3.0pre7
%define		_rel	1.2
Summary:	QEMU CPU Emulator
Summary(pl):	QEMU - emulator procesora
Name:		qemu
Version:	0.8.0
Release:	%{_rel}%{?with_kqemu:k}
License:	GPL
Group:		Applications/Emulators
#Source0Download: http://fabrice.bellard.free.fr/qemu/download.html
Source0:	http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
# Source0-md5:	eb175b26583280706fe7e4d8910d320d
Source1:	http://fabrice.bellard.free.fr/qemu/kqemu-%{_kqemu_version}.tar.gz
# NoSource1-md5:	3b77edbada790f924456aa4675edd0be
NoSource:	1
Patch0:		%{name}-nostatic.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-longjmp.patch
Patch3:		%{name}-dot.patch
Patch4:		%{name}-initrd_load_addr.patch
Patch5:		%{name}-gcc4_x86.patch
Patch6:		%{name}-gcc4_ppc.patch
Patch7:		%{name}-parallel.patch
Patch8:		%{name}-nosdlgui.patch
Patch9:		%{name}-ifup.patch
Patch10:	%{name}-gcc33.patch
Patch11:	%{name}-slirp_throttle.patch
URL:		http://fabrice.bellard.free.fr/qemu/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
%{!?with_gcc4:BuildRequires:	gcc < 5:4.0}
%if %{with kqemu} && %{with dist_kernel}
BuildRequires:	kernel-module-build >= 3:2.6.7
%endif
BuildRequires:	rpmbuild(macros) >= 1.217
BuildRequires:	sed >= 4.0
Requires:	SDL >= 1.2.1
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
ExclusiveArch:	%{ix86} %{x8664} %{!?with_kqemu:ppc}
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
  including a processor and various peripherials. It can also be used to
  provide virtual hosting of several virtual PC on a single server.

%description -l pl
QEMU to szybki(!) emulator procesora. Poprzez u¿ycie dynamicznego
t³umaczenia osi±ga rozs±dn± szybko¶æ i jest ³atwy do przeportowania,
aby dzia³a³ na kolejnych procesorach. QEMU ma dwa tryby pracy:

- Emulacja trybu u¿ytkownika. W tym trybie QEMU mo¿e uruchamiaæ
  procesy linuksowe skompilowane dla jednego procesora na innym
  procesorze. Linuksowe wywo³ania systemowe s± t³umaczone ze wzglêdu na
  niezgodno¶æ kolejno¶ci bajtów w s³owie i 32/64-bitowego rozmiaru
  s³owa. Wine (emulacja Windows) i DOSEMU (emulacja DOS-a) to g³ówne
  cele QEMU.

- Pe³na emulacja systemu. W tym trybie QEMU emuluje ca³y system,
  w³±czaj±c w to procesor i ró¿ne urz±dzenia peryferyjne. Mo¿e byæ tak¿e
  u¿ywane do wirtualnego hostowania kilku wirtualnych pecetów na
  pojedynczym serwerze.

%package -n kernel-misc-kqemu
Summary:	kqemu - kernel module
Summary(pl):	kqemu - modu³ j±dra
Version:	%{_kqemu_version}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
License:	Free to use, non-distributable
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel-misc-kqemu
kqemu - kernel module.

%description -n kernel-misc-kqemu -l pl
kqemu - modu³ j±dra.

%package -n kernel-smp-misc-kqemu
Summary:	kqemu - SMP kernel module
Summary(pl):	kqemu - modu³ j±dra SMP
Version:	%{_kqemu_version}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
License:	Free to use, non-distributable
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel-smp-misc-kqemu
kqemu - SMP kernel module.

%description -n kernel-smp-misc-kqemu -l pl
kqemu - modu³ j±dra SMP.

%prep
%setup -q %{?with_kqemu:-a1}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%if %{with gcc4}
%patch5 -p0
%patch6 -p1
%endif
# probably not needed
# %patch7 -p1
%{?with_nosdlgui:%patch8 -p1}
%patch9 -p1
%patch10 -p1
%patch11 -p0

%{__sed} -i -e 's/sdl_static=yes/sdl_static=no/' configure
%{__sed} -i 's/.*MAKE) -C kqemu$//' Makefile

# cannot use optflags on x86 - they cause "no register to spill" errors
%if %{with cflags_passing}
%{__sed} -i -e 's/-Wall -O2 -g/-Wall %{rpmcflags}/' Makefile Makefile.target
%else
%{__sed} -i 's/-Wall -O2 -g/-Wall -O2/' Makefile Makefile.target
%endif

%if %{with kqemu}
echo -n > kqemu-%{_kqemu_version}/install.sh
%endif

%build
%if %{with kernel}
cd kqemu-%{_kqemu_version}
mv -f kqemu-linux.c{,.orig}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	if grep -q "^CONFIG_PREEMPT_RT=y$" o/.config; then
		sed 's/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(kqemu_lock)/' \
			kqemu-linux.c.orig > kqemu-linux.c
	else
		cat kqemu-linux.c.orig > kqemu-linux.c
	fi

	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv kqemu.ko kqemu-mod-$cfg.ko
done
cd -
%endif

%if %{with userspace}
# --extra-cflags don't work (overridden by CFLAGS in Makefile*)
# they can be passed if the cflags_passing bcond is used
./configure \
	--prefix=%{_prefix} \
	--cc="%{__cc}" \
	%{?with_gcc4:--disable-gcc-check} \
	%{!?with_kqemu:--disable-kqemu} \
	--enable-alsa \
	--make="%{__make}" \
	--interp-prefix=%{_libdir}/%{name}
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/sbin
cat <<'EOF' > $RPM_BUILD_ROOT/sbin/qemu-ifup
#!/bin/sh
if [ -f /etc/sysconfig/qemu ]; then
	. /etc/sysconfig/qemu
fi
# of course this will work only for one interface. a lot possible to involve
sudo /sbin/ifconfig $1 ${INTERFACE_ADDR:-172.20.0.1}
EOF
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install kqemu-%{_kqemu_version}/kqemu-mod-up.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/kqemu.ko
%if %{with smp} && %{with dist_kernel}
install kqemu-%{_kqemu_version}/kqemu-mod-smp.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/kqemu.ko
%endif
install -d $RPM_BUILD_ROOT/etc/modprobe.d
echo 'alias char-major-250 kqemu' > $RPM_BUILD_ROOT/etc/modprobe.d/kqemu.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with kqemu}
%post
%banner %{name} -e <<EOF
To enable qemu accelerator (kqemu), the kqemu kernel module must be loaded:
modprobe kqemu
EOF
%endif

%post	-n kernel-misc-kqemu
%depmod %{_kernel_ver}

%postun -n kernel-misc-kqemu
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-kqemu
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-kqemu
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) /sbin/qemu-ifup
%attr(755,root,root) %{_bindir}/*
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
# FIXME: maybe better moved this into dev.spec
%if %{with kqemu}
%dev(c,250,0) %attr(666,root,root) /dev/kqemu
%endif
%endif

%if %{with kernel}
%files -n kernel-misc-kqemu
%defattr(644,root,root,755)
%doc kqemu-%{_kqemu_version}/LICENSE
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/kqemu.conf
/lib/modules/%{_kernel_ver}/misc/kqemu.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-misc-kqemu
%defattr(644,root,root,755)
%doc kqemu-%{_kqemu_version}/LICENSE
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/kqemu.conf
/lib/modules/%{_kernel_ver}smp/misc/kqemu.ko*
%endif
%endif
