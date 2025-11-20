// Google Apps Script for Career Insights Email Signup
// Deploy this as a web app and copy the URL to SHEETS_URL in app.js

// Configuration
const SHEET_NAME = 'Tool Leads';
const PDF_FILE_ID = '1nrtgM0SRhl-ykL5nzpfprUDwsOgxL5Ml'; // Get this from Google Drive URL
const RECIPIENT_EMAIL_SUBJECT = '🎓 Your Engineering Career Insights PDF';

/**
 * Main handler for form submissions
 */
function doPost(e) {
  try {
    const formData = e.parameter;
    const name = formData.name;
    const email = formData.email;
    const timestamp = new Date().toISOString();
    
    // Validate inputs
    if (!name || !email) {
      return ContentService.createTextOutput(
        JSON.stringify({ success: false, message: 'Missing name or email' })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Log to Google Sheets
    logToSheet(name, email, timestamp);
    
    // Send PDF via email
    const emailSent = sendPdfEmail(email, name);
    
    return ContentService.createTextOutput(
      JSON.stringify({ 
        success: true, 
        message: emailSent ? 'Form submitted successfully' : 'Form submitted but email delivery failed',
        email: email,
        name: name
      })
    ).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    Logger.log('Error: ' + error.toString());
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, message: error.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Log form submission to Google Sheets
 */
function logToSheet(name, email, timestamp) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    // Create sheet if it doesn't exist
    const newSheet = ss.insertSheet(SHEET_NAME);
    newSheet.appendRow(['Timestamp', 'Name', 'Email', 'Email Sent', 'Status', 'Notes']);
    newSheet.appendRow([timestamp, name, email, 'YES', 'Sent', '']);
    
    // Format header row
    const headerRange = newSheet.getRange('1:1');
    headerRange.setFontWeight('bold');
    headerRange.setBackground('#667eea');
    headerRange.setFontColor('#ffffff');
    
    // Auto-resize columns
    newSheet.autoResizeColumns(1, 6);
  } else {
    const row = [timestamp, name, email, 'YES', 'Sent', ''];
    sheet.appendRow(row);
  }
  
  Logger.log(`Logged email: ${email} | Name: ${name} | Time: ${timestamp}`);
}

/**
 * Send PDF via email
 */
function sendPdfEmail(recipientEmail, recipientName) {
  try {
    // Get the PDF file from Google Drive
    const pdfFile = DriveApp.getFileById(PDF_FILE_ID);
    
    // Compose email
    const emailBody = `Hi ${recipientName},

Thank you for your interest in Engineering Career Insights!

Your PDF guide is attached. It contains real-world advice from 100+ engineers discussing:
• Career growth and transitions
• Salary expectations
• Work-life balance
• Industry-specific insights
• Practical career tips

Start reading and take notes on insights that resonate with your goals!

Best regards,
Engineering Career Insights Team

---
Open source: https://github.com/MrWeeb0/Career-Insight-Reddit`;
    
    // Send email with PDF attachment
    GmailApp.sendEmail(recipientEmail, RECIPIENT_EMAIL_SUBJECT, emailBody, {
      attachments: [pdfFile.getAs(MimeType.PDF)],
      name: 'Career Insights',
      from: Session.getActiveUser().getEmail()
    });
    
    Logger.log(`✓ Email sent to: ${recipientEmail}`);
    return true;
  } catch (error) {
    Logger.log(`✗ Email send error for ${recipientEmail}: ${error.toString()}`);
    return false;
    // Don't throw - we still want to log the signup even if email fails
  }
}

/**
 * Test function - run this to verify the setup works
 */
function testSubmission() {
  const testData = {
    parameter: {
      name: 'Test User',
      email: 'test@example.com',
      timestamp: new Date().toISOString()
    }
  };
  
  const result = doPost(testData);
  Logger.log(result.getContent());
}

/**
 * Helper function to get file ID from Google Drive share link
 * Usage: Copy your PDF file ID from the URL
 * Example URL: https://drive.google.com/file/d/1a2b3c4d5e6f7g8h9i0j/view
 * File ID is: 1a2b3c4d5e6f7g8h9i0j
 */
function getFileIdFromDrive() {
  Logger.log('To get your PDF File ID:');
  Logger.log('1. Open your PDF in Google Drive');
  Logger.log('2. Copy the ID from the URL: https://drive.google.com/file/d/1nrtgM0SRhl-ykL5nzpfprUDwsOgxL5Ml/view');
  Logger.log('3. Paste it in the PDF_FILE_ID constant above');
}
