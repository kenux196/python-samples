from pydub import AudioSegment
import os

def convert_mp4_to_mp3(mp4_path, mp3_path=None):
    """Convert MP4 file to MP3"""
    try:
        # If mp3_path is not specified, create it from mp4_path
        if mp3_path is None:
            mp3_path = os.path.splitext(mp4_path)[0] + '.mp3'
        
        # Load the video file and extract audio
        audio = AudioSegment.from_file(mp4_path, format="mp4")
        
        # Export as MP3
        audio.export(mp3_path, format="mp3")
        
        print(f"Successfully converted {mp4_path} to {mp3_path}")
        
    except Exception as e:
        print(f"Error converting file: {str(e)}")

if __name__ == "__main__":
    # Example usage
    mp4_file = input("Enter the path to your MP4 file: ")
    convert_mp4_to_mp3(mp4_file)