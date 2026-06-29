# 1.0.16
- [fix] GET /dishes/{dish_id} now returns reactioned state, requires auth

# 1.0.15
- [feat] recommended dishes API (nearest food_vector to personal_vector, paginated)

# 1.0.14
- [feat] JWT auth middleware, admin-only route protection

# 1.0.13
- [feat] api for admin create dish

# 1.0.12
- [feat] file-based logging (all/error/scheduler logs with rotation), log read API
- [feat] api service in docker-compose, Dockerfile for the app

# 1.0.11
- [feat] achievements and user_achievements tables
- [feat] achievement criteria validation, refresh API, daily scheduler job

# 1.0.10
- [feat] add country field to dishes
- [feat] add fruit to material_tag enum

# 1.0.9
- [feat] recompute_personal_vector job, runs every 5 minutes

# 1.0.8
- [feat] personal_vector calculation service
- [feat] APScheduler setup, update_dish_rating job

# 1.0.7
- [feat] user dish interaction (stop-interaction, reaction)

# 1.0.6
- [feat] dish review 

# 1.0.5
- [feat] use backblaze to save images 

# 1.0.4
- [feat] upload images function 

# 1.0.3
- [feat] add tags and district into dishes 

# 1.0.2
- [feat] initial dish schema,  write create dish service, import sentences transformer
- [fix] sign up syntax

# 1.0.1
- [feat] login, signup service

# 1.0.0
- [feat] initial commit