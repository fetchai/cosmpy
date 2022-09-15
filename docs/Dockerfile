FROM python:3.7
RUN pip3 install --no-cache-dir pipenv

WORKDIR /app
ADD Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy
RUN mkdir /app/site

ENTRYPOINT [ "mkdocs" ]
CMD ["build"]
