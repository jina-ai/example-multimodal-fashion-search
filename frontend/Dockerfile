#FROM jinaai/jina:2.6.2-py39-standard
FROM python:3.9-bullseye

# setup the workspace
COPY . /workspace
WORKDIR /workspace

#RUN apt-get update && apt-get install --no-install-recommends -y build-essential g++\
    #&& pip install -r requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8509

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
