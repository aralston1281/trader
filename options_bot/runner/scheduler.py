"""
Scheduler for automated scans.
"""
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

from ..config import Settings
from .scan import run_scan

logger = logging.getLogger(__name__)


def premarket_scan():
    """Run premarket scan."""
    logger.info("Starting premarket scan...")
    run_scan(scan_name="Premarket Scan")


def midmorning_scan():
    """Run mid-morning scan."""
    logger.info("Starting mid-morning scan...")
    run_scan(scan_name="Mid-Morning Scan")


def start_scheduler():
    """
    Start the scheduler with configured scan times.
    """
    # Validate settings
    Settings.validate()
    Settings.ensure_directories()
    
    logger.info("Initializing scheduler...")
    
    scheduler = BlockingScheduler(timezone=Settings.TIMEZONE)
    
    # Parse schedule times
    premarket_hour, premarket_min = map(int, Settings.RUN_PREMARKET.split(':'))
    midmorning_hour, midmorning_min = map(int, Settings.RUN_MIDMORNING.split(':'))
    
    # Add premarket scan job
    scheduler.add_job(
        premarket_scan,
        CronTrigger(
            day_of_week='mon-fri',  # Monday to Friday
            hour=premarket_hour,
            minute=premarket_min,
            timezone=Settings.TIMEZONE
        ),
        id='premarket_scan',
        name='Premarket Options Scan',
        replace_existing=True
    )
    
    # Add mid-morning scan job
    scheduler.add_job(
        midmorning_scan,
        CronTrigger(
            day_of_week='mon-fri',  # Monday to Friday
            hour=midmorning_hour,
            minute=midmorning_min,
            timezone=Settings.TIMEZONE
        ),
        id='midmorning_scan',
        name='Mid-Morning Options Scan',
        replace_existing=True
    )
    
    logger.info(f"Scheduled premarket scan: {Settings.RUN_PREMARKET} ET (Mon-Fri)")
    logger.info(f"Scheduled mid-morning scan: {Settings.RUN_MIDMORNING} ET (Mon-Fri)")
    logger.info("Scheduler started. Press Ctrl+C to exit.")
    
    # Print next run times
    for job in scheduler.get_jobs():
        next_run = job.next_run_time
        if next_run:
            logger.info(f"Next {job.name}: {next_run.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    """Start scheduler from command line."""
    try:
        start_scheduler()
    except Exception as e:
        logger.error(f"Error running scheduler: {e}", exc_info=True)
        raise

