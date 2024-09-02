# fearandgreed

This Python script fetches the latest value and indications of the CNN Fear and Greed Index and stores the data in a JSON file.

## Key Features

- Retrieves the latest Fear and Greed Index data from CNN.
- Stores the fetched data as a JSON file with a timestamp.
- Easily modifiable to write data to any kind of database instead of a JSON file.
- Designed to run once per day as the Fear and Greed Index is updated only once per trading day, after market close.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/drhdev/fearandgreed.git
    cd fearandgreed
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script manually:

```bash
python3 fearandgreed.py
```

### Automate with Cron Job

Since the Fear and Greed Index is updated once per trading day after the market close, it's sufficient to run this script once a day at midnight NYC time. You can set up a cron job on your server to automate this:

1. Open the crontab editor:

    ```bash
    crontab -e
    ```

2. Add the following line to run the script daily at midnight NYC time:

    ```bash
    0 0 * * * /usr/bin/python3 /path/to/your/fearandgreed.py
    ```

## Customization

- **Data Storage**: The script saves the data to a JSON file as an example. You can easily modify the `save_data_to_json()` function to store the data in a database or any other format that suits your needs.

## License

This project is licensed under the GPL v3 License.
