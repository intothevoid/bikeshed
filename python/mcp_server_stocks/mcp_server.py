from flask import Flask, request, jsonify
import requests
import logging
import json
import time
import sys
import os
import socket
from waitress import serve

# Completely disable all logging
logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger('mcp_stock_server')
logger.disabled = True

# Create Flask app with minimal configuration
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_SORT_KEYS'] = False

# Disable all Flask logging
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port):
    port = start_port
    while is_port_in_use(port):
        port += 1
    return port

# Yahoo Finance API endpoint for stock chart data
def get_chart_url(ticker):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=1d"

def get_stock_price(ticker):
    """
    Fetch stock chart data from Yahoo Finance API by properly mimicking a browser request.
    """
    # No query parameters needed in URL as they're now part of the URL itself
    url = get_chart_url(ticker)
    
    # Comprehensive browser-like headers - this is critical to avoid 429 errors
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://finance.yahoo.com/",
        "sec-ch-ua": '"Google Chrome";v="120", "Chromium";v="120", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive"
    }
    
    try:
        # Use a new session for each request to avoid cookie tracking issues
        with requests.Session() as session:
            # First visit the base page to get cookies (like a real browser would)
            session.get("https://finance.yahoo.com/", headers=headers)
            
            # Then make the actual API request
            response = session.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract data from chart response structure
            chart_result = data.get("chart", {}).get("result", [])
            if not chart_result:
                return {"error": f"Chart data not found for {ticker}"}
                
            quote = chart_result[0].get("meta", {})
            
            # Get the latest price from quote
            current_price = quote.get("regularMarketPrice")
            
            if current_price is not None:
                return {
                    "ticker": ticker,
                    "price": float(current_price),
                    "currency": quote.get("currency", "USD"),
                    "exchange": quote.get("exchangeName", ""),
                    "timestamp": quote.get("regularMarketTime", 0)
                }
            else:
                return {"error": f"Price data not found for {ticker}"}
                
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {"error": f"API request failed: {str(e)}"}
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Error parsing response: {str(e)}")
        return {"error": f"Failed to parse API response: {str(e)}"}

# Original stock data endpoint
@app.route("/get_stock_data", methods=["GET"])
def handle_get_stock_data():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400
    
    result = get_stock_price(ticker)
    
    # Return appropriate status code based on result
    if "error" in result and "not found" in result["error"]:
        return jsonify(result), 404
    elif "error" in result:
        return jsonify(result), 500
    
    return jsonify(result)

# MCP Protocol Implementation
@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    try:
        # Parse the incoming request
        mcp_request = request.json
        
        # Check for required fields in MCP request
        if not mcp_request or "messages" not in mcp_request:
            return jsonify({
                "error": "Invalid MCP request format"
            }), 400
        
        # Extract the latest user message
        user_messages = [msg for msg in mcp_request["messages"] if msg.get("role") == "user"]
        if not user_messages:
            return jsonify({
                "error": "No user message found in request"
            }), 400
            
        latest_user_message = user_messages[-1]["content"]
        
        # Process the user message to extract ticker symbol
        # This is a simple implementation - you might want to add more sophisticated parsing
        ticker = None
        
        # Check if message contains stock price query format
        words = latest_user_message.lower().split()
        
        # Look for patterns like "price of AAPL" or "AAPL stock price" or "stock price for AAPL"
        for i, word in enumerate(words):
            if word.upper() == word and len(word) >= 1 and len(word) <= 5 and word.isalpha():
                # This looks like a ticker symbol (all caps, 1-5 letters)
                ticker = word.upper()
                break
                
            if i < len(words) - 1:
                if (word == "for" or word == "of") and words[i+1].upper() == words[i+1] and len(words[i+1]) <= 5:
                    ticker = words[i+1].upper()
                    break
        
        # If we couldn't find a ticker in the message
        if not ticker:
            return jsonify({
                "messages": [{
                    "role": "assistant",
                    "content": "I couldn't identify a stock ticker symbol in your message. Please specify a valid stock symbol like AAPL, MSFT, or TSLA."
                }]
            })
        
        # Get stock data
        stock_data = get_stock_price(ticker)
        
        # Format the response for Claude Desktop
        if "error" in stock_data:
            response_content = f"I encountered an error looking up {ticker}: {stock_data['error']}"
        else:
            # Format price with 2 decimal places
            price = f"{stock_data['price']:.2f}"
            response_content = f"The current price of {ticker} is {price} {stock_data['currency']} on {stock_data['exchange']}."
        
        # Return response in MCP format
        return jsonify({
            "messages": [{
                "role": "assistant",
                "content": response_content
            }]
        })
        
    except Exception as e:
        logger.error(f"MCP processing error: {str(e)}")
        return jsonify({
            "messages": [{
                "role": "assistant",
                "content": f"I encountered an error processing your request: {str(e)}"
            }]
        })

@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "service": "MCP Stock Server"})

# MCP Info endpoint to provide information about this MCP server
@app.route("/mcp/info", methods=["GET"])
def mcp_info():
    return jsonify({
        "name": "Stock Price Lookup",
        "version": "1.0.0",
        "description": "Get real-time stock prices from Yahoo Finance",
        "author": "Your Name",
        "properties": {
            "max_tokens_to_sample": 1000,
            "temperature": 0
        }
    })

if __name__ == "__main__":
    # Get port from environment or use default
    default_port = 8081
    port = int(os.environ.get('PORT', default_port))
    
    # Find an available port if the specified one is in use
    if is_port_in_use(port):
        port = find_available_port(port)
        print(f"Port {port} is available", file=sys.stderr)
    
    # Check if running in Claude Desktop environment
    if 'WERKZEUG_SERVER_FD' in os.environ:
        try:
            # Running in Claude Desktop - use the provided file descriptor
            serve(
                app,
                host="0.0.0.0",
                port=port,
                threads=1,
                _quiet=True,
                fd=int(os.environ["WERKZEUG_SERVER_FD"])
            )
        except Exception as e:
            print(f"Error starting server: {str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        # Running standalone - use waitress server
        serve(
            app,
            host="0.0.0.0",
            port=port,
            threads=1,
            _quiet=True
        )
