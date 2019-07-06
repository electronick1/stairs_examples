from core.app_config import app


@app.consumer_iter()
def deliver_train_data_to_model(image, label):
    """
    Forward result data to streaming service, which then will be handle by
    neural network.

    This is a "worker" function by default.

    You can add additional data processing here.
    """
    return image, label


@app.consumer_iter()
def deliver_validation_data_to_model(image, label):
    return image, label
