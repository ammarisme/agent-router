#!/usr/bin/env python3
"""Simple API test script."""

import asyncio
import httpx
import json

async def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("Testing API endpoints...")
        
        # Test health endpoint
        try:
            response = await client.get(f"{base_url}/health")
            print(f"Health check: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Health check failed: {e}")
        
        # Test agents endpoint
        try:
            response = await client.get(f"{base_url}/v1/agents?page=1&size=10")
            print(f"Agents endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  - Total agents: {data.get('total', 0)}")
                print(f"  - Page: {data.get('page', 0)}")
                print(f"  - Size: {data.get('size', 0)}")
                print(f"  - Pages: {data.get('pages', 0)}")
            else:
                print(f"  - Error: {response.text}")
        except Exception as e:
            print(f"Agents endpoint failed: {e}")
        
        # Test features endpoint
        try:
            response = await client.get(f"{base_url}/v1/features?page=1&size=10")
            print(f"Features endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  - Total features: {data.get('total', 0)}")
                print(f"  - Page: {data.get('page', 0)}")
                print(f"  - Size: {data.get('size', 0)}")
                print(f"  - Pages: {data.get('pages', 0)}")
            else:
                print(f"  - Error: {response.text}")
        except Exception as e:
            print(f"Features endpoint failed: {e}")
        
        # Test CORS preflight
        try:
            response = await client.options(f"{base_url}/v1/agents?page=1&size=10")
            print(f"CORS preflight: {response.status_code}")
            print(f"  - Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'Not set')}")
        except Exception as e:
            print(f"CORS preflight failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
