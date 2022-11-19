

# Plasma Donor Application [[Project link]](http://159.122.187.202:31326/)
![Alt Text](pic/demo.gif)


## **Link for our Project**
```
http://159.122.187.202:31326/
```


## Project Description:

During the COVID 19 crisis, the requirement of plasma became a high priority and the donor count has become low. Saving the donor information and helping the needy by notifying the current donors list, would be a helping hand. In regard to the problem faced, an application is to be built which would take the donor details, store them and inform them upon a request.


## LINK TO OUR PROJECT
```
http://159.122.187.202:31326/
```


## To Run this Applicaiton locally
    git clone https://github.com/IBM-EPBL/IBM-Project-43398-1660716566.git
    cd IBM-Project-43398-1660716566
    python app.py

## To pull my Docker Image.
    docker pull au.icr.io/value/pda:latest

## To make the changes in the production.
    make update-production

This commad is for most efficient way for updating your changes in production environments by make it the changes in to re-buliding the docker image in au.icr.io/value/pda:latest and Making the Kubernetes pod to restart.
