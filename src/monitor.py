#!/usr/bin/python3

from time import sleep

import schedule

from config import conf
from ethdata import EthData
from influx import Idbc
from logger import LOG
import EthMiningFetcher as EMF


__version__ = '1.2.1'


def data_process(ethdata, idbc):
    LOG.debug('Starting data process')

    ethdata.update()

    formated_data = ethdata.formated_data
    if formated_data is None:
        LOG.error('No data for InfluxDb')
        return
    for data_line in formated_data:
        LOG.debug(data_line)

    LOG.debug('Writing data to InfluxDb')
    if not idbc.write_data(formated_data):
        LOG.error('Error on writing data to InfluxDb')
        LOG.error(idbc.last_error)

    formated_payouts = ethdata.formated_payouts
    if formated_payouts is None:
        LOG.error('No payouts data for InfluxDb')
        return
    for data_line in formated_payouts:
        LOG.debug(data_line)

    LOG.debug('Writing payouts data to InfluxDb')
    if not idbc.write_data(formated_payouts, 'daily'):
        LOG.error('Error on writing data to InfluxDb')
        LOG.error(idbc.last_error)

    LOG.debug('Data process done')


if __name__ == "__main__":
    if len(conf.error) > 0:
        for err in conf.error:
            LOG.critical('Environment variable not set: ' + err)
        exit(1)

    title = 'Ethereum Mining Monitor - ' + __version__
    fetcher_version = '(fetcher version: ' + EMF.__version__ + ')'

    LOG.info('╔' + '═' * 78 + '╗')
    LOG.info('║' + title.center(78, ' ') + '║')
    LOG.info('║' + fetcher_version.center(78, ' ') + '║')
    LOG.info('╟' + '─' * 78 + '╢')
    for confentry in conf.conf_array:
        LOG.info('║ ' + confentry[0].ljust(18) +
                 '\t-> ' + str(confentry[1]).ljust(54) + '║')
    LOG.info('╚' + '═' * 78 + '╝')

    idbc = Idbc(conf.influx_db,
                conf.influx_host,
                conf.influx_user,
                conf.influx_pass,
                conf.influx_port)

    if conf.purge == "PURGE":
        LOG.warning('Purge DB')
        idbc.purge()

    ethdata = EthData(conf.wallet,
                      conf.etherscan_api,
                      conf.fiat,
                      conf.theorical_hrate)
    data_process(ethdata, idbc)

    schedule.every(conf.schedule_update).seconds.do(data_process,
                                                    ethdata,
                                                    idbc)

    while True:
        schedule.run_pending()
        sleep(1)
