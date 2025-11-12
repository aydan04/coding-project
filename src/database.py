from typing import Dict, Optional

# In-memory "database" for storing reports.
# In a real application, you would use a proper database like PostgreSQL.
_reports_db: Dict[str, Dict] = {}

def save_report(report_id: str, report: Dict) -> None:
    """
    Saves a report to the in-memory database.
    """
    _reports_db[report_id] = report

def get_report(report_id: str) -> Optional[Dict]:
    """
    Retrieves a report from the in-memory database.
    """
    return _reports_db.get(report_id)
