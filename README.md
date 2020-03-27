# Twitter Sentiment Analyzer

This project allows you to monitor sentiment on Twitter. By collecting tweets for a search query like `$TSLA` and generating a sentiment score, you can plot the overall Twitter sentiment for various companies.

**WARNING**: Running this app can cost you upwards of 500$ per year!

## How to run this

### Safeguards

Please set up budget alerts in your AWS account. The yearly cost of running this may exceed 500$ and I don't want any surprise bills for you.

### Prerequisites

1. You need an AWS account.
2. Create a DynamoDB table named `Tweets` or the name you set in `config.dev.json`.
3. Create a stream from that table and enter the stream ARN in the `config.dev.json`.
4. Install Python3 and pip on your computer.
5. Install Node on your computer.
6. Install the serverless framework on your computer.

### Configure

Create a Twitter app and generate OAuth 1 keys. Put those keys into the `config.dev.json`. Don't commit that to your own repository!

Adjust further configuration as you like in the config file `config.dev.json`.

### Deploy

1. Run `pip install -r requirements.txt` to install all the necessary python requirements.
2. Run `npm install` to install all the necessary deployment tooling.
3. Run `sls deploy` to deploy the application.

## Results

The cron job runs every 10 minutes. Once the cron has triggered and the collector AND analyzer have finished, you can find the sentiment scored tweets in your table (`Tweets` or whatever you called it).
