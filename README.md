# AutoTag

##Overview:

A project to automatically tag certain loans on Kiva.org.
Licensed under the Apache 2.0 license. 
Project currently in development, with many tags still in the testing phase
For testing, the project currently uses the csv of assigned loans from Kivatools.org. This cannot be uploaded to Github because it contains non-ASKI characters, but you can download it at http://kivatools.com/downloads. 
All of the testing and implementation are done in Python 3.4.
All new development is being done using scikit-learn's random forest classifier.
The system currently is running on an AWS EC2 server.

##Requirements:
All systems must be 99% accurate. This is tested using the assigned loans list using a list of loans the earliest of which was posted later than the latest-posted loan used for testing.
Pull requests on existing systems will be accepted if they pass this test and identify a larger percentage of loans than any current systems.

##Current Status:

Some tags are operational (see "Implemented"). Testing results from 1/31 can be found in JanTesting.pdf.

###Implemented:
One Acre Fund- tags #SustainableAg, #Eco-friendly, #Technology on loans from the One Acre Fund partner.
Elderly (just a parser for "xx years old" etc.)
Schooling (Currently only used for all loans in the Education sector)
HealthAndSanitation (Currently used for all loans in the Health sector along with a Random Forest for other loans)
Fabrics (Currently searches for common types of fabric)
Widowed (Currently searches for "widow" without the word "husband")
Eco-Friendly (Currently searches for loans for solar, used clothing, and used shoes)
Technology (Currently searches for loans for solar)

###Tags that have failed tests (testing results):
FirstLoan (74%)
IncomeProducingDurableAsset (identified too few loans)
Parent (97%)
WomanOwnedBiz (95%)
JobCreator (found too few loans)
RepeatBorrower (95%)

### Tags that will be updated soon:
Random Forest for HealthAndSanitation
Random Forest for Fabrics
Random Forest for Schooling
Random Forest for Widowed
Random Forest for Technology (hopefully)
