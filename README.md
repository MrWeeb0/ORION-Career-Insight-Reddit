# Engineering Career Insights Scraper

A Python tool that scrapes Reddit's r/AskEngineers subreddit for career-related discussions and generates beautifully formatted documents for engineering students.

## 🎯 Goal

Provide real-world career guidance and insights for engineering students by aggregating discussions, salary expectations, and work-life balance perspectives from practicing engineers.

## ✨ Features

- **Reddit API Scraping**: Fetches career-related posts from r/AskEngineers with proper rate limiting
- **Smart Categorization**: Organizes posts into 5 thematic chapters:
  1. The Transition (Student to Engineer)
  2. Expectations vs. Reality
  3. Career Strategy & Growth
  4. Workplace Dynamics & Ethics
  5. General Discussions & Advice
- **Multi-Format Output**:
  - 📄 **PDF**: Professional document with formatted chapters
  - 📝 **Text**: Human-readable formatted insights
  - 📊 **JSON**: Raw data for further analysis
- **Community Insights**: Extracts top comments from discussions
- **Rate Limiting**: Respects Reddit API limits with 2-second delays

## 📋 Prerequisites

- Python 3.8+
- Virtual Environment (recommended)
- Internet connection for Reddit scraping

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/engineering-career-insights.git
cd engineering-career-insights
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 💻 Usage

### 1. Scrape Reddit and Generate Insights

```bash
python main.py
```

This will:
- Search r/AskEngineers for "Career" keyword
- Fetch 100 relevant posts
- Extract top comments from top 10 posts
- Generate formatted output files

**Output files:**
- `Data/reddit_posts.json` - Raw post data
- `Data/reddit_posts.txt` - Formatted student insights
- `Data/Career_Insights_for_Students.pdf` - Professional PDF document

### 2. Generate PDF from JSON

```bash
python Data/generate_career_pdf.py
```

This converts the JSON data into a formatted PDF with chapters and styling.

## 📊 Output Format

### PDF Structure
- **Cover Page**: Title and description
- **5 Chapters**: Organized by career theme
- **Post Entries**: Title, author, content, community insights
- **Professional Styling**: Colors, typography, spacing

### JSON Format
```json
[
  {
    "title": "Post Title",
    "author": "username",
    "score": 372,
    "num_comments": 527,
    "selftext": "Post content...",
    "permalink": "/r/AskEngineers/comments/...",
    "created_utc": 1656432191
  }
]
```

### Text Format
```
📌 INSIGHT #1: Career Discussion Title
────────────────────────────────────
👤 Posted by: u/author
📈 Engagement: 372 upvotes | 527 comments
📅 Date: Jun 28, 2022
🔗 Link: https://reddit.com/r/AskEngineers/...

💬 TOP INSIGHT FROM COMMUNITY:
   By u/top_commenter (⬆️ 558 upvotes)
   "Comment text..."
```

## 🔧 Configuration

Edit these variables in `main.py` to customize:

```python
USER_AGENT = "Mozilla/5.0 (compatible; YourApp/1.0; +http://yoursite)"
SUBREDDIT = "askengineers"
SEARCH_TERM = "Career"
```

## 📚 API Details

This project respects Reddit API guidelines:
- ✅ Uses `User-Agent` header (mandatory)
- ✅ Appends `.json` to endpoints
- ✅ Uses `raw_json=1` to avoid HTML entity encoding
- ✅ Implements 2-second delays between requests
- ✅ Handles 429 rate limit errors gracefully
- ✅ Uses `restrict_sr=1` for subreddit-only searches

## 📝 Student Takeaways

The generated documents provide insights on:

1. **Career Growth**: Transitions, skill development, industry paths
2. **Salary Expectations**: Real-world compensation data
3. **Work-Life Balance**: Job satisfaction, workplace culture
4. **Field-Specific Advice**: Specialization insights
5. **Decision-Making**: Help choosing career paths

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool uses the Reddit API to aggregate public discussions. Please ensure you:
- Comply with Reddit's Terms of Service
- Respect the community and discussions
- Use data responsibly and ethically
- Don't spam or abuse the API

## 🐛 Issues & Bug Reports

Found a bug? Please open an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)

## 📧 Contact & Support

For questions or support:
- Open an issue on GitHub
- Check existing discussions
- Review the documentation

## 🎓 Educational Use

This project is designed for educational purposes. Students can:
- Learn about real-world engineering careers
- Understand industry expectations
- Make informed career decisions
- Connect with experienced engineers

## 📊 Data Sources

All data is aggregated from public discussions on [r/AskEngineers](https://www.reddit.com/r/AskEngineers/), a community of engineers sharing career and technical insights.

## 🔮 Future Enhancements

- [ ] Multi-subreddit support
- [ ] Interactive web dashboard
- [ ] Custom keyword searches
- [ ] Time-based trend analysis
- [ ] Career path recommendations
- [ ] Salary trend visualization
- [ ] Export to Excel/CSV
- [ ] PostgreSQL database integration

---

**Made with ❤️ for engineering students by the community**
