FROM jinaai/jina:3.0.0-py39-standard

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN pip install streamlit==1.2.0

EXPOSE 8509

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
