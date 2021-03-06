
## Stairs examples living here


### Projects:

**Hacker News**

It's a good example of statistic and analytic problems. Here we are trying
to grab a ton of data from Google Cloud and calculate some stats
values. Stairs will make calculations in parallel way.

The idea to grab some data from Google Cloud about Hacker News post
and calculate different values based on threads topics. You will find 
some tips about `batch_producer`, pipelines configs and general information
about Stairs components.


[Check it out](https://github.com/electronick1/stairs_examples/tree/master/hacker_news)


**Kaggle to Github**

This project is about parsing and how stairs could help you
extract data from any source.<br>

The main goal is to parse kaggle competitions and link them to
github repositories (which were mentioned inside)

In this example you can see all power of Flow components and 
data pipelines itself.

Note: we are considering to make some pipelines compatible with
python async, which will improve experience with such tasks/projects.

[Check it out](https://github.com/electronick1/stairs_examples/tree/master/kaggle_to_github)


**Bag of words**

Is basic example of ML algorithms for solving text/nlp problems.
You can find a very good example of this task on kaggle pages:

https://www.kaggle.com/c/word2vec-nlp-tutorial

There is a well build dataset and get started guide on solving this problem.

Here we have an example of how stairs could help on solving ML related
tasks. The amount of data is not very big here and it's not very related
to "streaming" idealogy, but it's a good example how ML playground 
could instantly became a production ready enviroment,  it's always
easy to tune and change the logic and it's always ready for big amount of
data.

[Check it out](https://github.com/electronick1/stairs_examples/tree/master/bag_of_words) 

