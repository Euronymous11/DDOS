from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import re
from datetime import datetime
from analytics import analyze_request_rate, analyze_unique_ips
from config import RATE_LIMIT

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='logs/ddos_protection.log', level=logging.INFO)

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{RATE_LIMIT} per minute"]  # Defined in config
)

# Serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# Provide real-time traffic status and stats
@app.route('/traffic-status')
def traffic_status():
    try:
        # Read and process the logs for traffic data
        ip_count = {}
        request_times = []
        
        with open('logs/ddos_protection.log', 'r') as log_file:
            logs = log_file.readlines()
            for log in logs:
                ip_match = re.search(r'IP: (\d+\.\d+\.\d+\.\d+)', log)
                time_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', log)
                
                if ip_match and time_match:
                    ip = ip_match.group(1)
                    time = time_match.group(1)
                    ip_count[ip] = ip_count.get(ip, 0) + 1
                    request_times.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
        
        # Total requests and unique IPs
        total_requests = len(logs)
        unique_ips = len(ip_count)

        # Request rates over time (requests per minute)
        request_rates, time_stamps = analyze_request_rate(request_times)
        
        return jsonify({
            "status": "High" if total_requests > 100 else "Normal",
            "total_requests": total_requests,
            "unique_ips": unique_ips,
            "request_rates": request_rates,
            "time_stamps": time_stamps
        })
    except Exception as e:
        return jsonify({"status": "Error retrieving traffic data", "error": str(e)})

# Log incoming requests and apply rate limiting
@app.before_request
def log_request_info():
    logging.info(f'{datetime.now()} - IP: {request.remote_addr}, Path: {request.path}')

# Rate-limited route for demo
@app.route('/rate-limited')
@limiter.limit("5 per minute")
def limited():
    return "This route is rate-limited to 5 requests per minute."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
