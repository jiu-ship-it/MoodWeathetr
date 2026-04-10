# Local Resources (Method B)

Put local audio/image files in this folder, then access through backend API.

## Directory
- `audio/`: music files (mp3/wav)
- `images/`: cover images (jpg/png)
- `music_list.json`: music metadata
- `emotion_feeds.json`: emotion feed metadata

## URL mapping
If JSON uses relative path like `audio/calm_demo.mp3`, backend returns:
`http://127.0.0.1:5000/api/local-resources/audio/calm_demo.mp3`

## Notes
- Keep UTF-8 encoding for JSON files.
- When file is missing, API item may be filtered out or resource request returns 404.
- In WeChat DevTools local debug, enable "Do not verify valid domain".

## Import Requirements
- `music_list.json` and `emotion_feeds.json` must be valid JSON arrays.
- Recommended file size:
	- single image <= 3 MB (jpg/png/webp)
	- single audio <= 20 MB (mp3/wav)
- Relative resource path rules:
	- audio under `audio/`, e.g. `audio/calm_demo.mp3`
	- image under `images/`, e.g. `images/calm_demo.jpg`
- If URL starts with `http://` or `https://`, backend returns it directly.
- Emotion tag values should use `1`, `2`, `3` (mapping: 1=失落预警, 2=平稳, 3=高兴).
- Suggested required fields:
	- `music_list.json`: `emotion_tag`, `name`, `author`, `url`, `is_active`
	- `emotion_feeds.json`: `emotion_tag`, `type`, `title`, `desc`, `is_active`
