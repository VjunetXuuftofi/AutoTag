# AutoTag

##Overview:
A project to automatically tag certain loans on Kiva.org.
Licensed under the Apache 2.0 license. 
Project currently in development, with almost everything still in the testing phase. 
For testing, the project currently uses the csv of assigned loans from Kivatools.org. This cannot be uploaded to Github because it contains non-ASKI characters, but you can download it at http://kivatools.com/downloads. 
All of the testing and implementation are done in Python 3.5, with some development done in R. 


##Requirements:
All systems must be 99% accurate. This is tested using the assigned loans list using a list of loans the earliest of which was posted later than the latest-posted loan used for testing.
Pull requests on existing systems will be accepted if they pass this test and identify a larger percentage of loans than any current systems.

##Current Status:

Some tags are operational. Please see "Implemented" Testing results from 1/31 can be found in JanTesting.pdf. 

###Implemented:
One Acre Fund- tags #SustainableAg, #Eco-friendly, #Technology on loans from the One Acre Fund partner.

Kivawide tags - #Elderly, #Schooling, #HealthAndSanitation, #Fabrics.

###Awaiting Approval from Loan Taggers Team Captians (100% tested accuracy):

JobCreator, Refugee, RepeatBorrower, Technology, Widowed

###Awaiting Testing on Mar 2 (previous testing results):

General #Animals (97.3%)

General #Eco-friendly (<90%)

General #FemaleEducation (<90%)

General #FirstLoan (<90%)

General #WomanOwnedBiz (N/A)

###Development Abandoned:

General #Trees (volume too small)

###Development not (yet) occurring (reasons why):

General #IncomeProducingDurableAsset (requires real human intuition to identify)

General #InspiringStory (subjective)

General #InterestingPhoto (subjective)

General #Orphan (very few loans)

General #Parent (mainly definition requires children to be dependent).

General #SingleParent and #Single (because of inability to tag for parent, I would not be able to distinguish between #SingleParent and #Single)

General #SustainableAg (almost all loans with this tag are from One Acre Fund currently)

General #Unique (subjective)

General #Vegan (very strict definition, not many loans)
