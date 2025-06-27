#!/usr/bin/env python3
"""
HealthQuest API 테스트 스크립트
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🎮 HealthQuest API 테스트 시작\n")
    
    # 1. 회원가입 테스트
    print("1. 회원가입 테스트...")
    register_data = {
        "email": f"user{int(time.time())}@example.com",
        "username": f"user{int(time.time())}",
        "nickname": "API테스터",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "gender": "female",
        "height": 165,
        "weight": 55,
        "activity_level": "active"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    if response.status_code == 201:
        print("✅ 회원가입 성공!")
        data = response.json()
        access_token = data['tokens']['access']
        user_id = data['user']['id']
        print(f"   사용자 ID: {user_id}, 닉네임: {data['user']['nickname']}")
    else:
        print(f"❌ 회원가입 실패: {response.text}")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 2. 사용자 정보 조회
    print("\n2. 사용자 정보 조회...")
    response = requests.get(f"{BASE_URL}/auth/me/", headers=headers)
    if response.status_code == 200:
        print("✅ 사용자 정보 조회 성공!")
        user_data = response.json()
        print(f"   닉네임: {user_data['nickname']}, 활동 수준: {user_data['activity_level']}")
    else:
        print(f"❌ 사용자 정보 조회 실패: {response.text}")
    
    # 3. 캐릭터 정보 조회
    print("\n3. 캐릭터 정보 조회...")
    response = requests.get(f"{BASE_URL}/characters/", headers=headers)
    if response.status_code == 200:
        print("✅ 캐릭터 정보 조회 성공!")
        character = response.json()
        print(f"   캐릭터: {character['name']}, 레벨: {character['level']}")
        print(f"   총 스탯: {character['total_stats']}, 건강 점수: {character['health_score']}")
    else:
        print(f"❌ 캐릭터 정보 조회 실패: {response.text}")
    
    # 4. 캐릭터 스탯 조회
    print("\n4. 캐릭터 스탯 조회...")
    response = requests.get(f"{BASE_URL}/characters/stats/", headers=headers)
    if response.status_code == 200:
        print("✅ 캐릭터 스탯 조회 성공!")
        stats = response.json()
        print(f"   체력: {stats['stamina']}, 근력: {stats['strength']}, 정신력: {stats['mental']}")
        print(f"   지구력: {stats['endurance']}, 심폐: {stats['cardio']}, 유연성: {stats['flexibility']}")
        print(f"   영양: {stats['nutrition']}, 회복: {stats['recovery']}")
    else:
        print(f"❌ 캐릭터 스탯 조회 실패: {response.text}")
    
    # 5. 퀘스트 목록 조회
    print("\n5. 퀘스트 목록 조회...")
    response = requests.get(f"{BASE_URL}/quests/", headers=headers)
    if response.status_code == 200:
        print("✅ 퀘스트 목록 조회 성공!")
        quests = response.json()
        print(f"   할당된 퀘스트 수: {quests['count']}")
    else:
        print(f"❌ 퀘스트 목록 조회 실패: {response.text}")
    
    # 6. 연속 완료 기록 조회
    print("\n6. 연속 완료 기록 조회...")
    response = requests.get(f"{BASE_URL}/quests/streak/", headers=headers)
    if response.status_code == 200:
        print("✅ 연속 완료 기록 조회 성공!")
        streak = response.json()
        print(f"   현재 연속: {streak['current_streak']}일, 최고 기록: {streak['longest_streak']}일")
    else:
        print(f"❌ 연속 완료 기록 조회 실패: {response.text}")
    
    # 7. 길드 목록 조회
    print("\n7. 길드 목록 조회...")
    response = requests.get(f"{BASE_URL}/guilds/", headers=headers)
    if response.status_code == 200:
        print("✅ 길드 목록 조회 성공!")
        guilds = response.json()
        print(f"   공개 길드 수: {len(guilds)}")
    else:
        print(f"❌ 길드 목록 조회 실패: {response.text}")
    
    # 8. 내 길드 조회 (없을 것임)
    print("\n8. 내 길드 조회...")
    response = requests.get(f"{BASE_URL}/guilds/my/", headers=headers)
    if response.status_code == 404:
        print("✅ 내 길드 조회 성공! (길드 미소속 상태)")
    else:
        print(f"❌ 예상과 다른 응답: {response.status_code} {response.text}")
    
    print("\n🎉 모든 API 테스트 완료!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. Docker 컨테이너가 실행 중인지 확인하세요.")
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")