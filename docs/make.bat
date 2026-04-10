@echo off
set SPHINXBUILD=sphinx-build
set SOURCEDIR=source
set BUILDDIR=_build

if "%1"=="" (
    %SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%\html
) else (
    %SPHINXBUILD% -b %1 %SOURCEDIR% %BUILDDIR%\%1
)

echo.
echo Build finished. The HTML pages are in %BUILDDIR%\html.
