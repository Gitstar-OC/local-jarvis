"""
Calling Service for Jarvis Bot
Handles phone calls using Twilio API
"""

import re
from typing import Optional, Dict
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


class CallingService:
    """
    Handles phone calling functionality using Twilio
    """
    
    def __init__(self, config):
        """
        Initialize calling service
        
        Args:
            config: Configuration object containing Twilio credentials
        """
        self.config = config
        
        # Get Twilio credentials
        self.account_sid = config.get('twilio_account_sid')
        self.auth_token = config.get('twilio_auth_token')
        self.twilio_number = config.get('twilio_phone_number')
        
        # Initialize Twilio client
        self.client = None
        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                print("Twilio client initialized successfully")
            except Exception as e:
                print(f"Failed to initialize Twilio client: {e}")
        else:
            print("Twilio credentials not configured. Calling functionality disabled.")
        
        # Contact directory
        self.contacts = self._load_contacts()
    
    def _load_contacts(self) -> Dict[str, str]:
        """Load contacts from configuration or file"""
        # For now, return empty dict. In production, this could load from a file
        return {
            'john': '+1234567890',
            'jane': '+0987654321',
            'support': '+1555123456',
        }
    
    def _format_phone_number(self, number: str) -> str:
        """
        Format phone number to E.164 format
        
        Args:
            number: Phone number string
        
        Returns:
            Formatted phone number or original if invalid
        """
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', number)
        
        # If it's a US number without country code, add +1
        if len(digits_only) == 10:
            return f"+1{digits_only}"
        elif len(digits_only) == 11 and digits_only.startswith('1'):
            return f"+{digits_only}"
        elif digits_only.startswith('1') and len(digits_only) > 11:
            return f"+{digits_only}"
        else:
            return f"+{digits_only}" if not number.startswith('+') else number
    
    def _resolve_contact(self, contact_identifier: str) -> Optional[str]:
        """
        Resolve contact name or number to phone number
        
        Args:
            contact_identifier: Contact name or phone number
        
        Returns:
            Phone number if found, None otherwise
        """
        # Check if it's already a phone number
        if re.match(r'[\d\+\-\(\)\s]+', contact_identifier):
            return self._format_phone_number(contact_identifier)
        
        # Look up in contacts directory
        contact_name = contact_identifier.lower().strip()
        if contact_name in self.contacts:
            return self.contacts[contact_name]
        
        # Try partial matching
        for name, number in self.contacts.items():
            if contact_name in name or name in contact_name:
                return number
        
        return None
    
    def make_call(self, target: str, message: Optional[str] = None) -> bool:
        """
        Make a phone call to the specified target
        
        Args:
            target: Phone number or contact name
            message: Optional message to play during call
        
        Returns:
            True if call was initiated successfully, False otherwise
        """
        if not self.client:
            print("Twilio client not initialized. Cannot make calls.")
            return False
        
        if not self.twilio_number:
            print("Twilio phone number not configured.")
            return False
        
        # Resolve target to phone number
        phone_number = self._resolve_contact(target)
        if not phone_number:
            print(f"Could not resolve contact: {target}")
            return False
        
        try:
            # Create TwiML for the call
            if message:
                twiml = f'<Response><Say>{message}</Say></Response>'
            else:
                twiml = '<Response><Say>Hello! This is a call from your Jarvis assistant.</Say></Response>'
            
            # Make the call
            call = self.client.calls.create(
                twiml=twiml,
                to=phone_number,
                from_=self.twilio_number
            )
            
            print(f"Call initiated successfully. Call SID: {call.sid}")
            return True
            
        except TwilioException as e:
            print(f"Twilio error: {e}")
            return False
        except Exception as e:
            print(f"Error making call: {e}")
            return False
    
    def make_voice_call(self, target: str, voice_message: str) -> bool:
        """
        Make a call with a custom voice message
        
        Args:
            target: Phone number or contact name
            voice_message: Message to speak during the call
        
        Returns:
            True if call was initiated successfully, False otherwise
        """
        return self.make_call(target, voice_message)
    
    def get_call_history(self) -> list:
        """
        Get recent call history
        
        Returns:
            List of recent calls
        """
        if not self.client:
            return []
        
        try:
            calls = self.client.calls.list(limit=10)
            call_history = []
            
            for call in calls:
                call_info = {
                    'sid': call.sid,
                    'to': call.to,
                    'from': call.from_,
                    'status': call.status,
                    'duration': call.duration,
                    'date_created': call.date_created.isoformat() if call.date_created else None
                }
                call_history.append(call_info)
            
            return call_history
            
        except TwilioException as e:
            print(f"Error fetching call history: {e}")
            return []
    
    def add_contact(self, name: str, phone_number: str):
        """
        Add a contact to the directory
        
        Args:
            name: Contact name
            phone_number: Phone number
        """
        formatted_number = self._format_phone_number(phone_number)
        self.contacts[name.lower()] = formatted_number
        print(f"Added contact: {name} -> {formatted_number}")
    
    def list_contacts(self) -> Dict[str, str]:
        """
        Get all contacts
        
        Returns:
            Dictionary of contacts
        """
        return self.contacts.copy()
    
    def test_connection(self) -> bool:
        """
        Test Twilio connection
        
        Returns:
            True if connection is working, False otherwise
        """
        if not self.client:
            return False
        
        try:
            # Try to fetch account info
            account = self.client.api.accounts(self.account_sid).fetch()
            print(f"Twilio connection test successful. Account: {account.friendly_name}")
            return True
        except Exception as e:
            print(f"Twilio connection test failed: {e}")
            return False