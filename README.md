# Plex to Sonarr Integration Script

A Python script to automate the process of adding TV shows from your Plex library to Sonarr. This script fetches a list of TV shows from Plex and checks if they already exist in Sonarr. It adds any missing shows and provides real-time progress updates in the terminal. Ideal if your Plex and Sonarr instances are on different machines.

## Features

- **Fetch Shows from Plex**: Retrieves TV shows from a specific section in your Plex library.
- **Check Sonarr for Existing Shows**: Ensures that shows aren't added to Sonarr if they already exist.
- **Real-time Progress Updates**: Displays real-time progress of how many shows have been processed, added, or failed.
- **Summary Report**: Provides a detailed summary after processing all shows, including the number of added shows, shows already in Sonarr, and any failed additions.

---

## Requirements

Ensure you have the following installed:

- **Python 3.6+**
- The following Python libraries:
  - `requests`

Install dependencies using `pip`:

```bash
pip install requests
```

---

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/cjaustin1792/plex-to-sonarr-integration.git
   cd plex-to-sonarr-integration
   ```

2. **Configure Plex and Sonarr**:

   - **Plex**:
     - Replace the `plex_url` variable with your Plex server URL, section ID, and Plex Token.
   - **Sonarr**:
     - Replace the `sonarr_url` with your Sonarr server URL and `sonarr_token` with your Sonarr API token.
     - Adjust the `rootFolderPath` in the script to match your directory structure for TV shows.

   Example Configuration in the Script:

   ```python
   plex_url = "http://<your-plex-ip>:32400/library/sections/2/all?X-Plex-Token=<your-plex-token>"
   sonarr_url = "http://<your-sonarr-ip>:8989/api/v3"
   sonarr_token = "<your-sonarr-api-token>"
   ```

---

## Usage

1. **Run the Script**:

   After configuring the script, run it with Python:

   ```bash
   python plex_to_sonarr.py
   ```

2. **Progress Display**:

   The script will show real-time progress as it processes each show from Plex and checks Sonarr.

   Example Progress Display:
   
   ```bash
   Processed 12/150 shows
   ```

3. **Summary Report**:

   After processing all shows, a summary will be displayed:

   ```bash
   Summary:
   Shows already in Sonarr: 10
   Shows added to Sonarr: 120
   Failed to add shows: 20
   Failed to add the following shows:
   - Show 1
   - Show 2
   ```

---

## Contributing

Feel free to submit pull requests or report issues. Contributions are welcome!

### How to Contribute:
1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push the branch (`git push origin feature-branch`).
5. Open a pull request.
