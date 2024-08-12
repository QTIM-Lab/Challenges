FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel

RUN apt-get update -y
RUN apt-get install -y libssl-dev
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libglib2.0-0

RUN pip install pydicom;
RUN pip install python-gdcm;
RUN pip install pandas;
RUN pip install scikit-learn;
RUN pip install opencv-python;

# CMD ["echo", "Test"]