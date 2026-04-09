"""
Alert Sender Module

Sends alerts (email, log file, etc) when issues found.
"""

import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class AlertSender:
    """Send alerts for critical issues."""
    
    def __init__(self, log_file="logs/alerts.log"):
        """Initialize alert sender."""
        self.log_file = log_file
    
    def send_alert(self, alert: Dict) -> bool:
        """Send single alert."""
        try:
            message = self._format_alert(alert)
            self._log_alert(message)
            logger.warning(f"🚨 ALERT SENT: {alert['metric']} - {alert['value']}{alert['unit']}")
            return True
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return False
    
    def send_alerts(self, alerts: List[Dict]) -> int:
        """Send multiple alerts."""
        if not alerts:
            logger.info("No alerts to send")
            return 0
        
        sent_count = 0
        for alert in alerts:
            if self.send_alert(alert):
                sent_count += 1
        
        logger.info(f"Sent {sent_count}/{len(alerts)} alerts")
        return sent_count
    
    def _format_alert(self, alert: Dict) -> str:
        """Format alert message."""
        timestamp = alert.get("timestamp", datetime.now().isoformat())
        metric = alert.get("metric", "UNKNOWN")
        value = alert.get("value", "N/A")
        unit = alert.get("unit", "")
        threshold = alert.get("threshold", "N/A")
        
        message = f"""
[{timestamp}] CRITICAL ALERT
Metric: {metric}
Current Value: {value}{unit}
Threshold: {threshold}{unit}
Status: {alert.get("status", "UNKNOWN")}
"""
        return message
    
    def _log_alert(self, message: str) -> None:
        """Log alert to file."""
        try:
            with open(self.log_file, "a") as f:
                f.write(message + "\n" + "="*50 + "\n")
            logger.info(f"Alert logged to {self.log_file}")
        except Exception as e:
            logger.error(f"Failed to log alert: {e}")
