from pytz import timezone
from datetime import datetime

def get_jakarta_time():
    jakarta = timezone('Asia/Jakarta')
    return datetime.now(jakarta)
