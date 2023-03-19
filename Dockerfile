# Python Poetry for Building Docker Images
# https://binx.io/2022/06/13/poetry-docker/
# Dockerize Your Python Command-Line Program
# https://medium.com/swlh/dockerize-your-python-command-line-program-6a273f5c5544

FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app


FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv

# CMD ["bash"]

# https://dteslya.engineer/blog/2022/07/14/how-to-run-a-python-cli-tool-inside-a-docker-container/
# Entrypoint script
# COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
# RUN chmod +x /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

