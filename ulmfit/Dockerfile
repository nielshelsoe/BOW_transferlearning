FROM nvcr.io/nvidia/pytorch:19.01-py3
RUN pip install wheel
RUN pip install fastai
RUN pip install pandas
RUN pip install jupyter
RUN pip install numpy
RUN pip install sklearn
volume ["/ulmfit"]
WORKDIR /ulmfit
EXPOSE 8888
