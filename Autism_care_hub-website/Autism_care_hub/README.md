# Autism Care Hub - Google Sheets Integration

This project integrates the Autism Care Hub screening tool with Google Sheets to store participant data and test results.

## Setup Instructions

1. Create a Google Cloud Platform Project:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable the Google Sheets API
   - Create a Service Account
   - Download the credentials JSON file

2. Create a Google Sheet:
   - Go to Google Drive
   - Create a new Google Sheet
   - Share the sheet with the service account email (found in the credentials JSON)
   - Note down the spreadsheet ID from the URL

3. Update the Backend Configuration:
   - Place the credentials JSON file in the `backend` directory
   - Update `SPREADSHEET_ID` in `backend/google_sheets.py` with your Google Sheet ID

4. Install Dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. Run the Backend Server:
   ```bash
   cd backend
   python google_sheets.py
   ```

6. Configure Frontend:
   - The frontend code is already set up to send data to the backend
   - Ensure the backend server is running before using the screening tool

## Data Flow

1. User completes the screening form
2. Frontend collects:
   - Basic information (name, gender, ethnicity, age)
   - Test results
   - Timestamp
3. Data is sent to the backend server
4. Backend saves the data to Google Sheets
5. User is redirected to the result page

## Security Notes

- Keep your credentials JSON file secure
- Never commit credentials to version control
- Consider using environment variables for sensitive information
- Ensure proper CORS configuration for the backend server

## Troubleshooting

If you encounter any issues:
1. Check if the backend server is running
2. Verify Google Sheets permissions
3. Check the browser console for errors
4. Ensure all required fields are filled out
