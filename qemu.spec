#
# TODO:
# - wait till the gcc bug http://gcc.gnu.org/PR16185 is fixed.
#
# Conditional build:
%bcond_without	kqemu			# disable KQEMU ACCELERATOR support in QEMU
%bcond_with	cflags_passing		# with passing rpmcflags to Makefiles
%bcond_with	dosguest		# add special patch when use with DOS as guest os
%bcond_with	nosdlgui		# do not use SDL gui (use X11 instead)
# Note that gcc4 build is very problematic and not supported by qemu team
%bcond_with	gcc4			# use gcc4 patches (broke build on gcc33)
%bcond_without	dist_kernel		# without distribution kernel
%bcond_without	kernel			# build kqemu KERNEL MODULES
%bcond_without	up			# don't build up module
%bcond_without	smp			# don't build SMP module
%bcond_without	userspace		# don't build userspace utilities
#
# no kernel kqemu module for ppc
%ifarch ppc
%undefine      with_kqemu
%undefine      with_kernel
%endif
%define	_kqemu_version	1.3.0pre11
%define		_rel	5
Summary:	QEMU CPU Emulator
Summary(pl):	QEMU - emulator procesora
Name:		qemu
Version:	0.9.0
Release:	%{_rel}%{?with_kqemu:k}
License:	GPL
Group:		Applications/Emulators
#Source0Download: http://fabrice.bellard.free.fr/qemu/download.html
Source0:	http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
# Source0-md5:	ab11a03ba30cf4a70641f0f170473d69
Source1:	http://fabrice.bellard.free.fr/qemu/k%{name}-%{_kqemu_version}.tar.gz
# Source1-md5:	970521874ef8b1ba4598925ace5936c3
Patch0:		%{name}-nostatic.patch
Patch1:		%{name}-cc.patch
Patch3:		%{name}-dot.patch
Patch4:		%{name}-gcc4_x86.patch
Patch5:		%{name}-gcc4_ppc.patch
Patch6:		%{name}-nosdlgui.patch
Patch7:		%{name}-ifup.patch
# Proof of concept, for reference, do not remove
Patch8:		%{name}-kde_virtual_workspaces_hack.patch
# http://gwenole.beauchesne.info/en/projects/qemu
Patch9:		%{name}-0.8.0-gcc4-hacks.patch
Patch11:	%{name}-0.7.2-gcc4-opts.patch
#Patch12:	%{name}-0.7.2-dyngen-check-stack-clobbers.patch
Patch13:	%{name}-dosguest.patch
# Fix crash when using qemu instances with NICs connected via socket
# This patch will be obsolete in versions after 0.9.0
Patch14:	%{name}-0.9.0-remove-iohandlers.patch
URL:		http://fabrice.bellard.free.fr/qemu/
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
%if %{with userspace}
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
%{!?with_gcc4:BuildRequires:	gcc < 5:4.0}
BuildRequires:	perl-tools-pod
BuildRequires:	tetex
BuildRequires:	sed >= 4.0
%endif
Requires:	SDL >= 1.2.1
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
ExclusiveArch:	%{ix86} %{x8664} %{!?with_kqemu:ppc}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some SPARC boot image in ELF format
%define		_noautostrip	.*%{_datadir}/qemu/openbios-sparc32

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

%package -n kernel%{_alt_kernel}-misc-kqemu
Summary:	kqemu - kernel module
Summary(pl):	kqemu - modu³ j±dra
Version:	%{_kqemu_version}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
License:	GPL v2
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-misc-kqemu
kqemu - kernel module.

%description -n kernel%{_alt_kernel}-misc-kqemu -l pl
kqemu - modu³ j±dra.

%package -n kernel%{_alt_kernel}-smp-misc-kqemu
Summary:	kqemu - SMP kernel module
Summary(pl):	kqemu - modu³ j±dra SMP
Version:	%{_kqemu_version}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
License:	GPL v2
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-smp-misc-kqemu
kqemu - SMP kernel module.

%description -n kernel%{_alt_kernel}-smp-misc-kqemu -l pl
kqemu - modu³ j±dra SMP.

%prep
%if %{with kernel}
%if %{with dist_kernel} && %{without up} && %{without smp}
%{error:%{name}: If building kernel module You need to enable at least one of up or smp}
exit 1
%endif
%endif

%setup -q %{?with_kernel:-a1}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%if %{with gcc4}
%patch9 -p1
%patch11 -p1
#%patch12 -p1
#%patch4 -p0
%patch5 -p1
%endif
%{?with_nosdlgui:%patch6 -p1}
%patch7 -p1
#%patch8 -p1
%patch14 -p1

%{__sed} -i -e 's/sdl_static=yes/sdl_static=no/' configure
%{__sed} -i 's/.*MAKE) -C kqemu$//' Makefile

# cannot use optflags on x86 - they cause "no register to spill" errors
%if %{with cflags_passing}
%{__sed} -i -e 's/-Wall -O2 -g/-Wall %{rpmcflags}/' Makefile Makefile.target
%else
%{__sed} -i 's/-Wall -O2 -g/-Wall -O2/' Makefile Makefile.target
%endif

%if %{with kernel}
echo -n > kqemu-%{_kqemu_version}/install.sh

cat <<'EOF' > modprobe.conf
# enable dynamic major
options kqemu major=0
# for autoloading from static dev
#alias char-major-250 kqemu
EOF

cat <<'EOF' > udev.conf
KERNEL=="kqemu", NAME="%k", MODE="0666"
EOF
%endif

%if %{with dosguest}
%patch13 -p1
%endif

%build
%if %{with kernel}
cd kqemu-%{_kqemu_version}

%{__sed} -i 's#include ../config-host.mak##' ./common/Makefile
%ifarch %{x8664}
%{__sed} -i 's/^#ARCH=x86_64/ARCH=x86_64/' ./common/Makefile
%{__make} -C common
mv -f kqemu-mod-x86_64.o{,.bin}
%else
%{__sed} -i 's/^#ARCH=i386/ARCH=i386/' ./common/Makefile
%{__make} -C common
mv -f kqemu-mod-i386.o{,.bin}
%endif

mv -f kqemu-linux.c{,.orig}
cat > Makefile <<'EOF'
obj-m := kqemu.o
kqemu-objs:= kqemu-linux.o kqemu-mod.o

$(obj)/kqemu-mod.o: $(src)/kqemu-mod-$(ARCH).o.bin
	cp $< $@
EOF

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
%if %{with kqemu}
	--kernel-path=%{_kernelsrcdir} \
%else
	--disable-kqemu \
%endif
	%{?with_gcc4:--disable-gcc-check} \
	--enable-alsa \
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
%install_kernel_modules -m kqemu-%{_kqemu_version}/kqemu -d misc
install -d $RPM_BUILD_ROOT/etc/{modprobe.d/%{_kernel_ver}{,smp},udev/rules.d}
install modprobe.conf $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/kqemu.conf
%if %{with smp} && %{with dist_kernel}
install modprobe.conf $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}smp/kqemu.conf
%endif
install udev.conf $RPM_BUILD_ROOT/etc/udev/rules.d/kqemu.rules
%endif

# already packaged
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-{doc,tech}.html

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%post
%banner %{name} -e <<EOF
To enable qemu accelerator (kqemu), the kqemu kernel module must be loaded:
modprobe kqemu
EOF
%endif

%post	-n kernel%{_alt_kernel}-misc-kqemu
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-kqemu
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-misc-kqemu
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-misc-kqemu
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
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-kqemu
%defattr(644,root,root,755)
%doc kqemu-%{_kqemu_version}/LICENSE
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/kqemu.rules
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/%{_kernel_ver}/kqemu.conf
/lib/modules/%{_kernel_ver}/misc/kqemu.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-misc-kqemu
%defattr(644,root,root,755)
%doc kqemu-%{_kqemu_version}/LICENSE
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/kqemu.rules
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/%{_kernel_ver}smp/kqemu.conf
/lib/modules/%{_kernel_ver}smp/misc/kqemu.ko*
%endif
%endif
