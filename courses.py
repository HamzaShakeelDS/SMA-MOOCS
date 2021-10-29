import base64
import json
import random

import numpy as np
import pandas as pd
import requests

course_url = "https://www.udemy.com/api-2.0/courses/"
PARAMS = {"page_size": 100, "page": 0}
CLIENT_ID = "ay5EaDJ0OHrFC4RrZ1X9zDi1IgAyz4dkpfsZqfMy"
CLIENT_SECRET = "m1LNQiGYUosTc8kQVR7awyeXoL8pQkccua1hTpESGni69rifyMhO1rbpfS3bZoWihY8Wm6btU71m0cprOkeuWATluRCPPhja6xGkH2P3UyjX0ZG6u3J3p7WJONxKOpSj"
b64Val = "eHVQRjVqc05MczY3OU1yeXhrb2Y0OUhWdUtYUExvd2lxTmpQNThIWToxbzR2OW5qZTJKSVFTZm5WSGc5anNEeTVOQXZsV3pZZVNCVXM3azRtcGJXSzRtaExWTHVBMjJWT1lnUFB1MEg1eWhnNGVlcG56cENRWnBURDYxTXMwZlVZaTNWSlV0OWI1aEJJSXB6NlJzS1FrZGRyR0dIMnMwcFpNMEN5OFhpMw=="
courses_list = []
categories = [
    "IT & Software",
    "Personal Development",
    "Finance & Accounting",
    "Business",
    "Marketing",
]


class SocialMediaAnalysis:
    @staticmethod
    def get_courses():
        for i in range(1, 3):
            PARAMS["page"] = i
            PARAMS["ordering"] = "relevance"
            PARAMS["instructional_level"] = "all"
            for category in categories:
                PARAMS["category"] = category
                print(f"Getting courses for category: {category}")
                JSONContent = requests.get(
                    course_url,
                    headers={"Authorization": "Basic " + b64Val},
                    params=PARAMS,
                ).json()
                print(
                    f"Length of courses for category: {category}={len(JSONContent['results'])}"
                )
                for course in JSONContent["results"]:
                    courses_list.append(
                        {
                            "id": course["id"],
                            "title": course["title"],
                            "published_title": course["published_title"],
                            "price": course["price"],
                            "headline": course["headline"],
                            "is_paid": course["is_paid"],
                            "instructor_name": course["visible_instructors"][0]["name"],
                            "instructor_job": course["visible_instructors"][0][
                                "job_title"
                            ],
                            "category": category,
                        }
                    )
                print(f"Incremental Length={len(courses_list)}")

        print(f"Length of complete courses={len(courses_list)}")

        # pd_courses = pd.DataFrame(courses_list,columns = ['id','title', 'published_title', 'price', 'headline','is_paid'])
        pd_courses = pd.DataFrame(courses_list)
        pd_courses.to_csv("new_courses.csv", encoding="utf-8")

    @staticmethod
    def get_course_reviews():
        courses = pd.read_csv("new_courses.csv")

        # loop through all courses
        course_review = []
        # For each channel, we access its information through its API
        for course in courses["id"]:
            print(f"Getting course reviews for course_id: {course}")
            JSONContent = requests.get(
                course_url + str(course) + "/reviews/",
                headers={"Authorization": "Basic " + b64Val},
            ).json()
            print(
                f"Length of course reviews for course_id: {course} is {len(JSONContent['results'])}"
            )
            if "error" not in JSONContent:
                for review in JSONContent["results"]:
                    course_review.append(
                        {
                            "course_review_id": review["id"],
                            "course_id": course,
                            "rating": review["rating"],
                            "user": review["user"]["title"]
                            or review["user"]["name"]
                            or review["user"]["display_name"],
                        }
                    )
        print(f"Length of course reviews is {len(course_review)}")

        dataset = pd.DataFrame(course_review)
        dataset.to_csv("updated_course_reviews.csv")

    @staticmethod
    def combine_course_and_course_reviews():
        df_courses = pd.read_csv("new_courses.csv")
        df_course_reviews = pd.read_csv("updated_course_reviews.csv")
        combined_data = pd.merge(
            df_courses[
                [
                    "id",
                    "title",
                    "published_title",
                    "price",
                    "headline",
                    "is_paid",
                    "instructor_name",
                    "instructor_job",
                    "category",
                ]
            ],
            df_course_reviews,
            left_on="id",
            right_on="course_id",
            how="inner",
        )
        dataset = pd.DataFrame(combined_data)
        dataset.to_csv("combined_courses_and_reviews.csv")

    @staticmethod
    def create_source_target_rating():
        df_course_reviews = pd.read_csv("combined_courses_and_reviews.csv")
        source_target = []
        for base_index, base_row in df_course_reviews.iterrows():
            print(f"Working for {base_row['user']}")
            for nested_index, nested_row in df_course_reviews.iterrows():
                if (
                    base_row["course_id"] == nested_row["course_id"]
                    and base_row["user"] != nested_row["user"]
                    and base_row["rating"] == nested_row["rating"]
                ):
                    source_target.append(
                        {
                            "source": base_row["user"],
                            "target": nested_row["user"],
                            "edge": base_row["rating"] or nested_row["rating"],
                        }
                    )
            print(f"Source Target Appended {source_target}")
        dataset = pd.DataFrame(source_target)
        dataset.to_csv("source_target_rating.csv")

    @staticmethod
    def create_source_target_pricing():
        df_course_reviews = pd.read_csv("combined_courses_and_reviews.csv")
        source_target = []
        for base_index, base_row in df_course_reviews.iterrows():
            print(f"Working for {base_row['user']}")
            for nested_index, nested_row in df_course_reviews.iterrows():
                if (
                    base_row["price"] == nested_row["price"]
                    and base_row["user"] != nested_row["user"]
                ):
                    source_target.append(
                        {
                            "source": base_row["user"],
                            "target": nested_row["user"],
                            "edge": base_row["price"] or nested_row["price"],
                        }
                    )
            print(f"Source Target Appended {source_target}")
        dataset = pd.DataFrame(source_target)
        dataset.to_csv("source_target_pricing.csv")

    @staticmethod
    def create_source_target_category():
        df_course_reviews = pd.read_csv("combined_courses_and_reviews.csv")
        source_target = []
        for base_index, base_row in df_course_reviews.iterrows():
            print(f"Working for {base_row['user']}")
            for nested_index, nested_row in df_course_reviews.iterrows():
                if (
                    base_row["category"] == nested_row["category"]
                    and base_row["user"] != nested_row["user"]
                ):
                    source_target.append(
                        {
                            "source": base_row["user"],
                            "target": nested_row["user"],
                            "edge": base_row["category"],
                        }
                    )
            print(f"Source Target Appended {source_target}")
        dataset = pd.DataFrame(source_target)
        dataset.to_csv("source_target_category.csv")

    @staticmethod
    def remove_duplicates():
        """
        This method removes duplicates and cleans data of the csv.
        """
        # READS THE CSV WHOSE DUPLICATES NEED TO BE REMOVED
        data = pd.read_csv("source_target_category.csv")
        data["merge"] = data["source"] + "," + data["target"]
        print(len(data))
        print(data.head())
        data = data[
            ~data["merge"].str.split(",").apply(frozenset).duplicated(keep="last")
        ]
        print(len(data))
        # DROPS COLUMNS THAT ARE NOT REQUIRED (MAY VARY AS PER THE DATASET)
        # data.drop(['merge', 'Unnamed: 0'], axis='columns', inplace=True)
        data.drop(["merge", "id"], axis="columns", inplace=True)
        print(data.head())
        # WRITES TO THE FILE (NAME IT ACCORDINGLY OR JUST OVERWRITE THE SOURCE FILE)
        data.to_csv("source_target_category.csv", index=False)


# WE CAN CALL ANY FUNCTION THAT WE WANT BY UNCOMMENTING THAT LIKE CURRENTLY get_courses() is CALLED.
SocialMediaAnalysis.get_courses()
# SocialMediaAnalysis.get_course_reviews()
# SocialMediaAnalysis.combine_course_and_course_reviews()
# SocialMediaAnalysis.create_source_target_rating()
# SocialMediaAnalysis.create_source_target_pricing()
# SocialMediaAnalysis.create_source_target_category()
# SocialMediaAnalysis.remove_duplicates()
