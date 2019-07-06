from stairs import App

app = App('kaggle_to_github')


app.config.update(
    cnt_competition_pages = 50,
    kaggle_competition_page = "https://www.kaggle.com/competitions.json",
)
