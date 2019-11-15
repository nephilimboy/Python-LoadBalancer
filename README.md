Python Load Balancer (Based on PumpkinLB project)
=========
**Intro**

Changing the LoadBalancer's Destination-Decision Algorithm during the run time without the needs of reloading the LoadBalancer itself and preventing the packet loss is considered as a major hindrance in the IT field. Knowing that, I have re-developed a Free OpenSource LoadBalancer called PumpkinLB and added a web server to it. By doing so, a new config file(new sets of destinations) as JSON format can be sent to the LoadBalancer as an Http post request in order to dynamically change the LoadBalancing algorithm. 

**Requirement**

-   Python 3.7 (ONLY :D)

**How To RUN**

Run the code below

``python3.7 PumpkinLB.py example.cfg``

**Initial Configuration and Config File**

To run this LoadBalancer a config file is needed. It is recommended that read more about this config file format here https://github.com/kata198/PumpkinLB

**How It Works**

During the LoadBalancer's start-time, separate processes are created for each listener (listeners are defined in the config file). Each listener process, moreover, creates sub-processes(request handler worker) to route the packet to the specific destination.

<img src="https://raw.githubusercontent.com/nephilimboy/Python-LoadBalancer/master/Screen%20Shot%202019-11-04%20at%208.57.05%20AM.png" />
=========

**LoadBalancing Algorithm**

<img src="https://raw.githubusercontent.com/nephilimboy/Python-LoadBalancer/master/Screen%20Shot%202019-11-04%20at%208.56.41%20AM.png" />
=========

**Examples JSON Post Requests**

The HTTP server for this LoadBalancer has been configured to run on port 9090

* Change LoadBalancing algorithm to Round Robin

    ```
    {
    "servers":[ {"addr":"192.168.1.2", "port":8000}, {"addr":"192.168.1.3", "port":8000}]
    } 
    ````
    
* Change LoadBalancing algorithm to Weighted (2 to 1)

    ```
    {
    "servers":[ {"addr":"192.168.1.2", "port":8000}, {"addr":"192.168.1.2", "port":8000}, {"addr":"192.168.1.3", "port":8000}]
    } 
    ````

* Change LoadBalancing algorithm to Weighted (3 to 2)

    ```
    {
    "servers":[ {"addr":"192.168.1.2", "port":8000}, {"addr":"192.168.1.2", "port":8000}, {"addr":"192.168.1.2", "port":8000}, {"addr":"192.168.1.3", "port":8000}, {"addr":"192.168.1.3", "port":8000}]
    } 
    ````
    
* Add new destination(192.168.1.4) to current destinations (current destinations are: "192.168.1.2" and "192.168.1.3") and the current LoadBalancing algorithm is Round Robin

    ```
        {
        "servers":[ {"addr":"192.168.1.2", "port":8000}, {"addr":"192.168.1.3", "port":8000}, {"addr":"192.168.1.4", "port":8000}]
        } 
    ````