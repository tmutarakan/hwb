FROM python:3.9-alpine
# set work directory
WORKDIR /app/
# install dependencies
RUN pip install --user -U aiogram==2.21 redis==4.3.4
ADD . .
ENTRYPOINT ["python", "app.py"]
