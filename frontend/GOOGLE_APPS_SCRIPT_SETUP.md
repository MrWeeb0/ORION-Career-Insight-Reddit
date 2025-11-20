# Google Apps Script Setup Guide

## Step 1: Create Google Apps Script Project

1. Go to [script.google.com](https://script.google.com)
2. Click **New Project**
3. Name it "Career Insights Email Handler"
4. Delete the default `Code.gs` file
5. Copy the entire code from `google_apps_script.gs` file into a new file

## Step 2: Set Up Google Drive Folder

1. Create a folder in Google Drive for this project
2. Upload your PDF file (`Career_Insights_for_Students.pdf`)
3. Right-click the PDF → **Share** → Set to "Anyone with the link can view"
4. Open the PDF → Copy the file ID from the URL:
   - URL format: `https://drive.google.com/file/d/YOUR_FILE_ID_HERE/view`
   - Copy the long ID between `/d/` and `/view`

## Step 3: Update Script Configuration 

In `google_apps_script.gs`, find this line:
```javascript
const PDF_FILE_ID = 'YOUR_PDF_FILE_ID_FROM_GOOGLE_DRIVE';
```

Replace `YOUR_PDF_FILE_ID_FROM_GOOGLE_DRIVE` with your actual PDF file ID from Step 2.

## Step 4: Create Google Sheet

1. In the Apps Script editor, click **Projects Settings** (gear icon)
2. Turn on **Show "appsscript.json" manifest file**
3. Create a new Google Sheet in Drive (name it anything, e.g., "Career Insights Signups")
4. Copy the spreadsheet ID from the URL
5. In Apps Script, go to **Project Settings** and add the sheet ID somewhere you can reference it, OR:
   - In the Apps Script project, click the **<>** icon next to the title
   - Select your Sheet in the linked Google Sheet section

## Step 5: Deploy as Web App

1. In Google Apps Script, click **Deploy** → **New Deployment**
2. Select type: **Web app**
3. Configure:
   - **Execute as:** Your Google account
   - **Who has access:** Anyone
4. Click **Deploy**
5. Copy the deployment URL (looks like: `https://script.google.com/macros/s/AKfycbx...`)
6. Grant permissions when prompted
7. Copy the deployment URL

## Step 6: Update Frontend JavaScript

In `frontend/static/js/app.js`, find this line:
```javascript
const SHEETS_URL = 'https://script.google.com/macros/s/YOUR_DEPLOYMENT_URL/exec';
```

Replace it with your deployment URL from Step 5:
```javascript
const SHEETS_URL = 'https://script.google.com/macros/s/AKfycbx.../exec';
```

## Step 7: Test the Setup

1. Run your Flask app: `python app.py` from the frontend folder
2. Visit `http://localhost:5000`
3. Fill out the form with a test email
4. Check:
   - ✅ Email received at test address with PDF
   - ✅ New row added to your Google Sheet
   - ✅ Success message on website

## Troubleshooting

**Email not sending?**
- Make sure Google Drive PDF is shared properly
- Check Apps Script logs: Click **Executions** tab to see errors
- Verify PDF_FILE_ID is correct

**Form not submitting?**
- Check browser console for CORS errors
- Verify SHEETS_URL is correct in app.js
- Make sure web app deployment is "Anyone can access"

**Sheet not updating?**
- Verify sheet name matches `SHEET_NAME` in script
- Make sure you have edit permission on the spreadsheet
- Check Apps Script logs for errors

**Getting "Failed to send email" in logs?**
- This is expected if the script account can't send emails
- The form submission still succeeds and data is logged
- Alternative: Use Zapier/Make.com to send emails based on sheet updates

## Advanced: Automated Emails via Google Sheets

If the Apps Script can't send emails directly, use this workaround:

1. Set up a Zapier zap or Make automation:
   - Trigger: New row in Google Sheet
   - Action: Send email with Gmail
   - Attach the PDF file

2. This keeps your app serverless and simple!
