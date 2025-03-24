from moviepy.editor import VideoFileClip
import os

def convert_mp4_to_mp3(mp4_path, mp3_path=None):
  """Convert MP4 file to MP3"""
  try:
    # If mp3_path is not specified, create it from mp4_path
    if mp3_path is None:
      mp3_path = os.path.splitext(mp4_path)[0] + '.mp3'
    
    # Load the video file
    video = VideoFileClip(mp4_path)
    
    # Extract the audio
    audio = video.audio
    
    # Write the audio file
    audio.write_audiofile(mp3_path)
    
    # Close the files
    audio.close()
    video.close()
    
    print(f"Successfully converted {mp4_path} to {mp3_path}")
    
  except Exception as e:
    print(f"Error converting file: {str(e)}")

if __name__ == "__main__":
  # Example usage
  mp4_file = input("Enter the path to your MP4 file: ")
  convert_mp4_to_mp3(mp4_file)