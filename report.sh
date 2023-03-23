#!/bin/bash

# Download the webpage HTML
curl -s "https://www.boursorama.com/cours/AAPL/" > webpage.txt
html2text webpage.txt | awk -F' *\\|' 'NR>2 {gsub(/^\||.\b/, ""); $1=$1; print}' > apple_boursorama.txt

# Extract info 
(grep -A1 'ouverture' apple_boursorama.txt | tail -n1) > ouverture
(grep -A1 'clÃ´ture veille' apple_boursorama.txt | tail -n1) > cloture
(grep -A2 "Qu'est-ce que le risque ESG ?" apple_boursorama.txt | tail -n1) > risque_ESG
