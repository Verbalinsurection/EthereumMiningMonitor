#!/usr/bin/python3

from datetime import datetime

import EthMiningFetcher as EMF
from logger import LOG


class EthData():
    def __init__(self, wallet, etherscan_api_key, fiat_code, theorical):
        self.__coin_info = EMF.Coin(fiat_code, 'ethereum')
        self.__pool_info = EMF.Ethermine(wallet, False)
        self.__wallet_info = EMF.EtherWallet(etherscan_api_key, wallet)
        self.__earn_calc = EMF.CoinCalculators('ethereum')
        self.__theorical = theorical
        self.__status = {}

    def update(self):
        dt_update = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        try:
            LOG.debug('Update coin info')
            if self.__coin_info.update():
                self.__status.update(
                    {'coin': self.__coin_info.last_update.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ")})
            else:
                LOG.warning('Update coin info failed: ' +
                            str(self.__coin_info.last_error))
        except AttributeError as e:
            LOG.warning('Update coin info failed: ' + str(e))

        try:
            LOG.debug('Update pool info')
            if self.__pool_info.update():
                self.__status.update(
                    {'pool': self.__pool_info.stat_time.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ")})
            else:
                LOG.warning('Update pool info failed: ' +
                            str(self.__pool_info.last_error))
        except AttributeError as e:
            LOG.warning('Update pool info failed: ' + str(e))

        try:
            LOG.debug('Update wallet info')
            if self.__wallet_info.update():
                self.__status.update({'wallet': dt_update})
            else:
                LOG.warning('Update wallet info failed: ' +
                            str(self.__wallet_info.last_error))
        except AttributeError as e:
            LOG.warning('Update wallet info failed: ' + str(e))

        try:
            LOG.debug('Update earning info')
            tmp_earn = \
                self.__earn_calc.get_calcul(self.__pool_info.reported_hrate)
            if tmp_earn is not None:
                self.__status.update({'earning_reported': dt_update})
                self.__earn_reported = tmp_earn
            else:
                LOG.warning('Update reported earning info failed: ' +
                            str(self.__wallet_info.last_error))

            tmp_earn = self.__earn_calc.get_calcul(self.__theorical)
            if tmp_earn is not None:
                self.__status.update({'earning_theorical': dt_update})
                self.__earn_theorical = tmp_earn
            else:
                LOG.warning('Update theorical earning info failed: ' +
                            str(self.__wallet_info.last_error))
        except AttributeError as e:
            LOG.warning('Update earning info failed: ' + str(e))

    def __data_wallet(self, dt_point):
        fields = {}
        fields['balance_eth'] = self.__wallet_info.balance
        fields['balance-fiat'] = round(
            self.__wallet_info.balance * self.__coin_info.price, 2)

        return {
            'measurement': 'wallet',
            'time': dt_point,
            'fields': fields,
            'tags': {
                'wallet': self.__wallet_info.wallet,
                'fiat': self.__coin_info.fiat,
            }
        }

    def __data_coin(self, dt_point):
        fields = {}
        fields['price'] = self.__coin_info.price
        fields['ath'] = self.__coin_info.ath
        fields['pc_24h'] = self.__coin_info.pc_24h

        return {
            'measurement': 'coin',
            'time': dt_point,
            'fields': fields,
            'tags': {
                'fiat': self.__coin_info.fiat,
            }
        }

    def __data_pool_info(self, dt_point):
        fields = {}
        fields['reported'] = self.__pool_info.reported_hrate
        fields['actual'] = self.__pool_info.current_hrate
        fields['theorical'] = self.__theorical
        fields['valid'] = self.__pool_info.valid_shares
        fields['stale'] = self.__pool_info.stale_shares
        fields['reject'] = self.__pool_info.invalid_shares
        fields['workers'] = self.__pool_info.active_workers
        fields['unpaid'] = self.__pool_info.unpaid_balance
        fields['min_payout'] = self.__pool_info.min_payout
        fields['next_payout'] = datetime.isoformat(
                    self.__pool_info.next_payout)
        fields['last_payout'] = datetime.isoformat(
                    self.__pool_info.payouts[0].paid_on)

        return {
            'measurement': 'pool',
            'time': dt_point,
            'fields': fields,
            'tags': {
                'wallet': self.__pool_info.wallet,
                'pool': self.__pool_info.pool_name,
            }
        }

    def __data_worker_info(self, dt_point, worker):
        fields = {}
        fields['reported'] = worker.reported_hrate
        fields['actual'] = worker.current_hrate
        fields['valid'] = worker.valid_shares
        fields['stale'] = worker.stale_shares
        fields['reject'] = worker.invalid_shares

        return {
            'measurement': 'worker',
            'time': dt_point,
            'fields': fields,
            'tags': {
                'wallet': self.__pool_info.wallet,
                'pool': self.__pool_info.pool_name,
                'worker': worker.name,
            }
        }

    def __data_gain_info(self, dt_point, ref, label):
        fields = {}
        fields['hour'] = ref.eth_hour
        fields['hour_fiat'] = round(ref.eth_hour * self.__coin_info.price, 2)
        fields['day'] = ref.eth_day
        fields['day_fiat'] = round(ref.eth_day * self.__coin_info.price, 2)
        fields['week'] = ref.eth_week
        fields['week_fiat'] = round(ref.eth_week * self.__coin_info.price, 2)
        fields['month'] = ref.eth_month
        fields['month_fiat'] = round(ref.eth_month * self.__coin_info.price, 2)

        return {
            'measurement': 'earnings',
            'time': dt_point,
            'fields': fields,
            'tags': {
                'wallet': self.__pool_info.wallet,
                'pool': self.__pool_info.pool_name,
                'earnings': label,
            }
        }

    def __data_status(self, dt_point):
        fields = {}
        for entry in self.__status:
            fields[entry] = self.__status[entry]

        return {
            'measurement': 'status',
            'time': dt_point,
            'fields': fields,
        }

    @property
    def formated_data(self):
        dt_point = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        data_points = []
        try:
            data_points.append(self.__data_wallet(dt_point))
            data_points.append(self.__data_coin(dt_point))
            data_points.append(self.__data_pool_info(dt_point))
            for worker in self.__pool_info.workers:
                data_points.append(self.__data_worker_info(dt_point, worker))
            data_points.append(self.__data_gain_info(
                dt_point, self.__pool_info.eth_pay_stats, 'estimated'))
            data_points.append(self.__data_gain_info(
                dt_point, self.__pool_info.eth_pay_from_last, 'real'))
            data_points.append(self.__data_gain_info(
                dt_point, self.__earn_reported, 'reported'))
            data_points.append(self.__data_gain_info(
                dt_point, self.__earn_theorical, 'theorical'))
            self.__status.update({'data': dt_point})
            data_points.append(self.__data_status(dt_point))
        except AttributeError as e:
            LOG.error('Unable to create data points: ' + str(e))
            return None

        return data_points
