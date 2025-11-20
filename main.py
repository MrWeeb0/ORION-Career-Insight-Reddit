import requests
import json
import time
import sys
from datetime import datetime

# Fix console encoding for emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Reddit API Configuration
USER_AGENT = "Mozilla/5.0 (compatible; EngineerPath/1.0; +http://localhost)"
SUBREDDIT = "askengineers"
SEARCH_TERM = "Career"

def fetch_with_rate_limit(url, params=None):
    """Fetch URL with rate limiting and error handling"""
    headers = {"User-Agent": USER_AGENT}
    try:
        print(f"[REQUEST] GET {url}")
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        
        # Check for rate limiting
        if resp.status_code == 429:
            print("⚠️ WARNING: Rate limited (429). Exiting.")
            sys.exit(1)
        
        resp.raise_for_status()
        time.sleep(2)  # Reddit API rate limit safety
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def search_subreddit(search_term, limit=100):
    """Search subreddit for a term"""
    url = f"https://www.reddit.com/r/{SUBREDDIT}/search.json"
    params = {
        "q": search_term,
        "restrict_sr": 1,
        "sort": "relevance",
        "limit": limit,
        "raw_json": 1
    }
    return fetch_with_rate_limit(url, params)

def get_top_comment(post_id):
    """Get top comment for a post"""
    url = f"https://www.reddit.com/r/{SUBREDDIT}/comments/{post_id}.json"
    params = {"raw_json": 1, "limit": 1}
    data = fetch_with_rate_limit(url, params)
    
    if data and len(data) > 1:
        comments = data[1].get("data", {}).get("children", [])
        if comments:
            comment_data = comments[0].get("data", {})
            return {
                "author": comment_data.get("author", "N/A"),
                "body": comment_data.get("body", "")[:200],
                "score": comment_data.get("score", 0)
            }
    return None

def format_for_students(posts):
    """Format posts into student-friendly career insights"""
    formatted = ""
    formatted += "\n" + "="*100 + "\n"
    formatted += "🎓 ENGINEERING CAREER INSIGHTS - From r/AskEngineers Community\n"
    formatted += "="*100 + "\n"
    formatted += f"📊 Total Posts Analyzed: {len(posts)}\n"
    formatted += f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    formatted += f"\n💡 GOAL: Provide career guidance for engineering students\n"
    formatted += "="*100 + "\n\n"
    
    for i, post_wrapper in enumerate(posts[:30], 1):  # Top 30 posts for readability
        post = post_wrapper.get("data", {})
        title = post.get("title", "N/A")
        url = f"https://reddit.com{post.get('permalink', '')}"
        selftext = post.get("selftext", "")
        author = post.get("author", "N/A")
        score = post.get("score", 0)
        comments = post.get("num_comments", 0)
        created = datetime.fromtimestamp(post.get("created_utc", 0)).strftime('%b %d, %Y')
        post_id = post.get("id", "N/A")
        
        # Header
        formatted += f"\n{'─'*100}\n"
        formatted += f"📌 INSIGHT #{i}: {title}\n"
        formatted += f"{'─'*100}\n\n"
        
        # Metadata
        formatted += f"👤 Posted by: u/{author}\n"
        formatted += f"📈 Engagement: {score:,} upvotes | {comments:,} comments\n"
        formatted += f"📅 Date: {created}\n"
        formatted += f"🔗 Link: {url}\n\n"
        
        # Content
        if selftext:
            # Extract key insights
            lines = selftext.split('\n')
            summary = '\n'.join(lines[:5])  # First 5 lines as preview
            formatted += f"📝 DISCUSSION:\n"
            formatted += f"{summary}\n"
            if len(selftext) > 300:
                formatted += f"\n[...more content available at link above...]\n"
        
        # Top comment (for first 10 posts)
        if i <= 10:
            top_comment = get_top_comment(post_id)
            if top_comment:
                formatted += f"\n💬 TOP INSIGHT FROM COMMUNITY:\n"
                formatted += f"   By u/{top_comment['author']} (⬆️ {top_comment['score']} upvotes)\n"
                formatted += f"   \"{top_comment['body']}\"\n"
        
        formatted += "\n"
    
    # Summary section
    formatted += "\n" + "="*100 + "\n"
    formatted += "📚 STUDENT TAKEAWAYS\n"
    formatted += "="*100 + "\n\n"
    formatted += "1️⃣  CAREER GROWTH: Browse discussions about career transitions, skill development, and industry insights.\n"
    formatted += "2️⃣  SALARY EXPECTATIONS: Find real-world salary ranges and compensation discussions from practicing engineers.\n"
    formatted += "3️⃣  WORK-LIFE BALANCE: Read experiences about job satisfaction, workplace culture, and career satisfaction.\n"
    formatted += "4️⃣  FIELD-SPECIFIC ADVICE: Learn from engineers in various specializations (ME, EE, Civil, etc).\n"
    formatted += "5️⃣  DECISION-MAKING: Get insights to help decide your career path and specialization.\n\n"
    formatted += "🎯 ACTION ITEMS FOR STUDENTS:\n"
    formatted += "   ✓ Visit the full discussion threads (links above) for more detailed conversations\n"
    formatted += "   ✓ Ask follow-up questions in the community threads\n"
    formatted += "   ✓ Connect with engineers in your field of interest\n"
    formatted += "   ✓ Use these insights to plan your internships and specializations\n\n"
    formatted += "="*100 + "\n"
    
    return formatted

# Main execution
print("\n" + "="*80)
print(f"REDDIT SCRAPER: Searching r/{SUBREDDIT} for '{SEARCH_TERM}'")
print("="*80 + "\n")

# Search for posts
search_results = search_subreddit(SEARCH_TERM)
if not search_results:
    print("❌ Failed to fetch search results")
    sys.exit(1)

posts = search_results.get("data", {}).get("children", [])
print(f"✓ Found {len(posts)} posts\n")

# Format for students
formatted_output = format_for_students(posts)
print(formatted_output)

# Save results
with open("Data/reddit_posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

with open("Data/reddit_posts.txt", "w", encoding="utf-8") as f:
    f.write(formatted_output)

print("✓ Results saved to Data/reddit_posts.json and Data/reddit_posts.txt")
