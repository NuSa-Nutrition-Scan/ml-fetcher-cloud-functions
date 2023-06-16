# ML Fetcher Cloud Functions

The ML Fetcher Cloud Functions project is an implementation of long-running tasks using Google Cloud Functions in the Google Cloud Platform (GCP) environment. The purpose of this project is to offload a time-intensive task to Cloud Functions. The task involves generating a result model based on user input.

# Team:
Cloud Computing

## Technology Stack

- Google Cloud Functions 2nd Generation: Serverless compute platform provided by Google Cloud for executing event-driven functions.
- Firestore: NoSQL document database provided by Google Cloud for storing and retrieving data.

## Why Cloud Functions?

Cloud Functions is chosen as the execution platform for this task due to its serverless nature and ability to handle event-driven workloads. By using Cloud Functions, we can leverage the scalability and automatic scaling capabilities provided by Google Cloud. It allows us to focus on the application logic without worrying about server management or infrastructure scaling.

## How To
1. Create Code for cloud functions in the documentation in [here](https://cloud.google.com/functions/docs/writing#directory-structure-python)
2. Setup Makefile for deploying to cloud functions. See example [here](https://github.com/NuSa-Nutrition-Scan/ml-fetcher-cloud-functions/blob/main/Makefile.example). If you dont want to use Makefile, just copy the example to your terminal
3. Run `make run`
4. Start Testing

## License

This project is licensed under the [MIT License](https://github.com/NuSa-Nutrition-Scan/ml-fetcher-cloud-functions/blob/main/LICENSE).
