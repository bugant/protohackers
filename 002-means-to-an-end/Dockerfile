from python:3.11

COPY . /tmp/proto
RUN python3.11 -m pip install /tmp/proto

ENTRYPOINT ["proto-means-to-an-end"]
CMD ["avg-server"]
