import requests
import xml.etree.ElementTree as ET
import sys
import time

# Plex and Sonarr URLs and tokens
plex_url = "http://<plex-ip>:32400/library/sections/<tv-shows-library-id>/all?X-Plex-Token=<plex-token>"
sonarr_url = "http://localhost:8989/api/v3"
sonarr_token = "<sonarr-api-token>"
headers = {'X-Api-Key': sonarr_token}

# Function to get shows from Plex
def get_plex_shows(plex_url):
    response = requests.get(plex_url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        tv_shows = [{'title': directory.get('title'), 'year': directory.get('year')} for directory in root.findall('Directory')]
        return tv_shows
    else:
        print(f"Failed to fetch from Plex API. Status Code: {response.status_code}")
        return []

# Function to get existing shows in Sonarr
def get_sonarr_shows():
    response = requests.get(f"{sonarr_url}/series", headers=headers)
    if response.status_code == 200:
        return {show['title'].lower(): show for show in response.json()}
    else:
        print(f"Failed to fetch Sonarr shows. Status Code: {response.status_code}")
        return {}

# Function to update progress in the terminal
def update_progress(processed, total):
    progress = f"Processed {processed}/{total} shows"
    sys.stdout.write(f"\r{progress}")
    sys.stdout.flush()

# Function to add a show to Sonarr
def add_show_to_sonarr(show, existing_sonarr_shows, results, processed, total):
    title, year = show['title'], show.get('year')
    # 
    # Check if the show is already in Sonarr
    if title.lower() in existing_sonarr_shows:
        results['already_in_sonarr'] += 1
    else:
        search_payload = {'term': title}
        search_response = requests.get(f"{sonarr_url}/series/lookup", params=search_payload, headers=headers)
        
        if search_response.status_code == 200:
            search_results = search_response.json()
            for result in search_results:
                if result['title'].lower() == title.lower() and (year is None or ('year' in result and result['year'] == int(year))):
                    add_payload = {
                        'title': result['title'],
                        'tvdbId': result['tvdbId'],
                        'qualityProfileId': 1,  # Adjust quality profile ID
                        'titleSlug': result['titleSlug'],
                        'images': result['images'],
                        'rootFolderPath': "/path/to/your/shows",  # Adjust root folder path
                        'seasons': result['seasons'],
                        'monitored': True,
                        'addOptions': {'searchForMissingEpisodes': False}
                    }
                    
                    add_response = requests.post(f"{sonarr_url}/series", json=add_payload, headers=headers)
                    if add_response.status_code == 201:
                        results['added'] += 1
                    else:
                        results['failed_to_add'].append(title)
                    break
            else:
                results['failed_to_add'].append(title)
        else:
            results['failed_to_add'].append(title)

    # Update progress
    update_progress(processed + 1, total)

# Main function
def main():
    plex_shows = get_plex_shows(plex_url)
    existing_sonarr_shows = get_sonarr_shows()
    total_shows = len(plex_shows)

    # Initialize results
    results = {
        'already_in_sonarr': 0,
        'added': 0,
        'failed_to_add': []
    }

    # Process each show one by one
    for i, show in enumerate(plex_shows):
        add_show_to_sonarr(show, existing_sonarr_shows, results, i, total_shows)

    # Print summary
    print("\n\nSummary:")
    print(f"Shows already in Sonarr: {results['already_in_sonarr']}")
    print(f"Shows added to Sonarr: {results['added']}")
    print(f"Failed to add shows: {len(results['failed_to_add'])}")
    if results['failed_to_add']:
        print("Failed to add the following shows:")
        for title in results['failed_to_add']:
            print(f"- {title}")

# Run the script
if __name__ == "__main__":
    main()
