FROM python:3.11.0-slim

WORKDIR /app
COPY flask_api.py /app
COPY . /app

# Install necessary build tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends sudo swig libgl1-mesa-glx build-essential libglib2.0-0 make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create a virtual environment and activate it
RUN python3 -m venv .venv \
    && echo "source .venv/bin/activate" >> ~/.bashrc \
    && . .venv/bin/activate

# Install packages and clean up
RUN pip install --no-cache-dir flask werkzeug pinecone-client openai schedule wget textract common dual tight data prox groq \
    && pip install --no-cache-dir -r pms/requirements_aws_py3_10.txt \
    && find /usr/local/lib/python3.11 -name '__pycache__' -exec rm -rf {} + \
    && find /usr/local/lib/python3.11 -name '*.pyc' -delete

# Remove unnecessary files and directories
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 5000
CMD ["python3", "flask_api.py", ".env_demo"]











