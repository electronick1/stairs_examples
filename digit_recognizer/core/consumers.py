from core.app_config import app


@app.consumer_iter()
def deliver_train_data_to_model(image, label):
    return image, label


@app.consumer_iter()
def deliver_validation_data_to_model(image, label):
    return image, label
