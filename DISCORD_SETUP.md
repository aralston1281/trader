# Discord Webhook Setup Guide

This guide will help you set up Discord notifications for the Options Bot.

## Step 1: Create a Discord Server (if needed)

If you don't already have a Discord server:
1. Open Discord
2. Click the "+" button on the left sidebar
3. Select "Create My Own"
4. Choose "For me and my friends" or "For a club or community"
5. Name your server (e.g., "Trading Alerts")

## Step 2: Create a Channel for Bot Messages

1. In your Discord server, create a new text channel
2. Name it something like "options-alerts" or "trading-bot"
3. Right-click the channel and select "Edit Channel"
4. Go to "Permissions" and ensure only you (and trusted users) can see it

## Step 3: Create a Webhook

1. In your channel, click the gear icon (⚙️) to open settings
2. Navigate to "Integrations" in the left menu
3. Click "Webhooks" (or "Create Webhook" if first time)
4. Click "New Webhook"
5. Give your webhook a name (e.g., "Options Bot")
6. (Optional) Upload an avatar image for the bot
7. Click "Copy Webhook URL" - this is your webhook URL!

## Step 4: Configure Options Bot

1. Open your `.env` file in the options_bot directory
2. Find the line `DISCORD_WEBHOOK_URL=`
3. Paste your webhook URL after the equals sign:
   ```
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/123456789/abcdefghijklmnop
   ```
4. Make sure `USE_DISCORD=true` is set
5. Save the file

## Step 5: Test the Connection

Run a manual scan to test:

```bash
python -m options_bot.runner.scan
```

You should see a message appear in your Discord channel!

## Customizing Notifications

### Change Message Format

Edit `options_bot/notify/discord_notifier.py` to customize:
- Colors (change the hex color codes)
- Emojis
- Field layout
- Content included

### Add Additional Webhooks

You can send to multiple channels by adding more webhook URLs in your `.env`:

```env
DISCORD_WEBHOOK_URL_PRIMARY=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_URL_ALERTS=https://discord.com/api/webhooks/...
```

Then modify the notification code to send to both.

## Security Notes

⚠️ **Keep your webhook URL secret!** Anyone with the URL can send messages to your channel.

- Never commit `.env` to git (it's in `.gitignore`)
- Don't share your webhook URL publicly
- If compromised, delete the webhook in Discord and create a new one

## Troubleshooting

### Messages not appearing

1. Check that the webhook URL is correct
2. Verify `USE_DISCORD=true` in `.env`
3. Check Discord's API status: https://discordstatus.com/
4. Look at the logs in `logs/options_bot.log` for errors

### Rate Limiting

Discord webhooks are rate-limited:
- 30 requests per minute
- 5 requests per 2 seconds

The bot should stay well under these limits for normal use.

### Messages too long

Discord has a 2000 character limit per message. If you have many ideas, they'll be split across multiple messages (max 10 embeds per message).

## Advanced: Discord Bot vs Webhook

Webhooks are simpler but limited. For advanced features (buttons, slash commands, etc.), consider creating a full Discord bot:

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Add a bot user
4. Get the bot token
5. Modify the notification code to use discord.py library

This allows for interactive features like:
- React to messages to get more details
- Slash commands to trigger scans
- Real-time updates
- Historical data queries

