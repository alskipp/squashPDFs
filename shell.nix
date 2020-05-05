with import <nixpkgs> { };
with python38Packages;

pkgs.stdenv.mkDerivation {
  name = "env";
  buildInputs = [ pypdf2 pkgs.ghostscript ];
}
