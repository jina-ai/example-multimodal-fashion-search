FROM python:3.9-bullseye

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN pip install jina[client]==3.0.0 streamlit==1.2.0

EXPOSE 8509

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
