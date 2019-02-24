## Hacker news example.

### Installation:

```bash
pip install -r req.pip
```

### The problem:

There is a ton of discussions happened in kaggle. A lot of people presenting
different solutions and explain how each solution works. 

In this example we want to parse kaggle competitions discussions and map each
competition with github repo (solution).

Is a standard scraping task and here you will find examples of how it could be
easily solved using stairs. 


### Solution for this problem:

Let's apply  brute force for this task. We will define pipeline which will grab
and parse three different pages:
- competitions page (Parse a list of all competitions)
- discussions page (Parse all discussion for each competitions)
- discussions page with a lot of comments

First page will generate a lot of links to second. Second a lot of links to
third. 
The idea is to run a ton of processes for each link and with stairs it will be
super easy to do. 

To solve this problem we could use thing called `subscribe_flow_as_producer`.
This method will subscribe Flow which could return list of objects. Each of this
object will be separately put into next pipeline step. 

As a result we will have following pipeline:

```python

@app.pipeline()
def parse_gh_repos(pipeline, competitions_url):
    return competitions_url\
        .subscribe_flow_as_producer(ExtractCompetitions(), as_worker=True)\
        .subscribe_flow_as_producer(ExtractDiscussions(), as_worker=True)\
        .subscribe_flow_as_producer(SearchForGHRepos(), as_worker=True)\
        .subscribe_consumer(save_gh_repo)
```

Each flow in this pipeline could return list of objects. Also each flow will be
a worker and everything will be executed in a parallel way. 

To make everything work just run producer:

```bash
python manager.py producer:process start_kaggle_parsing
```

And then start pipelines execution:

```bash
python manager.py pipelines:run
```

^ this is only one process which will be boring to run, you can specified amount
of processes and try to burn out your CPU :)

```python
python manager.py pipelines:run concurrency 100
```
^ This command will run 100 processes which will send a ton of requests to kaggle.



### Take aways

Still, multiprocessing way is not the optimal to solving "scrapping" tasks, so
in the near future it will be possible to run some steps (flows) using python async
methods. It will be possible to apply async only when its needed. Now image how
cool it will be to have "distributed async" system to process your data.
 