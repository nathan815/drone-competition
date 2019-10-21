import logging

log_format = '%(asctime)s %(levelname)-8s %(name)-20s %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=log_format,
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./web.log')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(log_format, datefmt='%H:%M:%S')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)
