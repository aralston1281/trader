"""
Output formatting for notifications.
"""
from typing import List
from ..models import RankedIdea


def format_brief(ideas: List[RankedIdea], scan_name: str) -> str:
    """
    Format ideas into a concise text report.
    
    Args:
        ideas: List of RankedIdea objects
        scan_name: Name of the scan
        
    Returns:
        Formatted string report
    """
    if not ideas:
        return f"{scan_name}\n\nNo ideas found in this scan."
    
    lines = [
        f"📊 {scan_name}",
        f"🕐 {ideas[0].timestamp.strftime('%Y-%m-%d %H:%M ET')}",
        ""
    ]
    
    for i, idea in enumerate(ideas, 1):
        # Direction emoji
        if idea.bias_direction == "BULLISH":
            emoji = "🟢"
        elif idea.bias_direction == "BEARISH":
            emoji = "🔴"
        else:
            emoji = "⚪"
        
        # IV/HV
        iv_hv = idea.options.iv_hv_ratio
        iv_hv_str = f"{iv_hv:.2f}" if iv_hv else "N/A"
        
        # Liquidity
        liq = idea.options.liquidity_score
        liq_label = "High" if liq >= 7 else "Medium" if liq >= 4 else "Low"
        
        # Catalyst
        catalyst_text = "None"
        if idea.catalyst.has_major_event_7d and idea.catalyst.event_description:
            catalyst_text = idea.catalyst.event_description
        elif idea.catalyst.days_to_earnings:
            catalyst_text = f"Earnings in {idea.catalyst.days_to_earnings} days"
        
        lines.append(f"{emoji} {i}. {idea.ticker} - {idea.bias_direction} (Score: {idea.score:.1f}/10)")
        lines.append(f"   📈 IV/HV: {iv_hv_str} (IV Rank: {idea.options.iv_rank_1y:.0f}%)" if idea.options.iv_rank_1y else f"   📈 IV/HV: {iv_hv_str}")
        lines.append(f"   💧 Liquidity: {liq_label}")
        lines.append(f"   📰 Catalyst: {catalyst_text}")
        lines.append(f"   🎯 Strategy: {idea.strategy}")
        lines.append(f"   📝 {idea.notes}")
        lines.append("")
    
    return "\n".join(lines)


def format_html(ideas: List[RankedIdea], scan_name: str) -> str:
    """
    Format ideas into an HTML report for email.
    
    Args:
        ideas: List of RankedIdea objects
        scan_name: Name of the scan
        
    Returns:
        HTML formatted string
    """
    if not ideas:
        return f"<h2>{scan_name}</h2><p>No ideas found in this scan.</p>"
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .idea {{ margin-bottom: 20px; padding: 15px; border-left: 4px solid #ccc; }}
            .bullish {{ border-left-color: #00ff00; }}
            .bearish {{ border-left-color: #ff0000; }}
            .neutral {{ border-left-color: #aaaaaa; }}
            .ticker {{ font-size: 18px; font-weight: bold; }}
            .score {{ color: #666; }}
            .detail {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h2>{scan_name}</h2>
        <p>{ideas[0].timestamp.strftime('%Y-%m-%d %H:%M ET')}</p>
    """
    
    for i, idea in enumerate(ideas, 1):
        bias_class = idea.bias_direction.lower()
        iv_hv = idea.options.iv_hv_ratio
        iv_hv_str = f"{iv_hv:.2f}" if iv_hv else "N/A"
        
        liq = idea.options.liquidity_score
        liq_label = "High" if liq >= 7 else "Medium" if liq >= 4 else "Low"
        
        catalyst_text = "None"
        if idea.catalyst.has_major_event_7d and idea.catalyst.event_description:
            catalyst_text = idea.catalyst.event_description
        elif idea.catalyst.days_to_earnings:
            catalyst_text = f"Earnings in {idea.catalyst.days_to_earnings} days"
        
        html += f"""
        <div class="idea {bias_class}">
            <div class="ticker">{i}. {idea.ticker} - {idea.bias_direction}</div>
            <div class="score">Score: {idea.score:.1f}/10</div>
            <div class="detail"><strong>IV/HV:</strong> {iv_hv_str}</div>
            <div class="detail"><strong>Liquidity:</strong> {liq_label}</div>
            <div class="detail"><strong>Catalyst:</strong> {catalyst_text}</div>
            <div class="detail"><strong>Strategy:</strong> {idea.strategy}</div>
            <div class="detail">{idea.notes}</div>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html

