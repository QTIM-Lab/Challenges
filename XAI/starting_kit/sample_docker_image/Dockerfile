FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel

RUN apt update -y;
RUN apt-get install -y libssl-dev;
RUN pip install pydicom;
RUN pip install python-gdcm;
RUN pip install pandas;
RUN pip install scikit-learn;

CMD ["echo", "Test"]