FROM python:3.9-bullseye

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt

EXPOSE 8509

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
