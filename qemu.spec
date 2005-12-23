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

%define	_kqemu_version	0.7.2
#
Summary:	QEMU CPU Emulator
Summary(pl):	QEMU - emulator procesora
Name:		qemu
Version:	0.8.0
%define		_rel	1
Release:	%{_rel}%{?with_kqemu:k}
License:	GPL
Group:		Applications/Emulators
#Source0Download: http://fabrice.bellard.free.fr/qemu/download.html
Source0:	http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
# Source0-md5:	eb175b26583280706fe7e4d8910d320d
%if %{with kqemu}
Source1:	http://fabrice.bellard.free.fr/qemu/kqemu-%{_kqemu_version}.tar.gz
# NoSource1-md5:	02cfdecda90458d6393781496ec6b48b
NoSource:	1
%endif
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
URL:		http://fabrice.bellard.free.fr/qemu/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
%if %{with kqemu} && %{with dist_kernel}
BuildRequires:	kernel-module-build >= 2.6.7
%endif
BuildRequires:	rpmbuild(macros) >= 1.217
BuildRequires:	sed >= 4.0
Requires:	SDL >= 1.2.1
ExclusiveArch:	%{ix86} %{x8664} ppc
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some SPARC boot image in ELF format
%define		_noautostrip	.*%{_datadir}/qemu/proll.elf

%if !%{with kqemu}
%undefine	with_kernel
%endif

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

%package -n kernel-misc-kqemu
Summary:	kqemu - kernel module
Summary(pl):	kqemu - modu� j�dra
Version:	%{_kqemu_version}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
License:	Free to use, non-distributable
Requires(post,postun):	/sbin/depmod

%description -n kernel-misc-kqemu
kqemu - kernel module.

%description -n kernel-misc-kqemu -l pl
kqemu - modu� j�dra.

%package -n kernel-smp-misc-kqemu
Summary:	kqemu - SMP kernel module
Summary(pl):	kqemu - modu� j�dra SMP
Version:	%{_kqemu_version}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
License:	Free to use, non-distributable
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-kqemu
kqemu - SMP kernel module.

%description -n kernel-smp-misc-kqemu -l pl
kqemu - modu� j�dra SMP.

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

%{__sed} -i -e 's/sdl_static=yes/sdl_static=no/' configure
%{__sed} -i 's/.*MAKE) -C kqemu$//' Makefile

# cannot use optflags on x86 - they cause "no register to spill" errors
%if %{with cflags_passing}
%{__sed} -i -e 's/-Wall -O2 -g/-Wall %{rpmcflags}/' Makefile Makefile.target
%else
%{__sed} -i 's/-Wall -O2 -g/-Wall -O2/' Makefile Makefile.target
%endif

%{?with_kqemu:echo -n > kqemu/install.sh}

%build
%if %{with kernel}
cd kqemu
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
%if %{without dist_kernel}
	ln -sf %{_kernelsrcdir}/scripts
%endif
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name 'kqemu-mod-*.*' -o" \
		M=$PWD O=$PWD
	%{__make} -C %{_kernelsrcdir} modules \
		M=$PWD O=$PWD
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
	--enable-alsa \
	%{!?with_kqemu:--disable-kqemu} \
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
install kqemu/kqemu-mod-up.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/kqemu.ko
%if %{with smp} && %{with dist_kernel}
install kqemu/kqemu-mod-smp.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/kqemu.ko
%endif
%endif

# This dir is unneeded
rm -rf $RPM_BUILD_ROOT/usr/share/doc/qemu

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
%banner %{name}-module -e <<EOF
To autoload kqemu module, add to /etc/modprobe.conf:
alias char-major-250 kqemu
EOF

%postun -n kernel-misc-kqemu
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-kqemu
%depmod %{_kernel_ver}smp
%banner %{name}-module -e <<EOF
To autoload kqemu module, add to /etc/modprobe.conf:
alias char-major-250 kqemu
EOF

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
%doc kqemu/LICENSE
/lib/modules/%{_kernel_ver}/misc/kqemu.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-misc-kqemu
%defattr(644,root,root,755)
%doc kqemu/LICENSE
/lib/modules/%{_kernel_ver}smp/misc/kqemu.ko*
%endif
%endif
