import argparse
from PIL import Image
import matplotlib.pyplot as plt

from anonymize import anonymize_png
from png_simple_parser import parse_png_chunks
from display import fourier_transform
from demo_crypto import run_demo

#using argparse to accept arguments from command line
def main():
    parser = argparse.ArgumentParser(description="PNG Decoder")
    parser.add_argument("file", help="Path to PNG file")
    parser.add_argument("--fft", action="store_true", help="Show FFT spectrum")
    parser.add_argument("--anonymize", metavar="OUTPUT", help="Strip metadata and save to OUTPUT")
    parser.add_argument("--crypto", metavar="OUTDIR", nargs='?', const='.', help="Run PNG crypto demo and save outputs to OUTDIR (default current dir)")
    args = parser.parse_args()

    #parsing image
    parse_png_chunks(args.file)

    #displaying image
    img = Image.open(args.file)
    plt.figure("PNG Image")
    plt.imshow(img)
    plt.axis('off')
    plt.title(args.file)
    plt.show()

    #FFT spectrum display
    if args.fft:
        gray = img.convert('L')
        fourier_transform(gray)

    #anonymizing
    if args.anonymize:
        anonymize_png(args.file, args.anonymize)

    #crypto demo
    if args.crypto is not None:
        run_demo(args.file, output_dir=args.crypto)


if __name__ == '__main__':
    main()
