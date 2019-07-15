FROM python:3.7.2

RUN mkdir -p /currency_service
RUN useradd -ms /bin/bash appuser
RUN chown -R appuser:appuser /currency_service

RUN mkdir -p /opt/runtime/
ADD scripts/* /opt/runtime/
USER appuser

ENTRYPOINT ["/opt/runtime/entrypoint.sh"]
CMD ["make", "runserver"]
