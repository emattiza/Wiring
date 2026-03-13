{ pkgs }: let 
  python = pkgs.python312.withPackages(ps: with ps; [pytest]); 
  ruby = pkgs.ruby;
in
  {
  deps = [
    pkgs.uv
    pkgs.entr
    python
    ruby
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    ];
    # PYTHONHOME = "${pkgs.python312Full}";
    # PYTHONBIN = "${pkgs.python312Full}/bin/python3.10";
    # LANG = "en_US.UTF-8";
    # STDERREDBIN = "${pkgs.replitPackages.stderred}/bin/stderred";
    # PRYBAR_PYTHON_BIN = "${pkgs.replitPackages.prybar-python310}/bin/prybar-python312";
  };
}