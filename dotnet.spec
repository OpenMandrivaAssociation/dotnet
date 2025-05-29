# Portions were reused from the Rocky Linux spec here:
# https://git.rockylinux.org/staging/rpms/dotnet9.0/-/blob/r8/SPECS/dotnet9.0.spec
# recipe was adapted to the monolithic repo for dotnet and to remove 
# unnecessary versioning info since newer .net versions support older
# versions

# Bootstrapping guidelines are found here:
# https://github.com/dotnet/source-build/blob/main/Documentation/bootstrapping-guidelines.md
# It must be created locally and uploaded as part of the spec binaries to ABF for each major version.

%define bootstrap_version 9.0.106
%ifarch %{x86_64}
%define bootstrap_arch x64
%endif
%ifarch %{aarch64}
%define bootstrap_arch arm64
%endif

Name:		   dotnet
Version:        9.0.5
Release:        3
Summary:        .NET SDK meta package
Group:          Development
License:        MIT
URL:            https://github.com/dotnet/dotnet

Source0:        https://github.com/%name/%name/archive/v%version.tar.gz#/%name-%version.tar.gz
Source1:        release-%version.json
Source2:        %name-sdk-%{bootstrap_version}-%{_vendor}.%{product_version}-%{bootstrap_arch}.tar.gz
Source3:        Private.SourceBuilt.Artifacts.%{bootstrap_version}-servicing.25230.1.%{_vendor}.%{product_version}-%{bootstrap_arch}.tar.gz

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
BuildRequires:  pkgconfig(mit-krb5)
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
Requires:     netstandard-targeting-pack >= %{version}

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
mkdir bs_sdk bs_artifacts
tar zxf %{S:2} -C bs_sdk 
tar zxf %{S:3} -C bs_artifacts
./prep-source-build.sh \
    --no-sdk \
    --no-artifacts \
    --no-bootstrap \
    --no-prebuilts \
    --no-binary-removal \
    --with-sdk %{_builddir}/%name-%version/bs_sdk \
    --with-packages %{_builddir}/%name-%version/bs_artifacts

%build
DOTNET_CLI_TELEMETRY_OPTOUT=1 ./build.sh \
    --source-only \
    --with-sdk %{_builddir}/%name-%version/bs_sdk \
    --with-packages %{_builddir}/%name-%version/bs_artifacts \
    --release-manifest %{S:1} \
    --with-system-libs brotli+llvmlibunwind+rapidjson+zlib 

%install
install -dm 0755 %{buildroot}%{_libdir}/%name

tar zxf artifacts/assets/Release/%name-sdk-*.tar.gz -C %{buildroot}%{_libdir}/dotnet/

# Delete bundled certificates: we want to use the system store only,
# except for when we have no other choice and ca-certificates doesn't
# provide it. Currently ca-ceritificates has no support for
# timestamping certificates (timestamp.ctl).
find %{buildroot}%{_libdir}/%name -name 'codesignctl.pem' -delete
if [[ $(find %{buildroot}%{_libdir}/%name -name '*.pem' -print | wc -l) != 1 ]]; then
    find %{buildroot}%{_libdir}/%name -name '*.pem' -print
    echo "too many certificate bundles"
    exit 2
fi

# Install managed symbols
tar zxf artifacts/assets/Release/%name-symbols-sdk-*.tar.gz \
   -C %{buildroot}%{_libdir}/%name/
find %{buildroot}%{_libdir}/%name/packs -iname '*.pdb' -delete

# Fix executable permissions on files
find %{buildroot}%{_libdir}/%name/ -type f -name 'apphost' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name 'ilc' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name 'singlefilehost' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.sh' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name 'lib*so' -exec chmod +x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.a' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.dll' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.h' -exec chmod 0644 {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.json' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.o' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.pdb' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.props' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.pubxml' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.targets' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.txt' -exec chmod -x {} \;
find %{buildroot}%{_libdir}/%name/ -type f -name '*.xml' -exec chmod -x {} \;

# Install dynamic completions
install -dm 0755 %{buildroot}/%{_datadir}/bash-completion/completions
install src/sdk/scripts/register-completions.bash %{buildroot}/%{_datadir}/bash-completion/completions/%name
install -dm 755 %{buildroot}/%{_datadir}/zsh/site-functions
install src/sdk/scripts/register-completions.zsh %{buildroot}/%{_datadir}/zsh/site-functions/_%name

install -dm 0755 %{buildroot}%{_bindir}
ln -s ../../%{_libdir}/%name/%name %{buildroot}%{_bindir}/

install -dm 0755 %{buildroot}%{_sysconfdir}/%name
echo "%{_libdir}/%name" >> install_location
install install_location %{buildroot}%{_sysconfdir}/%name/

install -dm 0755 %{buildroot}%{_libdir}/%name/source-built-artifacts
install -m 0644 artifacts/assets/Release/Private.SourceBuilt.Artifacts.*.tar.gz %{buildroot}/%{_libdir}/%name/source-built-artifacts/

find %{buildroot}%{_libdir}/%name/shared/Microsoft.NETCore.App -type f -and -not -name '*.pdb' | sed -E 's|%{buildroot}||' > %name-runtime-non-dbg-files
find %{buildroot}%{_libdir}/%name/shared/Microsoft.NETCore.App -type f -name '*.pdb'  | sed -E 's|%{buildroot}||' > %name-runtime-dbg-files
find %{buildroot}%{_libdir}/%name/shared/Microsoft.AspNetCore.App -type f -and -not -name '*.pdb'  | sed -E 's|%{buildroot}||' > aspnetcore-runtime-non-dbg-files
find %{buildroot}%{_libdir}/%name/shared/Microsoft.AspNetCore.App -type f -name '*.pdb' | sed -E 's|%{buildroot}||' > aspnetcore-runtime-dbg-files
find %{buildroot}%{_libdir}/%name/sdk -type d | tail -n +2 | sed -E 's|%{buildroot}||' | sed -E 's|^|%dir |' > %name-sdk-non-dbg-files
find %{buildroot}%{_libdir}/%name/sdk -type f -and -not -name '*.pdb' | sed -E 's|%{buildroot}||' >> %name-sdk-non-dbg-files
find %{buildroot}%{_libdir}/%name/sdk -type f -name '*.pdb'  | sed -E 's|%{buildroot}||' > %name-sdk-dbg-files

%check

%files host
%dir %{_libdir}/%name
%{_libdir}/%name/%name
%dir %{_libdir}/%name/host
%dir %{_libdir}/%name/host/fxr
%{_bindir}/%name
%license %{_libdir}/%name/LICENSE.txt
%license %{_libdir}/%name/ThirdPartyNotices.txt
# %doc %{_mandir}/man1/%name*.1.*
# %doc %{_mandir}/man7/%name*.7.*
%config(noreplace) %{_sysconfdir}/%name
%{_datadir}/bash-completion/completions/%name
%{_datadir}/zsh/site-functions/_%name


%files hostfxr
%dir %{_libdir}/%name/host/fxr
%{_libdir}/%name/host/fxr/*

%files runtime -f %name-runtime-non-dbg-files
%dir %{_libdir}/%name/shared
%dir %{_libdir}/%name/shared/Microsoft.NETCore.App
%dir %{_libdir}/%name/shared/Microsoft.NETCore.App/*

%files runtime-dbg -f %name-runtime-dbg-files

%files -n aspnetcore-runtime -f aspnetcore-runtime-non-dbg-files
%dir %{_libdir}/%name/shared
%dir %{_libdir}/%name/shared/Microsoft.AspNetCore.App
%dir %{_libdir}/%name/shared/Microsoft.AspNetCore.App/*

%files -n aspnetcore-runtime-dbg -f aspnetcore-runtime-dbg-files

%files templates
%dir %{_libdir}/%name/templates
%{_libdir}/%name/templates/*

%files sdk -f %name-sdk-non-dbg-files
%dir %{_libdir}/%name/sdk
%dir %{_libdir}/%name/sdk-manifests
%{_libdir}/%name/sdk-manifests/*
# FIXME is using a 8.0.100 version a bug in the SDK?
%{_libdir}/%name/metadata
%{_libdir}/%name/library-packs
%dir %{_libdir}/%name/packs
%dir %{_libdir}/%name/packs/Microsoft.AspNetCore.App.Runtime.*
%{_libdir}/%name/packs/Microsoft.AspNetCore.App.Runtime.*/*
%dir %{_libdir}/%name/packs/Microsoft.NETCore.App.Runtime.*
%{_libdir}/%name/packs/Microsoft.NETCore.App.Runtime.*/*

%files sdk-dbg -f %name-sdk-dbg-files

%files sdk-aot
%dir %{_libdir}/%name/packs
%dir %{_libdir}/%name/packs/runtime.*.Microsoft.DotNet.ILCompiler/
%{_libdir}/%name/packs/runtime.*.Microsoft.DotNet.ILCompiler/*

%files sdk-source-built-artifacts
%dir %{_libdir}/%name
%{_libdir}/%name/source-built-artifacts

