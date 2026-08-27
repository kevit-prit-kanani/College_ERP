from fastapi import APIRouter, Depends

from libs.utils.comman.auth.token_generation import require_roles

analytics = APIRouter(
    tags=["Analytics"],
    dependencies=[Depends(require_roles("Admin"))],
)

from libs.utils.db.mongodb import db_Intakes


@analytics.get("/analytics/student-count")
def student_count_by_year_and_branch():

    pipeline = [
        # 1. Convert branches array into individual documents
        {"$unwind": "$branches"},
        # 2. Get department/branch information
        {
            "$lookup": {
                "from": "Department",
                "localField": "branches.department_id",
                "foreignField": "_id",
                "as": "department",
            }
        },
        # 3. Convert lookup array into an object
        {"$unwind": "$department"},
        # 4. Group by year + branch
        {
            "$group": {
                "_id": {"year": "$year", "branch": "$department.name"},
                "branch_students": {"$sum": "$branches.totalStudentsIntake"},
            }
        },
        # 5. Group again by year
        {
            "$group": {
                "_id": "$_id.year",
                "total_students": {"$sum": "$branch_students"},
                "branches": {
                    "$push": {"name": "$_id.branch", "students": "$branch_students"}
                },
            }
        },
        # 6. Convert branches array into an object
        {
            "$project": {
                "_id": 0,
                "year": "$_id",
                "total_students": 1,
                "branches": {
                    "$arrayToObject": {
                        "$map": {
                            "input": "$branches",
                            "as": "branch",
                            "in": ["$$branch.name", "$$branch.students"],
                        }
                    }
                },
            }
        },
        # 7. Highest total student count first
        {"$sort": {"total_students": -1}},
    ]

    return list(db_Intakes.aggregate(pipeline))


@analytics.get("/analytics/vacant-seats")
def get_vacant_seats(
    batch: int | None = None,
    branch: str | None = None,
):

    pipeline = []

    if batch is not None:
        pipeline.append({"$match": {"year": batch}})

    pipeline.extend(
        [
            {"$unwind": "$branches"},
            {
                "$lookup": {
                    "from": "Department",
                    "localField": "branches.department_id",
                    "foreignField": "_id",
                    "as": "department",
                }
            },
            {"$unwind": "$department"},
        ]
    )

    if branch is not None:
        pipeline.append({"$match": {"department.name": branch}})

    pipeline.extend(
        [
            # Find students belonging to this
            # department and admission year
            {
                "$lookup": {
                    "from": "Student",
                    "let": {
                        "department_id": "$branches.department_id",
                        "admission_year": "$year",
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$department_id", "$$department_id"]},
                                        {
                                            "$eq": [
                                                "$admission_year",
                                                "$$admission_year",
                                            ]
                                        },
                                    ]
                                }
                            }
                        },
                        {"$count": "count"},
                    ],
                    "as": "students",
                }
            },
            {
                "$set": {
                    "totalStudents": {
                        "$ifNull": [{"$arrayElemAt": ["$students.count", 0]}, 0]
                    }
                }
            },
            {
                "$set": {
                    "availableIntake": {
                        "$subtract": ["$branches.totalStudentsIntake", "$totalStudents"]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$year",
                    "totalStudents": {"$sum": "$totalStudents"},
                    "totalStudentsIntake": {"$sum": "$branches.totalStudentsIntake"},
                    "branches": {
                        "$push": {
                            "name": "$department.name",
                            "totalStudents": "$totalStudents",
                            "totalStudentsIntake": "$branches.totalStudentsIntake",
                            "availableIntake": "$availableIntake",
                        }
                    },
                }
            },
            {
                "$set": {
                    "availableIntake": {
                        "$subtract": ["$totalStudentsIntake", "$totalStudents"]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "batch": "$_id",
                    "totalStudents": 1,
                    "totalStudentsIntake": 1,
                    "availableIntake": 1,
                    "branches": {
                        "$arrayToObject": {
                            "$map": {
                                "input": "$branches",
                                "as": "branch",
                                "in": [
                                    "$$branch.name",
                                    {
                                        "totalStudents": "$$branch.totalStudents",
                                        "totalStudentsIntake": "$$branch.totalStudentsIntake",
                                        "availableIntake": "$$branch.availableIntake",
                                    },
                                ],
                            }
                        }
                    },
                }
            },
            {"$sort": {"availableIntake": -1}},
        ]
    )

    return list(db_Intakes.aggregate(pipeline))
