# System Database

## Overview:
This contains the SQL scripts required to create the database schema for the application.

## Requirements: 
MySQL Community Server installed

## Files: 

create_database.sql -> Creates the office_hour_system_application database.
create_tables.sql -> Creates all tables and relationships within the database.

## Database name:
```
office_hour_system_application
```
## Setup: 
1. Open terminal, go to database folder
2. Start MySQL:
3. Run the database creation script

```sql
SOURCE create_database.sql;
```
4. Run the table creation script

```sql
SOURCE create_tables.sql;
```
5. check database and tables were created successfully

## Tables

| Table              | Description                                      |
|--------------------|--------------------------------------------------|
| users              | Stores all user accounts (students, TAs, admins).|
| classes            | Stores course information.                       |
| student_classes    | Maps students to enrolled classes.               |
| ta_classes         | Maps TAs to assigned classes.                    |
| locations          | Stores all possible office hour locations.       |
| office_hours       | Stores office hour time slots.                   |
| ta_office_hours    | Assigns TAs to office hour slots.                |
| faqs               | Stores FAQs for each class.                      |
| ta_reviews         | Stores student reviews of TAs.                   |
| student_help_queue | Stores students waiting for help.                |