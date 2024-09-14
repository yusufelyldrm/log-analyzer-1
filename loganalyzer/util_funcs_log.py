import csv
from datetime import datetime
from .util_models import Log
from collections import defaultdict

# burası değişebilir, childrenları olan bir class mantığıyla override bir şekilde oluşturtulabilir
logs_tree = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))))

# sunucu ilk ayağa kalktığında bir kere çalıştırır ve logs listesine logları ekler
def scan_file():
    with open("hn_logs.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")

        for line in tsv_file:
            log = Log(line[0], line[1])
            log_date = datetime.strptime(log.date_string, "%Y-%m-%d %H:%M:%S")
            
            # (yıl -> ay -> gün -> saat -> dakika -> saniye -> log)
            logs_tree[log_date.year][log_date.month][log_date.day][log_date.hour][log_date.minute][log_date.second].append(log)

def get_logs(year=None, month=None, day=None, hour=None, minute=None, second=None):
    _logs = []
    current_level = logs_tree
    
    for key, value in [("year", year), ("month", month), ("day", day), ("hour", hour), ("minute", minute), ("second", second)]:
        if value is not None:
            if value in current_level:
                current_level = current_level[value]
            else:
                return []
        else:
            break

    # current_level altındaki tüm logları toplar ve _logs listesine ekler, eğer current_level bir liste değilse(çünkü sadece ağacın sonu saniye altındaki loglar liste içinde) recursive olarak devam eder
    def collect_logs(tree):
        if isinstance(tree, list):
            _logs.extend(tree)
        elif isinstance(tree, defaultdict):
            for sub_tree in tree.values():
                collect_logs(sub_tree)

    collect_logs(current_level)
    return _logs

def scan_logs_for_unique(date_string):
    try:
        date_components = date_string.split("-")
        time_components = None
        
        if " " in date_string:
            date_part, time_part = date_string.split(" ")
            date_components = date_part.split("-")
            time_components = time_part.split(":")
        
        year = int(date_components[0])
        month = int(date_components[1]) if len(date_components) > 1 else None
        day = int(date_components[2]) if len(date_components) > 2 else None
        hour = int(time_components[0]) if time_components and len(time_components) > 0 else None
        minute = int(time_components[1]) if time_components and len(time_components) > 1 else None
        second = int(time_components[2]) if time_components and len(time_components) > 2 else None
        
        # olay burada
        logs = get_logs(year, month, day, hour, minute, second)

        log_texts_seen = set()
        duplicate_texts = set()
        
        for log in logs:
            if log.text in log_texts_seen:
                duplicate_texts.add(log.text)
            else:
                log_texts_seen.add(log.text)
        
        unique_logs = [log for log in logs if log.text not in duplicate_texts]

        return {'count': len(unique_logs), 'error': None}
    
    except ValueError as e:
        return {'count': 0, 'error': f'Invalid date format provided: {str(e)}, please provide a date in the format "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"'}
    
    except Exception as e:
        return {'count': 0, 'error': f'An unexpected error occurred: {str(e)}'}
