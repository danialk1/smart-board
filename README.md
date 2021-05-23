# smart-board
A dashboard that polls your SSD's SMART attributes and displays them in a helpful manner on any machine the user likes.

## Setting Up

#### Packages Needed 

Ensure that the following packages are installed and updated on the host machine: 

1. Python 3 

```yum install python3```

2. Smartmontools (Linux package) 

```yum install smartmontools ```

3. NVMe-CLI 

```yum install nvme-cli```

4. Prometheus Python Client (Python package) 

```pip install prometheus-client```

#### Installing Prometheus 

Find the latest Prometheus release at the following page: https://prometheus.io/download/. To get the URL, you can right-click on the filename and select __Copy Link Address__ (shown below). 

Graphical user interface, application

Description automatically generated


Now that you have the URL, on the host machine, download Prometheus using the __wget__ command (below is an example with Prometheus version 2.25.2 for Linux): 

```wget https://github.com/prometheus/prometheus/releases/download/v2.25.2/prometheus-2.25.2.linux-amd64.tar.gz ```

 
Now extract Prometheus using the following command: 

```tar xvfz prometheus-*.tar.gz```



Now there will be a folder beginning with __prometheus-__ where Prometheus is installed. We will refer to this as the __Prometheus__ folder.  


#### Configuring SMART Database 

Now get the __smart_dashboard.py__ script and the __prometheus.yml__ file from online.  
 
In the Prometheus folder, delete __prometheus.yml__, we will be replacing it. 

Move the __smart_dashboard.py__ and __prometheus.yml__ file into the Prometheus folder. 

The database can now be started by running the command: 

```python3 smart_dashboard.py ```

The program will continue indefinitely. Data will only be collected while the process is running, so you may need to use tmux or nohup to continue collecting data after closing your terminal. 

#### Setting up the Grafana Dashboard 

On the machine you want to view the dashboard from, download Grafana [here] (https://grafana.com/). 

Once Grafana is installed, you can reach Grafana Home by opening http://localhost:3000/ in a web browser.  

To set up the SMART Dashboard in Grafana: 
1. Hover over the plus icon on the left side of the screen and click __import__. 
A screenshot of a computer

Description automatically generated

2. Click “Upload JSON” file and select __smart_dashboard.json__ on your PC. 

3. Hover over the gear icon on the left side of the screen and click Data sources
A screenshot of a computer

Description automatically generated

4. Click Add data source and select Prometheus 

5. Name the data source “SMART Log Prometheus Server” 

6. In the URL field, enter the URL of the Prometheus database. This will likely be the IP of the host system, with port number 9090. 

7. Click “Save & Test” 

8. Go back home and view your dashboard. :) 


#### Additional Resources 

Prometheus Documentation - https://prometheus.io/docs/introduction/overview/ 

Grafana Documentation - https://grafana.com/docs/grafana/latest/getting-started/ 






