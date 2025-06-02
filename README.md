### MODELS
- User - Extra fields - is_verified, bio, skills_can_teach(M2M), skills_want_to_learn(M2M)
- Skills - Name
- Skill Sessions - Teacher(FK-User), learner(FK-User), Skills(FK-Skills), summary_file, created_at
- Rating - session, rating, feedback

### VIEWS
- SkillViewsSet - All Skills
- SkillSessionViewSet - All Sessions
- RatingViewSet - All rating
- UserViewSet - All users

### Serializers
- SkillSerializers - model - Skill, Fields - id, name
- UserSerializers - model - User, Fields - id, username, is_verified, bio, skills_can_teach, skills_want_to_learn
- SkillSessionSerializers - model - SkillSession, Fields- __all__, readonly - created_at
- RatingSerializers - model - Rating, fields - __all__

### Working URLs
- Add Skills - POST - http://127.0.0.1:8000/skill-swap/skills/
    -  Value -   {
                "name": "Python"
                  }
- Get Users - GET - http://127.0.0.1:8000/skill-swap/users/

### Future Updates
| Action              | Method   | Endpoint                          |
| ------------------- | -------- | --------------------------------- |
| List/Add Skills     | GET/POST | `/skill-swap/skills/`             |
| Create SkillSession | POST     | `/skill-swap/sessions/`           |
| Rate Session        | POST     | `/skill-swap/ratings/`            |
| Top 5 Teachers      | GET      | `/skill-swap/users/top_teachers/` |
