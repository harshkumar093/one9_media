import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# from generate_timestamp import generate_timestamps_from_audio
# from format_word_to_lines import format_words_into_lines_from_script

video_path = "video_0.mp4"
output_path = "output_video_with_styled_captions_pillow.mp4"

caption_data = [
    {
        "text": "In the bustling streets of Montrose Emily—a spirited travel photographer—was rushing to catch a train.",
        "start": None,
        "end": None,
        "style": {
            "position": "center",
            "font_size": 65,
            "text_color": "yellow",
            "stroke_color": "black",
            "stroke_width": 2,
            "shadow_enabled": True,
            "shadow_offset": (4, 4),
            "shadow_color": (50, 50, 50),
            "font_family": "arial.ttf" # Or a specific font file path like "C:/Windows/Fonts/Arial.ttf"
        }
    },
    {
        "text": "Her camera bag dangled precariously as she weaved through the crowd.",
        "start": None,
        "end": None,
        "style": {
            "position": "center",
            "font_size": 80,
            "text_color": "cyan",
            "stroke_color": "magenta",
            "stroke_width": 3,
            "shadow_enabled": False, # No shadow for this line
            "font_family": "arial.ttf"
        }
    },
    {
        "text": "Suddenly she collided with someone and her camera tumbled out of her hands.",
        "start": None,
        "end": None,
        "style": {
            "position": "center",
            "font_size": 55,
            "text_color": "white",
            "stroke_color": "blue",
            "stroke_width": 1,
            "shadow_enabled": True,
            "shadow_offset": (2, 2),
            "shadow_color": (0, 0, 0),
            "font_family": "arial.ttf"
        }
    },
    {
        "text": "A stranger caught the camera just in time.",
        "start": None,
        "end": None,
        "style": {
            "position": "center",
            "font_size": 55,
            "text_color": "lime",
            "stroke_color": "darkgreen",
            "stroke_width": 1.5,
            "shadow_enabled": True,
            "shadow_offset": (3, 3),
            "shadow_color": (0, 0, 0),
            "font_family": "arial.ttf"
        }
    },{
        "text": "He was tall with a rugged charm and a backpack slung over one shoulder.",
        "start": None,
        "end": None,
        "style": {
            "position": "center",
            "font_size": 80,
            "text_color": "cyan",
            "stroke_color": "magenta",
            "stroke_width": 3,
            "shadow_enabled": False, # No shadow for this line
            "font_family": "arial.ttf"
        }
    },
    {
        "text": "They locked eyes for a brief moment before Emily hurried aboard the train thinking she'd never see him again.",
        "start": None,
        "end": None,
        "style": {
            "position": "center",
            "font_size": 55,
            "text_color": "white",
            "stroke_color": "blue",
            "stroke_width": 1,
            "shadow_enabled": True,
            "shadow_offset": (2, 2),
            "shadow_color": (0, 0, 0),
            "font_family": "arial.ttf"
        }
    },
    {
        "text": "Little did she know fate had other plans.",
        "start": None,
        "end": None,
        "style": {
            "position": "center",
            "font_size": 55,
            "text_color": "lime",
            "stroke_color": "darkgreen",
            "stroke_width": 1.5,
            "shadow_enabled": True,
            "shadow_offset": (3, 3),
            "shadow_color": (0, 0, 0),
            "font_family": "arial.ttf"
        }
    }
]

whisper_model_size = "base"
device_to_use = "cpu"
compute_type = "int8"


def get_position_coordinates(position_key, video_width, video_height, text_width, text_height):
    print(f"Calculating position for '{position_key}' with video size {video_width}x{video_height} and text size {text_width}x{text_height}")
    padding = 30
    if position_key == "top-left":
        x = padding
        y = padding
    elif position_key == "top-right":
        x = video_width - text_width - padding
        y = padding
    elif position_key == "bottom-left":
        x = padding
        y = video_height - text_height - padding
    elif position_key == "bottom-right":
        x = video_width - text_width - padding
        y = video_height - text_height - padding
    elif position_key == "center":
        x = (video_width - text_width) / 2
        y = (video_height - text_height) / 2
    elif position_key == "bottom-center":
        x = (video_width - text_width) / 2
        y = video_height - text_height - padding
    elif position_key == "top-center":
        x = (video_width - text_width) / 2
        y = padding
    else:
        x = (video_width - text_width) / 2
        y = video_height - text_height - padding
    return (x, y)


def create_styled_text_image_clip(text, duration, start_time, video_width, video_height, style_settings):
    print(f"Creating styled text image clip for: '{text}'")
    style_settings.setdefault("position", "center")
    style_settings.setdefault("font_size", 50)
    style_settings.setdefault("text_color", "white")
    style_settings.setdefault("stroke_color", "black")
    style_settings.setdefault("stroke_width", 2)
    style_settings.setdefault("shadow_enabled", True)
    style_settings.setdefault("shadow_offset", (3, 3))
    style_settings.setdefault("shadow_color", (0, 0, 0))
    style_settings.setdefault("font_family", "arial.ttf")

    font_path = None
    try:
        font_path = ImageFont.truetype(style_settings["font_family"], style_settings["font_size"])
    except IOError:
        try:
            font_path = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", style_settings["font_size"])
        except IOError:
            font_path = ImageFont.load_default()
            # style_settings["font_size"] = 16
    if font_path is None:
        print("Error: No font could be loaded. Returning an empty clip.")
        return ImageClip(np.zeros((video_height, video_width, 3)), duration=duration).set_start(start_time).set_position((0,0))

    temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    
    max_text_width = video_width * 0.9
    
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = temp_draw.textbbox((0, 0), test_line, font=font_path)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_text_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    bbox = temp_draw.textbbox((0, 0), "\n".join(lines), font=font_path)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    margin = int(max(style_settings["stroke_width"] * 2, max(style_settings["shadow_offset"]))) + 20
    image_w = int(text_w + margin * 2)
    image_h = int(text_h + margin * 2)
    img = Image.new('RGBA', (image_w, image_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    text_x_base = (image_w - text_w) / 2
    text_y_start = (image_h - text_h) / 2

    if style_settings["shadow_enabled"]:
        y_offset = 0
        for line in lines:
            line_width = temp_draw.textbbox((0,0), line, font=font_path)[2]
            line_x_pos = text_x_base + (text_w - line_width) / 2 + style_settings["shadow_offset"][0]
            line_y_pos = text_y_start + y_offset + style_settings["shadow_offset"][1]
            draw.text(
                (line_x_pos, line_y_pos),
                line,
                fill=style_settings["shadow_color"],
                font=font_path
            )
            y_offset += font_path.getbbox(line)[3]

    y_offset = 0
    for line in lines:
        line_width = temp_draw.textbbox((0,0), line, font=font_path)[2]
        line_x_pos = text_x_base + (text_w - line_width) / 2
        line_y_pos = text_y_start + y_offset
        draw.text(
            (line_x_pos, line_y_pos),
            line,
            fill=style_settings["text_color"],
            font=font_path,
            stroke_width=int(style_settings["stroke_width"]),
            stroke_fill=style_settings["stroke_color"]
        )
        y_offset += font_path.getbbox(line)[3]
        
    img_array_rgba = np.array(img)
    image_clip = ImageClip(img_array_rgba)
    image_clip = image_clip.set_duration(duration).set_start(start_time)
    final_pos = get_position_coordinates(style_settings["position"], video_width, video_height, image_w, image_h)
    print(f"Created clip for '{text[:20]}...' (Size: {image_w}x{image_h}, Duration: {duration:.2f}s, Start: {start_time:.2f}s)") 
    return image_clip.set_position(final_pos)


def add_captions_to_video(video_path, output_path, caption_list):
    print("Adding styled captions to the video...")
    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Error loading video: {e}")
        print("Please ensure the video path is correct and FFmpeg is properly configured.")
        return

    video_width, video_height = video.size
    print(f"Video dimensions: {video_width}x{video_height}")

    text_clips = []
    for caption_line in caption_list:
        text_content = caption_line.get('text', '').strip()
        start_time = caption_line.get('start')
        end_time = caption_line.get('end')
        style_settings = caption_line.get('style', {})
        if not text_content or start_time is None or end_time is None:
            print(f"Warning: Skipping invalid caption entry: {caption_line}")
            continue
        duration = end_time - start_time
        if duration <= 0:
            print(f"Warning: Skipping text '{text_content}' due to non-positive duration.")
            continue

        txt_clip = create_styled_text_image_clip(
            text_content,
            duration,
            start_time,
            video_width,
            video_height,
            style_settings
        )
        text_clips.append(txt_clip)

    final_video = CompositeVideoClip([video] + text_clips)
    
    print(f"Writing final video to {output_path}...")
    final_video.write_videofile(output_path, fps=video.fps, codec="libx264", audio_codec="aac")
    print("Video generation complete!")   
    video.close()

# if __name__ == "__main__":
#     auto_generate_timestamps = any(item.get('start') is None for item in caption_data)
#     if auto_generate_timestamps:
#         print("Timestamps are missing in the input list. Generating them automatically...")
#         script_as_strings = [item["text"] for item in caption_data]
#         word_timestamps = generate_timestamps_from_audio(video_path, whisper_model_size, device_to_use, compute_type)
#         print(word_timestamps)
#         if not word_timestamps:
#             print("Failed to generate timestamps. Exiting.")
#             exit()
#         caption_lines_with_times = format_words_into_lines_from_script(word_timestamps, script_as_strings, textCase='upper')
#         if not caption_lines_with_times:
#             print("Failed to format captions from the script. Exiting.")
#             exit()
#         final_caption_list = []
#         for i, line in enumerate(caption_lines_with_times):
#             style_to_use = caption_data[i]["style"] if i < len(caption_data) else {}
#             final_caption_list.append({
#                 "text": line['text'],
#                 "start": line['start'],
#                 "end": line['end'],
#                 "style": style_to_use
#             })
#     else:
#         print("Timestamps are provided in the input list. Using them directly.")
#         final_caption_list = caption_data
#     add_captions_to_video(video_path, output_path, final_caption_list)