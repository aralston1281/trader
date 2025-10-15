"""
Configuration and settings management.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    UNIVERSE_CSV = os.getenv('UNIVERSE_CSV', 'config/universe.csv')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/options_bot.db')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/options_bot.log')
    
    # Timezone
    TIMEZONE = pytz.timezone(os.getenv('TIMEZONE', 'America/New_York'))
    
    # Discord
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
    USE_DISCORD = os.getenv('USE_DISCORD', 'true').lower() == 'true'
    
    # Email
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASS = os.getenv('SMTP_PASS')
    EMAIL_TO = os.getenv('EMAIL_TO')
    USE_EMAIL = os.getenv('USE_EMAIL', 'false').lower() == 'true'
    
    # Feature Flags
    USE_FINBERT = os.getenv('USE_FINBERT', 'false').lower() == 'true'
    USE_TECHNICAL_ANALYSIS = os.getenv('USE_TECHNICAL_ANALYSIS', 'true').lower() == 'true'
    USE_NEWS_ANALYSIS = os.getenv('USE_NEWS_ANALYSIS', 'true').lower() == 'true'
    USE_SEC_FILINGS = os.getenv('USE_SEC_FILINGS', 'true').lower() == 'true'
    USE_FDA_TRACKING = os.getenv('USE_FDA_TRACKING', 'true').lower() == 'true'
    USE_PAID_OPTIONS_API = os.getenv('USE_PAID_OPTIONS_API', 'false').lower() == 'true'
    
    # API Keys
    POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    QUANDL_API_KEY = os.getenv('QUANDL_API_KEY')
    BENZINGA_API_KEY = os.getenv('BENZINGA_API_KEY')
    TRADIER_API_KEY = os.getenv('TRADIER_API_KEY')
    TRADIER_SANDBOX = os.getenv('TRADIER_SANDBOX', 'true').lower() == 'true'
    
    # Scheduling
    RUN_PREMARKET = os.getenv('RUN_PREMARKET', '05:30')
    RUN_MIDMORNING = os.getenv('RUN_MIDMORNING', '09:45')
    
    # Scoring Weights
    WEIGHT_FUNDAMENTAL = float(os.getenv('WEIGHT_FUNDAMENTAL', '0.40'))
    WEIGHT_TECHNICAL = float(os.getenv('WEIGHT_TECHNICAL', '0.20'))
    WEIGHT_PREMIUM = float(os.getenv('WEIGHT_PREMIUM', '0.20'))
    WEIGHT_CATALYST = float(os.getenv('WEIGHT_CATALYST', '0.15'))
    WEIGHT_NEWS_SENTIMENT = float(os.getenv('WEIGHT_NEWS_SENTIMENT', '0.05'))
    
    # Output Settings
    MAX_PICKS = int(os.getenv('MAX_PICKS', '10'))
    MIN_LIQUIDITY_SCORE = float(os.getenv('MIN_LIQUIDITY_SCORE', '3.0'))
    MIN_MARKET_CAP = float(os.getenv('MIN_MARKET_CAP', '1000000000'))  # 1B default
    
    # Technical Analysis Settings
    TA_LOOKBACK_DAYS = int(os.getenv('TA_LOOKBACK_DAYS', '90'))
    TA_USE_RSI = os.getenv('TA_USE_RSI', 'true').lower() == 'true'
    TA_USE_MACD = os.getenv('TA_USE_MACD', 'true').lower() == 'true'
    TA_USE_SUPPORT_RESISTANCE = os.getenv('TA_USE_SUPPORT_RESISTANCE', 'true').lower() == 'true'
    TA_USE_VOLUME_PROFILE = os.getenv('TA_USE_VOLUME_PROFILE', 'true').lower() == 'true'
    
    # News Settings
    NEWS_LOOKBACK_DAYS = int(os.getenv('NEWS_LOOKBACK_DAYS', '7'))
    NEWS_MIN_RELEVANCE_SCORE = float(os.getenv('NEWS_MIN_RELEVANCE_SCORE', '0.5'))
    
    # Catalyst Settings
    TRACK_STOCK_SPLITS = os.getenv('TRACK_STOCK_SPLITS', 'true').lower() == 'true'
    TRACK_EARNINGS = os.getenv('TRACK_EARNINGS', 'true').lower() == 'true'
    TRACK_FDA_EVENTS = os.getenv('TRACK_FDA_EVENTS', 'true').lower() == 'true'
    TRACK_PATENT_FILINGS = os.getenv('TRACK_PATENT_FILINGS', 'false').lower() == 'true'
    TRACK_INSIDER_TRADING = os.getenv('TRACK_INSIDER_TRADING', 'true').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required settings."""
        if cls.USE_DISCORD and not cls.DISCORD_WEBHOOK_URL:
            raise ValueError("DISCORD_WEBHOOK_URL is required when USE_DISCORD is true")
        
        if cls.USE_EMAIL:
            if not all([cls.SMTP_USER, cls.SMTP_PASS, cls.EMAIL_TO]):
                raise ValueError("Email settings (SMTP_USER, SMTP_PASS, EMAIL_TO) required when USE_EMAIL is true")
        
        if not cls.USE_DISCORD and not cls.USE_EMAIL:
            raise ValueError("At least one notification method (Discord or Email) must be enabled")
        
        # Validate weights sum to 1.0 (approximately)
        total_weight = (cls.WEIGHT_FUNDAMENTAL + cls.WEIGHT_TECHNICAL + 
                       cls.WEIGHT_PREMIUM + cls.WEIGHT_CATALYST + cls.WEIGHT_NEWS_SENTIMENT)
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Scoring weights must sum to 1.0 (currently: {total_weight})")
        
        return True
    
    @classmethod
    def get_universe_path(cls) -> Path:
        """Get full path to universe CSV."""
        path = Path(cls.UNIVERSE_CSV)
        if not path.is_absolute():
            path = cls.BASE_DIR / path
        return path
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        (cls.BASE_DIR / 'data').mkdir(exist_ok=True)
        (cls.BASE_DIR / 'logs').mkdir(exist_ok=True)
        
        config_dir = cls.BASE_DIR / 'config'
        config_dir.mkdir(exist_ok=True)
    
    @classmethod
    def get_enabled_features(cls) -> dict:
        """Get dictionary of enabled features."""
        return {
            'technical_analysis': cls.USE_TECHNICAL_ANALYSIS,
            'news_analysis': cls.USE_NEWS_ANALYSIS,
            'sec_filings': cls.USE_SEC_FILINGS,
            'fda_tracking': cls.USE_FDA_TRACKING,
            'finbert_sentiment': cls.USE_FINBERT,
            'paid_options_api': cls.USE_PAID_OPTIONS_API,
            'stock_splits': cls.TRACK_STOCK_SPLITS,
            'insider_trading': cls.TRACK_INSIDER_TRADING
        }
    
    @classmethod
    def print_config_summary(cls):
        """Print configuration summary."""
        print("\n" + "="*60)
        print("OPTIONS BOT CONFIGURATION")
        print("="*60)
        print(f"Timezone: {cls.TIMEZONE}")
        print(f"Scan Times: {cls.RUN_PREMARKET}, {cls.RUN_MIDMORNING}")
        print(f"\nScoring Weights:")
        print(f"  Fundamental: {cls.WEIGHT_FUNDAMENTAL*100:.0f}%")
        print(f"  Technical:   {cls.WEIGHT_TECHNICAL*100:.0f}%")
        print(f"  Premium:     {cls.WEIGHT_PREMIUM*100:.0f}%")
        print(f"  Catalyst:    {cls.WEIGHT_CATALYST*100:.0f}%")
        print(f"  Sentiment:   {cls.WEIGHT_NEWS_SENTIMENT*100:.0f}%")
        print(f"\nEnabled Features:")
        for feature, enabled in cls.get_enabled_features().items():
            status = "✅" if enabled else "❌"
            print(f"  {status} {feature.replace('_', ' ').title()}")
        print(f"\nAPI Keys Configured:")
        print(f"  {'✅' if cls.POLYGON_API_KEY else '❌'} Polygon.io")
        print(f"  {'✅' if cls.FINNHUB_API_KEY else '❌'} Finnhub")
        print(f"  {'✅' if cls.ALPHA_VANTAGE_API_KEY else '❌'} Alpha Vantage")
        print(f"  {'✅' if cls.NEWS_API_KEY else '❌'} News API")
        print("="*60 + "\n")
