FROM oraclelinux:9
WORKDIR /app
COPY dist/sockchat-0.0.1-py3-none-any.whl .
#RUN rpm install python
CMD sleep 100