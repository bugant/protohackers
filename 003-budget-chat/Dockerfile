from python:3.11

COPY . /tmp/proto
RUN python3.11 -m pip install /tmp/proto

ENTRYPOINT ["proto-budget-chat"]
CMD ["chat-server"]
