
## Bag of words example.

(!) Under development

### The problem:

You can find whole description here

https://www.kaggle.com/c/word2vec-nlp-tutorial

Idea in short: based on movies reviews, predict if
review is positive or negative (using sentiment analysis)  


### Solution:


**Step1. Reading and preparing data**

Based on:
https://www.kaggle.com/c/word2vec-nlp-tutorial#part-1-for-beginners-bag-of-words

In the tutorial above we should prepare data for 3 models:

- Word2Vec
- Kmeans
- BagofWords (Random Forest)

In this example we are using 
'review_to_words' pipeline, which could be called from
any other pipelines (with a different cleanup flow)

Then after pipeline data comes to `consumer_iter` consumer
which allows to read queue/streaming service from any other
place (e.g. place where we building models)

**Step2. Building Word2Vec Kmeans**

Inside [model.py]() you could find two function for Word2Vec
and Kmeans training. 

In this case Word2Vec reading data from `fit_to_word2vec` 
consumer. The whole data initialization process looks like 
this:

Start data producer: <br>
`python manager.py producer:process bag_of_words.read_train_data_for_word2vec`

Start pipelines processes: <br>
`python manager.py pipelines:run`

Start Word2Vec training:
`python word2vec/model.py train_word2vec`

When Word2Vec done, you can start Kmean training:

`python word2vec/model.py train_kmean`


**Step3. Building Bug of Words model**

The process is similar to Word2Vec training:

Start data producer: <br>
`python manager.py producer:process bag_of_words.read_train_data_for_bagofwords`

Start pipelines processes: <br>
`python manager.py pipelines:run`

Start RandomForest training:
`python bag_of_words/model.py`

Done!


#### Things to note:

- Right now stairs `consumer_iter` is not very optimize for such
things. We are working on this. And in near future
stairs will be very friendly with NN models frameworks.

- Do not forgot that you can run multiple:
`pipeline:run` processes which makes everything work in parallel way

- In this example you can find how `apps` is good when you want
to use some algorithms in multiple places and have a chance to
easily modify logic inside. 


