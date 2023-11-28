<h1 align="centre">
   <img src="https://i.imgur.com/ycFUTNy.png">
</h1>

# Table of Contents
- [Introduction](#introduction) <br>
- [Requirements](#requirements) <br>
- [DB Schema](#db-schema) <br>
- [Documentation](#documentation) <br>
- [How to use](#how-to-use) <br>
- [Contribution](#contribution)

# Introduction
-	In the era of information overload, the "Text Summarization and Information Extraction Tool" is an innovative project designed to empower users with efficient and intelligent methods for processing textual content. This tool combines the capabilities of Natural Language Processing (NLP) and web scraping to facilitate text summarization and information retrieval from both user-provided text and online sources, such as Wikipedia articles.

# Requirements
For running the code, make sure that the following are installed on your local device.
|||
|--|--|
| [Python 3.11.x](https://www.python.org/) | <img src="https://i.imgur.com/SBirLsy.png" style="width:135px; height:20px;" alt="python3.11.x"> |
| [Streamlit 1.27.x](https://streamlit.io) | <img src="https://i.imgur.com/M8mzSyY.png" style="width:135px; height:20px;" alt="Streamlit1.27.x"> |
| [spacy 3.6.x](https://spacy.io) | <img src="https://i.imgur.com/Q9lPxGj.png" style="width:135px; height:20px;" alt="spacy3.6.x"> |
| [requests 2.31.x](https://pypi.org/project/requests/) | <img src="https://i.imgur.com/mprriAB.png" style="width:135px; height:20px;" alt="requests2.31.x"> |
| [pdfplumber 0.10.x](https://pypi.org/project/pdfplumber/) | <img src="https://i.imgur.com/86qztGR.png" style="width:135px; height:20px;" alt="pdfplumber0.10.x"> |
| [beautifulsoup4 4.12.x](https://pypi.org/project/beautifulsoup4/) | <img src="https://i.imgur.com/DqvfPbg.png" style="width:135px; height:20px;" alt="beautifulsoup44.12.x"> |

# DB Schema Design
The app has SQLite named **database.sqlite3** database with 7 tables in the database folder. These tables store user and manager credentials, categories and products managers add, a table to keep track of user purchases, sales for managers and cart to keep track of user items.

|Table Name|Column Details|
|----------|--------------|
|managers|manager_id(integer, primary key), username(string), password(string)|
|users|user_id(integer, primary key), username(string), password(string), email(string)|
|categories|category_id(string, primary key), name(string), search(string)|
|products|product_id(string, primary key), category_id(string), name(string), search(string), price(numeric), stock(numeric), unit(string), fractal_allowed(string)|
|cart|cart_id(string, primary key), user_id(string), product_id(string_, quantity(numeric), unit(string), price(numeric)|
|sales|product_id(string, primary key), category_id(string), quantity(numeric), sale(numeric)|
|purchases|Transaction_id(string, primary key), user_id(string), price(numeric), date(string)|

# Documentation
insert link

# How to use
1. Clone this repo. <br>

1. Install the required libraries from [Requirements](#requirements) <br>
1. Execute the python script <br>
1. Add star to this repo if you liked it 😄
   
# Contribution 
**This section provides instructions and details on how to submit a contribution via a pull request. It is important to follow these guidelines to make sure your pull request is accepted.**
1. Before choosing to propose changes to this project, it is advisable to go through the readme.md file of the project to get the philosphy and the motive that went behind this project. The pull request should align with the philosphy and the motive of the original poster of this project.
2. To add your changes, make sure that the programming language in which you are proposing the changes should be same as the programming language that has been used in the project. The versions of the programming language and the libraries(if any) used should also match with the original code.
3. Write a documentation on the changes that you are proposing. The documentation should include the problems you have noticed in the code(if any), the changes you would like to propose, the reason for these changes, and sample test cases. Remember that the topics in the documentation is strictly not limited to the topics aforementioned, but are just an inclusion.
4. Submit a pull request via [Git etiquettes](https://gist.github.com/mikepea/863f63d6e37281e329f8) 
