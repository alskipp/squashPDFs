# squashPDFs

A simple utility that takes a directory of PDFs containing images and a directory of PDFs containing text and makes a multi-page low-res PDF with images and text combined.


## Usage

``` python
python3 squashPDFs.py ~/Documents/image_pdfs ~/Documents/text_pdfs ~/Documents/output.pdf
```

---

## Dependencies

* [Ghostscript](https://www.ghostscript.com) to compress the PDFs
* [pyPDF2](https://pythonhosted.org/PyPDF2/) for merging image and text PDFs

## Installation

If you use the [Nix package manager](https://nixos.org/nix) then in the terminal, just enter:

`nix-shell`

Otherwise ensure you have `Python3.8`, `pyPDF2` and `Ghostscript` installed.

## Nix installation on Mac OS Catalina

For Mac OS Catalina users the installation requires some [extra setup](https://github.com/NixOS/nix/issues/2925#issuecomment-539570232)
