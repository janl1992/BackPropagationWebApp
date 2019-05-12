FROM python:3
ADD . /BackEnd 
WORKDIR /BackEnd
RUN pip install matplotlib
RUN pip install numpy
RUN pip install dataclasses
RUN pip install HTTPServer
EXPOSE 8080
CMD ["python", "WebServer.py", "8080"]