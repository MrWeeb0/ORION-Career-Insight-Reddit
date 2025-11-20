# Contributing to Engineering Career Insights

Thank you for your interest in contributing! We welcome contributions from everyone.

## Code of Conduct

Be respectful and inclusive. We're building this for students and the engineering community.

## How to Contribute

### Reporting Bugs

1. Check if the bug already exists in Issues
2. Open a new issue with:
   - Clear title describing the problem
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Suggesting Enhancements

1. Open a new issue with `[FEATURE]` in the title
2. Describe what you'd like to add and why
3. Provide examples if applicable

### Submitting Code

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/engineering-career-insights.git
cd engineering-career-insights
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow PEP 8 style guide
   - Add comments for complex logic
   - Test your changes

4. **Commit with clear messages**
```bash
git commit -m "Add feature: description of change"
```

5. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request**
   - Reference any related issues
   - Describe your changes
   - Explain why this change is needed

## Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/engineering-career-insights.git
cd engineering-career-insights

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test your changes
python main.py
```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

## Testing

Before submitting a PR:
1. Test the main.py script
2. Verify PDF generation works
3. Check JSON output is valid
4. Test with different search terms

## Areas for Contribution

- 🐛 Bug fixes
- ✨ New features (multi-subreddit, exports, etc.)
- 📚 Documentation improvements
- 🧪 Better error handling
- 💾 Database integration
- 🎨 UI/web dashboard
- 📊 Data visualization

## Questions?

- Open a discussion issue
- Check existing documentation
- Review other PRs for context

Thank you for making this project better! 🚀
