# Frontend Setup Guide

This folder contains the web interface for the Engineering Career Insights tool with email capture and PDF delivery.

## Features

- Beautiful landing page with gradient design
- Email capture form
- Automatic PDF email delivery
- Google Sheets integration for email tracking
- Mobile responsive design

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Gmail Setup (for PDF sending)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Copy the 16-character password

### 3. Google Sheets Setup (for email tracking)

1. Create a new Google Sheet titled "Career Insights Signups"
2. Add headers: Timestamp | Name | Email | Status
3. Go to Google Cloud Console: https://console.cloud.google.com
4. Create a new project
5. Enable Google Sheets API and Google Drive API
6. Create a Service Account
7. Download the JSON key file and save as `credentials.json` in this folder

### 4. Configure Environment

Copy `.env.example` to `.env` and fill in:

```bash
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
GOOGLE_SHEETS_KEY=your-spreadsheet-id
```

### 5. Run the Server

```bash
python app.py
```

The server will start on http://localhost:5000

### 6. Deploy

For production, use a service like:
- **Vercel** (frontend + serverless functions)
- **Heroku** (app + worker)
- **AWS Lambda** (serverless)
- **DigitalOcean** (VPS)

## File Structure

```
frontend/
├── index.html          # Landing page with email form
├── app.py              # Flask backend API
├── requirements.txt    # Python dependencies
├── .env.example        # Configuration template
└── credentials.json    # Google Sheets auth (create this)
```

## API Endpoints

### POST /api/signup
Send user email and receive PDF

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "PDF sent to your email!"
}
```

### GET /api/health
Health check endpoint

## Features

✓ Responsive mobile design
✓ Loading states and error handling
✓ Email validation
✓ PDF attachment in emails
✓ Google Sheets tracking
✓ CORS enabled for frontend communication

## Customization

- Edit `index.html` for content, colors, and messaging
- Update `app.py` to add more functionality (auth, database, etc.)
- Modify email templates in `app.py`

## Troubleshooting

**Emails not sending?**
- Check Gmail credentials in `.env`
- Verify App Password is correct
- Check spam folder

**PDF not attaching?**
- Ensure `Career_Insights_for_Students.pdf` exists in `Data/` folder
- Check file permissions

**Google Sheets not updating?**
- Verify `credentials.json` is valid
- Check sheet name and headers
- Verify service account has access to sheet

## Live Deployment

For production:

1. Generate fresh PDF: `python ../main.py`
2. Deploy to hosting (Vercel, Heroku, etc.)
3. Update email templates for production domain
4. Set up analytics tracking
5. Monitor email delivery rates

## Security Notes

- Never commit `.env` or `credentials.json`
- Use environment variables for secrets
- Validate all email inputs
- Consider rate limiting on signup
- Add CAPTCHA for production

## Support

For issues with the scraper, see: https://github.com/MrWeeb0/Career-Insight-Reddit
