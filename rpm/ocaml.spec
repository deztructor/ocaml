# based on https://build.opensuse.org/package/view_file/devel:languages:ocaml/ocaml/ocaml.spec?expand=1
# This ensures that the find_provides/find_requires calls ocamlobjinfo correctly.
%global __ocaml_requires_opts -c -f "%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo"
%global __ocaml_provides_opts -f "%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo"

%global do_opt 1

Name: ocaml
Version: 0.0.0
Release: 1
Group: Development/Languages/Other
License: QPL-1.0, LGPLv2
URL: http://caml.inria.fr/
Source0: %{name}-%{version}.tar.bz2
Summary: OCaml
BuildRequires:  binutils-devel
BuildRequires:  fdupes
BuildRequires:  ncurses-devel
Requires:       ocaml-runtime = %{version}
Provides:       ocaml(compiler) = %{version}
Requires:       gcc
Provides:       ocaml(ocaml.opt) = %{version}

%description
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler
and an optimizing native-code compiler), an interactive top level
system, Lex&Yacc tools, a replay debugger, and a comprehensive library.

%package       rpm-macros
Summary:        RPM macros for building OCaml source packages
License:        QPL-1.0 and SUSE-LGPL-2.0-with-linking-exception
Group:          Development/Languages/Other

%description       rpm-macros
A set of helper macros to unify common code used in ocaml spec files.

%package runtime
Summary:        The Objective Caml Compiler and Programming Environment
License:        QPL-1.0
Group:          Development/Languages/Other
Provides:       ocaml(runtime) = %{version}
%if 0%{?suse_version} < 1210
# Due to lack of generated requires in old rpm, force this
Requires:       ocaml-compiler-libs = %{version}
%endif

%description runtime
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package contains the runtime environment needed to run Objective
Caml bytecode.

%package source
Summary:        Source code for Objective Caml libraries
License:        QPL-1.0 and SUSE-LGPL-2.0-with-linking-exception
Group:          Development/Languages/Other
Requires:       ocaml = %{version}

%description source
Source code for Objective Caml libraries.

%package ocamldoc
Summary:        The Objective Caml Compiler and Programming Environment
License:        QPL-1.0
Group:          Development/Languages/Other
Requires:       ocaml = %{version}

%description ocamldoc
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package contains a documentation generator for Objective Caml.

%package docs
Summary:        The Objective Caml Compiler and Programming Environment
License:        GPL-2.0+ and QPL-1.0
Group:          Development/Languages/Other
Requires:       ocaml = %{version}

%description docs
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler
and an optimizing native-code compiler), an interactive top level
system, Lex&Yacc tools, a replay debugger, and a comprehensive library.

%package compiler-libs
Summary:        Libraries used internal to the OCaml Compiler
License:        QPL-1.0
Group:          Development/Libraries/Other
Requires:       ocaml = %{version}

%description compiler-libs
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package contains several modules used internally by the OCaml
compilers. They are not needed for normal OCaml development, but may
be helpful in the development of certain applications.

%package compiler-libs-devel
Summary:        Libraries used internal to the OCaml Compiler
License:        QPL-1.0
Group:          Development/Libraries/Other
Requires:       ocaml-compiler-libs = %{version}

%description compiler-libs-devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
%description devel
%summary

%prep
%setup -q

%build
./configure -prefix /usr -mandir %{_mandir}
make world.opt
#%{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
make install \
     BINDIR="%{buildroot}%{_bindir}" \
     LIBDIR="%{buildroot}%{_libdir}/ocaml" \
     MANDIR="%{buildroot}%{_mandir}"

sed -i -e "s|^$RPM_BUILD_ROOT||" %{buildroot}%{_libdir}/ocaml/ld.conf

export EXCLUDE_FROM_STRIP="ocamldebug ocamlbrowser"

# Install the compiler libs
install -d %{buildroot}%{_libdir}/ocaml/compiler-libs
cp -a typing/ utils/ parsing/ %{buildroot}%{_libdir}/ocaml/compiler-libs
%fdupes %{buildroot}

mkdir -vp %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.%{name} <<_EOF_
# get rid of /usr/lib/rpm/find-debuginfo.sh
# strip kills the bytecode part of ELF binaries
%if %{do_opt}
%%ocaml_preserve_bytecode \
	%%{nil}
%%ocaml_native_compiler 1
%else
%%ocaml_preserve_bytecode \
	%%undefine _build_create_debug \
	%%define __arch_install_post export NO_BRP_STRIP_DEBUG=true \
	%%{nil}
%%ocaml_native_compiler 0
%endif
_EOF_
cat %{buildroot}%{_sysconfdir}/rpm/macros.%{name}

%files
%defattr(-,root,root)
%doc Changes LICENSE README
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmxs
%{_libdir}/ocaml/*.cmxa
%{_libdir}/ocaml/*.cmx
%{_libdir}/ocaml/*.o
%{_libdir}/ocaml/*.mli
%{_libdir}/ocaml/libcamlrun_shared.so
%{_libdir}/ocaml/libasmrun_shared.so
%{_libdir}/ocaml/vmthreads/*.mli
%{_libdir}/ocaml/vmthreads/*.a
%{_libdir}/ocaml/threads/*.cmxa
%{_libdir}/ocaml/threads/*.cmx
%{_libdir}/ocaml/threads/*.a
%{_libdir}/ocaml/caml
%{_libdir}/ocaml/ocamlbuild
%{_libdir}/ocaml/Makefile.config
%{_libdir}/ocaml/VERSION
%{_libdir}/ocaml/extract_crc
%{_libdir}/ocaml/camlheader
%{_libdir}/ocaml/camlheader_ur
%{_libdir}/ocaml/expunge
%{_libdir}/ocaml/ld.conf
%{_libdir}/ocaml/objinfo_helper
%exclude %{_bindir}/ocamlrun
%exclude %{_bindir}/ocamldoc*
%exclude %{_libdir}/ocaml/ocamldoc

%files rpm-macros
%defattr(-,root,root,-)
%dir %{_sysconfdir}/rpm
%config %{_sysconfdir}/rpm/*

%files runtime
%defattr(-,root,root,-)
%{_bindir}/ocamlrun
%dir %{_libdir}/ocaml
%{_libdir}/ocaml/*.cmo
%{_libdir}/ocaml/*.cmi
%{_libdir}/ocaml/*.cmt
%{_libdir}/ocaml/*.cmti
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/stublibs
%dir %{_libdir}/ocaml/vmthreads
%{_libdir}/ocaml/vmthreads/*.cmi
%{_libdir}/ocaml/vmthreads/*.cma
%dir %{_libdir}/ocaml/threads
%{_libdir}/ocaml/threads/*.cmi
%{_libdir}/ocaml/threads/*.cma
%doc README LICENSE Changes

%files source
%defattr(-,root,root,-)
%{_libdir}/ocaml/*.ml

%files ocamldoc
%defattr(-,root,root,-)
%{_bindir}/ocamldoc*
%{_libdir}/ocaml/ocamldoc
%doc ocamldoc/Changes.txt

%files compiler-libs
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/ocaml/compiler-libs
%exclude %{_libdir}/ocaml/compiler-libs/*.cmx
%exclude %{_libdir}/ocaml/compiler-libs/*.o

%files compiler-libs-devel
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/ocaml/compiler-libs/*.cmx
%{_libdir}/ocaml/compiler-libs/*.o
