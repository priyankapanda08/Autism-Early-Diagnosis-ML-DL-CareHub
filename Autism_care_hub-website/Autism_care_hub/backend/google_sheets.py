import os
import json
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
SPREADSHEET_ID = '1ZbxBR39PWIp3guDOPIdb43a62WZ2S94Ryaro9lRFoc8'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TARGET_SHEET = 'Autism_care_hub'

def get_sheets_service():
    try:
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        return build('sheets', 'v4', credentials=credentials)
    except Exception as e:
        app.logger.error(f"Google Sheets init error: {e}")
        return None

@app.route('/test-sheets', methods=['GET'])
def test_sheets():
    service = get_sheets_service()
    if not service:
        return jsonify({'status': 'error', 'message': 'Failed to initialize Google Sheets service'}), 500

    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        return jsonify({
            'status': 'success',
            'message': 'Google Sheets accessed successfully',
            'spreadsheet_title': spreadsheet.get('properties', {}).get('title', 'Unknown')
        }), 200
    except Exception as e:
        error_msg = str(e)
        return jsonify({
            'status': 'error',
            'message': 'Accessing spreadsheet failed',
            'details': error_msg
        }), 404

@app.route('/save-screening', methods=['POST'])
def save_screening():
    data = request.json

    required_fields = ['name', 'gender', 'ethnicity', 'age', 'initial_answers', 'test_result', 'timestamp']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    service = get_sheets_service()
    if not service:
        return jsonify({'status': 'error', 'message': 'Failed to initialize Google Sheets service'}), 500

    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = spreadsheet.get('sheets', [])
        if not any(sheet.get('properties', {}).get('title') == TARGET_SHEET for sheet in sheets):
            return jsonify({
                'status': 'error',
                'message': f"Sheet '{TARGET_SHEET}' not found in the spreadsheet. Please ensure it exists."
            }), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Spreadsheet access error: {str(e)}'}), 404

    values = [
        [
            data.get('name', ''),
            data.get('gender', ''),
            data.get('ethnicity', ''),
            data.get('age', ''),
            data.get('test_result', ''),
            data.get('timestamp', ''),
            *data.get('initial_answers', [])  
        ]
    ]

    try:
        response = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{TARGET_SHEET}!A:Z',  
            valueInputOption='RAW',
            body={'values': values}
        ).execute()

        return jsonify({'status': 'success', 'message': 'Data saved successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to write to Google Sheets: {str(e)}'}), 500
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
