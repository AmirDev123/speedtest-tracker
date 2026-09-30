# speedtest-tracker

Track your internet connection speed over time. Runs real speed tests using [speedtest-cli](https://github.com/sivel/speedtest-cli), persists results in SQLite, and displays history and aggregate statistics.

## Features

- Measures download speed, upload speed, and ping
- Stores all results with timestamps in a local SQLite database
- Shows history table and min/max/avg stats

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py run         # Run a speed test (~20-30 sec)
python main.py history     # Show last 10 results
python main.py history -n 20
python main.py stats       # Show aggregate statistics
```

## Example output

```
$ python main.py stats

Statistics over 15 test(s):
  Download    latest=  94.3Mbps  avg=  91.2Mbps  min=  78.4Mbps  max=  97.6Mbps
  Upload      latest=  45.1Mbps  avg=  43.8Mbps  min=  38.0Mbps  max=  47.2Mbps
  Ping        latest=  11.2ms    avg=  12.5ms     min=   9.8ms    max=  18.4ms
```

## Running tests

```bash
pytest tests/
```

## Project structure

```
speedtest-tracker/
├── tracker/
│   ├── runner.py   # speedtest-cli wrapper
│   ├── storage.py  # SQLite persistence
│   └── stats.py    # Aggregate statistics
├── tests/
│   └── test_tracker.py
├── main.py
└── requirements.txt
```
