"""
Discord webhook notification.
"""
import requests
import logging
from typing import List
from ..models import RankedIdea

logger = logging.getLogger(__name__)


def send_discord(webhook_url: str, content: str, embeds: List[dict] = None) -> bool:
    """
    Send message to Discord via webhook.
    
    Args:
        webhook_url: Discord webhook URL
        content: Message content
        embeds: Optional list of embed objects
        
    Returns:
        True if successful, False otherwise
    """
    try:
        payload = {"content": content}
        
        if embeds:
            payload["embeds"] = embeds
        
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        
        logger.info("Discord notification sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error sending Discord notification: {e}")
        return False


def send_ideas_to_discord(webhook_url: str, ideas: List[RankedIdea], scan_name: str) -> bool:
    """
    Send ranked ideas to Discord with rich formatting.
    
    Args:
        webhook_url: Discord webhook URL
        ideas: List of RankedIdea objects
        scan_name: Name/title for the scan
        
    Returns:
        True if successful, False otherwise
    """
    if not ideas:
        return send_discord(webhook_url, f"📊 {scan_name}\n\n❌ No ideas found in this scan.")
    
    # Create embeds for each idea
    embeds = []
    
    for i, idea in enumerate(ideas, 1):
        # Determine color and emoji based on bias
        if idea.bias_direction == "BULLISH":
            color = 0x00ff00  # Green
            emoji = "🟢"
        elif idea.bias_direction == "BEARISH":
            color = 0xff0000  # Red
            emoji = "🔴"
        else:
            color = 0xaaaaaa  # Gray
            emoji = "⚪"
        
        # Build description
        iv_hv = idea.options.iv_hv_ratio
        iv_hv_str = f"{iv_hv:.2f}" if iv_hv else "N/A"
        
        liquidity_label = "High" if idea.options.liquidity_score >= 7 else \
                         "Medium" if idea.options.liquidity_score >= 4 else "Low"
        
        catalyst_text = "None"
        if idea.catalyst.has_major_event_7d and idea.catalyst.event_description:
            catalyst_text = idea.catalyst.event_description
        elif idea.catalyst.days_to_earnings:
            catalyst_text = f"Earnings in {idea.catalyst.days_to_earnings} days"
        
        # Build description with clear strategy display
        iv_rank_text = f"(IV Rank: {idea.options.iv_rank_1y:.0f}%)" if idea.options.iv_rank_1y else ""
        
        description = (
            f"🎯 **STRATEGY: {idea.strategy}**\n\n"
            f"📊 **Fundamentals:** P/E {idea.fundamentals.pe_ratio:.1f}" if idea.fundamentals.pe_ratio else "P/E N/A"
            f" | Bias: {idea.signals.fund_bias:+.1f}/10\n"
            f"📈 **Options:** IV/HV {iv_hv_str} {iv_rank_text} | Liq: {liquidity_label}\n"
            f"📰 **Catalyst:** {catalyst_text}\n"
            f"💡 **Notes:** {idea.notes}"
        )
        
        embed = {
            "title": f"{emoji} {i}. {idea.ticker} - {idea.bias_direction} (Score: {idea.score:.1f}/10)",
            "description": description,
            "color": color,
            "fields": [
                {
                    "name": "Fundamentals",
                    "value": f"P/E: {idea.fundamentals.pe_ratio:.1f}" if idea.fundamentals.pe_ratio else "P/E: N/A",
                    "inline": True
                },
                {
                    "name": "Premium",
                    "value": f"Bias: {idea.signals.premium_bias:.1f}",
                    "inline": True
                },
                {
                    "name": "Catalyst Score",
                    "value": f"{idea.signals.catalyst_score:.1f}/10",
                    "inline": True
                }
            ]
        }
        
        embeds.append(embed)
    
    # Discord has a limit of 10 embeds per message
    # If more ideas, split into multiple messages
    max_embeds_per_msg = 10
    
    for i in range(0, len(embeds), max_embeds_per_msg):
        batch = embeds[i:i + max_embeds_per_msg]
        
        if i == 0:
            content = f"📊 **{scan_name}**\n🕐 {ideas[0].timestamp.strftime('%Y-%m-%d %H:%M ET')}"
        else:
            content = f"📊 **{scan_name}** (continued...)"
        
        success = send_discord(webhook_url, content, batch)
        if not success:
            return False
    
    return True

