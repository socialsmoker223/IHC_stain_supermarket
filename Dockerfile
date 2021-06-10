FROM gcr.io/deeplearning-platform-release/base-cpu:latest 

COPY . /opt/app
WORKDIR /opt/app
#RUN apt-get update -y 
# # install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8080", "--server.address=0.0.0.0"]