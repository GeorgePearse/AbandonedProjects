#!/usr/bin/env python3
"""
Find abandoned Python projects on GitHub.

This script searches for popular Python repositories that have been abandoned
(no commits in 1+ year) and identifies potential maintained forks.
"""

import argparse
import csv
import json
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests


class GitHubAbandonedProjectFinder:
    """Find abandoned Python projects on GitHub."""

    def __init__(self, token: Optional[str] = None, min_stars: int = 1000,
                 days_abandoned: int = 365, max_results: int = 50):
        """
        Initialize the finder.

        Args:
            token: GitHub API token (optional, but recommended for higher rate limits)
            min_stars: Minimum number of stars
            days_abandoned: Minimum days since last commit to be considered abandoned
            max_results: Maximum number of results to return
        """
        self.token = token
        self.min_stars = min_stars
        self.days_abandoned = days_abandoned
        self.max_results = max_results
        self.session = requests.Session()

        if token:
            self.session.headers.update({
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        else:
            print("Warning: No GitHub token provided. Rate limits will be lower.")
            print("Set GITHUB_TOKEN environment variable or pass --token flag.")

    def search_abandoned_repos(self) -> List[Dict]:
        """Search for abandoned Python repositories."""
        print(f"Searching for Python repos with {self.min_stars}+ stars...")

        # Calculate date threshold
        threshold_date = datetime.now() - timedelta(days=self.days_abandoned)
        threshold_str = threshold_date.strftime('%Y-%m-%d')

        # GitHub search query
        query = (
            f"language:python stars:>={self.min_stars} "
            f"pushed:<{threshold_str} archived:false"
        )

        url = "https://api.github.com/search/repositories"
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': min(100, self.max_results)
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            repos = data.get('items', [])
            print(f"Found {len(repos)} candidate repositories")
            return repos

        except requests.RequestException as e:
            print(f"Error searching repositories: {e}")
            return []

    def get_repo_details(self, owner: str, repo: str) -> Dict:
        """Get detailed information about a repository."""
        url = f"https://api.github.com/repos/{owner}/{repo}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching {owner}/{repo}: {e}")
            return {}

    def get_last_commit_date(self, owner: str, repo: str) -> Optional[str]:
        """Get the date of the last commit."""
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {'per_page': 1}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            commits = response.json()

            if commits:
                return commits[0]['commit']['author']['date']
            return None
        except requests.RequestException as e:
            print(f"Error fetching commits for {owner}/{repo}: {e}")
            return None

    def find_active_forks(self, owner: str, repo: str, min_fork_stars: int = 100) -> Optional[Dict]:
        """Find the most active fork of a repository with minimum star threshold."""
        url = f"https://api.github.com/repos/{owner}/{repo}/forks"
        params = {
            'sort': 'newest',
            'per_page': 10  # Check top 10 forks
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            forks = response.json()

            # Find most recently updated fork with minimum stars
            active_forks = []
            cutoff_date = datetime.now() - timedelta(days=180)  # 6 months

            for fork in forks:
                pushed_at = datetime.strptime(
                    fork['pushed_at'], '%Y-%m-%dT%H:%M:%SZ'
                )

                # Filter by both activity and star count
                if pushed_at > cutoff_date and fork['stargazers_count'] >= min_fork_stars:
                    active_forks.append({
                        'name': fork['full_name'],
                        'url': fork['html_url'],
                        'last_commit': fork['pushed_at'],
                        'stars': fork['stargazers_count']
                    })

            # Return fork with most stars
            if active_forks:
                return max(active_forks, key=lambda x: x['stars'])

            return None

        except requests.RequestException as e:
            print(f"Error fetching forks for {owner}/{repo}: {e}")
            return None

    def calculate_score(self, stars: int, days_since_commit: int,
                       open_issues: int) -> float:
        """
        Calculate abandonment score.

        Higher score = better candidate for featuring.

        Args:
            stars: Number of stars
            days_since_commit: Days since last commit
            open_issues: Number of open issues

        Returns:
            Score value
        """
        # Normalize values
        star_factor = stars / 1000
        abandonment_factor = days_since_commit / 365
        issue_factor = 1 / (open_issues + 1)  # Fewer issues = higher score

        return star_factor * abandonment_factor * issue_factor

    def analyze_repositories(self, repos: List[Dict]) -> List[Dict]:
        """Analyze repositories and collect detailed information."""
        results = []

        for i, repo in enumerate(repos, 1):
            print(f"\nAnalyzing {i}/{len(repos)}: {repo['full_name']}")

            owner = repo['owner']['login']
            name = repo['name']

            # Get last commit date
            last_commit = self.get_last_commit_date(owner, name)
            if not last_commit:
                print(f"  Skipping (no commits found)")
                continue

            # Calculate days since last commit
            last_commit_dt = datetime.strptime(last_commit, '%Y-%m-%dT%H:%M:%SZ')
            days_since = (datetime.now() - last_commit_dt).days

            print(f"  Stars: {repo['stargazers_count']:,}")
            print(f"  Last commit: {days_since} days ago")
            print(f"  Open issues: {repo['open_issues_count']}")

            # Find active forks
            print(f"  Checking for active forks...")
            active_fork = self.find_active_forks(owner, name)

            if active_fork:
                print(f"  Found active fork: {active_fork['name']}")
            else:
                print(f"  No active forks found")

            # Calculate score
            score = self.calculate_score(
                repo['stargazers_count'],
                days_since,
                repo['open_issues_count']
            )

            result = {
                'name': name,
                'owner': owner,
                'url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'last_commit': last_commit_dt.strftime('%Y-%m-%d'),
                'days_abandoned': days_since,
                'open_issues': repo['open_issues_count'],
                'score': round(score, 2),
                'active_fork_name': active_fork['name'] if active_fork else '',
                'active_fork_url': active_fork['url'] if active_fork else '',
                'active_fork_stars': active_fork['stars'] if active_fork else '',
                'active_fork_last_commit': active_fork['last_commit'][:10] if active_fork else ''
            }

            results.append(result)

            # Rate limiting
            time.sleep(0.5)  # Be nice to GitHub API

        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def save_to_csv(self, results: List[Dict], filename: str):
        """Save results to CSV file."""
        if not results:
            print("No results to save")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'name', 'owner', 'url', 'stars', 'last_commit',
                'days_abandoned', 'open_issues', 'score',
                'active_fork_name', 'active_fork_url', 'active_fork_stars', 'active_fork_last_commit'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nResults saved to {filename}")

    def run(self, output_file: str = 'abandoned_projects.csv'):
        """Run the analysis."""
        print("=" * 60)
        print("GitHub Abandoned Python Project Finder")
        print("=" * 60)

        # Search for repos
        repos = self.search_abandoned_repos()

        if not repos:
            print("No repositories found")
            return

        # Analyze repos
        results = self.analyze_repositories(repos[:self.max_results])

        # Save results
        self.save_to_csv(results, output_file)

        # Print summary
        print("\n" + "=" * 60)
        print(f"Analysis complete! Found {len(results)} abandoned projects")
        print("\nTop 5 candidates:")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result['owner']}/{result['name']}")
            print(f"   Stars: {result['stars']:,} | "
                  f"Abandoned: {result['days_abandoned']} days | "
                  f"Score: {result['score']}")
            if result['active_fork_name']:
                print(f"   Active fork: {result['active_fork_name']}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Find abandoned Python projects on GitHub'
    )
    parser.add_argument(
        '--token',
        help='GitHub API token (or set GITHUB_TOKEN env var)'
    )
    parser.add_argument(
        '--min-stars',
        type=int,
        default=1000,
        help='Minimum stars (default: 1000)'
    )
    parser.add_argument(
        '--days-abandoned',
        type=int,
        default=365,
        help='Minimum days since last commit (default: 365)'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=50,
        help='Maximum number of results (default: 50)'
    )
    parser.add_argument(
        '--output',
        default='abandoned_projects.csv',
        help='Output CSV file (default: abandoned_projects.csv)'
    )

    args = parser.parse_args()

    # Get token from args or environment
    import os
    token = args.token or os.getenv('GITHUB_TOKEN')

    # Create finder and run
    finder = GitHubAbandonedProjectFinder(
        token=token,
        min_stars=args.min_stars,
        days_abandoned=args.days_abandoned,
        max_results=args.max_results
    )

    finder.run(args.output)


if __name__ == '__main__':
    main()
