FROM python:3.6

#mount folder in
VOLUME [ "/project" ]

#add the requriments.txt
ADD requirements.txt /

#pip install the libs there are neede for the scirpt to run
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#set workdir
WORKDIR /project

#expose port 8888 for jupyter
EXPOSE 8888