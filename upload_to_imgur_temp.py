#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📤 구조화된 카드 이미지를 Imgur에 임시 업로드
"""

import os
import base64
import requests
from PIL import Image
import io

def upload_to_imgur():
    """Imgur에 이미지 업로드"""
    
    # Imgur Client ID (공개용)
    CLIENT_ID = 'dd32dd3c6aaa9a0'
    
    output_dir = 'structured_cards_output'
    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])
    
    if not files:
        print("❌ 업로드할 이미지가 없습니다.")
        return
        
    print(f"📤 {len(files)}개 이미지를 Imgur에 업로드 중...")
    print("=" * 60)
    
    uploaded_images = []
    
    for file in files[:5]:  # 최대 5개만 업로드
        filepath = os.path.join(output_dir, file)
        
        try:
            # 이미지 파일 읽기
            with open(filepath, 'rb') as f:
                img_data = f.read()
            
            # Base64 인코딩
            b64_image = base64.b64encode(img_data).decode()
            
            # Imgur API 호출
            headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
            data = {
                'image': b64_image,
                'type': 'base64',
                'title': file.replace('.png', ''),
                'description': '전력산업 위클리 카드뉴스'
            }
            
            print(f"\n📤 업로드 중: {file}")
            response = requests.post(
                'https://api.imgur.com/3/image',
                headers=headers,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    img_link = result['data']['link']
                    uploaded_images.append({
                        'file': file,
                        'link': img_link,
                        'delete_hash': result['data']['deletehash']
                    })
                    print(f"✅ 성공: {img_link}")
                else:
                    print(f"❌ 실패: {result.get('data', {}).get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 업로드 실패 ({file}): {str(e)}")
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("📊 업로드 결과")
    print("=" * 60)
    
    if uploaded_images:
        print(f"\n✅ 성공적으로 업로드된 이미지: {len(uploaded_images)}개\n")
        
        for img in uploaded_images:
            card_type = img['file'].split('_')[-1].replace('.png', '')
            print(f"\n🖼️ {card_type.upper()} 카드:")
            print(f"   📎 링크: {img['link']}")
            print(f"   🗑️ 삭제 해시: {img['delete_hash']}")
        
        print("\n💡 이미지 보기:")
        print("위 링크를 클릭하거나 브라우저에 복사해서 보세요!")
        
        print("\n⚠️ 주의사항:")
        print("- 이 링크는 임시 링크입니다")
        print("- 일정 시간 후 자동 삭제될 수 있습니다")
        
    else:
        print("❌ 업로드된 이미지가 없습니다.")
        
    return uploaded_images

if __name__ == "__main__":
    upload_to_imgur()
