# Abandoned Project Finder

A Python script to discover popular but abandoned Python projects on GitHub and identify their actively maintained forks.

## Features

- 🔍 Searches GitHub for Python repositories with 1,000+ stars
- ⏰ Identifies projects with no commits in the last year
- 🍴 Finds actively maintained forks (commits in last 6 months)
- 📊 Scores projects based on popularity, abandonment, and maintenance burden
- 📄 Exports results to CSV for easy analysis

## Requirements

- Python 3.9+
- GitHub account (for API access)
- GitHub Personal Access Token (optional but recommended)

## Installation

1. Create a virtual environment (recommended):
```bash
cd scripts
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up GitHub authentication (optional but recommended for higher rate limits):
```bash
export GITHUB_TOKEN="your_github_token_here"
```

Or create a token at: https://github.com/settings/tokens
- Select: `public_repo` scope

## Usage

### Basic Usage

```bash
python find_abandoned_projects.py
```

This will:
- Search for Python repos with 1,000+ stars
- Filter for repos with no commits in 365+ days
- Analyze up to 50 repositories
- Save results to `abandoned_projects.csv`

### Advanced Options

```bash
python find_abandoned_projects.py \
  --min-stars 5000 \
  --days-abandoned 730 \
  --max-results 100 \
  --output my_results.csv
```

### Command-Line Arguments

- `--token`: GitHub API token (alternative to GITHUB_TOKEN env var)
- `--min-stars`: Minimum star count (default: 1000)
- `--days-abandoned`: Minimum days since last commit (default: 365)
- `--max-results`: Maximum repositories to analyze (default: 50)
- `--output`: Output CSV filename (default: abandoned_projects.csv)

## Output Format

The script generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `name` | Repository name |
| `owner` | Repository owner |
| `url` | Repository URL |
| `stars` | Number of stars |
| `last_commit` | Date of last commit |
| `days_abandoned` | Days since last commit |
| `open_issues` | Number of open issues |
| `score` | Abandonment score (higher = better candidate) |
| `active_fork_name` | Name of most active fork (if found) |
| `active_fork_url` | URL of active fork |
| `active_fork_last_commit` | Last commit date of active fork |

## Scoring Algorithm

Projects are scored using:

```
Score = (stars / 1000) × (days_abandoned / 365) × (1 / (open_issues + 1))
```

This formula balances:
- **Popularity** (stars): More popular projects have higher impact
- **Abandonment** (days): Longer abandoned = more problematic
- **Maintenance burden** (issues): Fewer open issues = less maintenance needed

## Rate Limiting

- **Without token**: 60 requests/hour
- **With token**: 5,000 requests/hour

The script includes automatic rate limiting delays to be respectful of GitHub's API.

## Example Output

```
================================================================================
GitHub Abandoned Python Project Finder
================================================================================
Searching for Python repos with 1000+ stars...
Found 87 candidate repositories

Analyzing 1/50: tornadoweb/tornado
  Stars: 21,234
  Last commit: 542 days ago
  Open issues: 234
  Checking for active forks...
  No active forks found

...

Results saved to abandoned_projects.csv

================================================================================
Analysis complete! Found 50 abandoned projects

Top 5 candidates:
1. tornadoweb/tornado
   Stars: 21,234 | Abandoned: 542 days | Score: 3.45
2. pallets/flask
   Stars: 67,821 | Abandoned: 401 days | Score: 7.12
3. ...
```

## Tips

1. **Start small**: Use `--max-results 10` for testing
2. **Filter by category**: Modify the search query in the code to focus on ML, web frameworks, etc.
3. **Review manually**: The script finds candidates, but human judgment is needed for final selection
4. **Check forks carefully**: Active forks may not be true drop-in replacements

## Troubleshooting

### Rate Limiting Errors

If you hit rate limits:
1. Add a GitHub token
2. Reduce `--max-results`
3. Wait an hour for limits to reset

### No Results Found

Try adjusting parameters:
- Lower `--min-stars` to 500
- Reduce `--days-abandoned` to 180 (6 months)

## Contributing

To adapt this script for other languages:
1. Change `language:python` in the search query
2. Adjust scoring weights based on ecosystem characteristics
3. Update minimum star thresholds (JavaScript projects often have more stars)

## License

This script is part of the Abandoned Projects showcase website.
