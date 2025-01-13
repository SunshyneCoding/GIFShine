# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import os
from typing import Tuple, List
class GifProcessor:
    def __init__(self, input_path: str):
        self.gif = Image.open(input_path)
        self.frames = []
        self.durations = []
        self.load_frames()

    def load_frames(self):
        try:
            while True:
                frame = self.gif.copy()
                self.frames.append(frame)
                self.durations.append(self.gif.info.get('duration', 100))
                self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            pass

    def resize(self, width: int, height: int):
        self.frames = [frame.resize((width, height), Image.Resampling.LANCZOS) 
                      for frame in self.frames]

    def crop_to_rect(self, x: int, y: int, width: int, height: int):
        """Crop all frames to the specified rectangle"""
        self.frames = [frame.crop((x, y, x + width, y + height))
                      for frame in self.frames]

    def create_circular_mask(self, size: Tuple[int, int]) -> Image.Image:
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0]-1, size[1]-1), fill=255)
        return mask

    def crop_circle(self):
        mask = self.create_circular_mask(self.frames[0].size)
        self.frames = [Image.composite(frame, 
                                     Image.new('RGBA', frame.size, (0, 0, 0, 0)),
                                     mask) 
                      for frame in self.frames]

    def split_gif(self, rows: int, cols: int) -> List[List[List[Image.Image]]]:
        width, height = self.frames[0].size
        chunk_width = width // cols
        chunk_height = height // rows
        
        chunks = []
        for y in range(rows):
            row_chunks = []
            for x in range(cols):
                left = x * chunk_width
                top = y * chunk_height
                chunk_frames = []
                for frame in self.frames:
                    chunk = frame.crop((left, top, left + chunk_width, top + chunk_height))
                    chunk_frames.append(chunk)
                row_chunks.append(chunk_frames)
            chunks.append(row_chunks)
        return chunks

    def optimize_chunks(self, chunks: List[List[List[Image.Image]]], max_size: int) -> List[List[List[Image.Image]]]:
        # Find the optimal quality setting that works for all chunks
        min_quality = 1
        max_quality = 100
        optimal_quality = None

        while min_quality <= max_quality:
            mid_quality = (min_quality + max_quality) // 2
            max_chunk_size = 0

            # Test compression with current quality
            for row in chunks:
                for chunk_frames in row:
                    test_bytes = self._get_compressed_size(chunk_frames, mid_quality)
                    max_chunk_size = max(max_chunk_size, test_bytes)

            if max_chunk_size > max_size * 1024:  # Convert max_size to bytes
                min_quality = mid_quality + 1
            else:
                optimal_quality = mid_quality
                max_quality = mid_quality - 1

        if optimal_quality is None:
            raise ValueError("Cannot compress chunks to desired size while maintaining quality")

        self.optimal_quality = optimal_quality
        return chunks

    def _get_compressed_size(self, frames: List[Image.Image], quality: int) -> int:
        """Helper method to get compressed size of an animated GIF"""
        import io
        buffer = io.BytesIO()
        frames[0].save(
            buffer,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            quality=quality,
            duration=self.durations,
            loop=0
        )
        return buffer.tell()

    def save_chunks(self, chunks: List[List[List[Image.Image]]], output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        
        for row_idx, row in enumerate(chunks):
            for col_idx, chunk_frames in enumerate(row):
                output_path = os.path.join(
                    output_dir, 
                    f'chunk_{row_idx}_{col_idx}.gif'
                )
                chunk_frames[0].save(
                    output_path,
                    format="GIF",
                    save_all=True,
                    append_images=chunk_frames[1:],
                    optimize=True,
                    quality=getattr(self, 'optimal_quality', 85),
                    duration=self.durations,
                    loop=0
                )
