#
# Conditional build:
%bcond_with	kqemu			# with QEMU accelerator module
#
Summary:	QEMU CPU Emulator
Summary(pl):	QEMU - emulator procesora
Name:		qemu
Version:	0.7.0
Release:	1.2
License:	GPL
Group:		Applications/Emulators
#Source0Download: http://fabrice.bellard.free.fr/qemu/download.html
Source0:	http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
# Source0-md5:	234e9ace03b00259bb57dc5a9c633056
%if %{with kqemu}
Source1:	http://fabrice.bellard.free.fr/qemu/kqemu-0.6.2-1.tar.gz
# NoSource1-md5:	c6bb3b40fb3d526d731eb0f1f9dee7ee
NoSource:	1
%endif
Patch0:		%{name}-nostatic.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-longjmp.patch
Patch3:		%{name}-dot.patch
Patch4:		%{name}-initrd_load_addr.patch
URL:		http://fabrice.bellard.free.fr/qemu/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	sed >= 4.0
%if %{with kqemu}
BuildRequires: kernel-source
%endif
ExclusiveArch:	%{ix86} %{x8664} ppc
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
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
  including a processor and various peripherials. 
  It can also be used to provide virtual hosting of several 
  virtual PC on a single server.

%description -l pl
QEMU to szybki(!) emulator procesora. Poprzez u¿ycie dynamicznego
t³umaczenia osi±ga rozs±dn± szybko¶æ i jest ³atwy do przeportowania,
aby dzia³a³ na kolejnych procesorach. QEMU ma dwa tryby pracy:

- Emulacja trybu u¿ytkownika. W tym trybie QEMU mo¿e uruchamiaæ
  procesy linuksowe skompilowane dla jednego procesora na innym
  procesorze. Linuksowe wywo³ania systemowe s± t³umaczone ze wzglêdu
  na niezgodno¶æ kolejno¶ci bajtów w s³owie i 32/64-bitowego rozmiaru
  s³owa. Wine (emulacja Windows) i DOSEMU (emulacja DOS-a) to g³ówne
  cele QEMU.

- Pe³na emulacja systemu. W tym trybie QEMU emuluje ca³y system,
  w³±czaj±c w to procesor i ró¿ne urz±dzenia peryferyjne.
  Mo¿e byæ tak¿e u¿ywane do wirtualnego hostowania kilku wirtualnych 
  pecetów na pojedynczym serwerze.

%prep
%setup -q %{?with_kqemu:-a1}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

sed -i -e 's/sdl_static=yes/sdl_static=no/' configure
# cannot use optflags on x86 - they cause "no register to spill" errors
#sed -i -e 's/-Wall -O2 -g/-Wall %{rpmcflags}/' Makefile Makefile.target

%{?with_kqemu:echo -n > kqemu/install.sh}

%build

%if %{with kqemu}
cp -rdp %{_kernelsrcdir}/ .
rm -f linux/.config
cp -f linux/config-smp linux/.config
make -C linux modules_prepare
%endif

# --extra-cflags don't work (overridden by CFLAGS in Makefile*)
./configure \
	--prefix=%{_prefix} \
	--cc="%{__cc}" \
  %if %{with kqemu}
	--enable-kqemu }\
	--kernel-path=`pwd`/linux \
  %endif
	--make="%{__make}"

%{__make} 

%if %{with kqemu}
mv kqemu/kqemu.ko kqemu/kqemu.smp
cp -f linux/config-up linux/.config
make -C linux modules_prepare
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with kqemu}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install kqemu/kqemu.smp $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/kqemu.ko
install kqemu/kqemu.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with kqemu}
%depmod

%banner %{name} -e << EOF
To enable qemu accelerator (kqemu), You must manually create device for it:
mknod /dev/kqemu c 250 0
chmod 666 /dev/kqemu

And before start qemu, the kqemu kernel module must be loaded:
modprobe kqemu
EOF
%endif

%postun
%{?with_kqemu: %depmod}

%files
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) %{_bindir}/*
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
%{?with_kqemu: /lib/*}
