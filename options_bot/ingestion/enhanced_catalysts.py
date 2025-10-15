"""
Enhanced catalyst detection combining multiple data sources.
"""
from typing import Dict, List, Optional
from datetime import datetime
import logging

from .catalysts import get_catalyst as get_basic_catalyst
from .news_fetcher import get_comprehensive_news
from .sec_filings import get_sec_catalysts
from .fda_tracker import get_fda_catalysts
from .stock_splits import get_corporate_actions
from ..config import Settings

logger = logging.getLogger(__name__)


class EnhancedCatalystAnalyzer:
    """Comprehensive catalyst analysis from multiple sources."""
    
    def __init__(self):
        self.news_api_key = Settings.NEWS_API_KEY if hasattr(Settings, 'NEWS_API_KEY') else None
        self.finnhub_api_key = Settings.FINNHUB_API_KEY if hasattr(Settings, 'FINNHUB_API_KEY') else None
        self.polygon_api_key = Settings.POLYGON_API_KEY if hasattr(Settings, 'POLYGON_API_KEY') else None
    
    def analyze_all_catalysts(self, ticker: str, company_name: str = None) -> Dict:
        """
        Analyze all catalyst sources for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            company_name: Optional company name for FDA/news search
            
        Returns:
            Comprehensive catalyst dictionary
        """
        catalysts = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat()
        }
        
        # 1. Basic catalysts (earnings, basic news)
        try:
            basic = get_basic_catalyst(ticker)
            if basic:
                catalysts['earnings'] = {
                    'next_date': basic.next_earnings_date.isoformat() if basic.next_earnings_date else None,
                    'timing': basic.earnings_bmo_amc,
                    'days_until': basic.days_to_earnings
                }
                catalysts['basic_headlines'] = basic.headlines
                catalysts['has_major_event_7d'] = basic.has_major_event_7d
        except Exception as e:
            logger.error(f"Error getting basic catalysts for {ticker}: {e}")
        
        # 2. Enhanced news from multiple sources
        if Settings.USE_NEWS_ANALYSIS:
            try:
                news = get_comprehensive_news(
                    ticker,
                    self.news_api_key,
                    self.finnhub_api_key,
                    self.polygon_api_key,
                    days=Settings.NEWS_LOOKBACK_DAYS if hasattr(Settings, 'NEWS_LOOKBACK_DAYS') else 7
                )
                catalysts['news'] = {
                    'count': len(news),
                    'articles': news[:10],  # Top 10
                    'has_significant_news': len(news) > 5
                }
            except Exception as e:
                logger.error(f"Error getting enhanced news for {ticker}: {e}")
                catalysts['news'] = {'count': 0, 'articles': []}
        
        # 3. SEC filings
        if Settings.USE_SEC_FILINGS:
            try:
                sec = get_sec_catalysts(ticker, days=30)
                catalysts['sec_filings'] = sec
            except Exception as e:
                logger.error(f"Error getting SEC filings for {ticker}: {e}")
                catalysts['sec_filings'] = {'catalyst_score': 0}
        
        # 4. FDA activity (for biotech/pharma)
        if Settings.USE_FDA_TRACKING:
            try:
                fda = get_fda_catalysts(ticker, company_name)
                catalysts['fda'] = fda
            except Exception as e:
                logger.error(f"Error getting FDA data for {ticker}: {e}")
                catalysts['fda'] = {'catalyst_score': 0}
        
        # 5. Corporate actions (splits, dividends)
        if Settings.TRACK_STOCK_SPLITS:
            try:
                corp_actions = get_corporate_actions(ticker)
                catalysts['corporate_actions'] = corp_actions
            except Exception as e:
                logger.error(f"Error getting corporate actions for {ticker}: {e}")
                catalysts['corporate_actions'] = {'catalyst_score': 0}
        
        # Calculate overall catalyst score
        catalysts['overall_score'] = self._calculate_overall_catalyst_score(catalysts)
        catalysts['summary'] = self._generate_catalyst_summary(catalysts)
        
        return catalysts
    
    def _calculate_overall_catalyst_score(self, catalysts: Dict) -> float:
        """Calculate overall catalyst score from all sources."""
        score = 0.0
        
        # Earnings proximity (0-5 points)
        earnings = catalysts.get('earnings', {})
        days_until = earnings.get('days_until')
        if days_until is not None:
            days_abs = abs(days_until)
            if days_abs <= 2:
                score += 5
            elif days_abs <= 5:
                score += 3
            elif days_abs <= 10:
                score += 2
            elif days_abs <= 20:
                score += 1
        
        # News volume (0-2 points)
        news_count = catalysts.get('news', {}).get('count', 0)
        if news_count > 10:
            score += 2
        elif news_count > 5:
            score += 1
        
        # SEC filings (0-3 points)
        sec_score = catalysts.get('sec_filings', {}).get('catalyst_score', 0)
        score += min(sec_score * 0.3, 3)
        
        # FDA activity (0-3 points)
        fda_score = catalysts.get('fda', {}).get('catalyst_score', 0)
        score += min(fda_score * 0.3, 3)
        
        # Corporate actions (0-2 points)
        corp_score = catalysts.get('corporate_actions', {}).get('catalyst_score', 0)
        score += min(corp_score * 0.2, 2)
        
        # Major events (0-2 points)
        if catalysts.get('has_major_event_7d'):
            score += 2
        
        return min(score, 10.0)
    
    def _generate_catalyst_summary(self, catalysts: Dict) -> str:
        """Generate human-readable catalyst summary."""
        summary_parts = []
        
        # Earnings
        earnings = catalysts.get('earnings', {})
        if earnings.get('days_until') is not None:
            days = earnings['days_until']
            if days == 0:
                summary_parts.append("Earnings today")
            elif days == 1:
                summary_parts.append("Earnings tomorrow")
            elif days == -1:
                summary_parts.append("Earnings yesterday")
            elif abs(days) <= 7:
                summary_parts.append(f"Earnings in {abs(days)} days" if days > 0 else f"Earnings {abs(days)} days ago")
        
        # News
        news_count = catalysts.get('news', {}).get('count', 0)
        if news_count > 10:
            summary_parts.append(f"{news_count} news articles")
        elif news_count > 5:
            summary_parts.append(f"{news_count} news stories")
        
        # SEC filings
        sec = catalysts.get('sec_filings', {})
        if sec.get('has_8k_filing'):
            summary_parts.append("Recent 8-K filing")
        if sec.get('has_merger_activity'):
            summary_parts.append("Merger activity")
        
        # FDA
        fda = catalysts.get('fda', {})
        if fda.get('has_recent_approval'):
            summary_parts.append("FDA approval")
        if fda.get('has_recall'):
            summary_parts.append("FDA recall")
        
        # Corporate actions
        corp = catalysts.get('corporate_actions', {})
        split_pred = corp.get('split_prediction', {})
        if split_pred.get('split_likelihood', 0) > 0.6:
            summary_parts.append("Potential split")
        
        if not summary_parts:
            return "No significant catalysts"
        
        return "; ".join(summary_parts)


def get_enhanced_catalysts(ticker: str, company_name: str = None) -> Dict:
    """
    Get comprehensive catalyst analysis for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        company_name: Optional company name
        
    Returns:
        Enhanced catalyst dictionary
    """
    analyzer = EnhancedCatalystAnalyzer()
    return analyzer.analyze_all_catalysts(ticker, company_name)

