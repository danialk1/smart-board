import schedule
import time
import subprocess
from prometheus_client import start_http_server, Gauge


def read_drives():
	p = subprocess.Popen(["nvme", "list"], stdout=subprocess.PIPE)
	(output, err) = p.communicate()
	outputList = output.splitlines()
	outputList = outputList[2:]

	driveList = []
	for line in outputList:
		driveList.append(line[0:10].decode("utf-8"))

	return driveList


# Declare metrics for each Smart attribute
temp          = Gauge("temperature", "Temperature of drive in Celsius", ["drive_path"])
crit_warning  = Gauge("critical_warning", "Critical Warning", ["drive_path"])
spare         = Gauge("available_spare", "Number of Reserve Blocks Remaining", ["drive_path"])
used          = Gauge("percent_used", "Percentage of lifespan used", ["drive_path"])
units_read    = Gauge("data_units_read", "Number of 512 byte data units host has read, in thousands", ["drive_path"])
units_written = Gauge("data_units_written", "Number of 512 byte data units host has written, in thousands", ["drive_path"])
host_read     = Gauge("host_read_commands", "Number of read commands completed by the controller", ["drive_path"])
host_written  = Gauge("host_write_commands", "Number of write commands completed by the controller", ["drive_path"])
busy          = Gauge("controller_busy", "Amount of time controller is busy with I/O commands, in minutes", ["drive_path"])
power_cycles  = Gauge("power_cycles", "Number of power cycles", ["drive_path"])
power_on      = Gauge("power_on_hours", "Number of power-on hours", ["drive_path"])
warning_time  = Gauge("warning_temperature_time", "Minutes the temperature has been over warning threshold", ["drive_path"])
critical_time = Gauge("critical_temperature_time", "Minutes the temperature has been over critical threshold", ["drive_path"])

# Create list with all connected NVMe drives
drive_list = read_drives()

# Start HTTP server endpoint (on port 8000)
start_http_server(8000)

# Start Prometheus database, configured to retain 30 days of data
subprocess.Popen(["./prometheus", "--storage.tsdb.retention.time", "30d"])

def job():
    for device in drive_list:
        p = subprocess.Popen(["smartctl", "-a", device], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        outputList = output.splitlines()
        for line in outputList:
            # Temperature
            if line[0:12].decode("utf-8") == "Temperature:":
                temp.labels(device).set(float(line.split()[1]))
                continue
            # Critical warning
            if line[0:17].decode("utf-8") == "Critical Warning:":
                crit_warning.labels(device).set(float(int((line.decode("utf-8")).split()[2], 16)))
                continue
            # Available spare
            if line[0:16].decode("utf-8") == "Available Spare:":
                spare.labels(device).set(float((line.decode("utf-8")).split()[2].replace('%', '')))
                continue
            # Percentage used
            if line[0:11].decode("utf-8") == "Percentage ":
                used.labels(device).set(float(line[36:-1]))
                continue
            # Data units read
            if line[0:12].decode("utf-8") == "Data Units R":
                units_read.labels(device).set((512/1000000)*float((line.decode("utf-8")).split()[3].replace(',', '')))
                continue
                #Should I add the MB/TB?
            # Data units written
            if line[0:12].decode("utf-8") == "Data Units W":
                units_written.labels(device).set((512/1000000)*float((line.decode("utf-8")).split()[3].replace(',', '')))
                continue
                #Should I add the MB/TB?
            # Host read commands
            if line[0:11].decode("utf-8") == "Host Read C":
                host_read.labels(device).set(float((line.decode("utf-8")).split()[3].replace(',', '')))
                continue
            # Host write commands
            if line[0:12].decode("utf-8") == "Host Write C":
                host_written.labels(device).set(float((line.decode("utf-8")).split()[3].replace(',', '')))
                continue
            # Controller busy
            if line[0:12].decode("utf-8") == "Controller B":
                busy.labels(device).set(float((line.decode("utf-8")).split()[3].replace(',', '')))
                continue
            # Power cycles
            if line[0:12].decode("utf-8") == "Power Cycles":
                power_cycles.labels(device).set(float((line.decode("utf-8")).split()[2].replace(',', '')))
                continue
            # Power on hours
            if line[0:12].decode("utf-8") == "Power On Hou":
                power_on.labels(device).set(float((line.decode("utf-8")).split()[3].replace(',', '')))
                continue
            # Warning composite temperature time
            if line[0:32].decode("utf-8") == "Warning  Comp. Temperature Time:":
                warning_time.labels(device).set(float((line.decode("utf-8")).split()[4].replace(',', '')))
                continue
            # Critical composite temperature time
            if line[0:32].decode("utf-8") == "Critical Comp. Temperature Time:":
                critical_time.labels(device).set(float((line.decode("utf-8")).split()[4].replace(',', '')))
                continue
			#for more information on SMART attributes, visit 
			#thomas-krenn.com/en/wiki/SMART_attributes_of_Intel_SSDs
			#or visit media.kingston.com/support/downloads/MKP_521.6_SMART-DCP1000_attribute.pdf

schedule.every(15).seconds.do(job)

while True:
	schedule.run_pending()
	time.sleep(1)
