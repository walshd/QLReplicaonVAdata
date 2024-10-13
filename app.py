from flask import Flask, render_template, request, jsonify
import json
import requests
from datetime import datetime, timedelta
import os
import logging
import re
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
socketio = SocketIO(app)

# V&A API base URL
API_BASE_URL = 'https://api.vam.ac.uk/v2/objects/search' 
CACHE_FILE = 'cache/vam_data.json'

def is_cache_expired(cache_file, hours=1):
    if not os.path.exists(cache_file):
        return True
    file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
    return datetime.now() - file_time > timedelta(hours=hours)

def extract_year(date_string):
    if not date_string or date_string == 'Unknown':
        return None
    
    # Handle date ranges
    if '-' in date_string:
        years = re.findall(r'\b(\d{4})\b', date_string)
        if len(years) >= 2:
            return int(years[0])  # Return the earlier year in the range
    
    # Try to extract a 4-digit year
    year_match = re.search(r'\b(\d{4})\b', date_string)
    if year_match:
        return int(year_match.group(1))
    
    # Try to parse various date formats
    date_formats = [
        "%Y",  # e.g., "1900"
        "%Y-%m-%d",  # e.g., "1900-01-01"
        "%d/%m/%Y",  # e.g., "01/01/1900"
        "%B %Y",  # e.g., "January 1900"
        "%Y-%m",  # e.g., "1900-01"
    ]
    
    for fmt in date_formats:
        try:
            date = datetime.strptime(date_string, fmt)
            return date.year
        except ValueError:
            continue
    
    # Handle century or decade references
    century_match = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s*century', date_string, re.IGNORECASE)
    if century_match:
        century = int(century_match.group(1))
        return (century - 1) * 100 + 50  # Return middle year of the century
    
    decade_match = re.search(r'(\d{3})0s', date_string)
    if decade_match:
        return int(decade_match.group(1) + '5')  # Return middle year of the decade
    
    # If all else fails, try to find any 4-digit number
    any_year = re.search(r'\d{4}', date_string)
    if any_year:
        return int(any_year.group())
    
    return None

def fetch_vam_data(pages=1, start_page=1):
    logging.info(f"Fetching {pages} pages of data from V&A API, starting from page {start_page}...")
    all_data = []
    try:
        for page in range(start_page, start_page + pages):
            url = f"{API_BASE_URL}?limit=15&images=true&collection=prints&collection=posters&page={page}"
            logging.info(f"Fetching page {page} from URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            logging.info(f"Received {len(data.get('records', []))} records from page {page}")
            
            for item in data.get('records', []):
                date = item.get('_primaryDate', 'Unknown')
                year = extract_year(date)
                processed_item = {
                    'id': item.get('systemNumber', ''),
                    'objectType': item.get('objectType', 'Unknown'),
                    'title': item.get('_primaryTitle', 'Untitled'),
                    'date': date,
                    'year': year,
                    'place': item.get('_primaryPlace', 'Unknown'),
                    'artist': item.get('_primaryMaker', {}).get('name', 'Unknown'),
                    'imageUrl': item.get('_images', {}).get('_iiif_image_base_url', '')
                }
                all_data.append(processed_item)
            
            logging.info(f"Processed {len(all_data)} items so far")
        
        logging.info(f"Total data processed: {len(all_data)} items")
        return all_data
    except Exception as e:
        logging.error(f"Error fetching V&A data: {str(e)}")
        logging.exception("Exception details:")
        return []

def fetch_and_cache_data(force_refresh=False, initial_pages=7, total_pages=20):
    logging.info(f"Fetching and caching data. Force refresh: {force_refresh}")
    if force_refresh or not os.path.exists(CACHE_FILE) or is_cache_expired(CACHE_FILE):
        initial_data = fetch_vam_data(pages=initial_pages)
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(initial_data, f)
        logging.info(f"Initial data cached: {len(initial_data)} items")
        
        # Start background task to fetch additional pages
        threading.Thread(target=fetch_additional_pages, args=(initial_pages, total_pages)).start()
        
        return initial_data
    else:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)

def fetch_additional_pages(start_page, end_page):
    logging.info(f"Starting background fetch from page {start_page + 1} to {end_page}")
    for page in range(start_page + 1, end_page + 1):
        logging.info(f"Fetching additional page {page}")
        new_items = fetch_vam_data(pages=1, start_page=page)
        update_cache_and_notify(new_items)

def update_cache_and_notify(new_data):
    with open(CACHE_FILE, 'r+') as f:
        current_data = json.load(f)
        current_data.extend(new_data)
        f.seek(0)
        json.dump(current_data, f)
        f.truncate()
    
    # Process new data for frontend
    timeline_data, words = process_data_for_frontend(current_data)
    
    # Notify frontend of new data
    socketio.emit('new_data', {
        'timeline_data': timeline_data,
        'words': list(words),
        'new_artifacts': new_data
    })
    logging.info(f"Emitted new data: {len(new_data)} new items, total {len(current_data)} items")

def process_data_for_frontend(data):
    timeline_data = {}
    words = set()
    for item in data:
        if item['year']:
            timeline_data[str(item['year'])] = timeline_data.get(str(item['year']), 0) + 1
        words.update([item['objectType'], item['place']])
    
    timeline_data = dict(sorted(timeline_data.items()))
    return timeline_data, words

@app.route('/')
def home():
    data = fetch_and_cache_data(initial_pages=7, total_pages=20)
    timeline_data, words = process_data_for_frontend(data)

    return render_template('index.html', 
                           timeline_data=json.dumps(timeline_data),
                           words=json.dumps(list(words)),
                           artifacts=json.dumps(data[:30]))  # Limit to 30 artifacts for initial load

@app.route('/refresh-data')
def refresh_data():
    logging.info("Refresh data route accessed")
    data = fetch_and_cache_data(force_refresh=True)
    
    timeline_data = {}
    words = set()
    for item in data:
        if item['year']:
            timeline_data[str(item['year'])] = timeline_data.get(str(item['year']), 0) + 1
        words.update([item['objectType'], item['place']])
    
    timeline_data = dict(sorted(timeline_data.items()))
    words = list(words)

    return jsonify({
        'status': 'success',
        'message': 'Data refreshed successfully',
        'timeline_data': timeline_data,
        'words': words,
        'new_artifacts': data[:30]
    })

@app.route('/fetch-more-data')
def fetch_more_data():
    current_data = fetch_and_cache_data()
    new_data = fetch_vam_data(pages=1)  # Fetch one more page
    updated_data = current_data + new_data
    
    # Update the cache file
    with open(CACHE_FILE, 'w') as f:
        json.dump(updated_data, f)
    
    # Process the new data for the frontend
    timeline_data = {}
    words = set()
    for item in updated_data:
        if item['year']:
            timeline_data[str(item['year'])] = timeline_data.get(str(item['year']), 0) + 1
        words.update([item['objectType'], item['place']])
    
    timeline_data = dict(sorted(timeline_data.items()))
    words = list(words)
    
    return jsonify({
        'status': 'success',
        'message': 'Data updated successfully',
        'timeline_data': timeline_data,
        'words': words,
        'new_artifacts': new_data
    })

@app.route('/filter-artifacts')
def filter_artifacts():
    year = request.args.get('year', type=int)
    word = request.args.get('word')
    data = fetch_and_cache_data()
    
    filtered_artifacts = data
    if year:
        filtered_artifacts = [artifact for artifact in filtered_artifacts if artifact['year'] == year]
    if word:
        filtered_artifacts = [artifact for artifact in filtered_artifacts 
                              if word.lower() in artifact['objectType'].lower() 
                              or word.lower() in artifact['place'].lower()]
    
    return jsonify({
        'status': 'success',
        'artifacts': filtered_artifacts[:30]  # Limit to 30 artifacts for performance
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)
