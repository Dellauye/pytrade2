import logging
from datetime import datetime, timedelta
from threading import Thread


class PeriodicalLearnStrategy:
    def __init__(self, config):
        self.learn_interval: timedelta = timedelta(seconds=config['biml.strategy.learn.interval.sec'])
        self.last_learn_time: datetime = datetime.min

    def learn_or_skip(self):
        time1 = datetime.now()
        if time1 - self.last_learn_time >= self.learn_interval:
            logging.info(f"{self.learn_interval} elapsed from last learn time{self.last_learn_time}")
            Thread(target=self.learn).start()
            self.last_learn_time = time1

    def learn(self):
        raise NotImplementedError()