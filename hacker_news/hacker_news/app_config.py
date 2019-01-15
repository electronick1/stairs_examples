from stairs import App

app = App("hacker_news")

app.config.update(
    agregation_redis_host='localhost',
    agregation_redis_port=6379,
)
