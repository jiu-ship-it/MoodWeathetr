# Local Resources

将图文/视频/音乐文件放在本目录，由后端统一转换为可访问 URL 并分发给前端。

## 1) 放置位置（当前项目推荐）
- `audio/`: 音乐或音频（mp3/wav）
- `images/`: 图文封面（jpg/png/webp）
- `videos/`: 本地视频（mp4）
- `music_list.json`: 音乐元数据
- `emotion_feeds.json`: 图文/视频元数据

## 2) 三类人群分发规则
系统按 `emotion_tag` 自动归类：
- `1`: 舒缓减压（低落预警人群）
- `2`: 稳定维持（平稳人群）
- `3`: 激活成长（积极高兴人群）

`emotion_feeds.json` 示例字段：
- `emotion_tag`, `type`, `title`, `desc`, `detail`, `cover`, `url`, `is_active`

`music_list.json` 示例字段：
- `emotion_tag`, `name`, `author`, `url`, `cover`, `duration`, `is_active`

## 3) 如何让所有用户可访问
- 当前方式：通过后端接口访问
  - `/api/local-resources/<path>`
  - `/api/resource-bundles`
- 这适合中小规模，部署简单。

若后续并发提升，建议将 `audio/images/videos` 迁移到对象存储（OSS/COS/S3）+ CDN：
- JSON 中 `url/cover` 直接填 CDN 链接
- 后端会原样返回，前端可直接访问

## 4) 路径规则
- 相对路径写法：
  - 音频：`audio/demo.mp3`
  - 图片：`images/demo.jpg`
  - 视频：`videos/demo.mp4`
- 绝对 URL（`http://` 或 `https://`）会直接透传。

## 5) 实用建议
- JSON 文件必须是 UTF-8 编码且为数组。
- 建议单图 <= 3MB，单音频 <= 20MB，视频尽量压缩。
- 文件缺失会导致该资源 404 或被过滤。
