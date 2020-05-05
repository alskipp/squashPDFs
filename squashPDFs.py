import argparse
import fnmatch
import glob
import os
import subprocess
import tempfile
from PyPDF2 import PdfFileReader, PdfFileWriter


def merge_pages(path_1, path_2):
    page_1_reader = PdfFileReader(path_1)
    page_2_reader = PdfFileReader(path_2)

    master_page = page_1_reader.getPage(0)
    overlay_page = page_2_reader.getPage(0)

    return overlay_text(master_page, overlay_page)


def overlay_text(master_page, overlay_page):
    (tx, ty) = translate_to_center(master_page.mediaBox, overlay_page.mediaBox)
    master_page.mergeTranslatedPage(overlay_page, tx, ty)

    return master_page


def translate_to_center(rect1, rect2):
    (x1, y1) = rect1.upperRight
    (x2, y2) = rect2.upperRight
    return ((x1 - x2) / 2, (y1 - y2) / 2)


def compress_pdf(input_file, output_file):
    gs = f"gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.6 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile={output_file} {input_file}"
    subprocess.call(gs, shell=True)


def process_files(output, pages, text):
    pdf_writer = PdfFileWriter()

    with tempfile.TemporaryDirectory() as tmpdirname:
        for page_path, text_path in zip(pages, text):
            compressed_file_path = os.path.join(tmpdirname, os.path.basename(page_path))

            print(
                f"processing: {os.path.basename(page_path)} & {os.path.basename(text_path)}"
            )

            compress_pdf(page_path, compressed_file_path)

            pdf_writer.addPage(merge_pages(compressed_file_path, text_path))

    with open(output, "wb") as fh:
        print(f"writing output file: {output}")
        pdf_writer.write(fh)


def pdf_files(dir):
    return sorted(glob.glob(dir + "/*.[pP][dD][fF]"))


def main():
    parser = argparse.ArgumentParser(
        description="Combine image and text PDFs into low-res PDF"
    )
    parser.add_argument("image_dir", type=str, help="Directory containing image PDFs")
    parser.add_argument("text_dir", type=str, help="Directory containing text PDFs")
    parser.add_argument("output_file", type=str, help="File path to save PDF file")

    args = vars(parser.parse_args())

    pages = pdf_files(args["image_dir"])
    text = pdf_files(args["text_dir"])
    process_files(args["output_file"], pages, text)


if __name__ == "__main__":
    main()

# Example Terminal useage:
# To get help:
# -> python3 squashPDFs.py --help
#
# To run the program (replace example args with locations of files to process):
# -> python3 squashPDFs.py /Documents/image_pdfs /Documents/text_pdfs /Documents/output.pdf
