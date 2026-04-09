from src.health_checker import SystemHealthChecker
from src.alert_sender import AlertSender


def main():
    checker = SystemHealthChecker()
    sender = AlertSender()

    results = checker.check_all()

    for alert in results:
        if alert["status"] == "CRITICAL":
            sender.send_alert(alert)


if __name__ == "__main__":
    main()
