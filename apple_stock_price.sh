#!/bin/bash

# Download the webpage HTML
curl -s "https://www.boursorama.com/cours/AAPL/" > webpage.txt
html2text webpage.txt | awk -F' *\\|' 'NR>2 {gsub(/^\||.\b/, ""); $1=$1; print}' > apple_boursorama.txt

# Extract the current stock price
(grep -A1 'CoursAPPLE' apple_boursorama.txt | tail -n1) > apple_stock.txt

# Output the current price
#cat apple_stock.txt
