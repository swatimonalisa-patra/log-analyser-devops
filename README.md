# Log Analyser DevOps

A comprehensive DevOps solution for automated log analysis, monitoring, and CI/CD pipeline integration.

## What This Project Does

This project provides automated tools for analyzing application log files to identify and report on ERROR and WARNING messages. It includes:

- **Log Analyser Script** (`log_analyser.py`): Parses log files, extracts ERROR/WARNING messages, counts frequencies, and generates summary reports
- **Log Monitor** (`log_monitor.py`): Automatically monitors folders for new log files and runs analysis on them
- **CI/CD Pipeline**: GitHub Actions workflow that runs log analysis on every push to main branch and fails if ERROR messages are found

## Features

- Extracts and counts ERROR and WARNING messages from log files
- Generates both text and JSON summary reports
- Identifies top 3 most frequent error/warning messages
- CI/CD pipeline integration with automatic failure on ERROR detection
- Folder monitoring for real-time log analysis
- Configurable output formats and failure conditions

## Prerequisites

- Python 3.6+
- For log monitoring: `pip install -r requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd log-analyser-devops
   ```

2. Install dependencies (for monitoring feature):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Log Analyser

Analyze a single log file:

```bash
python log_analyser.py sample.log
```

This will generate `summary.txt` and `summary.json` files.

Options:
- `--output <name>`: Specify base name for output files
- `--format txt|json|both`: Choose output format
- `--fail-on-error`: Exit with code 1 if ERROR messages are found (used by CI/CD)

### Log Monitor

Monitor a folder for new log files:

```bash
python log_monitor.py /path/to/log/folder
```

The monitor will automatically analyze any new or modified `.log` files in the specified folder.

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:

1. Triggers on pushes to the `main` branch
2. Sets up Python environment
3. Runs the log analyser on `sample.log` with `--fail-on-error` flag
4. Fails the build if any ERROR messages are detected
5. Uploads analysis results as artifacts

### Pipeline Status

The pipeline will:
- ✅ **Pass**: If the log file contains no ERROR messages (WARNINGs are allowed)
- ❌ **Fail**: If any ERROR messages are found in the log file

## Sample Log Format

The analyser expects logs in this format:
```
2024-01-15 10:23:01 INFO  Application started
2024-01-15 10:23:05 ERROR Database connection failed
2024-01-15 10:23:10 WARNING High memory usage detected
```

## Output Examples

### Text Report (summary.txt)
```
Log Analysis Summary Report
==============================

Total ERROR messages: 4
Total WARNING messages: 2
Total ERROR/WARNING messages: 6
Unique messages: 3

Top 3 Most Frequent Messages:
1. Database connection failed (occurrences: 3)
2. High memory usage detected (occurrences: 2)
3. Timeout while calling payment API (occurrences: 1)

All Frequencies:
- Database connection failed: 3
- Timeout while calling payment API: 1
- High memory usage detected: 2
```

### JSON Report (summary.json)
```json
{
  "total_errors": 4,
  "total_warnings": 2,
  "total_errors_warnings": 6,
  "unique_messages": 3,
  "top_3_messages": [
    ["Database connection failed", 3],
    ["High memory usage detected", 2],
    ["Timeout while calling payment API", 1]
  ],
  "all_frequencies": {
    "Database connection failed": 3,
    "Timeout while calling payment API": 1,
    "High memory usage detected": 2
  }
}
```

## Project Structure

```
log-analyser-devops/
├── log_analyser.py          # Main analysis script
├── log_monitor.py           # Folder monitoring script
├── requirements.txt         # Python dependencies
├── sample.log              # Sample log file for testing
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions workflow
└── README.md              # This file
```

## Future Improvements

If I had more time, I would add:

1. **Web Dashboard**: A simple web interface to view analysis results and historical trends
2. **Alerting Integration**: Email/Slack notifications when ERROR thresholds are exceeded
3. **Database Storage**: Store analysis results in a database for historical tracking
4. **Advanced Filtering**: Support for custom log formats and filtering rules
5. **Performance Monitoring**: Integration with monitoring tools like Prometheus/Grafana
6. **Multi-format Support**: Handle different log formats (JSON, XML, etc.)
7. **Parallel Processing**: Analyze multiple log files concurrently
8. **Configuration Management**: YAML/JSON config files for customizable rules
9. **Docker Containerization**: Containerized deployment for easy scaling
10. **Kubernetes Integration**: Deploy as a Kubernetes job/cronjob for production use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.