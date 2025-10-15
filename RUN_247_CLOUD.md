# 🌐 Run Options Bot 24/7 (Without Your Laptop)

Your bot needs to run at 5:30 AM and 9:45 AM ET every weekday, but your laptop won't always be on. Here are your options!

---

## 🏆 **BEST OPTIONS (Ranked)**

### 1. **Google Cloud Free Tier** ⭐ **RECOMMENDED - 100% FREE**
- **Cost**: $0/month (always free tier)
- **Setup Time**: 15 minutes
- **Difficulty**: Easy
- **Best For**: You!

### 2. **PythonAnywhere** ⭐ **EASIEST**
- **Cost**: $5/month (or $0 with limited features)
- **Setup Time**: 5 minutes
- **Difficulty**: Very Easy
- **Best For**: Absolute simplicity

### 3. **AWS Free Tier**
- **Cost**: $0 for 12 months
- **Setup Time**: 20 minutes
- **Difficulty**: Medium
- **Best For**: Those familiar with AWS

### 4. **Raspberry Pi** (if you have one)
- **Cost**: $0 (after hardware)
- **Setup Time**: 30 minutes
- **Difficulty**: Medium
- **Best For**: Tinkerers

---

## 🚀 **OPTION 1: Google Cloud (FREE FOREVER)**

### What You Get:
- ✅ Always-free e2-micro instance
- ✅ Runs 24/7/365
- ✅ No credit card initially required
- ✅ 30GB storage
- ✅ Perfect for this bot

### Step-by-Step:

#### 1. Create Google Cloud Account
```
1. Go to: https://cloud.google.com/free
2. Click "Get started for free"
3. Sign in with Google account
4. Get $300 free credits (12 months)
   - PLUS always-free tier after that!
```

#### 2. Create a VM Instance
```bash
# In Google Cloud Console:
1. Navigate to: Compute Engine → VM Instances
2. Click "CREATE INSTANCE"
3. Name: options-bot
4. Region: us-east1 (cheapest)
5. Machine type: e2-micro (always free!)
6. Boot disk: Ubuntu 22.04 LTS (10GB)
7. Firewall: Allow HTTP (optional)
8. Click CREATE
```

#### 3. Connect to Your VM
```bash
# Click "SSH" button in console (opens web terminal)
# Or use Cloud Shell
```

#### 4. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Clone your repository (or upload files)
git clone https://github.com/YOUR_USERNAME/options_bot.git
cd options_bot

# Install requirements
pip3 install -r requirements.txt
```

#### 5. Set Up Your .env File
```bash
# Create .env with your settings
nano .env

# Paste your configuration (with Discord webhook)
# Press Ctrl+X, then Y, then Enter to save
```

#### 6. Test It
```bash
python3 -m options_bot.runner.scan
```

#### 7. Set Up Automatic Scheduling
```bash
# Install and start the scheduler
nohup python3 -m options_bot.runner.scheduler > output.log 2>&1 &

# Or use systemd for auto-restart:
sudo nano /etc/systemd/system/options-bot.service
```

Paste this:
```ini
[Unit]
Description=Options Bot Scheduler
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/options_bot
ExecStart=/usr/bin/python3 -m options_bot.runner.scheduler
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable options-bot
sudo systemctl start options-bot
sudo systemctl status options-bot
```

✅ **Done! Bot runs 24/7 even when laptop is off!**

---

## 🐍 **OPTION 2: PythonAnywhere (EASIEST)**

### What You Get:
- ✅ Web-based Python hosting
- ✅ Free tier available (limited)
- ✅ $5/month for scheduled tasks
- ✅ No server management

### Step-by-Step:

#### 1. Sign Up
```
1. Go to: https://www.pythonanywhere.com/
2. Create free account
3. Upgrade to $5/month "Hacker" plan (for scheduled tasks)
```

#### 2. Upload Your Code
```bash
# In PythonAnywhere console:
1. Go to Files tab
2. Upload your options_bot folder
3. Or use git:
   git clone https://github.com/YOUR_USERNAME/options_bot.git
```

#### 3. Install Dependencies
```bash
# In Bash console:
cd options_bot
pip3 install --user -r requirements.txt
```

#### 4. Set Up Scheduled Tasks
```
1. Go to "Tasks" tab
2. Add scheduled task:
   - Command: python3 /home/YOUR_USERNAME/options_bot/options_bot/runner/scan.py
   - Time: 05:30 (UTC - adjust for ET timezone!)
3. Add second task:
   - Command: python3 /home/YOUR_USERNAME/options_bot/options_bot/runner/scan.py
   - Time: 09:45 (UTC)
```

✅ **Done! Runs every day automatically!**

---

## 📦 **OPTION 3: AWS Free Tier**

### What You Get:
- ✅ 750 hours/month free for 12 months
- ✅ t2.micro instance
- ✅ Professional infrastructure
- ✅ Credit card required

### Quick Setup:
```
1. Sign up: https://aws.amazon.com/free/
2. Launch EC2 instance (t2.micro, Ubuntu)
3. Connect via SSH
4. Install Python and dependencies
5. Upload your code
6. Set up systemd service (like Google Cloud above)
```

Similar to Google Cloud, but costs money after 12 months.

---

## 🏠 **OPTION 4: Raspberry Pi (If You Have One)**

### What You Get:
- ✅ Runs at home 24/7
- ✅ Very low power consumption (~$2/year electricity)
- ✅ One-time hardware cost (~$50-100)
- ✅ Full control

### Setup:
```bash
# Install Raspberry Pi OS
# Connect to network
# SSH into Pi

# Install dependencies
sudo apt update
sudo apt install python3 python3-pip git
pip3 install -r requirements.txt

# Set up systemd service
# Same as Google Cloud above
```

---

## 💰 **COST COMPARISON**

| Option | Monthly Cost | Setup Time | Difficulty |
|--------|--------------|------------|------------|
| **Google Cloud Free** | $0 | 15 min | Easy ⭐ |
| **PythonAnywhere** | $5 | 5 min | Very Easy ⭐⭐⭐ |
| **AWS Free Tier** | $0 (year 1), then ~$10 | 20 min | Medium |
| **Raspberry Pi** | $0* | 30 min | Medium |
| **DigitalOcean** | $4-6 | 15 min | Easy |
| **Heroku** | $0-7 | 10 min | Easy |

*After initial hardware purchase

---

## 🎯 **MY RECOMMENDATION FOR YOU:**

### **Start with Google Cloud Free Tier**

**Why:**
1. ✅ **100% Free forever** (e2-micro always free)
2. ✅ **Reliable** (Google infrastructure)
3. ✅ **Easy to set up** (15 minutes)
4. ✅ **24/7 uptime**
5. ✅ **No credit card required initially**
6. ✅ **$300 free credits** for experimenting

### **Or if you want EASIEST:**

### **Use PythonAnywhere** ($5/month)

**Why:**
1. ✅ **Easiest setup** (5 minutes)
2. ✅ **No server management**
3. ✅ **Built-in scheduler**
4. ✅ **Web interface for everything**
5. ✅ **Just $5/month**

---

## 📝 **QUICK START GUIDE: Google Cloud**

```bash
# 1. Create account at cloud.google.com
# 2. Create e2-micro VM (always free)
# 3. SSH into VM
# 4. Run these commands:

sudo apt update && sudo apt install python3-pip git -y
git clone YOUR_REPO_URL
cd options_bot
pip3 install -r requirements.txt
nano .env  # Add your Discord webhook
python3 -m options_bot.runner.scan  # Test
nohup python3 -m options_bot.runner.scheduler &  # Run 24/7
```

✅ **Done in 15 minutes!**

---

## 🔧 **TRANSFER YOUR BOT TO CLOUD**

### Method 1: Git (Recommended)
```bash
# On your laptop:
cd C:\Users\Andrew\options_bot
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_URL
git push -u origin main

# On cloud server:
git clone YOUR_GITHUB_URL
```

### Method 2: Direct Upload
```bash
# Compress folder
# Upload via SCP or web interface
# Extract on server
```

### Method 3: Copy .env Manually
```bash
# Copy your .env file content
# Paste on server using nano .env
```

---

## ⚙️ **MONITORING & MAINTENANCE**

### Check if Bot is Running:
```bash
# SSH into server
ps aux | grep python
tail -f logs/options_bot.log
```

### Restart if Needed:
```bash
sudo systemctl restart options-bot
```

### View Logs:
```bash
cat logs/options_bot.log
```

### Update Bot:
```bash
git pull origin main
sudo systemctl restart options-bot
```

---

## 🆘 **TROUBLESHOOTING**

### Bot Not Running
```bash
sudo systemctl status options-bot
journalctl -u options-bot -n 50
```

### Dependencies Missing
```bash
pip3 install -r requirements.txt --upgrade
```

### Timezone Issues
```bash
# Make sure server is in ET timezone
sudo timedatectl set-timezone America/New_York
```

---

## 🎁 **BONUS: All Cloud Providers with Free Tiers**

1. **Google Cloud** - e2-micro always free
2. **AWS** - t2.micro free for 12 months
3. **Azure** - B1S free for 12 months
4. **Oracle Cloud** - Always free tier (generous)
5. **Heroku** - Free dynos (limited hours)
6. **Railway** - $5 free credit/month
7. **Render** - Free tier available
8. **Fly.io** - Free tier for small apps

---

## 💡 **NEXT STEPS**

1. **Choose a provider** (I recommend Google Cloud Free)
2. **Set up VM** (15 minutes)
3. **Transfer your bot** (use git)
4. **Test it** (python3 -m options_bot.runner.scan)
5. **Set up scheduling** (systemd or cron)
6. **Enjoy!** Bot runs 24/7 while you sleep!

---

## 📞 **NEED HELP?**

I can walk you through setting up on:
- Google Cloud (recommended)
- PythonAnywhere (easiest)
- AWS
- Any other provider

Just ask! 🚀

---

**Your bot will run 24/7, sending picks to Discord every morning, even when your laptop is off!**

