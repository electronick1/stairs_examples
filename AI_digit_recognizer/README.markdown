## Digit recognizer example.

### Installation:

```bash
pip install -r req.pip
```

Download data:

```bash
kaggle competitions download -c digit-recognizer
```

### The problem:

From kaggle:

In this competition, your goal is to correctly identify digits from a dataset 
of tens of thousands of handwritten images. We’ve curated a set of 
tutorial-style kernels which cover everything from regression to neural 
networks. We encourage you to experiment with different algorithms to learn 
first-hand what works well and how techniques compare.

Link to competition: https://www.kaggle.com/c/digit-recognizer/overview/description

Here we will try to process data (images and labels) using Stairs pipelines.



### Solution for this problem:

Solution for this problem based on [follwing](https://www.kaggle.com/yassineghouzam/introduction-to-cnn-keras-0-997-top-6)
kernel. 

In kernel above author reads and transforms all data in one process. This is 
not scalable solution. It's hard to parallelize this solution and in case
when we have more data than RAM allows - it could be a problem, which hard
to solve based on propose approach. 

Also, there is one major problem, if something failed during data processing
neural network training will be halted and it will be hard to continue.

Stairs could solve all this problems using data pipelines and streaming services.
It's fast, simple and fault tolerance. In case if something failed, Neural Network
training process will be paused and could be continued.


Overview of the project:

[image]

**First step. Reading data.** 

We start reading process in core.producers; `read_image` Producer reads a file
with training data, split data by training and validation, and then forward
all data to `prepare_image_for_nn` data pipeline (through streaming service).


As soon as all data will be consumed by Neural Network `read_image` Producer
will be executed again - until specified amount of epochs. 

To run this `read_image` producer, simply execute:

```bash
python manage.py producer:run start_kaggle_parsing
```

It will start reading process. 


**Second step. Processing data.**

`read_image` sends images and labels to `prepare_image_for_nn` data pipeline. 
Inside this pipeline we call functions one by one, and transform images to 
the right format and apply augmentations. 

We should run this pipeline in a separate from producer process. You 
can also specify how many processes should working on your data:


```bash
python manage.py pipelines:run -p 20
```

In the end of pipeline, we forward data to consumer called `deliver_train_data_to_model`
it allows you to transfer result data to neural network (through streaming service)

**Third (and last) step. Run model training process**

Simply run:
```bash
python model.py 
```

In this process we build a neural network and start consume data from data pipelines
directly to neural network. 

Consumer (based on redis queues) allows you to forward 15,000 images per sec
to neural network, it's a way faster then neural network training process can
handle.
