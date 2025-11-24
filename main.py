import requests
import json
import time
import sys
import os
import argparse
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fix console encoding for emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Reddit API Configuration
USER_AGENT = "Mozilla/5.0 (compatible; EngineerPath/1.0; +http://localhost)"

# Load defaults from environment variables
DEFAULT_SUBREDDIT = os.getenv("SUBREDDIT", "engineering")
DEFAULT_SEARCH_TERM = os.getenv("SEARCH_TERM", "Career")
DEFAULT_LIMIT = int(os.getenv("POSTS_LIMIT", "100"))
DEFAULT_OUTPUT_DIR = os.getenv("OUTPUT_DIR", "Data")

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

def search_subreddit(subreddit, search_term, limit=100):
    """Search subreddit for a term"""
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {
        "q": search_term,
        "restrict_sr": 1,
        "sort": "relevance",
        "limit": limit,
        "raw_json": 1
    }
    return fetch_with_rate_limit(url, params)

def get_top_comment(subreddit, post_id):
    """Get top comment for a post"""
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
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

def format_for_students(posts, subreddit):
    """Format posts into student-friendly career insights"""
    formatted = ""
    formatted += "\n" + "="*100 + "\n"
    formatted += f"🎓 CAREER INSIGHTS - From r/{subreddit} Community\n"
    formatted += "="*100 + "\n"
    formatted += f"📊 Total Posts Analyzed: {len(posts)}\n"
    formatted += f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    formatted += f"\n💡 GOAL: Provide career guidance for students\n"
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
            top_comment = get_top_comment(subreddit, post_id)
            if top_comment:
                formatted += f"\n💬 TOP INSIGHT FROM COMMUNITY:\n"
                formatted += f"   By u/{top_comment['author']} (⬆️ {top_comment['score']} upvotes)\n"
                formatted += f"   \"{top_comment['body']}\"\n"
        
        formatted += "\n"
    
    # Summary section
    formatted += "\n" + "="*100 + "\n"
    formatted += "📚 KEY TAKEAWAYS\n"
    formatted += "="*100 + "\n\n"
    formatted += "1️⃣  CAREER GROWTH: Browse discussions about career transitions, skill development, and industry insights.\n"
    formatted += "2️⃣  SALARY EXPECTATIONS: Find real-world salary ranges and compensation discussions.\n"
    formatted += "3️⃣  WORK-LIFE BALANCE: Read experiences about job satisfaction and workplace culture.\n"
    formatted += "4️⃣  FIELD-SPECIFIC ADVICE: Learn from professionals in various specializations.\n"
    formatted += "5️⃣  DECISION-MAKING: Get insights to help decide your career path.\n\n"
    formatted += "🎯 ACTION ITEMS:\n"
    formatted += "   ✓ Visit the full discussion threads (links above) for more detailed conversations\n"
    formatted += "   ✓ Ask follow-up questions in the community threads\n"
    formatted += "   ✓ Connect with professionals in your field of interest\n"
    formatted += "   ✓ Use these insights to plan your career development\n\n"
    formatted += "="*100 + "\n"
    
    return formatted

def main():
    """Main execution with command-line argument support"""
    parser = argparse.ArgumentParser(description="Scrape Reddit for career-related posts")
    parser.add_argument("--subreddit", type=str, default=DEFAULT_SUBREDDIT, 
                       help=f"Subreddit to search (default: {DEFAULT_SUBREDDIT})")
    parser.add_argument("--search", type=str, default=DEFAULT_SEARCH_TERM, 
                       help=f"Search term (default: {DEFAULT_SEARCH_TERM})")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                       help=f"Maximum posts to fetch (default: {DEFAULT_LIMIT})")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_OUTPUT_DIR,
                       help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--no-pdf", action="store_true",
                       help="Skip PDF generation (only scrape)")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Create subdirectories for organizing outputs
    json_dir = os.path.join(args.output_dir, "json")
    txt_dir = os.path.join(args.output_dir, "txt")
    pdf_dir = os.path.join(args.output_dir, "pdf")
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print(f"REDDIT SCRAPER: Searching r/{args.subreddit} for '{args.search}'")
    print("="*80 + "\n")
    
    # Search for posts
    search_results = search_subreddit(args.subreddit, args.search, args.limit)
    if not search_results:
        print("❌ Failed to fetch search results")
        sys.exit(1)
    
    posts = search_results.get("data", {}).get("children", [])
    print(f"✓ Found {len(posts)} posts\n")
    
    # Format for students
    formatted_output = format_for_students(posts, args.subreddit)
    print(formatted_output)
    
    # Save results in organized subdirectories
    json_file = os.path.join(json_dir, f"{args.subreddit}_posts.json")
    txt_file = os.path.join(txt_dir, f"{args.subreddit}_posts.txt")
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(formatted_output)
    
    print(f"✓ Results saved to {json_file} and {txt_file}")
    
    # Generate PDF automatically (unless skipped)
    if not args.no_pdf:
        print("\n" + "="*80)
        print("GENERATING PDF...")
        print("="*80 + "\n")
        
        try:
            pdf_script = os.path.join(args.output_dir, "generate_career_pdf.py")
            subprocess.run(
                [sys.executable, pdf_script, "--subreddit", args.subreddit, 
                 "--input", json_file, "--output-dir", pdf_dir],
                check=True,
                capture_output=False
            )
            print("\n✓ Pipeline complete! All files generated.")
        except subprocess.CalledProcessError as e:
            print(f"\n⚠️ Warning: PDF generation failed: {e}")
            print("You can manually generate the PDF with:")
            print(f"  python Data/generate_career_pdf.py --subreddit {args.subreddit}")
        except FileNotFoundError:
            print(f"\n⚠️ Warning: PDF script not found at {pdf_script}")
            print("You can manually generate the PDF with:")
            print(f"  python Data/generate_career_pdf.py --subreddit {args.subreddit}")

if __name__ == "__main__":
    main()
