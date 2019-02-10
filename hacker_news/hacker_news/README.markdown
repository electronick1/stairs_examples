### App structure

Here you can see different app components, which help's you
to have a better visual structure of your data handlers. 

Stairs recommends to have customers, producers and pipelines
in different places, but you are completely free to use
any structure you want. 


The main things which defines your app is `App` object.

```python
from stairs import App
app = App("hacker_news")
```

Then based on "app" object you can create any stairs components
you want. 

Do not forgot to register this app in project, for this
simple add app name to config file or 

```python

from stairs import get_project
get_project().add_app(app)
```

By default stairs store app inside `app_config.py` module.

The whole process looks like this:

Producer -> Pipeline (functions, flows) -> Consumer

Just start from producer, and you will see where you data
will be next. 
