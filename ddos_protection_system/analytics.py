from collections import defaultdict
from datetime import datetime

def analyze_request_rate(request_times):
    """
    Analyzes the request rate by calculating the number of requests per minute.
    """
    rate_dict = defaultdict(int)
    
    for req_time in request_times:
        minute = req_time.strftime('%H:%M')
        rate_dict[minute] += 1
    
    sorted_rates = [rate_dict[minute] for minute in sorted(rate_dict)]
    sorted_times = sorted(set([t.strftime('%H:%M') for t in request_times]))
    
    return sorted_rates, sorted_times

def analyze_unique_ips(logs):
    """
    Returns the number of unique IPs based on logs.
    """
    unique_ips = set()
    for log in logs:
        ip_match = re.search(r'IP: (\d+\.\d+\.\d+\.\d+)', log)
        if ip_match:
            unique_ips.add(ip_match.group(1))
    
    return len(unique_ips)
