# Aws Api Data Processing

News API Data Collection and Querying

## Description

This project is designed to collect news articles from a news API at regular intervals using an AWS Lambda function and store them in two separate S3 buckets - one with the raw JSON data and the other with the same data in CSV format. A Python Flask-based website is also developed to allow users to search for articles based on various parameters such as name, title, description, and content.

## Architecture
The architecture of the project involves the following components:

- An AWS Lambda function that runs every 4 hours to collect news articles from the news API.
- Two S3 buckets - one to store the raw JSON data and the other to store the data in CSV format.
- A Python Flask-based website hosted on an EC2 instance that allows users to query the data stored in the S3 buckets.

# Technologies Used
The following technologies are used in this project:

- AWS Lambda
- Amazon S3
- Python Flask
- AWS EC2
- Pandas Library

# Usage

The website allows users to search for news articles based on various parameters such as name, title, description, and content. The user can enter a search query in the search bar and hit the search button. The website then displays the relevant articles along with their details.

## Contributing
To contribute to the project, follow the steps below:

1. Fork the repository.
2. Create a new branch.
3. Make the desired changes and commit them.
4. Push the changes to the forked repository.
5. Create a pull request.

## Credits
The following resources were used in developing this project:

- AWS documentation
- News API documentation
- Flask documentation