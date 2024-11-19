#! /usr/bin/env python3.11

import sys
from argparse import ArgumentParser
import logging
from omegaconf import OmegaConf

from config import Config
from engine import Engine


LOG_FMT = "[%(asctime)s] %(levelname)s %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger()


def init_stdout_logger(conf: Config):
    logger.setLevel(conf.common.level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(conf.common.level)
    formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATEFMT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def param_parser():
    parser = ArgumentParser(description="mailing-service")
    parser.add_argument(
        "--config", help="path to configuration file", required=True
    )
    return parser.parse_args()


def load_config(path: str) -> Config:
    loaded_config = OmegaConf.load(path)
    schema = OmegaConf.structured(Config)
    config = OmegaConf.merge(schema, loaded_config)
    return config


def main():
    args = param_parser()
    config = load_config(args.config)
    init_stdout_logger(config)

    logger.debug(f"{OmegaConf.to_yaml(config)}")
    logger.info("Starting")

    engine = Engine(
        config=config,
        logger=logger
    )

    engine.run()

    logger.info("Stopped")


if __name__ == "__main__":
    exit(main())
