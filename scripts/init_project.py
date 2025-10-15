"""
Initialize the options bot project after first clone/download.
"""
import os
import shutil
from pathlib import Path


def main():
    """Initialize project directories and files."""
    base_dir = Path(__file__).parent.parent
    
    print("🚀 Initializing Options Bot Project...")
    print("=" * 60)
    
    # Create directories
    directories = [
        base_dir / "data",
        base_dir / "logs",
        base_dir / "config"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory.name}/")
    
    # Check for .env file
    env_example = base_dir / ".env.example"
    env_file = base_dir / ".env"
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print(f"\n✓ Created .env file from .env.example")
            print("  ⚠️  IMPORTANT: Edit .env and add your DISCORD_WEBHOOK_URL")
        else:
            print(f"\n⚠️  Warning: .env.example not found")
    else:
        print(f"\n✓ .env file already exists")
    
    # Check for universe.csv
    universe_file = base_dir / "config" / "universe.csv"
    if not universe_file.exists():
        print(f"\n⚠️  Warning: config/universe.csv not found")
        print("   Creating default universe file...")
        
        default_universe = """ticker,enabled
AAPL,true
MSFT,true
GOOGL,true
AMZN,true
TSLA,true
NVDA,true
AMD,true
META,true
SPY,true
QQQ,true
"""
        universe_file.write_text(default_universe)
        print(f"✓ Created default config/universe.csv")
    else:
        print(f"\n✓ config/universe.csv already exists")
    
    # Next steps
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("=" * 60)
    print()
    print("1. Set up Discord webhook:")
    print("   → Read DISCORD_SETUP.md for instructions")
    print("   → Add webhook URL to .env file")
    print()
    print("2. Install dependencies:")
    print("   → pip install -r requirements.txt")
    print()
    print("3. Test the bot:")
    print("   → python -m options_bot.runner.scan")
    print()
    print("4. Start the scheduler:")
    print("   → python -m options_bot.runner.scheduler")
    print()
    print("5. Read the Quick Start guide:")
    print("   → See QUICKSTART.md for detailed instructions")
    print()
    print("=" * 60)
    print("✅ Initialization complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

