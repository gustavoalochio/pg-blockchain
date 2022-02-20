FROM python:3.8.12-alpine3.15
COPY . /app
WORKDIR /app
# RUN pip3 install pipenv
# RUN pipenv install --system --deploy --ignore-pipfile
# RUN pipenv update
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
