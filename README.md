
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/zombodotcom/twitchUserData">
    <img src="https://cdn.vox-cdn.com/thumbor/8GJB_zUFpn2WLB4LF_PGvScNHiU=/0x0:2400x1600/1200x800/filters:focal(1008x608:1392x992)/cdn.vox-cdn.com/uploads/chorus_image/image/65327022/01_Twitch_Logo.0.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Twitch User Data</h3>

  <p align="center">
    Get Chatters Followers List
	Multithreaded get requests for new Twitch API
	[New Twitch API](https://dev.twitch.tv/docs/api/)
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project


uses the new twitch api to get chatters from tmi.twitch.tv then convert username to login ID and 100 per request, then gets the first 100 Per username in the list of lists. 

it uses rate limiting from the twitch header. 
![Example User Data](https://i.imgur.com/MxLIXPV.png)

### Built With

* [Python 3.7]()



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
from matplotlib import rcParams

import matplotlib.animation as animation

from concurrent.futures import ThreadPoolExecutor as PoolExecutor
```
import json

import requests

from collections import defaultdict

import time

import pprint

import threading

import logging

import signal

import matplotlib.pyplot as plt

import random

from itertools import count

import config
```

### Installation
 
1. Clone the repo
```sh
git clone https:://github.com/github_username/repo.git
```
2. Install Python packages
```
pip3 install whatever the package you need
```
2. Add Authorization and ClientID to config.py



<!-- USAGE EXAMPLES -->
## Usage

run the program and it puts out 2 jsons, the user id's and the total follows. 

You can slice in both threaded areas. Just slice like so.
![Slicing](https://i.imgur.com/QjVgBOW.png)

doing this only does 100 chatters instead of all of them from username to userid

```
with PoolExecutor(max_workers=8) as executor:

    # _ is the body of each page that I'm ignoring right now
    for _ in executor.map(douserids, composite_id_list[:1]):
            # print(composite_viewer_list)
        pass
```

here is for the individual followers threaded code. should get only 100 users with [:1]
currently goes through all chatters because no slicing the list

```
# create a thread pool of 4 threads
# gets the follows multithreaded, change 8 to your max threads
with PoolExecutor(max_workers=8) as executor:
    # distribute the 1000 URLs among 4 threads in the pool
    # _ is the body of each page that I'm ignoring right now
    for x in composite_viewer_list[:1]:
        print(x)
        for _ in executor.map(dotogether, x):
            # print(composite_viewer_list)
            pass
```


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements







