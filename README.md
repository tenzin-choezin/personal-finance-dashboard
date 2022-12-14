# Personal Finances Dashboard
This program uses plotly's [dash](https://github.com/plotly/dash) library to visualize personal finances. It pulls all of its data from a few consolidated CSV files where all transactions are stored and then reflected on the dashboard. 

![](first.png)
![](second.png)
![](third.png)


## Usage
### Installing packages

```shell
import pandas as pd
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, State
from datetime import date, datetime, timedelta
```

You probably want to install them with `pip` or `conda`.

### Cloning the repo
```shell
$ git clone https://github.com/tenzin-choezin/personal-finance-dashboard
```
For more information on how to clone a repo, click [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).


### Adding your own data

In order to visualize your own finances, you'll have to find get transaction data in csv format and pass it into the cleandata function in the Dashboard.py application file.

### Running the application
```shell
python Dashboard.py
```

-----------------
<p align="left">
    <img src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white">
    <img src="https://img.shields.io/badge/numpy-%23F7931E.svg?style=for-the-badge&logo=numpy&logoColor=white">
    <img src="https://img.shields.io/badge/plotly-%037FFC.svg?style=for-the-badge&logo=plotly&logoColor=white">
    <img src="https://img.shields.io/badge/vscode-%23190458.svg?style=for-the-badge&logo=visualstudio&logoColor=white">
     <img src="https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white">
    <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white">
</p>

### Technologies used
* Python libraries - numpy, pandas, plotly, dash
* Version control - git 

### Tools and Services : 
* IDE - Vs code 
* Application deployment - Local server
* Code repository - GitHub
-----------------
