#######################
#      dnstester      #
#   DNS Performance   #
#######################

# A Python script that performs DNS performance testing.
# It pings different DNS servers to measure their response times,
# and saves the results as an HTML report in a table and chart format.
#
# Required libraries: ping3, matplotlib, numpy, base64, io

import os
import time
from ping3 import ping
import matplotlib.pyplot as plt
import numpy as np
import base64
import io

# Popular DNS servers
dns_servers = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "OpenDNS": "208.67.222.222",
    "Quad9": "9.9.9.9",
    "Level3": "209.244.0.3",
    "Comodo Secure": "8.26.56.26",
    "AdGuard DNS": "94.140.14.14",
    # Add more here
}

# Ping the servers and collect their response times
ping_times = {}
for name, server in dns_servers.items():
    ping_time = ping(server, timeout=2)
    if ping_time is not None:
        ping_times[name] = ping_time
    else:
        ping_times[name] = float("inf")
    time.sleep(1)

# Plot the results as a bar chart
plt.figure(figsize=(8, 6))
plt.bar(ping_times.keys(), ping_times.values(), color="royalblue")
plt.xticks(rotation=90, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("DNS Servers", fontsize=14)
plt.ylabel("Ping Times (ms)", fontsize=14)
plt.title("DNS Server Performances", fontsize=16)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Convert the plot to base64 format
buf = io.BytesIO()
plt.savefig(buf, format="png", bbox_inches="tight")
buf.seek(0)
image_data = buf.read()
image_base64 = base64.b64encode(image_data).decode()

# HTML report generation
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNS Performance Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #ccc;
        }}
        th {{
            background-color: #f2f2f2;
            text-align: left;
        }}
        img {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 80%;
        }}
        .footer {{
            margin-top: 50px;
            text-align: center;
            font-size: 14px;
        }}
        @keyframes fadein {{
            from {{ opacity: 0; }}
            to   {{ opacity: 1; }}
        }}
        h1 {{
            animation: fadein 2s;
        }}
    </style>
</head>
<body>
    <h1>DNS Performance Report</h1>
    <h2>Table</h2>
    <table>
        <thead>
            <tr>
                <th>DNS Server</th>
                <th>Ping Time (ms)</th>
            </tr>
        </thead>
        <tbody>
            {''.join([f'<tr><td>{name}</td><td>{time * 1000:.2f}</td></tr>' for name, time in ping_times.items()])}
        </tbody>
    </table>
    <h2>Chart</h2>
    <img src="data:image/png;base64,{image_base64}" alt="DNS performance chart" style="max-width: 100%; height: auto;">
    <div class="footer">
        <p>This report was generated using <a href="https://github.com/hasanbeder/dnstester" target="_blank">https://github.com/hasanbeder/dnstester</a>.</p>
    </div>
</body>
</html>
"""

# Save the HTML report
with open("dns_performance.html", "w", encoding="utf-8") as f:
    f.write(html_template)

# Display the DNS results report in the terminal
for name, time in ping_times.items():
    print(f"{name}: {time*1000:.2f} ms")
