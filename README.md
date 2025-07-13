# WebCrawler

A robust, multi-threaded web crawler built in Python for research, monitoring, and educational use.  
It saves crawl results to MongoDB, supports periodic crawling, and lets you enqueue new URLs via HTTP POST requests.  
**Just run `python main.py` to start both the server and the robot automatically!**

---

## Features

- **Automatic Startup:**  
  Run `python main.py` and both the HTTP server and robot worker start up in the background.
- **Enqueue URLs via HTTP:**  
  Add URLs to be crawled by sending a POST request to `/crawl` on the HTTP server.
- **Multi-threaded Crawling:**  
  Crawler uses multiple threads for efficient, parallel crawling.
- **Configurable Depth, Limits, and Workers:**  
  Set crawling depth, content/token limits, and worker threads via code or `.env`.
- **MongoDB Integration:**  
  Page results and metadata are stored in MongoDB (connection string set in `.env`).
- **Interval-based Crawling:**  
  The robot worker runs forever, picking up enqueued URLs and crawling them at intervals you configure.
- **Centralized Configuration:**  
  All runtime and sensitive configs (MongoDB URI, robot interval, etc.) are set via a `.env` file.
- **Health Endpoint:**  
  Check server status quickly via `/health`.

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/kushagra21-afk/WebCrawler.git
    cd WebCrawler
    ```
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure your `.env` file:**  
   This file belongs in the project root. Set these variables:

    ```dotenv
    MONGODB_URI=mongodb://localhost:27017/
    USER_AGENT=WebCrawler/1.0 contact your@email.com (educational purposes)
    robot_workers=4
    ROBOT_INTERVAL=600
    ```
    - `MONGODB_URI` — MongoDB connection string
    - `USER_AGENT` — User agent string for crawler requests
    - `robot_workers` — Number of parallel crawling threads (robot worker)
    - `ROBOT_INTERVAL` — Interval (in seconds) between robot cycles

---

## Usage

### 1. Start Everything Automatically

Run:

```bash
python main.py
```

- The HTTP server will start (default: http://localhost:8000).
- The robot worker will run in the background, crawling URLs at your interval.

### 2. Enqueue a URL to Crawl

Send a POST request to `/crawl` with the target URL:

```bash
curl -X POST http://localhost:8000/crawl \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```
You'll get a 202 Accepted response if the URL was queued successfully.

### 3. Check Server Health

```bash
curl http://localhost:8000/health
```

---

## How It Works

- **main.py:** Starts both the HTTP server and the robot worker in background threads.
- **HTTP Server:** Accepts POST requests to `/crawl` to enqueue URLs for crawling.
- **Robot Worker:** Periodically checks the queue and launches crawlers in parallel for each URL.
- **Crawler:** Extracts content and metadata, follows internal links (configurable depth), and stores results in MongoDB.
- **MongoDB:** Crawl results are stored in the database and collection specified in `.env`.

---

## File Structure

- `main.py` — Launches server and robot worker.
- `socket_server.py` — HTTP server for URL enqueueing and health checks.
- `robot.py` — Manages interval-based crawling and parallel execution.
- `crawler.py` — Implements the actual crawling logic.
- `db.py` — Handles MongoDB connections and inserts.
- `utils.py` — Helper functions for HTTP responses.

---

## Configuration

All major settings are in `.env`.  
**Always update your MongoDB connection string and robot interval in `.env` before running.**

---

## Contributing

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/foo`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/foo`)
5. Create a new Pull Request

---

## License

MIT License

---

## Notes

- You only need to run `python main.py` to start everything.
- URLs can be enqueued for crawling at any time using the HTTP API.
- See [main.py](https://github.com/kushagra21-afk/WebCrawler/blob/main/main.py), [socket_server.py](https://github.com/kushagra21-afk/WebCrawler/blob/main/socket_server.py), and [robot.py](https://github.com/kushagra21-afk/WebCrawler/blob/main/robot.py) for implementation details.
- Crawl results are saved to the `webcrawler.pages` collection in MongoDB.

---

## Contact

For questions or suggestions, open an issue or reach out via GitHub.
