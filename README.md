
# TikTok Soccer Video Scraper

This project is designed to search and download TikTok videos related to soccer training, categorized under different topics like technical skills, tactical understanding, and physical fitness. The scripts first search for videos using specific keywords and then fall back to hashtag searches if necessary. The downloaded videos and their metadata are stored in organized folders with formatted JSON files.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Script Execution Flow](#script-execution-flow)
- [Requirements](#requirements)
- [Notes on msToken](#notes-on-mstoken)
- [Troubleshooting and Updates](#troubleshooting-and-updates)

## Installation

To use this project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/TikTok-Api-Project.git
   cd TikTok-Api-Project
   ```

2. **Set Up a Virtual Environment**:
   Python 3.12 is recommended for this project.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```

3. **Install the Required Packages**:
   Make sure you have the latest versions of the required packages.
   ```bash
   pip install -r requirements.txt
   ```

   **Ensure you have Playwright installed**:
   ```bash
   playwright install
   ```

4. **Configure the `ms_token`**:
   - Obtain your `ms_token` by logging into TikTok on your web browser, performing a search, and then retrieving the `ms_token` from the browser's developer console.
   - Ensure you replace the placeholder `"YOUR_MS_TOKEN_HERE"` in the script with your actual `ms_token`.

## Usage

To run the scraper, use one of the provided Python scripts depending on the category you're interested in. For example:

```bash
python main.py
```

This will search and download videos related to the topics defined in `main.py`.

## Script Execution Flow

Each script in this project is designed to first perform a **search** using the TikTok API based on the specified keywords. If the search yields insufficient results or none at all, the script will automatically fall back to a **hashtag search**.

### How It Works

1. **Search Function**:
   - The script first constructs a search query using the provided keywords (e.g., "soccer dribbling drills").
   - It then sends this query to TikTok's search endpoint to retrieve videos related to the keyword.
   - The results from this search are processed, and if the number of videos found meets the specified maximum (`max_videos`), the script will proceed to download these videos.

2. **Hashtag Function**:
   - If the initial search does not retrieve enough videos, the script will automatically switch to a hashtag-based search using the corresponding hashtag (e.g., "soccerdribblingdrills").
   - The hashtag function searches for videos tagged with the specific hashtag.
   - Similar to the search function, the videos found are processed, and if they meet the conditions (e.g., related to the search term, created within the last two years), they will be downloaded.

3. **Download and Save**:
   - After gathering videos from either the search or hashtag method, the script will download the videos to the designated output folder.
   - Two JSON files are generated: one containing raw video data, and another formatted file with specific fields like `tags`, `pillars`, and `user_type` based on the search or hashtag term.

### Customization

You can adjust the `max_videos` parameter to control how many videos are downloaded per search or hashtag term. Additionally, the keywords and hashtags can be modified to tailor the search process to your specific needs.

This dual approach ensures that your search yields the maximum number of relevant videos, providing comprehensive coverage of the desired soccer training topics.

## Requirements

The project depends on the following Python libraries:

- `TikTokApi`: To interact with the TikTok platform.
- `yt-dlp`: For downloading videos from TikTok.
- `asyncio`: For managing asynchronous tasks.
- `datetime`: To handle date and time operations.
- `os` and `json`: For file and data handling.

Make sure all these libraries are installed by running:

```bash
pip install -r requirements.txt
```

## Notes on msToken

The `ms_token` is a critical piece of data needed to interact with TikTok's API. To obtain it:

1. Log in to TikTok via your web browser.
2. Perform a search on TikTok (e.g., "soccer training").
3. Open the browser's developer console (usually accessible via `F12` or `Ctrl+Shift+I`).
4. Locate the `ms_token` in the `Cookies` section under the `Application` tab.
5. Copy and paste this token into the script where indicated.

Make sure to keep this token secure and refresh it periodically if needed.

## Troubleshooting and Updates

This project uses the [TikTokApi](https://github.com/davidteather/TikTok-Api) library, which is an unofficial API for TikTok. Please refer to the issues tab on the GitHub repository for any known bugs or updates.

- **Playwright Version**: Ensure you are using the latest version of Playwright as it is crucial for interacting with TikTok's web pages.
- **Python Version**: This project is tested with Python 3.12. Ensure your environment is set up accordingly.

If you encounter any issues or the script doesn't behave as expected, consider checking for updates or issues on the [TikTokApi GitHub repository](https://github.com/davidteather/TikTok-Api).
