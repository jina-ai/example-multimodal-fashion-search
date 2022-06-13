FROM jinaai/jina:3.6.2-py39-standard

COPY . /workspace
WORKDIR /workspace

RUN pip install streamlit==1.9.0

EXPOSE 8509

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
