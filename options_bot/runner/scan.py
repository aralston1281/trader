"""
Main scan orchestration.
"""
import csv
import logging
from typing import List, Optional
from datetime import datetime
from pathlib import Path

from ..config import Settings
from ..models import RankedIdea
from ..ingestion import get_fundamentals, get_options_snapshot, get_catalyst
from ..ranker import rank_candidates
from ..notify.discord_notifier import send_ideas_to_discord
from ..notify.email_notifier import send_email
from ..notify.formatter import format_brief, format_html

# Set up logging
logging.basicConfig(
    level=getattr(logging, Settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Settings.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_universe() -> List[str]:
    """
    Load ticker universe from CSV.
    
    Returns:
        List of enabled ticker symbols
    """
    universe_path = Settings.get_universe_path()
    
    if not universe_path.exists():
        logger.error(f"Universe file not found: {universe_path}")
        return []
    
    tickers = []
    try:
        with open(universe_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('enabled', '').lower() == 'true':
                    tickers.append(row['ticker'].strip().upper())
        
        logger.info(f"Loaded {len(tickers)} tickers from universe")
        return tickers
        
    except Exception as e:
        logger.error(f"Error loading universe: {e}")
        return []


def fetch_data(tickers: List[str]) -> tuple[dict, dict, dict]:
    """
    Fetch all data for tickers.
    
    Args:
        tickers: List of ticker symbols
        
    Returns:
        Tuple of (fundamentals_dict, options_dict, catalysts_dict)
    """
    fundamentals = {}
    options = {}
    catalysts = {}
    
    for ticker in tickers:
        logger.info(f"Fetching data for {ticker}...")
        
        # Get fundamentals
        fund = get_fundamentals(ticker)
        if fund:
            fundamentals[ticker] = fund
        
        # Get options snapshot
        opts = get_options_snapshot(ticker)
        if opts:
            options[ticker] = opts
        
        # Get catalysts
        cat = get_catalyst(ticker)
        if cat:
            catalysts[ticker] = cat
    
    logger.info(f"Data fetched: {len(fundamentals)} fundamentals, {len(options)} options, {len(catalysts)} catalysts")
    return fundamentals, options, catalysts


def send_notifications(ideas: List[RankedIdea], scan_name: str) -> bool:
    """
    Send notifications via configured channels.
    
    Args:
        ideas: List of RankedIdea objects
        scan_name: Name of the scan
        
    Returns:
        True if at least one notification succeeded
    """
    success = False
    
    # Discord notification
    if Settings.USE_DISCORD and Settings.DISCORD_WEBHOOK_URL:
        logger.info("Sending Discord notification...")
        discord_success = send_ideas_to_discord(
            Settings.DISCORD_WEBHOOK_URL,
            ideas,
            scan_name
        )
        success = success or discord_success
    
    # Email notification
    if Settings.USE_EMAIL:
        logger.info("Sending email notification...")
        subject = f"Options Bot - {scan_name}"
        text_body = format_brief(ideas, scan_name)
        html_body = format_html(ideas, scan_name)
        
        email_success = send_email(
            Settings.SMTP_HOST,
            Settings.SMTP_PORT,
            Settings.SMTP_USER,
            Settings.SMTP_PASS,
            Settings.EMAIL_TO,
            subject,
            html_body,
            html=True
        )
        success = success or email_success
    
    return success


def run_scan(scan_name: Optional[str] = None, universe: Optional[List[str]] = None) -> List[RankedIdea]:
    """
    Run a complete options scan.
    
    Args:
        scan_name: Optional name for the scan (e.g., "Premarket Scan")
        universe: Optional list of tickers (uses config if not provided)
        
    Returns:
        List of RankedIdea objects
    """
    # Ensure directories exist
    Settings.ensure_directories()
    
    # Default scan name
    if not scan_name:
        now = datetime.now(Settings.TIMEZONE)
        scan_name = f"Options Scan - {now.strftime('%Y-%m-%d %H:%M')}"
    
    logger.info(f"Starting scan: {scan_name}")
    
    # Load universe if not provided
    if not universe:
        universe = load_universe()
    
    if not universe:
        logger.error("No tickers in universe")
        return []
    
    # Fetch data
    fundamentals, options, catalysts = fetch_data(universe)
    
    # Rank candidates
    ideas = rank_candidates(universe, fundamentals, options, catalysts)
    
    logger.info(f"Scan complete: {len(ideas)} ideas generated")
    
    # Send notifications
    if ideas:
        send_notifications(ideas, scan_name)
    else:
        logger.warning("No ideas to send")
    
    return ideas


if __name__ == "__main__":
    """Run scan from command line."""
    try:
        Settings.validate()
        ideas = run_scan()
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"Scan complete: {len(ideas)} ideas")
        print(f"{'='*60}\n")
        
        for idea in ideas[:5]:  # Show top 5
            print(f"{idea.ticker}: {idea.score:.1f}/10 - {idea.strategy}")
        
    except Exception as e:
        logger.error(f"Error running scan: {e}", exc_info=True)
        raise

