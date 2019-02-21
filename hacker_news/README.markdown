## Hacker news example.

### Installation:

```bash
pip install -r req.pip
```

Please set GOOGLE_APPLICATION_CREDENTIALS or explicitly create credentials.  
For more information, please visit https://cloud.google.com/docs/authentication/getting-started


### The problem:

- Read X amount of data from Google Cloud
- Cleanup, filter and save localy hacker news posts
- Based on clean data calculate "sentiment" and "mentions" stats


Should be:

- Safe. We should not loose or duplicate any data
- Fast. Get all power from all available machine as possible.
- "Scalable". Should be easy to modify the logic and change pipelines
if data has changed.


### Solution:


**Step1. Reading and cleanup data**

We could read data from google cloud in two ways:

- one process which will ask google for data and then add items to
streaming service (workers)
- multiple processes which will in parallel punch google as many of 
your CPU available.


First approach could be realized by "app.producer" component. Which will
send one request, and iterate over response.

[Checkout](https://github.com/electronick1/stairs_examples/blob/master/hacker_news/hacker_news/producers.py#L17) 

To run this producer type:

`python manager.py producer:process hacker_news.read_google_big_table`



Second approach is a bit complicated but more powerful. 

We have 2 generators:

- first makes "batches".
- second process each batch in parallel way.

Checkout ->    

To generate "batches" run (it should be done once):

` python manager.py producer:init_session hacker_news.read_google_big_table_parallel`

Then you can run as many "workers" you want, which will 
read those batches. The overall system if quite safe from data lost:

`python manager.py producer:process hacker_news.read_google_big_table_parallel`

Both producers - control queue size and prevent memory overflow.


**Now** when reading process had started in the same time you can start
data processing, for this just run:

`python manager.py pipelines:run`

It will start reading queue based on defined pipeline [here]()

As you can see in [cleanup_and_save_localy](https://github.com/electronick1/stairs_examples/blob/master/hacker_news/hacker_news/pipelines.py#L13) pipeline
got multiple vars and:
- combine them to one DataFrame
- assign "Cleanup" flow, which will process text info
- assign "filter" flow, which will filter information.
- in the end "consumer" will be called, and data will be saved localy.

Important to note: 
There is standalone_consumer, which allow you to process data in separate
process, in case you have distributed system, it's allow you to save
data on one of your machine. Just run:

`python manager.py consumer:standalone hacker_news.save_topic_related_data`


**Step2. Reading and cleanup data**

Now when we cleanup and filter data, we could calculate any stats 
we want.

[Let's read it first](https://github.com/electronick1/stairs_examples/blob/master/hacker_news/hacker_news/producers.py#L48)

Now we made a pipeline which allows to calculate this data in "parallel"
way, just marked some subscribe/apply function "as_worker".


[Checkout whole pipeline](https://github.com/electronick1/stairs_examples/blob/master/hacker_news/hacker_news/pipelines.py#L56)

In the end we could save stats in redis using simple "consumer" which will be
run inside "pipelines:run" (don't need special process for this.)



### Result

You can see all "stats" inside redis (`sentiment` or `libs` keys).

As a result we have a system, which quite easy to tune and run in 
distributed/parallel way.

For example:

If you want for example to use another "filtering" topic, just make another
pipeline and call `cleanup_and_save_localy` with another config:

```python
@app.pipeline()
def my_cleanup_and_save_localy(pipeline, score, time, type, text):
    hacker_news_record = concatenate(
        score=score,
        time=time,
        type=type,
        text=text
    )
    
    return hacker_news_record.subscribe_pipeline(
        cleanup_and_save_localy,
        config=dict(filter_comments=dict(topic='MyCustomTopic'))   
    )

```

Then you can even call this pipelines simultaneously:

```python
@app.producer(cleanup_and_save_localy, my_cleanup_and_save_localy)
def read_google_big_table():
    #.........
    # ........
```

You have always a clear view of whats going on in your system.


Another example:

If you want to change how Flow inside pipeline operate, just inherite flow call
and change some step:

```python

class MyPrepareText(PrepareText):

    @step(apply_steming)
    def filter_stop_words(self, words):
        # USING SPANISH STOPWORDS
        stop_words = set(stopwords.words('spanish'))
        words = [w for w in words if not w in stop_words]
        return dict(
            words=words
        )
```

Then replace this flow in pipeline (or paste inside config). 
 