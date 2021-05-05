# Ethereum Mining Monitor

[![CodeFactor](https://www.codefactor.io/repository/github/verbalinsurection/EthereumMiningMonitor/badge)](https://www.codefactor.io/repository/github/verbalinsurection/ethereumminingmonitor)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Verbalinsurection_EthereumMiningMonitor&metric=alert_status)](https://sonarcloud.io/dashboard?id=Verbalinsurection_ethereumminingmonitor)

:warning: **Work in progress - Feel free to participate !**

:warning: **Clone with submodule** :warning:

To clone repo with submodules :

```bash
git clone https://github.com/.....
git submodule init
git submodule update
```

## Introduction

Python script to track your mining informations and push to InfluxDb

- It use my [EthMiningFetcher module](https://github.com/Verbalinsurection/EthMiningFetcher)
- For now, only Ethermine is supported
- **Docker image can be found at [https://hub.docker.com/r/verbalinsurection/ethereumminingmonitor](https://hub.docker.com/r/verbalinsurection/ethereumminingmonitor)**

### Informations retrieved

- Wallet value - From [Etherscan](https://etherscan.io/) (need etherscan API key)
- Ethereum price, evolution, ATH - From [Coingecko](https://www.coingecko.com/)
- Ethermine pool - From [Ethermine](https://ethermine.org/)
  - Unpaid income
  - Treshold
  - Date of last payout
  - *Calculated next payout (based on estimated earnings from Ethermine)*
  - Progression for next payout
  - *Estimated income (based on estimated earnings from Ethermine) and compared to : (From [Coincalculators](https://www.coincalculators.io))*
    - *Estimated income based on reported hashrate*
    - *Estimated income based on graphic card theorical hashrate (you have to set this). The goal is to compare the income to a no optimized CG raw hashrate from Coincalculators result*
    - *Estimated income based on average gain since last payout*
  - Reported hashrate, actual, historical data over 3 range, shares
  - Workers informations

### InfluxDb downsampling

The app automatically create all the needs for downsampling data:

- Create *daily* policy with infinite retention
- Update *autogen* policy with 40 days retention
- Create 2 continuous query:
  - Downsampling mining gain (daily eth gain)
  - Downsampling wallet value (daily eth and fiat value)
If policy or continuous query is manually modified, the app ovewrite them.

## Python informations

### Version

Write using Python 3.9

### Dependency

- schedule==0.6.0
- influxdb==5.3.0

## Configuration

:construction: Use of config file is on the way :construction:

### Set environment variable

| Variable name       | Required | Default | Description                                       | Exemple |
| ------------------- | -------- | ------- | ------------------------------------------------- | ------- |
| `LOGLEVELCONSOLE`   | False    | `20`    | Set the level of console output | `10` |
| `WALLET`            | **True** |         | The wallet you use for pool | `0x168d4F3316fCD48102744a6984FdB5e4d57b1ed7` |
| `ETHERSCAN_API`     | **True** |         | Api key from [Etherscan](https://etherscan.io/apis) | `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` |
| `FIAT`              | False    | `usd`   | The fiat you want to use from [Coingecko](https://api.coingecko.com/api/v3/simple/supported_vs_currencies) | `eur` |
| `THEORICAL_HRATE`   | False    | `100`   | Theorical hashrate from your rig | `180` |
| `SCHEDULE_UPDATE_S` | False    | `60`    | Interval in seconds between update | `600` |
| `INFLUX_HOST`       | **True** |         | InfluxDb host adress | `myinflux.lan` |
| `INFLUX_PORT`       | False    | `8086`  | InfluxDb host port | `8086` |
| `INFLUX_DB`         | **True** |         | InfluxDb database | `ethereum_mining` |
| `INFLUX_USER`       | **True** |         | InfluxDb user | `my_user` |
| `INFLUX_PASS`       | **True** |         | InfluxDb password | `my_pass` |
| `PURGE`             | False    | Empty   | Set this to `PURGE` to remove all measurments in the database | `PURGE` |

### Logging Levels

| Level    | Numerical value |
| -------- | :-------------: |
| CRITICAL | `50`            |
| ERROR    | `40`            |
| WARNING  | `30`            |
| INFO     | `20`            |
| DEBUG    | `10`            |
| NOTSET   | `0`             |

## :construction: Things to do

- More things...

## Yeah :wink: you can donate but there is no real reson to do this

- ETH : 0x168d4f3316fcd48102744a6984fdb5e4d57b1ed7 (you can target your rig to this for some minutes on ethermine :) )
- TRX : TLLBe2pvo3WcxPMALjpJySursJQiHQ48yu
- BTC : 12VVvqiimyaew5SskgzkWsVwnXARR83iE6
- XRP : rLADRnxwS5M7LFgrC9zmn3jmU9Vnc98Dh9
- ZEC : t1b26RYTcq77YYuyTsvfbFktYKoTN4QmFiz
