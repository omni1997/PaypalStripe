import logging
import os

filename = os.path.splitext(os.path.basename(__file__))[0]

logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s - {filename} - %(message)s',
    datefmt='%H:%M:%S'
)

if __name__ == '__main__':
    logging.info('[START]')
    logging.info('[ END ]')