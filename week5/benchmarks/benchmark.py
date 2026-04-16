import requests
import time

API_BASE = "http://127.0.0.1:8001/books"
ITERATIONS = 20
OFFSET = 95000

def print_data_sample(data_list):
    if not data_list:
        return
    if len(data_list) <= 5:
        for item in data_list:
            print("  ", item)
    else:
        for item in data_list[:3]:
            print("  ", item)
        print("   ...")
        for item in data_list[-2:]:
            print("  ", item)

def test_endpoint(name, url):
    total_time = 0
    server_time = 0
    print(f"Calling: {name} (Run {ITERATIONS} times)...")
    last_data = None
    for _ in range(ITERATIONS):
        start = time.time()
        res = requests.get(url)
        latency = time.time() - start
        
        data = res.json()
        total_time += latency
        server_time += data.get("db_query_time_ms", 0)
        last_data = data
        
    avg_latency = (total_time / ITERATIONS) * 1000  # ms
    avg_server = (server_time / ITERATIONS)  # Already in ms from server response
    
    print(f"\n=> Retrieved data sample ({name}):")
    print_data_sample(last_data.get("data", []))
    print(f"=> Average DB time: {avg_server:.3f} ms")
    
    return avg_server, avg_latency

def main():
    print(f"{'='*65}")
    print(f" PAGINATION BENCHMARK REPORT (Offset/Cursor checkpoint = {OFFSET})")
    print(f"{'='*65}")
    
    # 1. No pagination (single run because this puts heavy load on DB/cache)
    print("\n[Strategy 1] No pagination")
    print("Test: retrieving all 100,000 rows...")
    start_time = time.time()
    res = requests.get(f"{API_BASE}/no-page?limit=100000")
    no_page_latency = (time.time() - start_time) * 1000
    data = res.json()
    no_page_server = data.get("db_query_time_ms", 0)
    print(f"\n=> Retrieved data sample (No pagination):")
    print_data_sample(data.get("data", []))
    print(f"=> Number of fetched rows: {data.get('count_fetched')}")
    print(f"=> DB time: {no_page_server:.3f} ms")
    print(f"=> HTTP Latency: {no_page_latency:.3f} ms")
    input("\nPress Enter to continue...")
    
    # 2. Offset Pagination
    print("\n[Strategy 2] Offset Pagination")
    os, _l_os = test_endpoint("Offset Pagination", f"{API_BASE}/offset?offset={OFFSET}&limit=20")
    input("\nPress Enter to continue...")
    
    # 3. Cursor Pagination
    print("\n[Strategy 3] Cursor Pagination")
    cs, _l_cs = test_endpoint("Cursor Pagination", f"{API_BASE}/cursor?cursor_id={OFFSET}&limit=20")
    input("\nPress Enter to show the result table...")
    
    # Print Markdown table
    print("\n[+] SPEED COMPARISON TABLE:")
    print(f"| {'Strategy':<25} | {'DB Query Time (ms)':<20} | {'HTTP Latency (ms)':<20} |")
    print(f"|{'-'*27}|{'-'*22}|{'-'*22}|")
    print(f"| {'No Pagination (Z->A)':<25} | {no_page_server:<20.3f} | {no_page_latency:<20.3f} |")
    print(f"| {'Offset (Skip {OFFSET})':<25} | {os:<20.3f} | {_l_os:<20.3f} |")
    print(f"| {'Cursor (WHERE id > {OFFSET})':<25} | {cs:<20.3f} | {_l_cs:<20.3f} |")
    
    print(f"\n[+] AUTO CONCLUSION:")
    if cs < os:
        diff = os / cs if cs > 0 else 999
        print(f"Cursor pagination is ~{diff:.1f}x faster than offset pagination!")
        print("-> Explanation: Offset must count and iterate through 95k skipped rows. Cursor uses the B-Tree index to jump directly to row 95000 (near O(1) access).")

if __name__ == "__main__":
    main()
