#!/usr/bin/env bash
# Runs all three parts. Each part writes its tables to <part>/results/ and plots to <part>/figures/.
set -euo pipefail
cd "$(dirname "$0")"

echo "### Part 1 - second-price auction";  python3 part1_second_price_auction/run_part1.py
echo "### Part 2 - first-price auction";   python3 part2_first_price_auction/run_part2.py
echo "### Part 3 - VCG path auction";      python3 part3_vcg_cheapest_path/run_part3.py
