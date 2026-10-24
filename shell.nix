{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = with pkgs; [
    python312
    pdm
    gcc
    linuxHeaders
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (
    with pkgs;
    [
      stdenv.cc.cc.lib # libstdc++
      zlib
      libGL
      glib
      libxkbcommon
      xorg.libX11
      xorg.libXext
      xorg.libXrender
      xorg.libSM
      xorg.libICE
      fontconfig
      freetype
    ]
  );

  shellHook = ''
    export C_INCLUDE_PATH="${pkgs.linuxHeaders}/include:$C_INCLUDE_PATH"
  '';
}
