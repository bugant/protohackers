from python:3.11

COPY . /tmp/proto-prime-time
RUN python3.11 -m pip install /tmp/proto-prime-time

ENTRYPOINT ["proto-prime-time"]
CMD ["prime-server"]
