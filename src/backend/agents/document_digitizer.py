"""
Document Digitizer Agent - Extracts information from receipts and documents using OCR
Processes expense receipts, freight bills, and other logistics documents
"""
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import base64
import io
from typing import Dict, Optional, List, Any
from datetime import datetime
import json

class DocumentDigitizerAgent:
    def __init__(self):
        self.name = "Document Digitizer Agent"
        self.version = "1.0.0"
        
        # Configure tesseract (adjust path if needed)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    async def extract_freight_amount(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract freight amount from receipt image using OCR
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Preprocess image for better OCR
            processed_image = self._preprocess_image_for_ocr(image)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6')
            
            # Extract amount using regex patterns
            amount_info = self._extract_amount_from_text(extracted_text)
            
            # Extract additional details
            receipt_details = self._extract_receipt_details(extracted_text)
            
            return {
                "success": True,
                "extracted_amount": amount_info.get("amount"),
                "currency": amount_info.get("currency", "INR"),
                "confidence": amount_info.get("confidence", 0.5),
                "receipt_details": receipt_details,
                "raw_text": extracted_text,
                "processing_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "extracted_amount": None,
                "confidence": 0.0,
                "processing_timestamp": datetime.utcnow().isoformat()
            }
    
    async def process_expense_receipt(self, image_data: bytes) -> Dict[str, Any]:
        """
        Process expense receipt and extract comprehensive information
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Preprocess image
            processed_image = self._preprocess_image_for_ocr(image)
            
            # Extract text
            extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6')
            
            # Parse receipt information
            receipt_info = {
                "vendor": self._extract_vendor_name(extracted_text),
                "date": self._extract_date(extracted_text),
                "amount": self._extract_amount_from_text(extracted_text),
                "category": self._classify_expense_category(extracted_text),
                "items": self._extract_line_items(extracted_text),
                "location": self._extract_location(extracted_text),
                "receipt_number": self._extract_receipt_number(extracted_text)
            }
            
            # Calculate confidence score
            confidence = self._calculate_extraction_confidence(receipt_info, extracted_text)
            
            return {
                "success": True,
                "receipt_info": receipt_info,
                "confidence": confidence,
                "raw_text": extracted_text,
                "processing_timestamp": datetime.utcnow().isoformat(),
                "suggested_expense": self._generate_expense_suggestion(receipt_info)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "confidence": 0.0,
                "processing_timestamp": datetime.utcnow().isoformat()
            }
    
    async def extract_freight_bill_details(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract details from freight bills and shipping documents
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            processed_image = self._preprocess_image_for_ocr(image)
            extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6')
            
            # Extract freight-specific information
            freight_details = {
                "consignor": self._extract_consignor(extracted_text),
                "consignee": self._extract_consignee(extracted_text),
                "origin": self._extract_origin(extracted_text),
                "destination": self._extract_destination(extracted_text),
                "weight": self._extract_weight(extracted_text),
                "freight_amount": self._extract_amount_from_text(extracted_text),
                "bill_number": self._extract_bill_number(extracted_text),
                "vehicle_number": self._extract_vehicle_number(extracted_text),
                "date": self._extract_date(extracted_text)
            }
            
            confidence = self._calculate_extraction_confidence(freight_details, extracted_text)
            
            return {
                "success": True,
                "freight_details": freight_details,
                "confidence": confidence,
                "raw_text": extracted_text,
                "processing_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "confidence": 0.0,
                "processing_timestamp": datetime.utcnow().isoformat()
            }
    
    def _preprocess_image_for_ocr(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image to improve OCR accuracy
        """
        # Convert PIL Image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def _extract_amount_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract monetary amounts from text using regex patterns
        """
        amount_patterns = [
            r'(?:total|amount|sum|paid|payment)?\s*[:\-]?\s*(?:rs\.?|₹|inr)?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'₹\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'rs\.?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:rs\.?|₹|inr)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'  # Generic number pattern
        ]
        
        found_amounts = []
        
        for pattern in amount_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                amount_str = match.group(1) if match.groups() else match.group(0)
                try:
                    # Clean amount string
                    clean_amount = amount_str.replace(',', '').replace('₹', '').replace('rs', '').replace('.', '').strip()
                    
                    # Convert to float (assuming last two digits are decimal places if > 100)
                    if len(clean_amount) > 2 and clean_amount.isdigit():
                        amount = float(clean_amount[:-2] + '.' + clean_amount[-2:]) if len(clean_amount) > 2 else float(clean_amount)
                    else:
                        amount = float(clean_amount)
                    
                    if amount > 1:  # Reasonable minimum amount
                        found_amounts.append({
                            "amount": amount,
                            "raw_text": amount_str,
                            "pattern_used": pattern
                        })
                except ValueError:
                    continue
        
        if found_amounts:
            # Return the largest amount found (likely the total)
            best_amount = max(found_amounts, key=lambda x: x["amount"])
            return {
                "amount": best_amount["amount"],
                "currency": "INR",
                "confidence": 0.8 if len(found_amounts) == 1 else 0.6,
                "alternatives": found_amounts
            }
        
        return {
            "amount": None,
            "currency": "INR",
            "confidence": 0.0,
            "alternatives": []
        }
    
    def _extract_vendor_name(self, text: str) -> Optional[str]:
        """Extract vendor/merchant name from receipt text"""
        lines = text.split('\n')
        
        # Look for likely vendor names in the first few lines
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            if len(line) > 3 and not line.isdigit() and not self._is_address_line(line):
                # Skip common receipt headers
                skip_words = ['receipt', 'bill', 'invoice', 'tax', 'gst', 'date', 'time']
                if not any(word in line.lower() for word in skip_words):
                    return line
        
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract date from receipt text"""
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'\d{1,2}\s+\w+\s+\d{2,4}',
            r'\w+\s+\d{1,2},?\s+\d{2,4}'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    def _classify_expense_category(self, text: str) -> str:
        """Classify expense category based on receipt content"""
        text_lower = text.lower()
        
        fuel_keywords = ['petrol', 'diesel', 'fuel', 'hp', 'bharat petroleum', 'iocl', 'bpcl']
        if any(keyword in text_lower for keyword in fuel_keywords):
            return "fuel"
        
        food_keywords = ['restaurant', 'hotel', 'food', 'meal', 'breakfast', 'lunch', 'dinner']
        if any(keyword in text_lower for keyword in food_keywords):
            return "food"
        
        toll_keywords = ['toll', 'highway', 'expressway', 'nhai']
        if any(keyword in text_lower for keyword in toll_keywords):
            return "toll"
        
        maintenance_keywords = ['service', 'repair', 'garage', 'workshop', 'spare', 'parts']
        if any(keyword in text_lower for keyword in maintenance_keywords):
            return "maintenance"
        
        parking_keywords = ['parking', 'park']
        if any(keyword in text_lower for keyword in parking_keywords):
            return "parking"
        
        return "other"
    
    def _extract_line_items(self, text: str) -> List[Dict[str, Any]]:
        """Extract individual line items from receipt"""
        lines = text.split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            # Look for lines with item and price pattern
            item_pattern = r'(.+?)\s+(\d+(?:\.\d{2})?)'
            match = re.search(item_pattern, line)
            
            if match and len(line) > 5:
                item_name = match.group(1).strip()
                try:
                    price = float(match.group(2))
                    if price > 0 and len(item_name) > 2:
                        items.append({
                            "name": item_name,
                            "price": price
                        })
                except ValueError:
                    continue
        
        return items
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location/address from receipt"""
        lines = text.split('\n')
        
        # Look for address-like lines
        for line in lines:
            if self._is_address_line(line):
                return line.strip()
        
        return None
    
    def _extract_receipt_number(self, text: str) -> Optional[str]:
        """Extract receipt/bill number"""
        patterns = [
            r'(?:receipt|bill|invoice)\s*(?:#|no\.?|number)?\s*:?\s*([a-zA-Z0-9]+)',
            r'(?:#|no\.?)\s*([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_consignor(self, text: str) -> Optional[str]:
        """Extract consignor from freight bill"""
        pattern = r'(?:consignor|from|sender)[:]*\s*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_consignee(self, text: str) -> Optional[str]:
        """Extract consignee from freight bill"""
        pattern = r'(?:consignee|to|receiver)[:]*\s*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_origin(self, text: str) -> Optional[str]:
        """Extract origin location from freight bill"""
        pattern = r'(?:origin|from|pickup)[:]*\s*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_destination(self, text: str) -> Optional[str]:
        """Extract destination from freight bill"""
        pattern = r'(?:destination|to|delivery)[:]*\s*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_weight(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract weight information"""
        pattern = r'(\d+(?:\.\d+)?)\s*(kg|kgs|ton|tons|mt)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return {
                "value": float(match.group(1)),
                "unit": match.group(2).lower()
            }
        
        return None
    
    def _extract_bill_number(self, text: str) -> Optional[str]:
        """Extract bill number from freight bill"""
        patterns = [
            r'(?:bill|invoice|lr)\s*(?:#|no\.?|number)?\s*:?\s*([a-zA-Z0-9]+)',
            r'lr\s*(?:#|no\.?)?\s*:?\s*([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_vehicle_number(self, text: str) -> Optional[str]:
        """Extract vehicle number"""
        pattern = r'(?:vehicle|truck|lorry)\s*(?:#|no\.?|number)?\s*:?\s*([a-zA-Z0-9\s]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # Look for Indian vehicle number pattern
        indian_vehicle_pattern = r'[A-Z]{2}\s*\d{2}\s*[A-Z]{1,2}\s*\d{4}'
        match = re.search(indian_vehicle_pattern, text)
        
        if match:
            return match.group(0)
        
        return None
    
    def _is_address_line(self, line: str) -> bool:
        """Check if a line looks like an address"""
        address_indicators = ['road', 'street', 'lane', 'area', 'city', 'pin', 'pincode', 'state']
        return any(indicator in line.lower() for indicator in address_indicators)
    
    def _calculate_extraction_confidence(self, extracted_info: Dict[str, Any], raw_text: str) -> float:
        """Calculate confidence score for extraction"""
        confidence = 0.0
        total_fields = len(extracted_info)
        filled_fields = sum(1 for value in extracted_info.values() if value is not None)
        
        # Base confidence from field coverage
        confidence += (filled_fields / total_fields) * 0.5
        
        # Boost for amount extraction
        if extracted_info.get("amount") or (isinstance(extracted_info.get("freight_amount"), dict) and extracted_info["freight_amount"].get("amount")):
            confidence += 0.3
        
        # Boost for date extraction
        if extracted_info.get("date"):
            confidence += 0.1
        
        # Boost for vendor/consignor extraction
        if extracted_info.get("vendor") or extracted_info.get("consignor"):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _generate_expense_suggestion(self, receipt_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate expense entry suggestion based on extracted data"""
        suggestion = {
            "description": f"Expense at {receipt_info.get('vendor', 'Unknown vendor')}",
            "category": receipt_info.get("category", "other")
        }
        
        if receipt_info.get("amount") and isinstance(receipt_info["amount"], dict):
            suggestion["amount"] = receipt_info["amount"].get("amount", 0)
        
        if receipt_info.get("date"):
            suggestion["expense_date"] = receipt_info["date"]
        
        return suggestion
