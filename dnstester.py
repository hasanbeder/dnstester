###############################
#      dnstester              #
#   DNS Performance Testing   #
###############################

# A Python script for DNS performance testing.
# It pings different DNS servers to measure their response times,
# and saves the results as an HTML report in a table and chart format.

# Required libraries: ping3, matplotlib, numpy, base64, io

import os
import time
from ping3 import ping
import matplotlib.pyplot as plt
import numpy as np
import base64
import io
import platform

# DNS servers to test
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

# Function to ping DNS servers and collect response times
def ping_dns_servers(servers, timeout=2, interval=1):
    """
    Pings DNS servers and collects response times.
    
    Args:
        servers (dict): Dictionary of DNS server names and IP addresses.
        timeout (int): Timeout value for ping operation.
        interval (int): Interval between ping operations.
        
    Returns:
        dict: Dictionary containing DNS server names as keys and ping times as values.
    """
    ping_times = {}
    for name, server in servers.items():
        ping_time = ping(server, timeout=timeout)
        if ping_time is not None:
            ping_times[name] = ping_time
        else:
            ping_times[name] = float("inf")
        time.sleep(interval)
    return ping_times

# Function to generate HTML report
def generate_html_report(ping_times, image_base64):
    """
    Generates an HTML report containing ping results and a chart.
    
    Args:
        ping_times (dict): Dictionary containing DNS server names and ping times.
        image_base64 (str): Base64 encoded image data for chart.
        
    Returns:
        str: HTML report as a string.
    """
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
    return html_template

# Function to plot ping times as a bar chart
def plot_bar_chart(ping_times):
    """
    Plots ping times as a bar chart.
    
    Args:
        ping_times (dict): Dictionary containing DNS server names and ping times.
        
    Returns:
        str: Base64 encoded image data for the chart.
    """
    plt.figure(figsize=(8, 6))
    plt.bar(ping_times.keys(), ping_times.values(), color="royalblue")
    plt.xticks(rotation=90, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel("DNS Servers", fontsize=14)
    plt.ylabel("Ping Times (ms)", fontsize=14)
    plt.title("DNS Server Performances", fontsize=16)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    image_data = buf.read()
    image_base64 = base64.b64encode(image_data).decode()
    
    return image_base64

# Function to open HTML report in a web browser
def open_html_report():
    """
    Opens the HTML report in a web browser.
    """
    system = platform.system()
    if system == "Windows":
        os.system("start dns_performance.html")
    elif system == "Darwin":
        os.system("open dns_performance.html")
    elif system == "Linux":
        os.system("xdg-open dns_performance.html")
    else:
        print("Unsupported operating system.")

# Main function to execute the script
def main():
    ping_times = ping_dns_servers(dns_servers)
    image_base64 = plot_bar_chart(ping_times)
    html_report = generate_html_report(ping_times, image_base64)
    
    with open("dns_performance.html", "w", encoding="utf-8") as f:
        f.write(html_report)
    
    # Display the DNS results report in the terminal
    for name, time in ping_times.items():
        print(f"{name}: {time*1000:.2f} ms")

    # Open HTML report in web browser
    open_html_report()

if __name__ == "__main__":
    main()
