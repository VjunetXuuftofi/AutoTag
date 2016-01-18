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

###Implemented:
One Acre Fund- tags #SustainableAg, #Eco-friendly, #Technology on loans from the One Acre Fund partner

###Awaiting Approval from Loan Taggers Team Captians:
None

###Awaiting Testing on Jan 31:

General #Animals

General #Eco-friendly

General #Fabrics

General #FemaleEducation

General #FirstLoan

General #Elderly

General #HealthAndSanitation

General #JobCreator

General #Refugee

General #RepeatBorrower

General #Schooling

General #Technology

General #Trees

General #Widowed

General #WomanOwnedBiz


###No Development Planned (reasons why):

General #IncomeProducingDurableAsset (requires real human intuition to identify)

General #InspiringStory (subjective)

General #InterestingPhoto (subjective)

General #Orphan (very few loans)

General #Parent (mainly definition requires children to be dependent).

General #SingleParent and #Single (because of inability to tag for parent, I would not be able to distinguish between #SingleParent and #Single)

General #SustainableAg (almost all loans with this tag are from One Acre Fund currently)

General #Unique (subjective)

General #Vegan (very strict definition, not many loans)
