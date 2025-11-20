import json
import re
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, 'reddit_posts.json')
OUTPUT_PDF = os.path.join(SCRIPT_DIR, 'Career_Insights_for_Students.pdf')

def clean_text(text):
    """Cleans up Reddit Markdown/HTML artifacts."""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove common Reddit artifacts
    text = text.replace('', '').replace('', '')
    text = text.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    return text.strip()

def get_category(title, text):
    """Categorizes posts based on keywords."""
    content = (title + " " + text).lower()
    
    categories = {
        "Chapter 1: The Transition (Student to Engineer)": [
            "student", "grad", "degree", "knowledge", "first job", "early career", 
            "imposter", "stagnat", "learn", "university", "college"
        ],
        "Chapter 2: Expectations vs. Reality": [
            "reality", "boring", "bored", "hate", "depress", "autocad", "paperwork", 
            "square pipe", "day in the life", "expect", "bad"
        ],
        "Chapter 3: Career Strategy & Growth": [
            "promotion", "mba", "salary", "raise", "consulting", "career path", 
            "pigeonhole", "industry", "future", "manager"
        ],
        "Chapter 4: Workplace Dynamics & Ethics": [
            "boss", "holiday", "politics", "ethics", "pinto", "communication", 
            "skill", "soft skill", "management", "respect", "fired"
        ]
    }
    
    for cat, keywords in categories.items():
        if any(k in content for k in keywords):
            return cat
            
    return "Chapter 5: General Discussions & Advice"

def create_pdf():
    # Load Data
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Please ensure the JSON file is in the same directory.")
        return

    # Setup PDF Document
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], fontSize=24, spaceAfter=20, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='CoverSub', parent=styles['Heading2'], alignment=TA_CENTER, fontSize=14, textColor=colors.gray))
    styles.add(ParagraphStyle(name='ChapterHeader', parent=styles['Heading1'], fontSize=18, spaceAfter=12, spaceBefore=20, textColor=colors.teal))
    styles.add(ParagraphStyle(name='PostTitle', parent=styles['Heading3'], fontSize=12, spaceBefore=10, spaceAfter=4, textColor=colors.black))
    styles.add(ParagraphStyle(name='PostMeta', parent=styles['Normal'], fontSize=8, textColor=colors.grey, spaceAfter=8))
    styles.add(ParagraphStyle(name='PostBody', parent=styles['Normal'], fontSize=10, leading=14, alignment=TA_JUSTIFY))

    story = []

    # --- Cover Page ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("Career Insight for Students", styles['CoverTitle']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Real-World Stories & Advice from r/AskEngineers", styles['CoverSub']))
    story.append(Spacer(1, 50))
    story.append(Paragraph("Generated from user discussions regarding career paths, workplace ethics, and engineering reality.", styles['Normal']))
    story.append(PageBreak())

    # --- Process Data ---
    categorized_content = {}
    
    for entry in raw_data:
        # Handle both formats: direct data dict or wrapped in kind/data
        if isinstance(entry, dict) and 'kind' in entry:
            if entry.get('kind') != 't3': 
                continue
            data = entry.get('data', {})
        else:
            # Direct data dict format
            data = entry
        
        # Skip AutoModerator "Career Monday" threads as they are usually empty prompts
        if data.get('author') == 'AutoModerator':
            continue

        title = data.get('title', 'Untitled')
        raw_selftext = data.get('selftext', '')
        author = data.get('author', 'Anonymous')
        
        # Clean text
        clean_body = clean_text(raw_selftext)
        
        # Skip empty posts
        if not clean_body and len(title) < 10:
            continue

        # Categorize
        category = get_category(title, clean_body)
        if category not in categorized_content:
            categorized_content[category] = []
        
        categorized_content[category].append({
            'title': title,
            'author': author,
            'body': clean_body
        })

    # --- Build Content ---
    # Sort categories to ensure chapters 1-4 appear in order
    sorted_categories = sorted(categorized_content.keys())

    for cat in sorted_categories:
        posts = categorized_content[cat]
        
        # Chapter Header
        story.append(Paragraph(cat, styles['ChapterHeader']))
        story.append(Spacer(1, 10))
        
        for post in posts:
            # Post Title
            story.append(Paragraph(post['title'], styles['PostTitle']))
            # Author Meta
            story.append(Paragraph(f"Posted by u/{post['author']}", styles['PostMeta']))
            
            # Post Body (Handle paragraphs)
            if post['body']:
                for para in post['body'].split('\n'):
                    if para.strip():
                        story.append(Paragraph(para.strip(), styles['PostBody']))
                        story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("*(No text content - Discussion Thread)*", styles['PostMeta']))
            
            # Divider
            story.append(Spacer(1, 15))
            story.append(Paragraph("_" * 50, styles['Normal']))
            story.append(Spacer(1, 15))
            
        story.append(PageBreak())

    # Generate
    try:
        doc.build(story)
        print(f"Success! PDF created at: {os.path.abspath(OUTPUT_PDF)}")
    except Exception as e:
        print(f"An error occurred while creating the PDF: {e}")

if __name__ == "__main__":
    create_pdf()