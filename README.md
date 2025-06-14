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
```
    "skills": "http://127.0.0.1:8000/api/skill-swap/skills/",
    "sessions": "http://127.0.0.1:8000/api/skill-swap/sessions/",
    "ratings": "http://127.0.0.1:8000/api/skill-swap/ratings/",
    "users": "http://127.0.0.1:8000/api/skill-swap/users/"
```
### Frontend URLs
```
Index.html : http://127.0.0.1:8000/
User.html : http://127.0.0.1:8000/users/
Skills.html : http://127.0.0.1:8000/skills/
Sessions.html : http://127.0.0.1:8000/sessions/
```

### Future Updates
| Action              | Method   | Endpoint                          |
| ------------------- | -------- | --------------------------------- |
| List/Add Skills     | GET/POST | `/api/skill-swap/skills/`             |
| Create SkillSession | POST     | `/api/skill-swap/sessions/`           |
| Rate Session        | POST     | `/api/skill-swap/ratings/`            |
| Top 5 Teachers      | GET      | `/api/skill-swap/users/top_teachers/` |

