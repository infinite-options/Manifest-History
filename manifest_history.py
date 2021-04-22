#!/usr/bin/python
import requests
import datetime, pytz
import urllib, json
from pytz import timezone
def get_dayend_utctime(zone,hr,mm):
     temp=datetime.datetime.now(pytz.timezone(zone))
     temp = temp - datetime.timedelta(seconds=3600)
     #print(x.strftime('%Y%m%d_%H:%M:%S - '))
     temp = temp.replace(hour =hr, minute = mm)
     #print(temp.strftime('%Y%m%d_%H:%M:%S - '))
     utc_temp = temp.astimezone(timezone('UTC'))
     return (utc_temp)

with open ('/home/sharmilasabarathinam/runtest.txt','a') as f:
     f.write(datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S - '))
     f.write('\n')
     set1 = set()
     url = 'https://3s3sftsr90.execute-api.us-west-1.amazonaws.com/dev/api/v2/getUserAndTime'
     post_url = 'https://3s3sftsr90.execute-api.us-west-1.amazonaws.com/dev/api/v2/changeHistory/'
     json_url = urllib.urlopen(url)
     data=json.loads(json_url.read())
     #print(data)
    
     utc_time =datetime.datetime.now()
     utc_timezone = pytz.timezone('UTC')
     utc_time = utc_timezone.localize(utc_time)
     #utc_time = utc_time.astimezone(utc_timezone)
     print(utc_time.strftime('%Y%m%d_%H:%M:%S - '))
     stime = datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    
    
     for d in data['result']:
           day_end_hour =int(d['day_end'].split(':',1)[0])
           day_end_min =int(d['day_end'].split(':',1)[1])
        
           dayend_utc_time = get_dayend_utctime(d['time_zone'], day_end_hour, day_end_min)
           print(dayend_utc_time.strftime('%Y%m%d_%H:%M:%S - '), utc_time.strftime('%Y%m%d_%H:%M:%S - '))
           time_diff = dayend_utc_time-utc_time
           output = d['user_unique_id'] + '\t' + d['time_zone'] + '\t\t' + d['day_end'] + '\t\tday_end_utc_time=' + dayend_utc_time.strftime('%Y%m%d_%H:%M:%S') + '\t\tCurr_utc_time=' + utc_time.strftime('%Y%m%d_%H:%M:%S') + '\t\tTime difference=' + str(time_diff.total_seconds()) + 's ' + str(time_diff.total_seconds()/3600) + '\n'
           f.write(output)
          # print(d['user_unique_id'],d['time_zone'], day_end_hour, day_end_min, utc_time.hour,utc_time.minute)
          # print(dayend_utc_time)
          # print(utc_time)
          # print(time_diff.total_seconds())
           if(time_diff.total_seconds()>=-3540 and time_diff.total_seconds()<=10):
                   set1.add(d['user_unique_id'])
               # print(d['user_unique_id'],d['day_end'])
           for i in set1:
                  new_url =post_url+ i
                  # print(new_url)
                  f.write('before requests.post() call')
                  try:
                       r = requests.post(new_url)
                       f.write(r.text)
                       f.write('\n')
                       r.raise_for_status()
                  except requests.ConnectionError as e:
                       err = 'requests.post(): Connection Error!'
                  except requests.exceptions.HTTPError as e:
                       err = 'requests.post(): HTTP Error!'
                  else:
                       err = ''
                  f.write(err)
                  f.write(i)
                  f.write('\n')
                  f.write('------------------------------------------------------------------\n')
           set1.clear()
