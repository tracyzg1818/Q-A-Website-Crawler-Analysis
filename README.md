# Q&A website user crawler & analysis
The project built a Python web crawler to scrape profile information of 37k+ users from a question-and-answer website, built a K-Means clustering model, conducted descriptive analysis and text analysis.

## Technology
The project is created with:
* Python version: 3.7
* Scrapy version: 1.8

## Table of Contents
* Project Background
* Conclusions
* Dataset Overview
* K-Mean Clustering
* Text Analysis

## Project Background
The project was built in a consulting setting. A consulting firm was about to start a project for a client in the media & entertainment industry who planned to launch a new business targeting customers interested in a science fiction topic called *The Three-Body*. The consultants hoped to have a preliminary understanding of the profiles of potential customers. Therefore, a crawler was built to provide some input for the consultants.

## Conclusions
The following conclusions are obtained from clustering analysis and text analysis.
#### Clustering Analysis Conclusion
* The majority of users who followed *The Three-Body* are those with few followers (<100) and few answers (<10)
(3.5% of users have more than 1,000 followers)

#### Text Analysis Conclusion
* By Industry: Most users are from Internet (24%), computer science (7%) and finance industry (4%)
* By Education: 985 & 211-university (the top universities in China) graduates are the majority
* By Region: Most users are in first-tier and second-tier cities.

However, according to [Zhihu product analysis report](https://zhuanlan.zhihu.com/p/25844273), the user group of Zhihu website itself also has similar characteristics:
* The majority are Internet practitioners
* The majority are white-collar workers and college students with good education background
* The majority are urban users

This means our conclusion may have selection bias, that is:
* Although the users we crawled followed the specific topic *The Three-Body*, they reflected the general characteristics of the whole website users;
* On the contrary, we can also infer that the whole Zhihu user group probably has much interest in *The Three-BodY*.

<b>That is to say, the whole Zhihu users are likely to be interested in *The Three-Body*.</b>

## Dataset Overview
This project crawled users who followed the topic *The Three-Body* on Zhihu (the largest Q&A website in China) and stored data in a MySQL database. The head of the dataset looks like this:

![Head of the dataset](https://github.com/tracyzg1818/Q-A-Website-Crawler-Analysis/blob/master/Analysis/User%20dataset%20head.png?raw=true)

There were two types of features in the dataset:
* Numerical features  
* Text features

Numerical features include:
* answer (# of questions that a user answers)
* follower (# of followers that a user has)
* following (# of users that a user follows)
* articles (# of articles that a user writes)
* thanked (# of times that a user is thanked)
* voteup (# of likes that a user has)
* favorited (# of times that a user is favorited)

Text features include:
* location
* headline (one sentence to describe the user himself/herself)
* school
* major
* industry

## K-Mean Clustering
The point of doing K-mean clustering is to have a rough sense of what segmentation of users do we have in the dataset, and what proportion of each segment is. Specifically, I did 2-dimensional K-means clustering by follower vs answer, voted vs follower, voteup vs following, voteup vs favorited, and thanked vs favorited.

#### Criteria for choosing K - Example
From answer & follower perspective, set K equals to 3 assuming that the group could be categorized into 3 types:
* <b>Internet celebrities / Well-known users</b>: many followers + many answers / many followers + few followers
* <b>Active users</b>: many answers + few followers
* <b>Inactive users</b>: few answers + few followers

Also tried K = 4, which didn't make too much difference. Results are shown below:

![Clustering result](https://github.com/tracyzg1818/Q-A-Website-Crawler-Analysis/blob/master/Analysis/follower_answer_clustering.png?raw=true)

## Text Analysis
For the text analysis part, I used Jieba to tokenize headline text and count the frequencies. Location, school, major, and industry were also counted to have an overview of the users. Here're some interesting findings.

![Headline frequency counts](https://github.com/tracyzg1818/Q-A-Website-Crawler-Analysis/blob/master/Analysis/headline_analysis_result.png?raw=true)

![User major counts](https://github.com/tracyzg1818/Q-A-Website-Crawler-Analysis/blob/master/Analysis/User_major_counts.png?raw=true)

![User industry counts](https://github.com/tracyzg1818/Q-A-Website-Crawler-Analysis/blob/master/Analysis/User_industry_counts.png?raw=true)


## Potential Improvements for the Project
The project was conducted in Apr 2019 at a rapid pace. Improvements in data volume and analysis method could be made to refine the project and may extract more insights.

#### Data: Crawled more features of user profile
Limited by Zhihu anti-crawler mechanism and the workload of crawling, the project didn't obtain more detailed features like recent events, answers that liked, articles that favorited. These features are helpful for building a more vivid user profile and for more detailed user segmentation.

#### Method: Clustering based on more features and try more K
- The project only clustered users on two dimensions, which was easy to interpret but may lack sufficient differentiation from the perspective of data volume (A large majority of users are clustered into one group). 
- Try different K may also yield some interesting clusters. 
