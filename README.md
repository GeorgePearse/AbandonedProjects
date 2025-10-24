# ⚠️ Abandoned Projects

> A curated showcase of unmaintained GitHub projects that pose security risks and package compatibility issues

[![Live Site](https://img.shields.io/badge/Live-Site-blue)](https://georgepearse.github.io/AbandonedProjects/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/GeorgePearse/AbandonedProjects)

## 🎯 Purpose

This project highlights popular open-source packages that have been abandoned, deprecated, or left unmaintained. When developers continue to use these packages, they expose their projects to:

- **Security vulnerabilities** - No patches for newly discovered exploits
- **Compatibility issues** - Breaking changes with modern tooling and dependencies
- **Technical debt** - Harder to maintain and migrate away from over time
- **Supply chain risks** - Potential targets for malicious takeovers

## 🚀 Features

- **Visual Card Layout** - Easy-to-scan cards displaying project information
- **Last Commit Tracking** - Shows how long each project has been abandoned
- **Risk Assessment** - Explains why each abandoned project matters
- **GitHub Integration** - Direct links to repositories with star counts
- **Dark/Light Mode** - Automatic theme based on system preferences
- **Responsive Design** - Works seamlessly on mobile and desktop

## 📊 What's Tracked

Each project card displays:

- **Project name** and GitHub repository
- **Star count** - Popularity indicator
- **Last commit date** - When maintainers stopped work
- **Description** - What the package does
- **Risk explanation** - Why abandonment matters

## 🗂️ Featured Abandoned Projects

The site currently tracks notable projects including:

- **request** - 16M+ weekly downloads, deprecated since 2020
- **moment.js** - 47K+ stars, officially in maintenance mode
- **node-sass** - Deprecated in favor of Dart Sass
- **colors.js** - Sabotaged by maintainer with infinite loop
- **bower** - Deprecated package manager
- And more...

## 🛠️ Technology Stack

- **[Astro](https://astro.build)** - Modern static site generator
- **TypeScript** - Type-safe development
- **JSON Data** - Easy-to-update project list
- **GitHub Pages** - Free hosting with GitHub Actions deployment

## 📁 Project Structure

```
abandoned-projects/
├── src/
│   ├── components/
│   │   └── ProjectCard.astro   # Reusable project card component
│   ├── data/
│   │   └── projects.json       # List of abandoned projects
│   └── pages/
│       └── index.astro          # Main homepage
├── astro.config.mjs             # Astro configuration
└── package.json                 # Dependencies
```

## 🚦 Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or pnpm

### Installation

```bash
# Clone the repository
git clone https://github.com/GeorgePearse/AbandonedProjects.git

# Navigate to the project
cd AbandonedProjects/abandoned-projects

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit `http://localhost:4321` to see the site locally.

### Building for Production

```bash
npm run build
```

The static files will be in the `dist/` folder.

## ➕ Adding Projects

To add a new abandoned project, edit `src/data/projects.json`:

```json
{
  "name": "project-name",
  "repo": "owner/repo",
  "url": "https://github.com/owner/repo",
  "description": "Brief description of the project",
  "lastCommit": "YYYY-MM-DD",
  "stars": 12345,
  "reason": "Explanation of why this abandonment matters"
}
```

## 🤝 Contributing

Contributions are welcome! To suggest an abandoned project:

1. Fork the repository
2. Add the project to `src/data/projects.json`
3. Ensure it meets the criteria:
   - Officially deprecated OR no commits in 2+ years
   - Has significant usage/downloads
   - Poses security or compatibility risks
4. Submit a pull request

## 📝 Criteria for Inclusion

Projects should meet at least one of these criteria:

- Officially deprecated by maintainers
- No security updates in 2+ years
- Known to cause compatibility issues with modern tools
- Has significant usage despite abandonment
- Historical significance (e.g., caused ecosystem disruption)

## ⚖️ License

This project is open source. The code is available under the MIT License.

## 🙏 Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code)
- Inspired by the need for transparency in open-source dependency health
- Data sourced from GitHub and npm registry

## 🔗 Links

- **Live Site**: https://georgepearse.github.io/AbandonedProjects/
- **GitHub**: https://github.com/GeorgePearse/AbandonedProjects
- **Report Issues**: https://github.com/GeorgePearse/AbandonedProjects/issues

---

**Note**: This site is for educational purposes to raise awareness about dependency maintenance. Always check the current status of packages before making decisions about their use.
