"""
GifSplit CLI Interface
Command-line interface for the GifSplit tool, allowing batch processing and automation.

Features:
- Crop GIFs to specific dimensions
- Optional circular cropping
- Grid-based splitting
- Size optimization
- Output resizing with aspect ratio preservation
"""

import argparse
from gif_processor import GifProcessor

def main():
    """Process GIF files according to command-line arguments."""
    # Set up command-line argument parser with detailed help messages
    parser = argparse.ArgumentParser(description='Split and process GIF files')
    parser.add_argument('--input', required=True, help='Input GIF file')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--width', type=int, default=200, help='Selection width')
    parser.add_argument('--height', type=int, default=200, help='Selection height')
    parser.add_argument('--out_width', type=int, default=None, help='Target width')
    parser.add_argument('--out_height', type=int, default=None, help='Target height')
    parser.add_argument('--grid', default='2x2', help='Grid size (e.g., 2x2)')
    parser.add_argument('--circular', action='store_true', help='Crop the GIF into a circle')
    parser.add_argument('--max-size', type=int, default=500,
                      help='Maximum size per chunk in KB')
    parser.add_argument('--left', type=int, default=0, help='Left position')
    parser.add_argument('--top', type=int, default=0, help='Top position')
    
    args = parser.parse_args()
    
    try:
        # Parse grid dimensions
        rows, cols = map(int, args.grid.split('x'))
        
        print(f"Processing {args.input}...")

        # Initialize GIF processor
        processor = GifProcessor(args.input)

        # Step 1: Crop to selection rectangle
        print(" Cropping to rectangle...")
        processor.crop_to_rect(args.left, args.top, args.width, args.height)
        
        # Step 2: Resize output if dimensions specified
        if args.out_width or args.out_height:
            print(" Resizing GIF...")
            # Calculate missing dimension to maintain aspect ratio
            aspect = args.width / args.height
            out_width = args.out_width
            out_height = args.out_height
            if not out_width:
                out_width = int(out_height * aspect)
            if not out_height:
                out_height = int(out_width / aspect)

            processor.resize(out_width, out_height)
        
        # Step 3: Apply circular crop if requested
        if args.circular:
            print(" Creating circular crop...")
            processor.crop_circle()
        
        # Step 4: Split into grid
        print(" Splitting frames...")
        chunks = processor.split_gif(rows, cols)
        
        # Step 5: Optimize and save chunks
        print(" Optimizing chunks...")
        chunks = processor.optimize_chunks(chunks, args.max_size)
        
        print(" Saving chunks...")
        processor.save_chunks(chunks, args.output)
        
        print("Done!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
