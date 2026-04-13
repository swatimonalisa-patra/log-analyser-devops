#!/usr/bin/env python3
"""
Log Analyser Script
Parses log files to extract ERROR and WARNING messages,
counts their frequencies, and generates a summary report.
"""

import sys
import json
from collections import Counter
import argparse


def parse_log_file(file_path):
    """
    Parse the log file and extract ERROR and WARNING messages.

    Args:
        file_path (str): Path to the log file

    Returns:
        tuple: (error_messages, warning_messages)
    """
    error_messages = []
    warning_messages = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                # Find the log level (ERROR, WARNING, INFO)
                parts = line.split()
                if len(parts) < 3:
                    continue

                # Assume format: timestamp level message...
                # Timestamp is first two parts, level is third, rest is message
                timestamp = f"{parts[0]} {parts[1]}"
                level = parts[2]
                message = ' '.join(parts[3:])

                if level == 'ERROR':
                    error_messages.append(message)
                elif level == 'WARNING':
                    warning_messages.append(message)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return error_messages, warning_messages


def analyze_messages(error_messages, warning_messages):
    """
    Analyze the messages to count frequencies and find top 3.

    Args:
        error_messages (list): List of error messages
        warning_messages (list): List of warning messages

    Returns:
        dict: Analysis results
    """
    all_messages = error_messages + warning_messages

    if not all_messages:
        return {
            'total_errors': 0,
            'total_warnings': 0,
            'total_errors_warnings': 0,
            'unique_messages': 0,
            'top_3_messages': [],
            'all_frequencies': {}
        }

    # Count frequencies for all messages
    frequencies = Counter(all_messages)

    # Get top 3 most frequent
    top_3 = frequencies.most_common(3)

    return {
        'total_errors': len(error_messages),
        'total_warnings': len(warning_messages),
        'total_errors_warnings': len(all_messages),
        'unique_messages': len(frequencies),
        'top_3_messages': top_3,
        'all_frequencies': dict(frequencies)
    }


def generate_text_report(analysis, output_file):
    """
    Generate a text summary report.

    Args:
        analysis (dict): Analysis results
        output_file (str): Output file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Log Analysis Summary Report\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Total ERROR messages: {analysis['total_errors']}\n")
        f.write(f"Total WARNING messages: {analysis['total_warnings']}\n")
        f.write(f"Total ERROR/WARNING messages: {analysis['total_errors_warnings']}\n")
        f.write(f"Unique messages: {analysis['unique_messages']}\n\n")

        if analysis['top_3_messages']:
            f.write("Top 3 Most Frequent Messages:\n")
            for i, (message, count) in enumerate(analysis['top_3_messages'], 1):
                f.write(f"{i}. {message} (occurrences: {count})\n")
        else:
            f.write("No ERROR or WARNING messages found.\n")

        f.write("\nAll Frequencies:\n")
        for message, count in analysis['all_frequencies'].items():
            f.write(f"- {message}: {count}\n")


def generate_json_report(analysis, output_file):
    """
    Generate a JSON summary report.

    Args:
        analysis (dict): Analysis results
        output_file (str): Output file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Analyze log files for ERROR and WARNING messages.')
    parser.add_argument('log_file', help='Path to the log file to analyze')
    parser.add_argument('--output', '-o', default='summary', help='Base name for output files (default: summary)')
    parser.add_argument('--format', choices=['txt', 'json', 'both'], default='both',
                       help='Output format: txt, json, or both (default: both)')
    parser.add_argument('--fail-on-error', action='store_true',
                       help='Exit with code 1 if any ERROR messages are found')

    args = parser.parse_args()

    # Parse log file
    error_messages, warning_messages = parse_log_file(args.log_file)

    # Analyze messages
    analysis = analyze_messages(error_messages, warning_messages)

    # Generate reports
    if args.format in ['txt', 'both']:
        generate_text_report(analysis, f"{args.output}.txt")

    if args.format in ['json', 'both']:
        generate_json_report(analysis, f"{args.output}.json")

    print(f"Analysis complete. Reports generated: {args.output}.txt and/or {args.output}.json")

    # Exit with error code if there are ERROR messages and flag is set
    if args.fail_on_error and analysis['total_errors'] > 0:
        print(f"Found {analysis['total_errors']} ERROR messages. Failing the build.")
        sys.exit(1)


if __name__ == "__main__":
    main()