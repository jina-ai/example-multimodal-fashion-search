FROM jinaai/jina:3.7.14-standard

COPY . /workspace
WORKDIR /workspace

RUN pip install streamlit==1.12.0

EXPOSE 8509

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
