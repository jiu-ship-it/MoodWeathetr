import json
import os
from urllib.parse import quote


RESOURCE_GROUP_META = {
    '1': {
        'key': 'relief',
        'name': '舒缓减压',
        'audience': '低落预警人群',
        'description': '优先推送安抚型图文、呼吸放松与情绪承接内容。'
    },
    '2': {
        'key': 'balance',
        'name': '稳定维持',
        'audience': '平稳人群',
        'description': '优先推送习惯维护、轻复盘与节奏管理内容。'
    },
    '3': {
        'key': 'thrive',
        'name': '激活成长',
        'audience': '积极高兴人群',
        'description': '优先推送目标推进、行动放大与成长型内容。'
    }
}


def init_resource_paths(app):
    root = os.path.join(app.root_path, 'local_resources')
    app.config['LOCAL_RESOURCE_ROOT'] = root
    app.config['LOCAL_EMOTION_FEED_FILE'] = os.path.join(root, 'emotion_feeds.json')
    app.config['LOCAL_MUSIC_FILE'] = os.path.join(root, 'music_list.json')
    os.makedirs(root, exist_ok=True)
    os.makedirs(os.path.join(root, 'audio'), exist_ok=True)
    os.makedirs(os.path.join(root, 'images'), exist_ok=True)


def normalize_emotion_tag(raw_value):
    text = str(raw_value or '').strip().lower()
    map_table = {
        '1': '1',
        '2': '2',
        '3': '3',
        '低落预警': '1',
        '低落': '1',
        'sad': '1',
        '平稳': '2',
        'stable': '2',
        '高兴': '3',
        '开心': '3',
        'happy': '3'
    }
    return map_table.get(text, '')


def resource_group_info(tag):
    return RESOURCE_GROUP_META.get(tag or '', {
        'key': 'general',
        'name': '通用资源',
        'audience': '全部人群',
        'description': '适用于全部用户的通用内容。'
    })


def load_json_array(file_path, default_items):
    if not os.path.exists(file_path):
        return default_items
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            payload = json.load(f)
        if isinstance(payload, list):
            return payload
    except (OSError, json.JSONDecodeError):
        pass
    return default_items


def local_resource_url(path_value, host_url):
    if not path_value:
        return None
    text = str(path_value).strip()
    if not text:
        return None
    if text.startswith('http://') or text.startswith('https://'):
        return text
    normalized = text.lstrip('/').replace('\\', '/')
    encoded = '/'.join(quote(part) for part in normalized.split('/'))
    return f"{host_url.rstrip('/')}/api/local-resources/{encoded}"


def load_emotion_feed_rows(target_tag, feed_file, host_url):
    default_items = [
        {
            'emotion_tag': '1',
            'type': 'imageText',
            'title': '低落期自我支持清单',
            'desc': '先稳住，再行动，先从最小步开始。',
            'detail': '先做一件5分钟内可完成的小事，再决定下一步。',
            'is_active': True
        },
        {
            'emotion_tag': '2',
            'type': 'imageText',
            'title': '稳定情绪维护法',
            'desc': '固定作息和轻量复盘，保持心态稳定。',
            'detail': '每天固定10分钟复盘，记录最稳的一刻。',
            'is_active': True
        },
        {
            'emotion_tag': '3',
            'type': 'video',
            'title': '积极状态放大术',
            'desc': '趁状态好，把可执行目标拆小并推进。',
            'url': 'https://www.bilibili.com/video/BV1V4411Z7VA',
            'is_active': True
        }
    ]
    source = load_json_array(feed_file, default_items)
    image_text = []
    videos = []

    for item in source:
        if not isinstance(item, dict):
            continue
        if item.get('is_active', True) is False:
            continue

        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if target_tag and tag and tag != target_tag:
            continue

        row = {
            'title': item.get('title') or '未命名内容',
            'desc': item.get('desc') or '',
            'detail': item.get('detail') or item.get('desc') or '',
            'emotion_tag': tag
        }
        group_info = resource_group_info(tag)
        row['group_key'] = group_info['key']
        row['group_name'] = group_info['name']

        item_type = str(item.get('type') or 'imageText').strip()
        if item_type == 'video':
            row['url'] = local_resource_url(item.get('url'), host_url)
            row['cover'] = local_resource_url(item.get('cover'), host_url)
            if row['url']:
                videos.append(row)
        else:
            row['cover'] = local_resource_url(item.get('cover'), host_url)
            image_text.append(row)

    return image_text, videos


def load_music_rows(target_tag, music_file, host_url):
    default_items = [
        {
            'emotion_tag': '2',
            'name': 'Calm Demo',
            'author': 'WarmLabel',
            'url': 'audio/calm_demo.mp3',
            'is_active': True
        }
    ]
    source = load_json_array(music_file, default_items)
    music_items = []

    for item in source:
        if not isinstance(item, dict):
            continue
        if item.get('is_active', True) is False:
            continue

        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if target_tag and tag and tag != target_tag:
            continue

        group_info = resource_group_info(tag)
        row = {
            'name': item.get('name') or '未命名音乐',
            'author': item.get('author') or '未知创作者',
            'url': local_resource_url(item.get('url'), host_url),
            'cover': local_resource_url(item.get('cover'), host_url),
            'duration': item.get('duration'),
            'emotion_tag': tag,
            'group_key': group_info['key'],
            'group_name': group_info['name']
        }
        if row['url']:
            music_items.append(row)

    return music_items


def build_resource_bundles(target_tag, feed_file, music_file, host_url):
    image_text, videos = load_emotion_feed_rows('', feed_file, host_url)
    musics = load_music_rows('', music_file, host_url)

    groups = {}
    for tag in ('1', '2', '3'):
        meta = resource_group_info(tag)
        groups[tag] = {
            'emotion_tag': tag,
            'group_key': meta['key'],
            'group_name': meta['name'],
            'audience': meta['audience'],
            'description': meta['description'],
            'imageText': [],
            'videos': [],
            'music': []
        }

    for item in image_text:
        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if tag in groups:
            groups[tag]['imageText'].append(item)

    for item in videos:
        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if tag in groups:
            groups[tag]['videos'].append(item)

    for item in musics:
        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if tag in groups:
            groups[tag]['music'].append(item)

    recommended_tag = target_tag if target_tag in groups else ''
    if not recommended_tag:
        max_tag = ''
        max_total = -1
        for tag, block in groups.items():
            total = len(block['imageText']) + len(block['videos']) + len(block['music'])
            if total > max_total:
                max_total = total
                max_tag = tag
        recommended_tag = max_tag

    return {
        'recommended_emotion_tag': recommended_tag,
        'recommended_group': groups.get(recommended_tag),
        'groups': groups
    }
