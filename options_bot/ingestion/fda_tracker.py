"""
FDA trials and approvals tracker for biotech/pharma catalysts.
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FDATracker:
    """Track FDA trials, approvals, and regulatory events."""
    
    def __init__(self):
        self.base_url = "https://api.fda.gov"
    
    def search_drug_events(self, company_name: str, limit: int = 10) -> List[Dict]:
        """
        Search FDA drug events database.
        
        Args:
            company_name: Company name to search for
            limit: Max results to return
            
        Returns:
            List of FDA events
        """
        try:
            url = f"{self.base_url}/drug/event.json"
            
            params = {
                'search': f'companynumb:"{company_name}"',
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 404:
                return []  # No results found
            
            response.raise_for_status()
            data = response.json()
            
            events = []
            for result in data.get('results', []):
                events.append({
                    'date': result.get('receivedate'),
                    'serious': result.get('serious', 0),
                    'reaction': result.get('patient', {}).get('reaction', [])
                })
            
            return events
            
        except Exception as e:
            logger.debug(f"No FDA drug events found for {company_name}: {e}")
            return []
    
    def check_drug_approvals(self, company_name: str) -> List[Dict]:
        """
        Check recent FDA drug approvals.
        
        Args:
            company_name: Company name
            
        Returns:
            List of approvals
        """
        try:
            url = f"{self.base_url}/drug/drugsfda.json"
            
            params = {
                'search': f'openfda.manufacturer_name:"{company_name}"',
                'limit': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 404:
                return []
            
            response.raise_for_status()
            data = response.json()
            
            approvals = []
            for result in data.get('results', []):
                products = result.get('products', [])
                for product in products:
                    approvals.append({
                        'drug_name': product.get('brand_name'),
                        'active_ingredient': product.get('active_ingredients', [{}])[0].get('name'),
                        'approval_date': product.get('marketing_status_date')
                    })
            
            return approvals
            
        except Exception as e:
            logger.debug(f"No FDA approvals found for {company_name}: {e}")
            return []
    
    def check_recalls(self, company_name: str) -> List[Dict]:
        """
        Check FDA drug recalls.
        
        Args:
            company_name: Company name
            
        Returns:
            List of recalls
        """
        try:
            url = f"{self.base_url}/drug/enforcement.json"
            
            params = {
                'search': f'openfda.manufacturer_name:"{company_name}"',
                'limit': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 404:
                return []
            
            response.raise_for_status()
            data = response.json()
            
            recalls = []
            for result in data.get('results', []):
                recalls.append({
                    'product_description': result.get('product_description'),
                    'reason': result.get('reason_for_recall'),
                    'classification': result.get('classification'),
                    'recall_date': result.get('recall_initiation_date'),
                    'status': result.get('status')
                })
            
            return recalls
            
        except Exception as e:
            logger.debug(f"No FDA recalls found for {company_name}: {e}")
            return []


def get_fda_catalysts(ticker: str, company_name: str = None) -> Dict[str, any]:
    """
    Get FDA-related catalysts for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        company_name: Company name (will try to derive from ticker if not provided)
        
    Returns:
        Dictionary with FDA catalyst information
    """
    if not company_name:
        # Try to get company name from ticker
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            company_name = stock.info.get('longName', ticker)
        except:
            company_name = ticker
    
    tracker = FDATracker()
    
    approvals = tracker.check_drug_approvals(company_name)
    recalls = tracker.check_recalls(company_name)
    events = tracker.search_drug_events(company_name, limit=5)
    
    # Score based on FDA activity
    catalyst_score = 0
    
    # Recent approvals are very positive
    if approvals:
        catalyst_score += min(len(approvals) * 3, 8)
    
    # Recalls are negative but still catalyst
    if recalls:
        recent_recalls = [r for r in recalls if r.get('status') == 'Ongoing']
        if recent_recalls:
            catalyst_score += 2
    
    has_fda_activity = len(approvals) > 0 or len(recalls) > 0
    
    return {
        'ticker': ticker,
        'company_name': company_name,
        'approvals': approvals,
        'recalls': recalls,
        'adverse_events_count': len(events),
        'has_fda_activity': has_fda_activity,
        'has_recent_approval': len(approvals) > 0,
        'has_recall': len(recalls) > 0,
        'catalyst_score': min(catalyst_score, 10),
        'note': self._generate_fda_note(approvals, recalls)
    }


def _generate_fda_note(approvals: List, recalls: List) -> str:
    """Generate summary note for FDA activity."""
    notes = []
    
    if approvals:
        notes.append(f"{len(approvals)} recent FDA approval(s)")
    
    if recalls:
        notes.append(f"{len(recalls)} recall(s)")
    
    return "; ".join(notes) if notes else "No recent FDA activity"

