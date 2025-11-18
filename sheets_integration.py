import os
import pandas as pd
import streamlit as st
import requests
from io import StringIO

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

class GoogleSheetsManager:
    def __init__(self):
        self.credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        self.service = None
        self.credentials = None
        self.use_public_access = True  # Default to public access (no credentials needed)
        
        # Load team member GIDs from environment
        self.team_sheets = {
            'Rejna': os.getenv('SHEET_REJNA'),
            'Saurav': os.getenv('SHEET_SAURAV'),
            'Aakib': os.getenv('SHEET_AAKIB'),
            'Ankisha': os.getenv('SHEET_ANKISHA'),
            'Priyanka': os.getenv('SHEET_PRIYANKA'),
            'Ankita': os.getenv('SHEET_ANKITA'),
            'Sujal': os.getenv('SHEET_SUJAL')
        }
        
    def authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        if not GOOGLE_API_AVAILABLE:
            return False
            
        try:
            if not self.credentials_file or not os.path.exists(self.credentials_file):
                # No credentials, will use public access
                self.use_public_access = True
                return False
            
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            
            self.credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=SCOPES
            )
            
            self.service = build('sheets', 'v4', credentials=self.credentials)
            self.use_public_access = False
            return True
            
        except Exception as e:
            st.warning(f"⚠️ Could not authenticate with credentials, using public access: {e}")
            self.use_public_access = True
            return False
    
    def get_sheet_data_public(self, gid=None):
        """Fetch data from public Google Sheet using CSV export (no authentication needed)"""
        try:
            if not self.sheet_id:
                st.error("Google Sheet ID not configured")
                return None
            
            # Construct CSV export URL
            if gid:
                # Specific sheet by GID
                url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv&gid={gid}"
            else:
                # First sheet
                url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv"
            
            # Fetch the CSV data
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse CSV into DataFrame
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)
            
            return df
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                st.error("❌ Access denied. Please make sure your Google Sheet is set to 'Anyone with the link can view'")
                st.info("""
                **To fix this:**
                1. Open your Google Sheet
                2. Click 'Share' button (top right)
                3. Click 'Change to anyone with the link'
                4. Set permission to 'Viewer'
                5. Click 'Done'
                """)
            else:
                st.error(f"❌ HTTP Error: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Error fetching public sheet data: {e}")
            return None
    
    def get_sheet_data(self, gid=None, range_name=None):
        """Fetch data from Google Sheet by GID or range"""
        # Try public access first (no authentication needed)
        if self.use_public_access:
            return self.get_sheet_data_public(gid)
        
        # Fall back to authenticated access
        if not self.service:
            if not self.authenticate():
                # If authentication fails, try public access
                return self.get_sheet_data_public(gid)
        
        try:
            # Get sheet metadata to find sheet name by GID
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.sheet_id
            ).execute()
            
            sheets = sheet_metadata.get('sheets', [])
            if not sheets:
                st.error("No sheets found in the spreadsheet")
                return None
            
            # Find the target sheet by GID or use range_name
            target_sheet = None
            
            if gid:
                # Find sheet by GID
                for sheet in sheets:
                    if str(sheet['properties']['sheetId']) == str(gid):
                        target_sheet = sheet['properties']['title']
                        break
                
                if not target_sheet:
                    st.error(f"Sheet with GID {gid} not found")
                    return None
            elif range_name:
                target_sheet = range_name
            else:
                # Use first sheet if nothing specified
                target_sheet = sheets[0]['properties']['title']
            
            # Fetch the data
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=target_sheet
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                st.warning(f"No data found in sheet: {target_sheet}")
                return None
            
            # Convert to DataFrame
            if len(values) > 1:
                df = pd.DataFrame(values[1:], columns=values[0])
            else:
                df = pd.DataFrame(values)
            
            return df
            
        except HttpError as e:
            st.error(f"❌ Error fetching Google Sheet data: {e}")
            # Try public access as fallback
            return self.get_sheet_data_public(gid)
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            # Try public access as fallback
            return self.get_sheet_data_public(gid)
    
    def get_team_member_data(self, team_member):
        """Fetch data for a specific team member"""
        gid = self.team_sheets.get(team_member)
        if not gid:
            st.error(f"GID not found for team member: {team_member}")
            return None
        
        return self.get_sheet_data(gid=gid)
    
    def get_team_members(self):
        """Get list of available team members"""
        return list(self.team_sheets.keys())
    
    def get_sheet_names(self):
        """Get list of all sheet names in the spreadsheet"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.sheet_id
            ).execute()
            
            sheets = sheet_metadata.get('sheets', [])
            sheet_names = [sheet['properties']['title'] for sheet in sheets]
            return sheet_names
            
        except Exception as e:
            st.error(f"Error getting sheet names: {e}")
            return []
    
    def validate_credentials(self):
        """Check if all required credentials are set"""
        if not self.sheet_id or self.sheet_id == "your_google_sheet_id_here":
            return False, "Google Sheet ID not configured"
        
        # Public access doesn't require credentials file
        if self.use_public_access:
            return True, "Using public sheet access (no credentials needed)"
        
        if not self.credentials_file:
            return True, "Using public sheet access (no credentials file)"
        
        if not os.path.exists(self.credentials_file):
            return True, "Using public sheet access (credentials file not found)"
        
        return True, "Credentials validated"
