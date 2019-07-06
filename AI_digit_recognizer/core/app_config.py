import imgaug.augmenters as iaa

from stairs import App


app = App("core")

app.config.update(dict(
    train_data_file_path='data/train.csv'
))

app.config.update(dict(
    num_epoch=3,
    num_classes=10,
    steps_per_epoch=41990,
    num_validation_images=10
))


app.config.update(dict(
    image_h=28,
    image_w=28,
))


app.config.update(dict(
    data_augmentation=iaa.Sequential([
        iaa.Fliplr(0.5),
        iaa.Affine(translate_px={"x": (-40, 40)}, rotate=(-45, 45)),
        iaa.Crop(px=(0, 10)),
        iaa.Resize({"height": app.config.image_h,
                    "width": app.config.image_w})

    ])
))