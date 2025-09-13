#!/usr/bin/env python3
"""
API测试脚本
用于测试注册和登录功能
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:5000"
HEADERS = {'Content-Type': 'application/json'}

def test_health():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_register(username, email, password):
    """测试用户注册"""
    print(f"=== 测试用户注册: {username} ===")
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/register", 
                           headers=HEADERS, 
                           data=json.dumps(data))
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()
    return response

def test_login(username, password):
    """测试用户登录"""
    print(f"=== 测试用户登录: {username} ===")
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/login", 
                           headers=HEADERS, 
                           data=json.dumps(data))
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()
    return response

def test_profile(token):
    """测试获取用户信息"""
    print("=== 测试获取用户信息 ===")
    headers = {**HEADERS, 'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

if __name__ == "__main__":
    print("开始测试WarmLabel后端API...")
    
    # 测试健康检查
    test_health()
    
    # 测试注册
    register_response = test_register("testuser", "test@example.com", "password123")
    
    if register_response.status_code == 201:
        # 测试登录
        login_response = test_login("testuser", "password123")
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            test_profile(token)
    
    print("测试完成！")