from datetime import datetime
import jdatetime
import json

def is_between(early ,right ,late):
    return early <= right <= late

class Record() :
    """Save methode"""
    count = 0

    def __init__(self ,person ,date_time ,movement):
        self.person = str(person)
        self.date_time = date_time
        self.movement = movement
        Record.count += 1

    def __del__(self):
        Record.count -= 1

class Records() :
    """Creates readable method of traffic & filter them"""
    def __init__(self ,records=[] ,jallali=True):
        self.records = records
        self.jallali = jallali
    
    def latest_now(self):
        return jdatetime.datetime.now().replace(hour=23 ,minute=59 ,second=59) if self.jallali else datetime.datetime.now().replace(hour=23 ,minute=59 ,second=59)

    def read(self ,path_record):
        try:
            with open(path_record, "r") as file:
                lines = file.readlines()
        except Exception as e:
            return True
        
        lines = [line.replace('\t', ' ').strip().split(' ') for line in lines]
        lines = lines[::-1]

        try :
            for line in lines :
                date_time = str(line[1]+' '+line[2])
                date_time = jdatetime.datetime.fromgregorian(date=datetime.strptime(date_time ,'%Y-%m-%d %H:%M:%S')) if self.jallali else datetime.strptime(date_time ,'%Y-%m-%d %H:%M:%S')
                person = line[0]
                movement = 'login' if str(line[4]) == '0' else 'logout'
                self.records.append(Record(person=person ,date_time=date_time ,movement=movement))
            return False
        except Exception as e :
            return True
    
    def get_names(self ,path_person):
        with open(path_person, "r") as file:
            persons = json.load(file)
        named = []
        for rec in self.records :
            if rec.person in persons.keys():
                rec.person = persons[rec.person]
            named.append(rec)
        return Records(named)

    def by_person(self ,person_code):
        filtered = []
        for rec in self.records :
            if rec.person == str(person_code) :
                filtered.append(rec)
        return Records(filtered ,self.jallali)
    
    def by_datetime(self ,early ,late):
        filtered = []
        for Record in self.records :
            if is_between(early ,Record.date_time ,late) :
                filtered.append(Record)
        return Records(filtered ,self.jallali)

    def by_movement(self ,movement):
        filtered = []
        for rec in self.records :
            if rec.movement == movement :
                filtered.append(rec)
        return Records(filtered ,self.jallali)

    def by_days_ago(self ,days):
        now = self.latest_now()
        before = (now - jdatetime.timedelta(days=days)).replace(hour=0 ,minute=0 ,second=0) if self.jallali else (now - datetime.timedelta(days=days)).replace(hour=0 ,minute=0 ,second=0)
        return self.by_datetime(before ,now)

    def by_today(self):
        return self.by_days_ago(0)
    
    def by_this_week(self):
        ago = self.latest_now().weekday()
        return self.by_days_ago(ago)
    
    def by_this_month(self):
        ago = self.latest_now().day - 1
        return self.by_days_ago(ago)
    
    def by_last_week(self):
        return self.by_days_ago(7)
    
    def by_last_month(self):
        return self.by_days_ago(30)
    
    def group_by_day(self):
        grouped = {}
        for rec in self.records :
           date = rec.date_time.date()
           if date not in grouped.keys():
               grouped[date] = []
           grouped[date].append(rec)
        for date ,group in grouped.items() :
            grouped[date] = group[::-1]
        self.grouped = grouped
        return grouped

if __name__ == '__main__' :
    PiPi = Records([] ,False)
    print(PiPi.read('data/1_attlog.dat'))
    #PiPi = PiPi.by_datetime(datetime.datetime(hour=5 ,second=6 ,minute=10 ,day=6 ,month=10 ,year=1400),jdatetime.datetime(hour=5 ,second=6 ,minute=10 ,day=6 ,month=10 ,year=1404)).group_by_day()
    PiPi = PiPi.group_by_day
    for date ,group in PiPi.items() :
        print(f'\n\n{str(date)} :')
        for record in group :
            print(f'{record.person} {str(record.date_time.time())} {record.movement}')