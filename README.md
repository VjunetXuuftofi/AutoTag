# AutoTag

## Overview:

A project to automatically tag certain loans on Kiva.org.
Licensed under the Apache 2.0 license. 
Project currently in development, with almost everything still in the testing phase. 
For testing, the project currently uses the csv of assigned loans from Kivatools.org.
All of the testing and implementation are done in Python 3.4.
All new development is being done using scikit-learn's random forest
classifier. This has proven very effective for many loans.
The system currently is running on an AWS EC2 server.

## Requirements:
All systems must be 99% accurate. This is tested using the assigned loans list using a list of loans the earliest of which was posted later than the latest-posted loan used for testing.
Pull requests on existing systems will be accepted if they pass this test and identify a larger percentage of loans than any current systems.

### Implemented Tags:

Kivawide tags (Random Forest) - #Animals, #Refugee, #Fabrics, #Widowed,
\#Schooling, #Technology, #Trees

Autotags with some coverage (no Random Forest) - #SustainableAg, #Elderly,
\#HealthAndSanitation, #RepeatBorrower

