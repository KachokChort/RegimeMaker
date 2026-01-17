import requests
import concurrent.futures
import time


def test_single_request(i):
    """Функция для одного запроса"""
    params = {
        "user": "Tima",
        "password": "bacuk22q",
        "selected_date": "2025-12-04",
        "duty_name": "Ronnie Coleman"
    }

    start = time.time()
    try:
        r = requests.post("http://127.0.0.1:8001/duty/", json=params, timeout=5)
        elapsed = (time.time() - start) * 1000

        if r.status_code == 200:
            return f"✓ {i}: {r.status_code} за {elapsed:.0f}ms"
        else:
            return f"✗ {i}: {r.status_code} за {elapsed:.0f}ms - {r.text[:50]}"

    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return f"💥 {i}: УПАЛ за {elapsed:.0f}ms - {str(e)[:50]}"


print("🚀 ТЕСТ ПАРАЛЛЕЛЬНЫХ ЗАПРОСОВ К /duty/")
print("=" * 60)

# Тест 1: 10 запросов одновременно
print("\n1. 10 запросов одновременно (имитация 10 быстрых кликов):")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(test_single_request, i) for i in range(10)]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())

time.sleep(1)  # Даем отдохнуть

# Тест 2: 5 потоков, но много запросов
print("\n2. 50 запросов через 5 потоков:")
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(test_single_request, i) for i in range(50)]

    completed = 0
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
        completed += 1

        # Прогресс-бар
        if completed % 10 == 0:
            print(f"   ... обработано {completed}/50")

print("\n" + "=" * 60)
print("🎯 ТЕСТ ЗАВЕРШЕН")