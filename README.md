# ServiceMonitor

Welcome to the service monitor platform!
Used to monitor and analyze all the services running on the server. 

supported on Windows & Linux

The monitor has two modes: 
1. Monitor - automatic mode that will sample all the processes every X time you pick 
and will write it to a log file named serviceList.txt, 
and all the changes will be writen to Status_Log.txt

2. manual - you will be asked to enter 2 time samples, 
the program will return all the process changes between the two samples

to exit you will be asked to press 0 


how to run? 
download the main.py file, open terminal/cmd and write ` python3 main.py` then follow the instructions on the screen

about the program: 
the program samples the processes running on the server using the `psutil` library.
the times are calculated using the python `datetime` default library 

the program running from one main function that calls 2 functions - one for every mode
* `monitor()` - uses the get_current_services function to sample all the currently
running processes on the server and then writes them, using the write_to_servicelist function to the log
* `manual(start_time, end_time)` - the function gets two time objects, findes in the serviceList the 
closest 2 samples to the times, and using the diff function, returns the diffrences between the 
two samples
another helping functions are 
* `diff(older, newer)` - the function gets 2 dicts where the key is time 
and the value is a dict of processes {pid:name} and returns a list of differences
 between the time samples
* `get_current_services()`  - the function returns a dict of the currntly running services 
where key is pid and value is the name of the process
* `write_to_servicelist(ts_obj)` - the function gets a dict repressenting a time stamp 
with the processes and writes it to the serviceList.txt file 
* `write_to_statusLog(diff_list)` - the function gets a list of diffrences between two timestemps
and writes it to the Status_Log.txt. file 
* `string_to_sample_dict(s)` - the function gets a string and returns a dict wuth one k,v pair 
where the key is time as a datetime object and the value is a dict is processes where key is 
pid and value is process name 
* `sample_dict_to_string(d)` - the function get a dict with one k,v pair 
where the key is time as a datetime object and the value is a dict is processes where key is 
pid and value is process name, and returns it as a string


 
