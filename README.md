# Career Insights Scraper

A flexible Python tool that scrapes Reddit for career-related discussions and generates beautifully formatted documents for students and professionals. Support for any subreddit!

## 🎯 Goal

Provide real-world career guidance and insights by aggregating discussions, salary expectations, and work-life balance perspectives from Reddit communities.

## ✨ Features

- **Flexible Multi-Subreddit Support**: Scrape any subreddit for career insights
- **Reddit API Scraping**: Fetches career-related posts with proper rate limiting
- **Smart Categorization**: Organizes posts into 5 thematic chapters:
  1. The Transition (Student/Entry-Level)
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
- **Environment Configuration**: Customizable via `.env` file

## 📋 Prerequisites

- Python 3.8+
- Virtual Environment (recommended)
- Internet connection for Reddit scraping

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/MrWeeb0/Career-Insight-Reddit.git
cd Career-Insight-Reddit
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

4. **Configure environment**
```bash
# Copy example file
cp .env.example .env

# Edit .env with your preferred settings
```

## 💻 Usage

### Quick Start (Default: r/engineering)

```bash
python main.py
```

This runs a complete pipeline:
1. Scrapes r/engineering for "Career" posts
2. Generates JSON, text, and PDF files automatically

### Scrape Different Subreddits

```bash
# Scrape r/learnprogramming (with automatic PDF generation)
python main.py --subreddit learnprogramming

# Scrape r/askengineers with custom search term
python main.py --subreddit askengineers --search "salary"

# Scrape with custom limit
python main.py --subreddit engineering --limit 200

# Custom output directory
python main.py --subreddit engineering --output-dir MyData
```

### Scraping Only (Skip PDF Generation)

```bash
# Scrape without generating PDF
python main.py --no-pdf

# Useful for quick data collection
python main.py --subreddit engineering --no-pdf
```

### Standalone PDF Generation

If you need to regenerate PDFs without scraping:

```bash
# Generate PDF from existing data
python Data/generate_career_pdf.py --subreddit learnprogramming

# Custom input/output files
python Data/generate_career_pdf.py --subreddit engineering --input Data/custom_posts.json --output Data/output.pdf
```

## ⚙️ Configuration

### Environment File (.env)

Create a `.env` file (copy from `.env.example`):

```env
# Reddit Scraper Configuration
SUBREDDIT=engineering
SEARCH_TERM=Career
POSTS_LIMIT=100
OUTPUT_DIR=Data
```

**Configuration Options:**
- `SUBREDDIT`: Default subreddit to scrape (without r/ prefix)
- `SEARCH_TERM`: Default search keyword
- `POSTS_LIMIT`: Maximum posts to fetch
- `OUTPUT_DIR`: Output directory for files

### Command-Line Arguments

All `.env` defaults can be overridden via command-line:

```bash
# Override environment settings
python main.py --subreddit learnprogramming --search "career" --limit 50

# PDF generation with custom settings
python Data/generate_career_pdf.py --subreddit learnprogramming
```

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
    "permalink": "/r/subreddit/comments/...",
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
🔗 Link: https://reddit.com/r/subreddit/...

💬 TOP INSIGHT FROM COMMUNITY:
   By u/top_commenter (⬆️ 558 upvotes)
   "Comment text..."
```

## 📁 Output Files

Scripts organize outputs into type-specific subdirectories:

```
Data/
├── pdf/
│   ├── Career_Insights_Engineering.pdf
│   ├── Career_Insights_Learnprogramming.pdf
│   └── Career_Insights_Cscareerquestions.pdf
├── json/
│   ├── engineering_posts.json
│   ├── learnprogramming_posts.json
│   └── cscareerquestions_posts.json
├── txt/
│   ├── engineering_posts.txt
│   ├── learnprogramming_posts.txt
│   └── cscareerquestions_posts.txt
└── generate_career_pdf.py
```

**All files are organized by type:**
- **pdf/**: Professional documents with categorized chapters
- **json/**: Raw post data for analysis
- **txt/**: Formatted human-readable insights

## 📚 API Details

This project respects Reddit API guidelines:
- ✅ Uses `User-Agent` header (mandatory)
- ✅ Appends `.json` to endpoints
- ✅ Uses `raw_json=1` to avoid HTML entity encoding
- ✅ Implements 2-second delays between requests
- ✅ Handles 429 rate limit errors gracefully
- ✅ Uses `restrict_sr=1` for subreddit-only searches

## 💡 Example Workflows

### Complete Pipeline: Scrape & Generate PDF

```bash
# Engineering career insights (scrapes + generates PDF)
python main.py --subreddit engineering

# Software development careers
python main.py --subreddit learnprogramming

# Programming careers
python main.py --subreddit cscareerquestions
```

### Scrape Multiple Subreddits in Batch

```bash
# Scrape all without generating PDFs first
python main.py --subreddit engineering --no-pdf
python main.py --subreddit learnprogramming --no-pdf
python main.py --subreddit cscareerquestions --no-pdf

# Then generate all PDFs manually
python Data/generate_career_pdf.py --subreddit engineering
python Data/generate_career_pdf.py --subreddit learnprogramming
python Data/generate_career_pdf.py --subreddit cscareerquestions
```

### Custom Search Across Subreddits

```bash
# Complete pipeline with custom search terms
python main.py --subreddit engineering --search "salary negotiation"
python main.py --subreddit engineering --search "work life balance"
```

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

This project is designed for educational purposes. Users can:
- Learn about real-world career insights
- Understand industry expectations
- Make informed career decisions
- Compare career paths across fields

## 📊 Supported Subreddits

Works with any subreddit! Some popular options:
- `engineering` - Engineering careers and insights
- `askengineers` - Engineering Q&A
- `learnprogramming` - Programming education
- `cscareerquestions` - Computer science careers
- `webdev` - Web development careers
- `Python` - Python development
- `java` - Java development
- And many more!

## 🔮 Future Enhancements

- [ ] Interactive web dashboard
- [ ] Time-based trend analysis
- [ ] Career path recommendations
- [ ] Salary trend visualization
- [ ] Export to Excel/CSV
- [ ] Database integration
- [ ] Advanced filtering options
- [ ] Sentiment analysis

---

**Made with ❤️ for career explorers and students**

