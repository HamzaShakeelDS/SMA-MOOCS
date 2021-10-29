# SMA-MOOCS
Social Media Analysis on MOOCS

# Dataset URL (Udemy Affiliate API): https://www.udemy.com/developers/affiliate/


# Step # 1 (Extract data from Udemy Affiliate API)

Creating an Affiliate API Client

To make any calls to Udemy REST API, you will need to create an API client. Affiliate API client consists of a bearer token, which is connected to a user account on Udemy.
If you want to create an Affiliate API client, Sign up on www.udemy.com and go to API Clients page in your user profile. Once your Affiliate API client request is approved, your newly created Affiliate API client will be active and your bearer token will be visible on API Clients page.

Sending an Authenticated Request

Udemy Affiliate API requires basic authentication parameters to validate the client. The auth parameters have to be sent in every call or you will get a 401 UNAUTHORIZED error.=
To send authenticated requests, provide the client_id and client_secret values as a base64 encoded HTTP Authorization header.

We created a python script courses.py to extract and clean the data.

    -Courses Detail (new_courses.csv) 
    -Courses Reviews Detail (updated_course_reviews.csv)

# Step # 2 (Merge Dataset)

Merge Course detail and review dataset into single file.

    -combined_courses_and_reviews.csv

# Step # 3 (Edge list)

Create edge list file

Based on Course Categories (Node: User & Edge: Course Category)

    -source_target_category.csv

Based on Course Prices (Node: User & Edge: Course Price)

    -source_target_price.csv
   
# Step # 4 (Data Sampling)   

We created to edge list csv files.

    1) source_target_category.csv
    2) source_target_price.csv

But the dataset was too large to visualize in gephi so we took sample of 100k records to perform our analysis.

Script for data sampling
    
    Data_Sampling.py

# Step # 5 (Create Bipartite Network)

Create Bipartite Network using combined_courses_and_reviews.csv and perform analysis on network.
    
    Type of Nodes
    1) Courses
    2) Users

# Step # 6 (Create Unipartite Network)

Create Unipartite Network using source_target_category.csv/source_target_price.csv and perform analysis on network.

Unipartite 1

    Node  -> Users 
    Edges -> Course Category
    

Unipartite 2

    Node  -> Users 
    Edges -> Course Price

    



