FROM python:3.10.13

WORKDIR /app/morph

RUN apt-get update && \
    apt-get install -y mecab mecab-ipadic-utf8 python3-mecab git make curl xz-utils file && \
    apt-get clean

    
RUN wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz && \
    tar xvfz mecab-0.996-ko-0.9.2.tar.gz && \
    cd mecab-0.996-ko-0.9.2 && \
    ./configure && \
    make && \ 
    make install && \
    cd ..
    
RUN wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz && \
    tar xvfz mecab-ko-dic-2.1.1-20180720.tar.gz && \
    cd mecab-ko-dic-2.1.1-20180720 && \
    ./configure && \
    ./autogen.sh && \
    tools/add-userdic.sh && \
    make && \
    make install && \
    cd ..

# RUN git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git && \
#     cd mecab-python-0.996 && \
#     python3 setup.py build && \
#     python3 setup.py install

# WORKDIR /morph

COPY ./ .

RUN pip install --no-cache-dir -r /app/morph/requirements.txt

# # FastAPI 실행
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10092"]