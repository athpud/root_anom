# root_anom
"Understanding the root cause for abberrant customer behavior" 
### A Consulting Project for [Lazy Lantern](https://www.lazylantern.com)

## Athula Pudhiyidath, Ph.D.   
Data Science Fellow    
[Insight Data Science](https://insightfellows.com/data-science)   
May 2020

### About the project
This project was developed over the course of ~3 weeks during the first part of my fellowship at Insight Data Science. For this project, I consulted with a company, Lazy Lantern, that tracks how customers behave on the many **platforms** (web, iOS, Android) of their **client companies**. For a given platform, there are multiple user interactions or **events** that can occur (i.e. clicking on the home screen, clicking on a list of products, etc. Each of these clicks are a different event). Lazy Lantern uses an algorithm to determine user interactions for the events on the site fall within a predicted range. If an event's activity falls out of a preidcted range, an anomaly is triggered and the client company is alerted. 

Whenever, multiple events are triggered as anomalous events in close succession and lead to a long period of downtime on the website, the root of which particular event triggered this chained anomlay response is unknown. Thus, this project aims to compare users' navigation behavior through events during an time-period when an anomaly was logged vs. a time period when an anomaly was not logged. 

To compare user behaviors between anomalous and non-anomalous time periods, I generated a Markov Chain model which catalogged how users navigated through events within the corresponding time periods. This created an event x event probability matrix that compared the likelihood users would traverse from event to event on a given platform for a given time period, and then I took the difference between the two matracies to see which event resulted in the greatest distruption or change in proabability. 

I created a Streamlit dashboard for Lazy Lantern so that they could streamline their process of understanding user behavior for a given client company's platform. 

### Using this Python codebase
1. Clone this repo locally to your computer. The data used in this repository (located in: root_anom/data) is limited in scope and anonomyzed for this demonstration. 
2. Via Anaconda, create a conda environment, activate said environment, and then download all the required packages listed in the requirements.txt via ```pip3 install -r requirements.txt```
3. Activate the dashboard via ```streamlit run root_anom_dash.py```
