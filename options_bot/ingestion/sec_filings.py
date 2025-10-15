"""
SEC EDGAR filings tracker.
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class SECFilingsTracker:
    """Track SEC filings for catalysts."""
    
    def __init__(self):
        self.base_url = "https://www.sec.gov"
        self.headers = {
            'User-Agent': 'Options Bot contact@example.com',  # SEC requires user agent
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
    
    def get_recent_filings(self, ticker: str, days: int = 30) -> List[Dict]:
        """
        Get recent SEC filings for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            days: Lookback period in days
            
        Returns:
            List of filing dictionaries
        """
        try:
            # Get CIK (Central Index Key) for the ticker
            cik = self._get_cik(ticker)
            if not cik:
                logger.warning(f"Could not find CIK for {ticker}")
                return []
            
            # Fetch recent filings
            url = f"{self.base_url}/cgi-bin/browse-edgar"
            params = {
                'action': 'getcompany',
                'CIK': cik,
                'type': '',
                'dateb': '',
                'owner': 'exclude',
                'count': 40,
                'search_text': ''
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse filings
            filings = self._parse_filings_page(response.text, days)
            
            return filings
            
        except Exception as e:
            logger.error(f"Error fetching SEC filings for {ticker}: {e}")
            return []
    
    def _get_cik(self, ticker: str) -> Optional[str]:
        """Get CIK number for a ticker."""
        try:
            # Use SEC's ticker lookup
            url = f"{self.base_url}/cgi-bin/browse-edgar"
            params = {
                'action': 'getcompany',
                'company': ticker,
                'type': '',
                'dateb': '',
                'owner': 'exclude',
                'count': 1
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            cik_elem = soup.find('span', class_='companyName')
            if cik_elem:
                cik_text = cik_elem.text
                cik = cik_text.split('CIK#:')[1].split('(')[0].strip() if 'CIK#:' in cik_text else None
                return cik.zfill(10) if cik else None
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting CIK for {ticker}: {e}")
            return None
    
    def _parse_filings_page(self, html: str, days: int) -> List[Dict]:
        """Parse filings from SEC page."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            filings = []
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Find filing table
            table = soup.find('table', class_='tableFile2')
            if not table:
                return []
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 4:
                    continue
                
                filing_type = cols[0].text.strip()
                filing_date = cols[3].text.strip()
                description = cols[2].text.strip()
                
                # Parse date
                try:
                    filing_datetime = datetime.strptime(filing_date, '%Y-%m-%d')
                except:
                    continue
                
                if filing_datetime < cutoff_date:
                    continue
                
                # Get filing URL
                link = cols[1].find('a')
                filing_url = f"{self.base_url}{link['href']}" if link else None
                
                filings.append({
                    'type': filing_type,
                    'date': filing_date,
                    'description': description,
                    'url': filing_url,
                    'is_material': self._is_material_filing(filing_type)
                })
            
            return filings
            
        except Exception as e:
            logger.error(f"Error parsing SEC filings: {e}")
            return []
    
    def _is_material_filing(self, filing_type: str) -> bool:
        """Determine if filing type is material."""
        material_types = [
            '8-K',      # Current events
            '10-K',     # Annual report
            '10-Q',     # Quarterly report
            'S-1',      # IPO registration
            'S-3',      # Shelf registration
            'S-4',      # Merger registration
            'SC 13D',   # Ownership changes
            'SC 13G',   # Passive ownership
            '13F',      # Institutional holdings
            'DEF 14A',  # Proxy statement
        ]
        
        return any(mat_type in filing_type.upper() for mat_type in material_types)


def get_sec_catalysts(ticker: str, days: int = 30) -> Dict[str, any]:
    """
    Get SEC filing catalysts for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        days: Lookback period in days
        
    Returns:
        Dictionary with filing information
    """
    tracker = SECFilingsTracker()
    filings = tracker.get_recent_filings(ticker, days)
    
    material_filings = [f for f in filings if f['is_material']]
    
    # Check for specific catalysts
    has_8k = any('8-K' in f['type'] for f in filings)
    has_merger = any('S-4' in f['type'] or 'merger' in f['description'].lower() for f in filings)
    has_shelf = any('S-3' in f['type'] for f in filings)
    recent_material = len([f for f in material_filings if (datetime.now() - datetime.strptime(f['date'], '%Y-%m-%d')).days <= 7])
    
    return {
        'ticker': ticker,
        'total_filings': len(filings),
        'material_filings': len(material_filings),
        'recent_material_count': recent_material,
        'has_8k_filing': has_8k,
        'has_merger_activity': has_merger,
        'has_shelf_registration': has_shelf,
        'filings': material_filings[:5],  # Return top 5 material filings
        'catalyst_score': min(recent_material * 2, 10)  # Score based on recent activity
    }

