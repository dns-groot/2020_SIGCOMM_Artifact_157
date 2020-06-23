FROM dnsgt/groot:SIGCOMM_AE

LABEL maintainer="sivakesava@cs.ucla.edu"

ENV HOME /home/groot

RUN sudo apt-get -yq install python3-pip && \
    pip3 install matplotlib

RUN rm -rf bin/groot_old.cpp \
       README.md \
       Dockerfile \
       .github \
       groot.sln


COPY README.md README.md

COPY sigcomm_artifact.sln sigcomm_artifact.sln 

COPY Dockerfile Dockerfile

COPY scripts/ scripts

RUN sudo chown -R groot:groot README.md  sigcomm_artifact.sln Dockerfile scripts

CMD [ "bash" ]
