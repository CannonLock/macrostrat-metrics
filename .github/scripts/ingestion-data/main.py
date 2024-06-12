import requests
import json
from datetime import date

INGESTION_URL = "https://dev2.macrostrat.org/api/ingest/ingest-process?page=0&page_size=10000"
DATA_PATH = "ingestion-metrics"

METRIC_SCHEMA = {
    "total": 0,
    "states": {},
    "tags": {}
}


def get_latest_metrics():

    # Copy the metric schema to avoid side effects
    metrics = METRIC_SCHEMA.copy()

    response = requests.get(INGESTION_URL, headers={"Content-Type": "application/json"})
    data = response.json()

    metrics['total'] = len(data)

    for ingest in data:
        increment_key(ingest['state'], metrics['states'])

        for tag in ingest['tags']:
            increment_key(tag, metrics['tags'])

    return metrics


def increment_key(key, dictionary):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def main():
    metrics = get_latest_metrics()

    # Write the metrics to the data path and the latest.json file
    with open(f"{DATA_PATH}/{date.today()}.json", "w") as f:
        json.dump(metrics, f)

    with open(f"{DATA_PATH}/latest.json", "w") as f:
        json.dump(metrics, f)


if __name__ == "__main__":
    main()
