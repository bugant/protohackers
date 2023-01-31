from python:3.11

COPY . /tmp/proto-smoke-test
RUN python3.11 -m pip install /tmp/proto-smoke-test

ENTRYPOINT ["proto-smoke-test"]
CMD ["echo-server"]
