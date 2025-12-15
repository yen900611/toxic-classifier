import requests
import time
import statistics
import os

# 設定 API URL 和 Key
# 如果你的 Docker 是跑在 8000 port
API_URL = "http://localhost:8000/predict"
API_KEY = "frontend-dev-key"  # 使用我們設定的預設 Key

# 測試用的假資料
TEST_PAYLOAD = {"text": "This is a test comment to benchmark the API latency."}
HEADERS = {"X-API-Key": API_KEY}


def run_benchmark(num_requests=100):
    print(f"🚀 開始執行 Benchmark (壓力測試)... 目標: {num_requests} 次請求")
    print(f"🎯 Target URL: {API_URL}")

    latencies = []
    errors = 0

    # 1. 暖機 (Warm-up)
    # 第一個請求通常比較慢（因為要建立連線或載入 Lazy Load 的資源），我們不計入統計
    try:
        requests.post(API_URL, json=TEST_PAYLOAD, headers=HEADERS)
        print("🔥 暖機完成 (Warm-up request sent)")
    except Exception as e:
        print(f"❌ 無法連線到 API: {e}")
        print("請確認 Docker 是否正在執行 (docker-compose up)")
        return

    # 2. 開始正式測試
    start_total_time = time.time()

    for i in range(num_requests):
        try:
            req_start = time.time()
            response = requests.post(API_URL, json=TEST_PAYLOAD, headers=HEADERS)
            req_end = time.time()

            # 計算耗時 (毫秒)
            latency_ms = (req_end - req_start) * 1000

            if response.status_code == 200:
                latencies.append(latency_ms)
                # print(f"請求 {i+1}: {latency_ms:.2f} ms") # 如果不想看太多刷屏可以註解掉
            else:
                print(f"請求 {i + 1} 失敗: Status {response.status_code}")
                errors += 1

        except Exception as e:
            print(f"請求錯誤: {e}")
            errors += 1

    total_time = time.time() - start_total_time

    # 3. 統計結果
    if latencies:
        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th Percentile
        p99_latency = statistics.quantiles(latencies, n=100)[98]  # 99th Percentile
        min_latency = min(latencies)
        max_latency = max(latencies)

        print("\n" + "=" * 40)
        print("📊 Benchmark 測試結果報告")
        print("=" * 40)
        print(f"✅ 成功請求數: {len(latencies)} / {num_requests}")
        print(f"❌ 失敗請求數: {errors}")
        print(f"⏱️ 總執行時間: {total_time:.2f} 秒")
        print("-" * 20)
        print(f"⚡ 平均延遲 (Average Latency): {avg_latency:.2f} ms")
        print(f"⚡ P95 延遲 (95% 的請求快於):  {p95_latency:.2f} ms")
        print(f"⚡ 最快回應: {min_latency:.2f} ms")
        print(f"⚡ 最慢回應: {max_latency:.2f} ms")
        print("=" * 40)

        print("\n📝 【你可以直接貼到履歷上的句子】：")
        print(
            f'> "Engineered a high-performance REST API handling inference requests with an average latency of {avg_latency:.0f}ms (P95 < {p95_latency:.0f}ms), utilizing FastAPI asynchronous workers."')
    else:
        print("沒有收集到成功的數據。")


if __name__ == "__main__":
    run_benchmark()