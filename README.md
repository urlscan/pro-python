urlscan Pro Python Tool
=======================

This is a very basic tool to query the urlscan Pro API for different brands and
return the recent pages detected as phishing for that brand.

Usage
-----

1. Generate an API-Key for your account on urlscan.io
2. Install the required dependencies from requirements.txt: `pip install -r requirements.txt`
3. Run the script

# Get a list of brands
`python query.py showbrands --apikey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

# Get the latest phishing sites targeting a specific brand
`python query.py showlatest --brand leumi --apikey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx --since 24h --limit=100`

# Get the latest phishing sites targeting all brands
`python query.py showlatest --apikey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx --since 1h --limit=100`

# Add a query string
`python query.py showlatest --apikey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx --since 1h --limit=100 --query "NOT task.source:(phishtank OR openphish)"`

Questions
---------
Please send questions and feedback to info@urlscan.io
