#!/usr/bin/env python3
"""
Direct test of USDA API to understand the data structure
"""

import requests
import json

def test_usda_direct():
    api_key = "bSMXb6Dq3W5l1ebpOKvpaBUNHocBCZkfdkTTw0n1"
    base_url = "https://api.nal.usda.gov/fdc/v1"

    print("🧪 Direct USDA API Test")
    print("=" * 30)

    # Test search
    search_url = f"{base_url}/foods/search"
    search_params = {
        'query': 'apple',
        'dataType': ['Foundation', 'SR Legacy'],
        'pageSize': 1,
        'api_key': api_key
    }

    try:
        print(f"🔍 Searching for 'apple'...")
        response = requests.get(search_url, params=search_params, timeout=15)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            search_data = response.json()
            print(f"📊 Found {len(search_data.get('foods', []))} results")

            if search_data.get('foods'):
                food = search_data['foods'][0]
                food_id = food['fdcId']
                print(f"🆔 Food ID: {food_id}")
                print(f"📝 Description: {food.get('description', 'N/A')}")

                # Get detailed info
                print(f"\n🔍 Getting detailed nutrition for ID {food_id}...")
                detail_url = f"{base_url}/food/{food_id}"
                detail_params = {'api_key': api_key}

                detail_response = requests.get(detail_url, params=detail_params, timeout=15)
                print(f"Status: {detail_response.status_code}")

                if detail_response.status_code == 200:
                    food_data = detail_response.json()

                    print(f"\n📋 Food Data Keys: {list(food_data.keys())}")

                    nutrients = food_data.get('foodNutrients', [])
                    print(f"🧪 Found {len(nutrients)} nutrients")

                    # Show first few nutrients
                    print(f"\n🔬 Sample Nutrients:")
                    for i, nutrient in enumerate(nutrients[:5]):
                        print(f"  {i+1}. {nutrient}")

                    # Extract key nutrients
                    key_nutrients = {}
                    for nutrient in nutrients:
                        try:
                            name = nutrient.get('nutrient', {}).get('name', '')
                            amount = nutrient.get('amount')
                            unit = nutrient.get('nutrient', {}).get('unitName', '')

                            if name in ['Energy', 'Protein', 'Carbohydrate, by difference', 'Total lipid (fat)']:
                                key_nutrients[name] = f"{amount} {unit}"
                        except:
                            continue

                    print(f"\n🎯 Key Nutrition (per 100g):")
                    for name, value in key_nutrients.items():
                        print(f"  {name}: {value}")

                else:
                    print(f"❌ Detail request failed: {detail_response.text}")
            else:
                print("❌ No foods found in search")
        else:
            print(f"❌ Search failed: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_usda_direct()