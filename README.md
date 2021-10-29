# SMA-MOOCS
Social Media Analysis on MOOCS

# Dataset URL (Udemy Affiliate API): https://www.udemy.com/developers/affiliate/

# Step # 1 (Extract data from Udemy Affiliate API)

  -Course.py is script for data extraction and data cleansing.
  -Courses Detail (new_courses.csv)
  -Courses Reviews Detail (updated_course_reviews.csv)

# Step # 2 

  -Merge Course detail and review dataset into single file (combined_courses_and_reviews.csv).

# Step # 3 

  Create edge list file

  -Based on Course Categories (Node: User & Edge: Course Category)
   source_target_category.csv

  -Based on Course Prices (Node: User & Edge: Course Price)
   source_target_price.csv

# Step # 4 (Create Bipartite Network)

  -Create Bipartite Network using combined_courses_and_reviews.csv and perform analysis on network.

# Step # 5 (Create Unipartite Network)
  -Create Bipartite Network using c source_target_category.csv/source_target_price.csv and perform analysis on network.



