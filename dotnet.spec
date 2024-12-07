# Portions were reused from the Rocky Linux spec here:
# https://git.rockylinux.org/staging/rpms/dotnet9.0/-/blob/r8/SPECS/dotnet9.0.spec
# recipe was adapted to the monolithic repo for dotnet and to remove 
# unnecessary versioning info since newer .net versions support older
# versions

# set to nil when packaging a release, 
# or the long commit tag for the specific git branch
%global commit_tag %{nil}

# set with the commit date only if commit_tag not nil 
# git version (i.e. master) in format date +Ymd
%if "%{commit_tag}" != "%{nil}"
%global commit_date %(git show -s --date=format:'%Y%m%d' %{commit_tag})
%endif

# repack non-release git branches as .7z with the commit date
# in the following format <name>-<version>-<commit_date>.7z
# the short commit tag should be 7 characters long

Name:		   dotnet
Version:        9.0.101%{?commit_date:~%{commit_date}}
Release:        1
Summary:        .NET SDK meta package
Group:          Development
License:        MIT
URL:            https://github.com/dotnet/dotnet

# change the source URL depending on if the package is a release version or a git version
%if "%{commit_tag}" != "%{nil}"
Source0:        https://github.com/%{name}/%{name}/archive/%{commit_tag}.tar.gz#/%{name}-%{version}.tar.xz
%else
Source0:        https://github.com/%{name}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.xz
%endif

Source1:        release.json

BuildRequires:  cmake
BuildRequires:  curl
BuildRequires:  cpio
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  git
BuildRequires:  gnupg2
BuildRequires:  hostname
BuildRequires:  ninja
BuildRequires:  tar
BuildRequires:  util-linux
BuildRequires:  python3

BuildRequires:  pkgconfig(lttng-ust)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libbrotlicommon)
BuildRequires:  pkgconfig(libunwind-llvm)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(RapidJSON)

%description
.NET is a fast, lightweight and modular platform for creating
cross platform applications that work on Linux, macOS and Windows.

It particularly focuses on creating console applications, web
applications and micro-services.

.NET contains a runtime conforming to .NET Standards a set of
framework libraries, an SDK containing compilers and a 'dotnet'
application to drive everything.

%package host

Summary:        .NET command line launcher

%description host
The .NET host is a command line program that runs a standalone
.NET application or launches the SDK.

.NET is a fast, lightweight and modular platform for creating
cross platform applications that work on Linux, Mac and Windows.

It particularly focuses on creating console applications, web
applications and micro-services.

%package hostfxr

Summary:        .NET command line host resolver

Requires:       %{name}-host >= %{version}

%description hostfxr
The .NET host resolver contains the logic to resolve and select
the right version of the .NET SDK or runtime to use.

.NET is a fast, lightweight and modular platform for creating
cross platform applications that work on Linux, Mac and Windows.

It particularly focuses on creating console applications, web
applications and micro-services.

%package runtime

Summary:      .NET Runtime

Requires:     pkgconfig(icu-uc)
Requires:     %{name}-hostfxr >= %{version}

%description runtime
The .NET runtime contains everything needed to run .NET applications.
It includes a high performance Virtual Machine as well as the framework
libraries used by .NET applications.

.NET is a fast, lightweight and modular platform for creating
cross platform applications that work on Linux, Mac and Windows.

It particularly focuses on creating console applications, web
applications and micro-services.

%package runtime-dbg

Summary:      Managed debug symbols .NET runtime

Requires:     %{name}-runtime = %{version}

%description runtime-dbg
This package contains the managed symbol (pdb) files useful to debug the
managed parts of the .NET runtime itself.

%package -n aspnetcore-runtime

Summary:      ASP.NET Core runtime

Requires:     %{name}-runtime = %{version}

%description -n aspnetcore-runtime
The ASP.NET Core runtime contains everything needed to run .NET
web applications. It includes a high performance Virtual Machine as
well as the framework libraries used by .NET applications.

ASP.NET Core is a fast, lightweight and modular platform for creating
cross platform web applications that work on Linux, Mac and Windows.

It particularly focuses on creating console applications, web
applications and micro-services.

%package -n aspnetcore-runtime-dbg

Summary:      Managed debug symbols for the ASP.NET Core runtime

Requires:      aspnetcore-runtime = %{version}

%description -n aspnetcore-runtime-dbg
This package contains the managed symbol (pdb) files useful to debug the
managed parts of the ASP.NET Core runtime itself.

%package templates

Summary:      .NET templates

Requires:     %{name}-host >= %{version}

%description templates
This package contains templates used by the .NET SDK.

.NET is a fast, lightweight and modular platform for creating
cross platform applications that work on Linux, Mac and Windows.

It particularly focuses on creating console applications, web
applications and micro-services.

%package sdk

Summary:      .NET Software Development Kit

Requires:     %{name}-runtime >= %{version}
Requires:     aspnetcore-runtime >= %{version}

Requires:     %{name}-apphost-pack >= %{version}
Requires:     %{name}-targeting-pack >= %{version}
Requires:     aspnetcore-targeting-pack >= %{version}
Requires:     netstandard-targeting-pack-2.1 >= %{version}

Requires:     %{name}-templates >= %{version}

%description sdk
The .NET SDK is a collection of command line applications to
create, build, publish and run .NET applications.

.NET is a fast, lightweight and modular platform for creating
cross platform applications that work on Linux, Mac and Windows.

It particularly focuses on creating console applications, web
applications and micro-services

%package sdk-dbg

Summary:      Managed debug symbols for the .NET Software Development Kit

Requires:     %{name}-sdk = %{version}

%description sdk-dbg
This package contains the managed symbol (pdb) files useful to debug the .NET
Software Development Kit (SDK) itself.

%package sdk-aot

Summary:      Ahead-of-Time (AOT) support for the .NET Software Development Kit

Requires:     %{name}-sdk = %{version}

Requires:     pkgconfig(libbrotlicommon)
Requires:     pkgconfig(ssl)
Requires:     pkgconfig(zlib)

%description sdk-aot

This package provides Ahead-of-time (AOT) compilation support for the .NET SDK.

%package apphost-pack

Summary:      Targeting Pack for apphost

Requires:     %{name}-host

%description apphost-pack
Allows developers to compile and target apphost using .NET SDK.

%files apphost-pack
%dir %{_libdir}/dotnet/packs
%{_libdir}/dotnet/packs/Microsoft.NETCore.App.Host.*

%package targeting-pack

Summary:      Targeting Pack for %{name}

Requires:     %{name}-host

%description targeting-pack
Allows developers to compile and target %{name} using .NET SDK.

%files targeting-pack
%dir %{_libdir}/dotnet/packs
%{_libdir}/dotnet/packs/Microsoft.NETCore.App.Ref

%package -n aspnetcore-targeting-pack

Summary:      Targeting Pack for aspnetcore

Requires:     %{name}-host

%description -n aspnetcore-targeting-pack
Allows developers to compile and target aspnetcore using .NET SDK.

%files -n aspnetcore-targeting-pack
%dir %{_libdir}/dotnet/packs
%{_libdir}/dotnet/packs/Microsoft.AspNetCore.App.Ref

%package -n netstandard-targeting-pack

Summary:      Targeting Pack for NETStandard.Library 2.1

Requires:     %{name}-host

%description -n netstandard-targeting-pack
Allows developers to compile and target NETStandard library 2.1 using .NET SDK.

%files -n netstandard-targeting-pack
%dir %{_libdir}/dotnet/packs
%{_libdir}/dotnet/packs/NETStandard.Library.Ref

%package sdk-source-built-artifacts

Summary:      Internal package for building .NET Software Development Kit

%description sdk-source-built-artifacts
The .NET source-built archive is a collection of packages needed
to build the .NET SDK itself.

These are not meant for general use.

%prep
%autosetup -p1
# since abf does not allow downloading components during builds
# prep-source-build.sh is temporarily run manually 
# and then the source is compressed
# until a better solution can be found
%build
./build.sh -sb --clean-while-building \
    --release-manifest %{S:1} \
    --with-system-libs brotli+llvmlibunwind+rapidjson+zlib

%install
install -dm 0755 %{buildroot}%{_libdir}/dotnet

tar xf artifacts/assets/Release/dotnet-sdk-*.tar.gz -C %{buildroot}%{_libdir}/dotnet/

# Delete bundled certificates: we want to use the system store only,
# except for when we have no other choice and ca-certificates doesn't
# provide it. Currently ca-ceritificates has no support for
# timestamping certificates (timestamp.ctl).
find %{buildroot}%{_libdir}/dotnet -name 'codesignctl.pem' -delete
if [[ $(find %{buildroot}%{_libdir}/dotnet -name '*.pem' -print | wc -l) != 1 ]]; then
    find %{buildroot}%{_libdir}/dotnet -name '*.pem' -print
    echo "too many certificate bundles"
    exit 2
fi

# Install managed symbols
tar xf artifacts/assets/Release/dotnet-symbols-sdk-*.tar.gz \
   -C %{buildroot}%{_libdir}/dotnet/
find %{buildroot}%{_libdir}/dotnet/packs -iname '*.pdb' -delete

# Fix executable permissions on files
find %{buildroot}%{_libdir}/dotnet/ -type f -name 'apphost' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name 'ilc' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name 'singlefilehost' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.sh' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name 'lib*so' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.a' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.dll' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.h' -exec chmod 0644 {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.json' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.o' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.pdb' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.props' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.pubxml' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.targets' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.txt' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/dotnet/ -type f -name '*.xml' -exec chmod -x {} \;

# Install dynamic completions
install -dm 0755 %{buildroot}/%{_datadir}/bash-completion/completions
install src/sdk/scripts/register-completions.bash %{buildroot}/%{_datadir}/bash-completion/completions/dotnet
install -dm 755 %{buildroot}/%{_datadir}/zsh/site-functions
install src/sdk/scripts/register-completions.zsh %{buildroot}/%{_datadir}/zsh/site-functions/_dotnet

install -dm 0755 %{buildroot}%{_bindir}
ln -s ../../%{_libdir}/dotnet/dotnet %{buildroot}%{_bindir}/

for section in 1 7; do
    install -dm 0755 %{buildroot}%{_mandir}/man${section}/
    find -iname 'dotnet*'.${section} -type f -exec cp {} %{buildroot}%{_mandir}/man${section}/ \;
done

install -dm 0755 %{buildroot}%{_sysconfdir}/dotnet
echo "%{_libdir}/dotnet" >> install_location
install install_location %{buildroot}%{_sysconfdir}/dotnet/

install -dm 0755 %{buildroot}%{_libdir}/dotnet/source-built-artifacts
install -m 0644 artifacts/assets/Release/Private.SourceBuilt.Artifacts.*.tar.gz %{buildroot}/%{_libdir}/dotnet/source-built-artifacts/

find %{buildroot}%{_libdir}/dotnet/shared/Microsoft.NETCore.App -type f -and -not -name '*.pdb' | sed -E 's|%{buildroot}||' > dotnet-runtime-non-dbg-files
find %{buildroot}%{_libdir}/dotnet/shared/Microsoft.NETCore.App -type f -name '*.pdb'  | sed -E 's|%{buildroot}||' > dotnet-runtime-dbg-files
find %{buildroot}%{_libdir}/dotnet/shared/Microsoft.AspNetCore.App -type f -and -not -name '*.pdb'  | sed -E 's|%{buildroot}||' > aspnetcore-runtime-non-dbg-files
find %{buildroot}%{_libdir}/dotnet/shared/Microsoft.AspNetCore.App -type f -name '*.pdb' | sed -E 's|%{buildroot}||' > aspnetcore-runtime-dbg-files
find %{buildroot}%{_libdir}/dotnet/sdk -type d | tail -n +2 | sed -E 's|%{buildroot}||' | sed -E 's|^|%dir |' > dotnet-sdk-non-dbg-files
find %{buildroot}%{_libdir}/dotnet/sdk -type f -and -not -name '*.pdb' | sed -E 's|%{buildroot}||' >> dotnet-sdk-non-dbg-files
find %{buildroot}%{_libdir}/dotnet/sdk -type f -name '*.pdb'  | sed -E 's|%{buildroot}||' > dotnet-sdk-dbg-files

%check

%files host
%dir %{_libdir}/dotnet
%{_libdir}/dotnet/dotnet
%dir %{_libdir}/dotnet/host
%dir %{_libdir}/dotnet/host/fxr
%{_bindir}/dotnet
%license %{_libdir}/dotnet/LICENSE.txt
%license %{_libdir}/dotnet/ThirdPartyNotices.txt
%doc %{_mandir}/man1/dotnet*.1.*
%doc %{_mandir}/man7/dotnet*.7.*
%config(noreplace) %{_sysconfdir}/dotnet
%{_datadir}/bash-completion/completions/dotnet
%{_datadir}/zsh/site-functions/_dotnet


%files hostfxr
%dir %{_libdir}/dotnet/host/fxr
%{_libdir}/dotnet/host/fxr/*

%files runtime -f %{name}-runtime-non-dbg-files
%dir %{_libdir}/dotnet/shared
%dir %{_libdir}/dotnet/shared/Microsoft.NETCore.App
%dir %{_libdir}/dotnet/shared/Microsoft.NETCore.App/*

%files runtime-dbg -f %{name}-runtime-dbg-files

%files -n aspnetcore-runtime -f aspnetcore-runtime-non-dbg-files
%dir %{_libdir}/dotnet/shared
%dir %{_libdir}/dotnet/shared/Microsoft.AspNetCore.App
%dir %{_libdir}/dotnet/shared/Microsoft.AspNetCore.App/*

%files -n aspnetcore-runtime-dbg -f aspnetcore-runtime-dbg-files

%files templates
%dir %{_libdir}/dotnet/templates
%{_libdir}/dotnet/templates/*

%files sdk -f %{name}-sdk-non-dbg-files
%dir %{_libdir}/dotnet/sdk
%dir %{_libdir}/dotnet/sdk-manifests
%{_libdir}/dotnet/sdk-manifests/*
# FIXME is using a 8.0.100 version a bug in the SDK?
%{_libdir}/dotnet/metadata
%{_libdir}/dotnet/library-packs
%dir %{_libdir}/dotnet/packs
%dir %{_libdir}/dotnet/packs/Microsoft.AspNetCore.App.Runtime.*
%{_libdir}/dotnet/packs/Microsoft.AspNetCore.App.Runtime.*/*
%dir %{_libdir}/dotnet/packs/Microsoft.NETCore.App.Runtime.*
%{_libdir}/dotnet/packs/Microsoft.NETCore.App.Runtime.*/*

%files sdk-dbg -f %{name}-sdk-dbg-files

%files sdk-aot
%dir %{_libdir}/dotnet/packs
%dir %{_libdir}/dotnet/packs/runtime.*.Microsoft.DotNet.ILCompiler/
%{_libdir}/dotnet/packs/runtime.*.Microsoft.DotNet.ILCompiler/*

%files sdk-source-built-artifacts
%dir %{_libdir}/dotnet
%{_libdir}/dotnet/source-built-artifacts

