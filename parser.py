import argparse


class syslogLog:
    def __init__(self, time, device_id, msg_num, msg_text):
        self.time = time
        self.device_id = device_id
        self.msg_num = msg_num
        self.msg_text = msg_text

# Parser setup
parser = argparse.ArgumentParser(description="Analyze Linux Logs")
parser.add_argument('file', help='File to be passed as input')

args = parser.parse_args()

# TODO: Catch FileNotFound 
with open(args.file, 'r') as log:
    all_lines = log.readlines()


# Parse raw lines into syslogLog objects and place into list
log_list = []
for line in all_lines:
    split_line = line.split()
    log = syslogLog(" ".join(split_line[:3]),
                    split_line[3],
                    split_line[4],
                    split_line[7:])

    log_list.append(log)

# Add application metadata 
applications = []
for x in log_list:
    # Account for rsyslog variants that include PID after process name
    app_no_pid = x.msg_num.split("[")[0]
    if ( not app_no_pid in applications):
        applications.append(app_no_pid) 
    pass

# Output metadata
print("Log timeline: {} <-> {}".format(log_list[0].time, log_list[-1].time))
print("Line count: {}".format(len(log_list)))
print("Applications: ")
for x in sorted(applications):
    print("- {}".format(x))

# TODO: Print metadata only with no args besides filename passed
# TODO: Add arguments for searching by process